# Sadboi

## Setup

```
pip install -r requirements.txt
```

Create `.env` file in project root directory:
```
FACE_SUBSCRIPTION_KEY=<your subscription key>
```

This repo provides a template for a Python/Flask app that streams images from the users webcam to a video player on an HTML page. Then when the use clicks a button, it will capture the image and POST it to a route in the Flask app. This route will send the image to the Azure Face API for face detection

## Acknowledgements
Used hackathon [template](https://github.com/jimbobbennett/Hackathon-CaptureImageForFaceDetection)

