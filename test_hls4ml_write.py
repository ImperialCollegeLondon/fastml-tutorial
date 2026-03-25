import sys

import keras
from keras.models import Sequential
from keras.layers import Dense, Input
import hls4ml

# Load project name
PROJECT_NAME = sys.argv[1]
print("Keras version:", keras.__version__)
print("hls4ml version:", hls4ml.__version__)

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
# 3. Convert to hls4ml model and save
# -------------------------
hls_model = hls4ml.converters.convert_from_keras_model(
    model,
    hls_config=config,
    backend='oneAPI',
    output_dir=PROJECT_NAME,
    part='Agilex7'
)
print("--> HLS model created and saved")

# -------------------------
# 4. Write hls4ml model
# -------------------------
hls_model.write()
print("--> HLS model written")
