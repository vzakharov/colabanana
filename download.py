#@title Download the model
#@markdown ## 👈 Copy the contents of `download.py` here
#@markdown **Note:** Ideally, you want to rewrite the models so that they are downloaded and later reused from Google Drive. This way, you won't need to download the model every time you start a runtime. However, the code will be specific to the model you are using, so we will leave it as an exercise for the notebook user.

# In this file, we define download_model_weights
# It runs during container build time to get model weights built into the container

# In this example: A Huggingface BERT model

from transformers import pipeline

def download_model_weights():

  try:

    weights_downloaded
    # Hereinafter, this trick allows us to avoid downloading the model whenever the cell is run. Once the model is downloaded for the first time, the variable `weights_downloaded` is set to True, so no error is raised and the model (which is downloaded in the except block) is not downloaded again.

  except NameError:
    
    # do a dry run of loading the huggingface model, which will download weights
    pipeline('fill-mask', model='bert-base-uncased')

    weights_downloaded = True

if __name__ == "__main__":
    download_model_weights()