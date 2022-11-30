#@ Define the test inputs
#@markdown ## 👈 Copy the contents of `test.py` here

# You generally only need to change the `default_model_inputs` variable, which defines the default inputs to your model

default_model_inputs = dict(

  prompt = "Hello I am a [MASK] model."

)

# 🚧🚧🚧 Do not modify the code below this line unless you're sure you know what you're doing 🚧🚧🚧

#@markdown **Notes:**
#@markdown There are two ways to run the test:
#@markdown - Using the /test endpoint after the server is running (see the last cell of this notebook), or
#@markdown - By running `python3 test.py` in the terminal (from anywhere, e.g. your local machine).
#@markdown
#@markdown In the case of the /test endpoint, you can provide the model inputs as query parameters (e.g. `http://<some_id>.ngrok.io/test?prompt=Hello%20I%20am%20a%20[MASK]%20model.`). In the case of the terminal, you can provide the model inputs as command line arguments (e.g. `python3 test.py --prompt "Hello I am a [MASK] model."`).
#@markdown
#@markdown #### Testing environment
#@markdown When running as a script (`python3 test.py`), you can specify which environment to use (dev/prod) by adding the `--env` argument, e.g. `python3 test.py --env prod`. If you don't specify the environment, you will be prompted to enter it or skip it (defaulting to `dev`):
#@markdown - Choosing `prod` will make a call to an already deployed Banana server;
#@markdown - Choosing `dev` will make a call to the server running in the current notebook.
#@markdown
#@markdown In the case of `dev`, you will need to provide the public URL of the server, which you can find in the console after running the last cell of this notebook). We do not store this information locally on purpose, as the URL is likely to change every time you run the notebook.

import json
import os
import requests
import sys

def test_inference(model_inputs={}):

  meta_args = {}
  meta_keys = ['env', 'api_key', 'model_key']

  # If no model_inputs are provided, either use the ones from command line (if any) or the default ones
  if model_inputs == {}:
    # Check if any command line arguments were provided. Keep in mind that the command line arguments is of form "python3 test.py arg1 arg2 arg3"
    if not 'google.colab' in sys.modules and len(sys.argv) > 1:

      print(f"Using command line arguments: {sys.argv[1:]}")

      # The inputs would be provided in the form --[json key] [json value]
      # For example: --prompt "Hello I am a [MASK] model."
      # For meta keys, add them to the meta_args dict instead
      for i in range(1, len(sys.argv), 2):
        key = sys.argv[i].replace('--', '')
        value = sys.argv[i+1]
        dict_to_use = model_inputs if key not in meta_keys else meta_args
        dict_to_use[key] = value

    else:
      # Default inputs
      model_inputs = default_model_inputs
  
  print(f"Using model inputs: {model_inputs}")
  print(f"Using meta args: {meta_args}")

  if 'google.colab' in sys.modules:

    url = ngrok_tunnel.public_url
    res = requests.post(url, json=model_inputs)

  else:

    # Check which environment we're in (dev/prod)
    env = meta_args['env'] if 'env' in meta_args else input("Enter environment (dev/prod) or press Enter to use dev: ") or 'dev'

    if env == 'prod':

      credential_prompts = dict(
        api_key = "Enter your API key (go to https://app.banana.dev/ to get one)",
        model_key = "Enter your model key (from your model's page on https://app.banana.dev/)"
      )

      # Load credentials from 'credentials.json' if it exists
      if os.path.exists('credentials.json'):
        with open('credentials.json', 'r') as f:
          credentials = json.loads(f.read())
          print("Loaded credentials from credentials.json")
      else:
        credentials = {}

      credentials_changed = False
      for key, prompt in credential_prompts.items():
        if key not in meta_args:
          if key in credentials:
            print(f"Using {key} from credentials.json")
          else:
            credentials[key] = input(f"{prompt}: ")
            credentials_changed = True
        else:
          credentials[key] = meta_args[key]
          credentials_changed = True
      
      # Save credentials to 'credentials.json' if they changed
      if credentials_changed:
        with open('credentials.json', 'w') as f:
          f.write(json.dumps(credentials))
          print("Saved credentials to credentials.json")

      res = requests.post("https://api.banana.dev/start/v4/", json=dict(
        apiKey = credentials['api_key'],
        modelKey = credentials['model_key'],
        modelInputs = model_inputs
      )).json()

    else:

      url = input("Enter the public URL of your server (e.g. http://<some_id>.ngrok.io, look for it in the console after running the notebook's last cell): ")
      res = requests.post(url, json=model_inputs)

  print(f"Response: {res}")

  return res

# If not running in Colab, run the test
if not 'google.colab' in sys.modules:
  test_inference()
else:
  print("Running in Colab, skipping test (you will be able to run it later by using the /test endpoint)")