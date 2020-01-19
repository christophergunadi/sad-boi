import os, io, base64, random, time, requests
from flask import Flask, render_template, request, jsonify, make_response
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
            'happy': 1,
            'boi': '/static/pics/happyboi.png'
        })
    else:
        return jsonify({
            'happy': 0,
            'boi': '/static/pics/normalboi.png'
        })

db = list()  # The mock database

posts = 500  # num posts to generate
quantity = 20  # num posts to return per request

curated_memes = [
    ["Wristband!", "https://i.ibb.co/yqvL1J1/Image-from-i-OS.jpg"],
    ["What is sleep?", "https://i.ibb.co/2sBT4WS/image.png"],
    ["It be like that sometimes", "https://i.ibb.co/tXwF5TF/meme.png"],
    ["Meme loading...", "https://i.ibb.co/tcxSNcY/Phil-Swift-Slaps-On-Flex-Tape-Leak-18012020185640.jpg"],
    ["Perfectly balanced", "https://i.ibb.co/n1DXsp5/1.jpg"],
    ["007", "https://i.ibb.co/VwWJwHt/2.jpg"],
    ["You cannot take our freedom!", "https://i.ibb.co/hYdRx6q/3.jpg"],
    ["Keep scrolling", "https://i.ibb.co/chzYdMz/4.jpg"],
    ["Free T-Shirts from Hack Cambridge?", "https://i.ibb.co/vBMxH92/5.jpg"],
    ["Dog vs Hoodie", "https://media.giphy.com/media/emHFoQ3y689ne2HhLR/giphy.gif"],
    ["Bug-catching kitty", "https://media.giphy.com/media/Y1vaVnrSYeDe9Hy5ak/giphy.gif"],
    ["Just trying to work out", "https://media.giphy.com/media/jnniZ3sMZWnkxmZPyn/giphy.gif"],
    ["Awww", "https://media.giphy.com/media/YmPNGMrizkE28kufai/giphy.gif"],
    ["Facts", "https://img.ifunny.co/images/8e267b93ac018b6dd43baee5bf9dcd368465fa644c0a4a07ccb69c67788dacd8_1.jpg"],
    ["Hackerman", "https://img-9gag-fun.9cache.com/photo/aN0R810_460s.jpg"],
    ["Hackerman2", "https://images3.memedroid.com/images/UPLOADED117/5d78580e9c694.jpeg"],
    ["Man", "https://images7.memedroid.com/images/UPLOADED822/5aa0836df0d4c.jpeg"],
    ["it be like that", "https://i.chzbgr.com/full/9310034432/h89A4C820/saying-oh-no-mesa-disappearin-text-above-reads-when-your-professor-says-attendance-isnt-mandatory"],
    ["goddeem", "https://i.chzbgr.com/full/9371521792/h1A810A06/on-me-with-joe-oh-shit-who-told-you-wait-this-was-just-supposed-to-be-for-a-meme-whos-joe-joe-mama"],
    ["","https://external-preview.redd.it/bZUo5Q3MmQas3fOlXKpf9Ao8p0UwUy0S8vcDbh3LPT0.jpg?auto=webp&s=2f3ef451d903f7c38dbfc9745a9cda6c474ad2ef"],
    ["","https://pics.onsizzle.com/napoleon-returns-to-france-1815-huh-i-wonder-who-thats-52093194.png"],
    ["", "https://files.slack.com/files-pri/TS7F0A0F5-FSWT49T62/meme.jpg"],
    ["", "https://cdn2.kontraband.com/uploads/image/2019/6/21/preview_e96bc679.jpeg"],
    ["", "https://images3.memedroid.com/images/UPLOADED338/5c0846cda7957.jpeg"],
    ["", "http://meme-drop.com/wp-content/uploads/2017/11/ukTRSvy-1024x930.jpg"]]

# Use imgflip API to collect memes 😎
# data = requests.get(url="https://api.imgflip.com/get_memes").json()["data"]["memes"]

for x in range(posts):
    """
    Fills db with a meme.
    """
    # index = x % len(data)

    # title = data[index]["name"]
    # url   = data[index]["url"]

    index = x % len(curated_memes)

    if index == 0:
        random.shuffle(curated_memes)

    title = curated_memes[index][0]
    url   = curated_memes[index][1]

    db.append([title, url])

@app.route("/load")
def load():
    """ Route to return the posts """

    time.sleep(0.2)  # Used to simulate delay

    if request.args:
        counter = int(request.args.get("c"))  # The 'counter' value sent in the QS

        if counter == 0:
            print(f"Returning posts 0 to {quantity}")
            # Slice 0 -> quantity from the db
            res = make_response(jsonify(db[0: quantity]), 200)

        elif counter == posts:
            print("No more posts")
            res = make_response(jsonify({}), 200)

        else:
            print(f"Returning posts {counter} to {counter + quantity}")
            # Slice counter -> quantity from the db
            res = make_response(jsonify(db[counter: counter + quantity]), 200)

    return res
