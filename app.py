#@ Define model init/inference functions
#@markdown ## 👈 Copy the contents of `app.py` here

from transformers import pipeline
import torch

# Init is ran on server startup
# Load your model to GPU as a global variable here using the variable name "model"
def init():
  
    global model
  
    device = 0 if torch.cuda.is_available() else -1
    model = pipeline('fill-mask', model='bert-base-uncased', device=device)
    
    print("Model loaded")

# Inference is ran for every server call
# Reference your preloaded global model variable here.
def inference(model_inputs:dict) -> dict:
    global model
    print(f"Running inference with inputs: {model_inputs}")

    # Parse out your arguments
    prompt = model_inputs.get('prompt', None)
    if prompt == None:
      return {'message': "No prompt provided"}
    
    # Run the model
    result = model(prompt)
    print(f"Result: {result}")

    # Return the results as a dictionary
    return result



# 🚧🚧🚧 Some service code again; ignore everything below this line

import sys 

# If testing with Colab, define a user_src object which has attributes for init and inference
# Check if imported modules include google.colab
if 'google.colab' in sys.modules:
  class UserSrc:
    def __init__(self):
      self.init = init
      self.inference = inference

  user_src = UserSrc()