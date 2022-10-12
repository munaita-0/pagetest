from flask import Flask, jsonify, make_response
from google.cloud import storage

app = Flask(__name__)


@app.route("/")
def test():
    client = storage.Client()
    bucket = client.get_bucket('test-suzuki-onesdata-stg')
    html_str = bucket.get_blob('form/test.html').download_as_text()
    response = jsonify({'html': html_str})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response



@app.route("/cookie_test")
def cookie_test_2():
    resp = make_response()
    max_age = 60 * 60 * 24 * 1000
    # domain="xxxx" でdomain指定できるが、配信元以外のドメインを指定しするとcookie setされなかった
    # domainを指定しないと自動的に配信元のdomainが指定される
    resp.set_cookie('uid', value="asdf", max_age=max_age, path='/', secure=True, httponly=True)
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return resp


@app.route("/cookie_test_with_1st_domain")
def cookie_test_3():
    resp = make_response()
    max_age = 60 * 60 * 24 * 1000  # 120 days
    # pathを指定しないと自動的に / が指定される
    resp.set_cookie('uid', value="asdf", max_age=max_age, domain="ones-form-test.55-inc.jp", secure=True, httponly=True)
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return resp
