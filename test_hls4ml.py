import os
import sys
import ndjson

import keras
from keras.models import Sequential
from keras.layers import Dense, Input
import hls4ml

# Load project name
PROJECT_NAME = sys.argv[1]
print("Project name:", PROJECT_NAME)
print("* Keras version:", keras.__version__)
print("* hls4ml version:", hls4ml.__version__)

# -------------------------
# 1. Define tiny Keras model
# -------------------------
model = Sequential([
    Input(shape=(4,)),
    Dense(4, activation='relu', name="dense1"),
    Dense(1, activation='linear', name="output")
])
model.summary()

# -------------------------
# 2. Create hls4ml config
# -------------------------
config = hls4ml.utils.config_from_keras_model(
    model,
    granularity='model',
    backend='oneAPI'
)
# Keep build tiny & fast
config['Model']['Precision'] = 'ap_fixed<16,6>'
config['Model']['ReuseFactor'] = 1
print("\n--> Building hls4ml config")
print(config)

# -------------------------
# 3. Convert to hls4ml model
# -------------------------
hls_model = hls4ml.converters.convert_from_keras_model(
    model,
    hls_config=config,
    backend='oneAPI',
    output_dir=PROJECT_NAME,
    part='Agilex7'
)
print("--> HLS model created")

# -------------------------
# 4. Compile hls4ml model
# -------------------------
hls_model.compile()
print("--> HLS model compiled")


# -------------------------
# 5. Build hls4ml model
# -------------------------
hls_model.build(build_type='report')
print("--> HLS model built")

# -------------------------
# 6. Print build report
# -------------------------
report_file = os.path.join(
    PROJECT_NAME,
    'build',
    'myproject.report.prj',
    'reports',
    'resources',
    'json',
    'summary.ndjson'
)

with open(report_file, "r") as f:
    summary = ndjson.load(f)

# Summarise report contents
resource_names = list(filter(lambda x: x["name"] == "Estimated Resource Usage", summary))[0]['columns'][1:-1]
available = list(filter(lambda x: x["name"] == "Available", summary))[0]['data'][:-1]
estimated_resources = list(filter(lambda x: x["name"] == "Total", summary))[0]['data'][:-1]

print("~~~~~~~~~~~~~~ Resource usage ~~~~~~~~~~~~~~")
for i, resource in enumerate(resource_names):
    print(f"--> {resource}:")
    print(f"      * Available resource: {available[i]}")
    print(f"      * Used resource (estimated): {estimated_resources[i]}")
    print(f"      * Percentage of used resource (estimated): {100*float(estimated_resources[i])/float(available[i]):.2f}%")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
