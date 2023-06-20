from flask import Flask
from flask_cors import CORS
import os
import json as json
from flask import Flask, jsonify, request, url_for, send_file, render_template
import requests
import createMultiPreview
from google.cloud import storage
import uuid
import uniqueWebpage
from pymongo import MongoClient
import bson
import random

app = Flask(__name__)

CORS(app)

# create a MongoDB client
mongo_client = MongoClient("mongodb+srv://ethanthewells:wN72WqVgAuUaEf6N@multi-link-preview.pxruagg.mongodb.net/imageID-to-links-db")

# connect to mongoDB database
db = mongo_client["imageID-to-links"]

# Create a google cloud storage client
googleCloudStorageClient = storage.Client()

# linkpreview api key
apiKey = 'ee90116b69e85da1f27ab213596f28fb'

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/createMultiLink', methods=['GET'])
def create_multi_link():
    # delete previous preview generated
    if os.path.exists("multi-link-preview.jpg"):  # If the file exists, delete it
        os.remove("multi-link-preview.jpg")
    links = request.args.getlist('links')  # get list of links from query param
    if links is None:
        return 'No link provided', 400  # return Bad Request response
    print("received links:")
    print(f"bulk: {links} | type: {type(links)} | len: {len(links)}")
    for i, link in enumerate(links):
        print(f"{i}: {link}")
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

    # upload image to google cloud storage
    bucket = googleCloudStorageClient.bucket("multi-link-preview-images")  # get bucket
    
    # generate unique id for image
    uniqueId = ""
    while True:  # keep looping until we get a unique ID
        uniqueId = str(random.randint(1000000000, 9999999999))  # generate 10-digit random number and convert to string
        if db.links.find_one({"_id": uniqueId}) is None:  # if the ID doesn't exist in the database
            break  # we've found a unique ID, so we can stop looping
    print(f"uniqueID: {str(uniqueId)}")

    blob = bucket.blob(f"{uniqueId}.jpg")  # create blob
    blob.upload_from_filename("multi-link-preview.jpg")  # upload image to blob
    print(f"google cloud blob: https://storage.cloud.google.com/multi-link-preview-images/{uniqueId}.jpg?authuser=1")
    # insert new imageID-to-links mapping entry into MongoDB
    doc = {"_id": str(uniqueId), "links": links}
    db.links.insert_one(doc)

    # generate the URL for the webpage
    webpage_url = url_for('multi_link', id=str(uniqueId), _external=True)
    
    # return the URL to the client
    return jsonify({'url': webpage_url}), 200


# Create webpage for unique image id
# This is the webpage that will be shared
@app.route('/multi-link/<id>')
def multi_link(id):
    # get the entry with this uniaue imageID from MongoDB database
    doc = db.links.find_one({"_id": id})
    print(f"doc: {doc}  id: {id}")

    # check if the document exists
    if doc is None:
        return "Page not found | imageID not stored in DB", 404

    # get the list of links
    links = doc["links"]

    return uniqueWebpage.create_webpage(id, links)



port = int(os.environ.get("PORT", 5000))
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)