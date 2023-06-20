from flask import Flask
from flask_cors import CORS
import os
import mysql.connector
import json as json
from flask import Flask, jsonify, request
import requests
import shutil
import createMultiPreview
from flask import send_file

app = Flask(__name__)

CORS(app)

# linkpreview api key
apiKey = 'ee90116b69e85da1f27ab213596f28fb'

@app.route('/createMultiLink', methods=['GET'])
def hello_world():
    # delete previous preview generated
    if os.path.exists("multi-link-preview.jpg"):  # If the file exists, delete it
        os.remove("multi-link-preview.jpg")
    links = request.args.getlist('links')  # get list of links from query param
    if links is None:
        return 'No link provided', 400  # return Bad Request response
    
    # process each link:
    image_names = []
    for i, link in enumerate(links):
        # get link preview data from LinkPreview API
        linkPreviewResponse = requests.get(f"http://api.linkpreview.net/?key={apiKey}&q={link}")
        data = linkPreviewResponse.json()  # convert response to json

        # Make request to download image from data
        imageResponse = requests.get(data['image'])

        # check if request was successful
        if imageResponse.status_code == 200:
            # save image to local storage
            with open(f'image{i}.jpg', 'wb') as f:
                for chunk in imageResponse.iter_content(chunk_size=1024):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)
            image_names.append(f'image{i}.jpg')
        else: 
            return f'Error downloading image: {link}', 500
    createMultiPreview.run(image_names)  # create multi preview image
    # delete all images saved locally
    for image_name in image_names:
        os.remove(image_name)
    return send_file('multi-link-preview.jpg', mimetype='image/jpeg'), 200

port = int(os.environ.get("PORT", 5000))
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)