import os

from auth import user
from flask import Flask, request, render_template

app = Flask(__name__)

# @app.route('/')
# def hello_world():
#     page = render_template('index.html')
#     return page

# Disable browser caching so changes in each step are always shown
@app.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/', methods=['GET'])
def say_hello():
    user_email = request.headers.get('X-Goog-Authenticated-User-Email')
    user_id = request.headers.get('X-Goog-Authenticated-User-ID')
    jwt_header = request.headers.get('X-Goog-IAP-JWT-Assertion')

    verified_email, verified_id = user()

    page = render_template('index.html',
        email=user_email,
        id=user_id,
        verified_email=verified_email,
        verified_id=verified_id,
        jwt=jwt_header)
    return page

@app.route('/privacy', methods=['GET'])
def show_policy():
    page = render_template('privacy.html')
    return page


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))