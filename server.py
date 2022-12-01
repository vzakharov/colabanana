#@title Start the server
#@markdown Usually, you don’t need to change anything in this cell. However, if you change the `server.py` file, double-click on the cell to edit the code and paste its  contents.

import asyncio
import datetime
import time
import subprocess
import sys

import numpy as np
import torch as t

from flask import Flask, request, jsonify
from pyngrok import ngrok

try:
  port += 1
except NameError:
  port = 8000
  # (This is a hack to avoid "address already in use" errors when running the cell multiple times)

if not 'google.colab' in sys.modules:

  import app as user_src
  user_src.init()

else:

  class user_src:
    init = init
    inference = inference

  try:
    model
    print("Model already loaded")
  except NameError:
    print("Loading model...")
    user_src.init()
    print("Model loaded")

  # Start the ngrok tunnel
  print("Starting tunnel")

  for tunnel in ngrok.get_tunnels():
    ngrok.disconnect(tunnel.public_url)      
  # (We need this to remove the already created tunnel if running the cell multiple times, as free ngrok only allows so many tunnels)

  ngrok_tunnel = ngrok.connect(port)
  print(ngrok_tunnel)
  print("This is the public URL of your server ☝️☝️☝️ (you can also use https)")
  # The public URL will be printed to the console after this line, so look for it there

# We do the model load-to-GPU step on server startup
# so the model object is available globally for reuse

# Create the http server app.
try:
  # First let's kill the server and its server_thread if it's already running (on Colab)
  del server
  del server_thread
  print("Stopped running server")
except ( AssertionError, NameError ):
  pass
  
# Use timestamp in server name for debug purposes
server = Flask(f"server-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}")

# Healthchecks verify that the environment is correct on Banana Serverless
@server.route('/healthcheck', methods=['GET'])
def healthcheck():
  # dependency free way to check if GPU is visible
  gpu = False
  out = subprocess.run("nvidia-smi", shell=True)
  if out.returncode == 0: # success state on shell command
    gpu = True
  return jsonify(dict(
    state="healthy",
    gpu=gpu,
    timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  ))

# Inference POST handler at '/' is called for every http call from Banana
@server.route('/', methods=['POST'])
def run_inference():
  global output 

  model_inputs = request.get_json()
  print(f"Received request: {model_inputs}")

  output = user_src.inference(model_inputs)
  print(f"Sending response: {output}")

  # If the output is not serializable, try converting it to a serializable type
  def is_serializable(x):
    try:
      json.dumps(x)
      return True
    except:
      return False

  if not is_serializable(output):
    print(f"Output is {type(output)}, converting to a serializable type")
    # Go recursively through each dimension and convert
    def convert_to_list(x):
      if isinstance(x, np.ndarray):
        return x.tolist()
      elif isinstance(x, t.Tensor):
        return x.cpu().numpy().tolist()
      elif isinstance(x, (list, tuple)):
        return [convert_to_list(y) for y in x]
      elif not is_serializable(x):
        raise Exception(f"Cannot convert {x} to a serializable type")
      else:
        return x

    output = convert_to_list(output)

  return jsonify(output)

if 'google.colab' in sys.modules:

  # GET /test to call a sample inference using the public URL from ngrok_tunnel
  @server.route('/test', methods=['GET'])
  def test_endpoint():


    global test_inference

    url = ngrok_tunnel.public_url
    print(f"Sending a test inference request to {url}")

    # Take model_inputs from query params
    model_inputs = request.args.to_dict()

    print(f"Request: {model_inputs}")
    print("✂=== Below are logs from the server processing the test request\n")

    res = test_inference(model_inputs)

    print("\n✂=== End of logs from the server processing the test request")
    print(f"Response: {res.json()}")
    return jsonify(res.json())

if __name__ == '__main__':
  # Start the  server in a new thread
  print("Starting server")
  import threading
  server_thread = threading.Thread(target=server.run, kwargs={"host": "0.0.0.0", "port": port})
  server_thread.start()

  if 'google.colab' in sys.modules:
    # Print that the server is started and a test URL after a second (so the server has time to start)
    time.sleep(1)
    print(f"Server started; test: {ngrok_tunnel.public_url}/test")

    # Keep the cell running so we can see the logs
    print("Keeping the cell running so you can see the server logs")
    while True:
      time.sleep(1)