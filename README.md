### Setup

1. Install google-cloud-language: ```virtualenv env && source env/bin/activate && pip install google-cloud-language```
2. Get Token: https://cloud.google.com/storage/docs/authentication#storage-authentication-python
2. Put Token into ```/home/$USER/.../project/token.json```
2. ``` export GOOGLE_APPLICATION_CREDENTIALS=/home/$USER/.../project/token.json```
3. Try ```python example.py```
