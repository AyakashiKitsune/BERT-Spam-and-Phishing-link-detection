# to work with the project:

1. change directory to this root project where you can see requirements.txt
2. initialize your environment
3. install venv module

   ```
   pip install virtualenv
   ```
4. create enviroment

   ```
   python3.10 -m venv env
   ```
5. run

   ```
   . env\Scripts\activate //in windows
   source env/bin/activate
   ```
6. run

   ```
   pip install -r requirements.txt
   ```
7. to run the server

   ```
   python -m app 
   // or
   python app.py
   ```

# note to the project



* checkpoints - contains all the checkpoint of training weights
* dataset - you know it
* experiments - past experiments
* models - contains all the models that are trained and used for the app server
* app.py - main application server
* Phising_model_creation.ipynb - the notebook creations for the model
* SpamHam_detection_creation.ipynb - the notebook creations for the model
* profanity.txt - contains all the profanity strings
* requirements.txt - contains all the dependencies used for the project
