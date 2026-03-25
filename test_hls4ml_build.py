import os
import sys
import ndjson

import keras
import hls4ml

# Load project name
PROJECT_NAME = sys.argv[1]
print("Project name:", PROJECT_NAME)
print("* Keras version:", keras.__version__)
print("* hls4ml version:", hls4ml.__version__)

# -------------------------
# 1. Load model from project directory
# -------------------------
# Load keras model from project directory
model = keras.models.load_model(os.path.join(PROJECT_NAME, 'keras_model.keras'))
print("--> Keras model loaded")

hls_model = hls4ml.converters.link_existing_project(PROJECT_NAME)
print("--> Linked existing hls4ml project")

# -------------------------
# 2. Compile hls4ml model
# -------------------------
hls_model.compile()
print("--> HLS model compiled")

# -------------------------
# 3. Build hls4ml model
# -------------------------
hls_model.build(build_type='report')
print("--> HLS model built")

# -------------------------
# 4. Print build report
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
