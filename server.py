#@ Start the server
#@markdown ## 👈 Copy the contents of `server.py` here

import asyncio
import subprocess
import sys
from flask import Flask, request, jsonify

try:
  port += 1
except NameError:
  port = 8000
  # (This is a hack to avoid "address already in use" errors when running the cell multiple times)

if 'google.colab' in sys.modules:

  # Start the ngrok tunnel

  from pyngrok import ngrok

  print("Starting tunnel")

  for tunnel in ngrok.get_tunnels():
    ngrok.disconnect(tunnel.public_url)      
  # (We need this to remove the already created tunnel if running the cell multiple times, as free ngrok only allows so many tunnels)

  ngrok_tunnel = ngrok.connect(port)
  print(ngrok_tunnel)
  print("This is the public URL of your server ☝️☝️☝️")
  # The public URL will be printed to the console after this line, so look for it there

else:

  import app as user_src
  # (If testing with colab, the app interface is defined in the cell above)

# We do the model load-to-GPU step on server startup
# so the model object is available globally for reuse
user_src.init()

# Create the http server app.

server = Flask(__name__)

# Healthchecks verify that the environment is correct on Banana Serverless
@server.route('/healthcheck', methods=['GET'])
def healthcheck():
  # dependency free way to check if GPU is visible
  gpu = False
  out = subprocess.run("nvidia-smi", shell=True)
  if out.returncode == 0: # success state on shell command
    gpu = True
  # return {"state": "healthy", "gpu": gpu}
  # Flask:
  return jsonify({"state": "healthy", "gpu": gpu})

# Inference POST handler at '/' is called for every http call from Banana
@server.route('/', methods=['POST'])
def inference():
  model_inputs = request.get_json()

  output = user_src.inference(model_inputs)

  return jsonify(output)


if __name__ == '__main__':
  # Start the  server in a new thread
  print("Starting server")
  import threading
  server_thread = threading.Thread(target=server.run, kwargs={"host": "0.0.0.0", "port": port})
  server_thread.start()
  # Keep the colab notebook running
  while True:
    pass