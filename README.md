# Sadboi

A few too many nights spent binge-eating a whole tub of Ben and Jerry's, crying in bed and watching reruns of Friends. What if you could rely on a friendly website to whose goal is to put a smile on your face?

This WebApp is designed to turn you from a sad boi to a happy boi. Utilizing real-time emotional feedback provided by Microsoft Face API, our page reflects your mood and is with you every step of the way. It turns happy when you're happy and sad when you're sad. It offers personalized uplifting compliments and a near endless supply of curated memes in a minimal way. Experience it yourself by heading over to [sadboi.space](http://sadboi.space).

This project was built from [this template](https://github.com/jimbobbennett/Hackathon-CaptureImageForFaceDetection).


## Setup

- Install required Python dependencies.
```
pip install -r requirements.txt
```

- Create an environment `.env` file in project root directory:
```
FACE_SUBSCRIPTION_KEY=<your subscription key>
FACE_ENDPOINT=<your endpoint>
```

- Run the app locally on localhost:5000.
```
flask run
```
tip: set `FLASK_ENV=development` to turn on debugging.


### Tech stack
Python Flask framework for backend. Boostrap, HTML and vanilla JS for frontend.

### Gallery
![sad bois](https://challengepost-s3-challengepost.netdna-ssl.com/photos/production/software_photos/000/913/393/datas/gallery.jpg)

![happy bois](https://challengepost-s3-challengepost.netdna-ssl.com/photos/production/software_photos/000/913/394/datas/gallery.jpg)

##### Built for Hack Cambridge 2020.



