#@ Start the server
#@markdown ## 👈 Copy the contents of `server.py` here

import asyncio
import subprocess
import sys
from sanic import Sanic, response

try:
  port += 1
except NameError:
  port = 8000
  # (This is a hack to avoid "address already in use" errors when running the cell multiple times)

if 'google.colab' in sys.modules:

  Sanic._app_registry = {}
  # (We need this to remove the already created app if running the cell multiple times)

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


app = Sanic("my_app")

# Healthchecks verify that the environment is correct on Banana Serverless
@app.route('/healthcheck', methods=["GET"])
def healthcheck(request):
  # dependency free way to check if GPU is visible
  gpu = False
  out = subprocess.run("nvidia-smi", shell=True)
  if out.returncode == 0: # success state on shell command
    gpu = True

  return response.json({"state": "healthy", "gpu": gpu})

# Inference POST handler at '/' is called for every http call from Banana
@app.route('/', methods=["POST"]) 
def inference(request):
  try:
    model_inputs = response.json.loads(request.json)
  except:
    model_inputs = request.json

  output = user_src.inference(model_inputs)

  return response.json(output)


if __name__ == '__main__':
  # # app.run(host='0.0.0.0', port=port, workers=1, single_process=True, loop=asyncio.get_event_loop())
  # server = app.create_server(host='0.0.0.0', port=port)
  # loop = asyncio.get_event_loop()
  # task = asyncio.ensure_future(server)
  # loop.run_forever()
  async def start_server():
    server = app.create_server(host='0.0.0.0', port=port)
    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(server)
    loop.run_forever()
    
  