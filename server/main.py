from flask import Flask, jsonify
from google.cloud import storage

app = Flask(__name__)


@app.route("/")
def test():
    # html_str = "<!doctype html>\r\n" \
    #     "<html>\r\n" \
    #     "<div id='gtm_form'>\r\n" \
    #     "<p> aaaaaa</p>\r\n" \
    #     "<p> aaaaaa</p>\r\n" \
    #     "<p> aaaabb</p>\r\n" \
    #     "<p> aaaabb</p>\r\n" \
    #     "</html>"
    client = storage.Client()
    bucket = client.get_bucket('test-suzuki-onesdata-stg')
    html_str = bucket.get_blob('form/test.html').download_as_text()
    response = jsonify({'html': html_str})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
