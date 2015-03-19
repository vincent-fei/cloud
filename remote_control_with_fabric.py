#!/usr/bin/env python
from fabric.api import *

env.user = "username"
env.gateway = "54.xx.xx.xx"
env.password = "password"
env.roledefs = {
    'webpay' : ['10.0.0.x','10.0.1.x'],
    'www'    : ['10.1.0.x','10.1.1.x'],
    'nginx'  : ['10.2.0.x','10.2.1.x']
    }

@runs_once
def local_task():
    local("whoami")

@roles('webpay')
def webpay_task():
    #restart all tomcats instance
    with cd("/home/webapp/admin"):
        run("./restart.sh")

@roles('www')
def www_task():
    #restart php-fpm
        sudo("/etc/init.d/php-fpm restart")

@roles('nginx')
def nginx_task():
    #reload nginx
        sudo("/usr/local/nginx/sbin/nginx -s reload")

def deploy():
    execute(webpay_task)
    execute(www_task)
    execute(nginx_task)

if __name__ == '__main__':
    webpay_task()
    www_task()
    nginx_task()
