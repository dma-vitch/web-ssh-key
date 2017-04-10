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
logging.basicConfig(level = logging.DEBUG)
config_file = "conf/config"

# DEFAULTS = {
#     'debug': 'false',
#     'host': '0.0.0.0',
# }

# Parsing config file
if not os.path.exists(config_file):
    logging.info('Not found configuration file %s' %(config_file))
    exit(65)

config = SafeConfigParser()

# Load the configuration file
config.read(config_file)

logging.info('Reading configuration from %s' % (config_file))

server_host = config.get('server_setting', 'host')
server_port = config.get('server_setting', 'port')

# Render main page
@app.route("/")
def appMain():
    return redirect(url_for('login'))

# Render login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


def pexec(*args):
    # return subprocess.Popen(args, stdout=subprocess.PIPE).communicate()[0].rstrip()
    return subprocess.Popen(args, shell=True, stderr=subprocess.PIPE)

#cmd = "/bin/ssh-copy-id" ' ' + "-i" + ' ' + "pub_key" + ' ' + result

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


#key = open(os.path.dirname).read()
print(key)
#username = os.getlogin()
#password = getpass()
# hosts = ["hostname1", "hostname2", "hostname3"]
# for host in hosts:
#     deploy_key(key, host, username, password)

if __name__ == "__main__":
    app.run(host = server_host, port = server_port)
