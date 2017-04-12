#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
from flask import Flask, render_template, url_for, redirect
from ConfigParser import SafeConfigParser
import subprocess
import paramiko

app = Flask(__name__)

# set logger level
logging.basicConfig(level=logging.DEBUG)
config_file = "conf/config"

# DEFAULTS = {
#     'debug': 'false',
#     'host': '0.0.0.0',
# }

# Parsing config file
if not os.path.exists(config_file):
    logging.info('Not found configuration file %s' % (config_file))
    exit(65)

config = SafeConfigParser()

# Load the configuration file
config.read(config_file)
logging.info('Reading configuration from %s' % (config_file))

server_host = config.get('server_setting', 'host')
server_port = config.getint('server_setting', 'port')
server_debug = config.get('server_setting', 'debug')
# This is the path to the upload directory
uploaded_dir = config.get('server_setting', 'dirupload')
# These are the extension that we are accepting to be uploaded
allowed_extensions = config.get('server_setting', 'allow_extension')

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ['allowed_extensions']

# Render main page
@app.route("/")
def index():
    return render_template('index.html')
    # return redirect(url_for('login'))

# Render login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded file
        return redirect(url_for('uploaded_file', filename=filename))
    else:
        return render_template('404.html')

# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('uploaded_dir',
                               filename)

def pexec(*args):
    # return subprocess.Popen(args, stdout=subprocess.PIPE).communicate()[0].rstrip()
    return subprocess.Popen(args, shell=True, stderr=subprocess.PIPE)


# cmd = "/bin/ssh-copy-id" ' ' + "-i" + ' ' + "pub_key" + ' ' + result

# result = username + '@' + hostname
# pexec('/bin/ssh-copy-id', '-i', 'pub_key', result)

# deploys key on server
def deploy_key(key, server, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, username=username, password=password)
    # client.exec_command('mkdir -p ~/.ssh/')
    client.exec_command('echo "%s" >> ~/.ssh/authorized_keys' % key)
    # client.exec_command('chmod 644 ~/.ssh/authorized_keys')
    # client.exec_command('chmod 700 ~/.ssh/')


# key = open(os.path.dirname).read()
#print(key)
# username = os.getlogin()
# password = getpass()
# hosts = ["hostname1", "hostname2", "hostname3"]
# for host in hosts:
#     deploy_key(key, host, username, password)

if __name__ == "__main__":
    app.run(
        host=server_host,
        port=server_port,
        debug=server_debug
    )
