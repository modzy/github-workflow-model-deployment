import os
import time
import json
import pickle
import cloudpickle
import numpy as np
from typing import Mapping
from chassisml import ChassisModel
from chassis.builder import BuildOptions 

with open("model_info.json", "r") as model_file:
    model_info = json.load(model_file)

# load model 
model = pickle.load(open(model_info["weightsFilePath"], "rb")) 

# define predict function
def predict(input_bytes: Mapping[str, bytes]) -> dict[str, bytes]:
    inputs = np.array(json.loads(input_bytes['input']))
    inference_results = model.predict_proba(inputs)
    structured_results = []
    for inference_result in inference_results:
        structured_output = {
            "data": {
                "result": {"classPredictions": [{"class": np.argmax(inference_result).item(), "score": round(np.max(inference_result).item(), 5)}]}
            }
        }
        structured_results.append(structured_output)
    return {'results.json': json.dumps(structured_results).encode()}

# create chassis model object, add required dependencies, and define metadata
chassis_model = ChassisModel(process_fn=predict)                
chassis_model.add_requirements(["scikit-learn", "numpy"])       
chassis_model.metadata.model_name = model_info["name"]         
chassis_model.metadata.model_version = model_info["version"]
chassis_model.metadata.add_input(
    key="input",
    accepted_media_types=["application/json"],
    max_size="10M",
    description="Numpy array representation of digits image"
)
chassis_model.metadata.add_output(
    key="results.json",
    media_type="application/json",
    max_size="1M",
    description="Top digit prediction and confidence score"
)    

options = BuildOptions(base_dir="./build", python_version="3.10")
chassis_model.prepare_context(options)
print("Context prepared!")
