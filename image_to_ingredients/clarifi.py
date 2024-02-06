from flask import Flask, render_template, request
from clarifai_client import ClarifaiApp

# Replace with your Clarifai app ID and access token
app_id = "YOUR_APP_ID"
access_token = "YOUR_ACCESS_TOKEN"

# Initialize Clarifai app
app = ClarifaiApp(app_id, access_token)

# Flask app
flask_app = Flask(__name__)

@flask_app.route('/', methods=['GET', 'POST'])
def index():
    ingredients = []
    if request.method == 'POST':
        image_file = request.files['image']
        # Use Clarifai to get predictions
        response = app.models.general_image_recognition.predict([image_file])
        # Extract ingredient concepts from predictions
        ingredients = [concept["name"] for concept in response["outputs"][0]["data"]["concepts"] if concept["name"].startswith("ingredient")]

    return render_template('index.html', ingredients=ingredients)

if __name__ == '__main__':
    flask_app.run(debug=True)
