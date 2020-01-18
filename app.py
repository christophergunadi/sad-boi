import os, io, base64
from flask import Flask, render_template, request, jsonify
from azure.cognitiveservices.vision.face import FaceClient, models
from msrest.authentication import CognitiveServicesCredentials

credentials = CognitiveServicesCredentials(os.environ['FACE_SUBSCRIPTION_KEY'])
face_client = FaceClient(os.environ['FACE_ENDPOINT'], credentials=credentials)

app = Flask(__name__)

# The root route, returns the home.html page
@app.route('/')
def home():
    # Add any required page data here
    page_data = {}
    return render_template('home.html', page_data = page_data)

def is_happy(emotion):
    emotions = {}
    emotions['anger'] = emotion.anger
    emotions['contempt'] = emotion.contempt
    emotions['disgust'] = emotion.disgust
    emotions['fear'] = emotion.fear
    emotions['happiness'] = emotion.happiness
    emotions['neutral'] = emotion.neutral
    emotions['sadness'] = emotion.sadness
    emotions['surprise'] = emotion.surprise
    best_emotion = max(zip(emotions.values(), emotions.keys()))[1]
    return best_emotion == 'happiness'

@app.route('/process_image', methods=['POST'])
def check_results():
    # Get the JSON passed to the request and extract the image
    # Convert the image to a binary stream ready to pass to Azure AI services
    body = request.get_json()
    image_bytes = base64.b64decode(body['image_base64'].split(',')[1])
    image = io.BytesIO(image_bytes)

    # Send the image to the Face API service
    # This gets all the possible attributes
    # face_attributes = list(map(lambda c: c.value, models.FaceAttributeType))
    faces = face_client.face.detect_with_stream(image,
                                                return_face_attributes=['emotion'])
    
    if len(faces) >= 1 and is_happy(faces[0].face_attributes.emotion):
        return jsonify({
            'message': 'What a nice smile 😍🥰🌈🔥'
        })
    else:
        return jsonify({
            'message': 'not happy 😢'
        })
