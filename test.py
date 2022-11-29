# This file is used to verify your http server acts as expected
# Run it with `python3 test.py``

import requests

model_inputs = {'prompt': 'Hello I am a [MASK] model.'}

public_url = input("Enter the public URL of your server (e.g. http://<some_id>.ngrok.io, look for it in the console after running the notebook's last cell): ")

res = requests.post(public_url, json=model_inputs)

print(res.json())