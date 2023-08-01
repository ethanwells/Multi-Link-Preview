from flask_cors import CORS
import os
import mysql.connector
import json as json
from flask import Flask, jsonify, request, send_file, render_template, make_response, url_for, redirect
from googleapiclient.discovery import build
import requests
import shutil
import createMultiPreview
import base64 
from flask_tailwind import Tailwind

app = Flask(__name__)
tailwind = Tailwind(app)

CORS(app)

# linkpreview api key
apiKey = 'ee90116b69e85da1f27ab213596f28fb'

@app.route('/')
def index():
     
    try:                
        api_key = 'AIzaSyBT5a_DbhbqdKQUJ1RK8rtCX9c5K8P5x1w'
        youtube = build('youtube', 'v3', developerKey=api_key)
        request = youtube.search().list(
            part='snippet',
            q='plaza',
            type='video',
            maxResults=5
        )
        response= request.execute()
        video_results = []
        for item in response['items']:
            video_id = item['id']['videoId']
            video_link = f'https://youtube.com/watch?v={video_id}'
            encoded_link = base64.b64encode(video_link.encode()).decode('utf-8')
            video_title = item['snippet']['title']
            video_results.append({'link': video_link, 'encoded_link': encoded_link, 'title': video_title})

        return render_template('pages/index.html', video_results=video_results)

    except Exception as e:
          return jsonify({'error': str(e)})

@app.route("/second")
def second():
    current_url = request.url
    video_url = request.args.get('video_url')
    decoded_url = base64.b64decode(video_url).decode('utf-8')    
    url = render_template('pages/preview.html', next_url=decoded_url)
    resp = make_response(url)
    resp.set_cookie('prev_url', current_url)
    # return render_template('pages/preview.html', next_url)
    return resp
    

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
    app.run(host='0.0.0.0', port=port, debug=true)

