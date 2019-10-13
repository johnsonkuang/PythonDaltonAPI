import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from daltonize.daltonize import Daltonize
import requests
import base64

# Support for gomix's 'front-end' and 'back-end' UI.
app = Flask(__name__, static_folder='public', template_folder='views')
CORS(app)

# Set the app secret key from the secret environment variables.
app.secret = os.environ.get('SECRET')

daltonizer = Daltonize()

@app.route("/")
def hello():
    return jsonify({'url':'blank'})

@app.route("/image", methods=["GET"])
def convertImage():
  print(request.args.get('url'))
  try:
    url = request.args.get('url')

    tempimg = open('images/tempimg.jpg', 'wb')
    tempimg.write(requests.get(url).content)
    tempimg.close()

    daltonizer.daltonizeImage('tempimg.jpg', 'images/')

    with open('images/tempimg.jpg', 'rb') as image_file:
      return jsonify({"image": base64.b64encode(image_file.read())})
  except:
    return jsonify({"image": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="})
    

if __name__ == '__main__':
    app.run()