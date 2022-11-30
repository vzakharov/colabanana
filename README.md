
# Colabanana — test your 🍌 Banana environment with Colab

[Banana](banana.dev) is a framework to serve ML models in production using simple HTTP servers. This repository contains a template for building a Banana-compatible model that you can, by copying and pasting, deploy to and test on [Google Colab](https://colab.research.google.com/).

## Why bother?

Banana is a great tool for serving ML models in production, but it can be a bit tricky to test, as it has no debugging capabilities, the deploying process takes a while, and actually running the model costs quite a bit. Although there are ML testing platforms out there such as [Brev](https://brev.dev/), they require quite a bit of hacking to get to work, especially for ~~someone as stupid as me~~ Windows users. It is not free either. (But seriously, Brev is great, and you should check it out.)

Colab, on the other hand, is a (mostly) free, easy-to-use, and powerful platform for building and testing ML models. Besides, it’s a tool many ML practitioners like myself are already familiar with. So why not use it to test your Banana models?

So I went ahead and created this template. Basically it’s based on (and is a fork of) Banana’s [serverless template](https://github.com/bananaml/serverless-template) with a few modifications to make it work with Colab. It’s not perfect — copying and pasting the code from your `py` files into the Colab notebook is a bit tedious and prone to errors — but hey, it works.

If, like me, you suck at infrastructure and just want to get your model server up and running, this might be for you.

## How to use this template

1. Clone this repository

2. Edit `download.py`, `app.py`, `test.py` and `requirements.txt` to your liking (read the [serverless framework guide](https://docs.banana.dev/banana-docs/core-concepts/inference-server/serverless-framework) for more information).

3. Create a new Colab notebook from `colabana.ipynb` or copy the template one located [here](https://colab.research.google.com/drive/1ODP4Aw8cPRB2xcH8y-Tl5unib0jdfwHZ).

4. Follow the instructions in the notebook to run and test your model with Colab.

5. Once done testing, deploy your model to Banana as described in the [serverless framework guide](https://docs.banana.dev/banana-docs/core-concepts/inference-server/serverless-framework).

## Prerequisites

It is assumed that you understand the basics of Banana. If you don't, please refer to the [Banana documentation](https://banana.dev/docs), most importantly:

- The [Quickstart guide](https://docs.banana.dev/banana-docs/quickstart)
- The [Serverless Framework guide](https://docs.banana.dev/banana-docs/core-concepts/inference-server/serverless-framework)