from flask import render_template


def create_webpage(uniqueImageID, links):
    # construct the URL of the image
    image_url = f"https://storage.googleapis.com/multi-link-preview-images/{uniqueImageID}.jpg"

    # render a webpage with the image and the list of links
    return render_template('unique_webpage.html', image_url=image_url, links=links)