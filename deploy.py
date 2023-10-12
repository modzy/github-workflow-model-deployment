import os
import json
from modzy import ApiClient

# load metadata config file
with open("model_info.json", "r") as model_file:
    model_info = json.load(model_file)

# instantiate Modzy API Client
client = ApiClient(os.getenv("MODZY_URL"), os.getenv("MODZY_API_KEY"))

print(f"Deploying model to {os.getenv('MODZY_URL')}")
# deploy model
new_model_data = client.models.deploy(
    container_image=os.getenv("CONTAINER"),
    model_name=model_info["name"],
    model_version=model_info["version"],
    sample_input_file=model_info["sampleDataFilePath"],
    model_id=model_info["modelId"]
)

print(new_model_data)    
