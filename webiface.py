#!/usr/bin/python

import web
import sys
#import json

sys.dont_write_bytecode = True

import os
import time

from xml_db import xml_db
from login import login, logout

import session

from admin import admin
from status import status
from menu import build_menu
from services import services
from communication import communication
from setup import setup
from statusbar import statusbar




os.chdir("/jlinklte/webiface/")



urls = ('/', 'webiface',
        '/statusbar', 'statusbar',
        '/rou', 'setup',
        '/status', 'status', '/device', 'status', '/lans', 'status', '/uhfs',
        'status', '/gsms', 'status', '/wifis', 'status', '/bts', 'status',
        '/gpss', 'status', '/ntrips', 'status', '/tcps', 'status', '/tcpos', 'status', '/dyndnss', 'status', '/power', 'status',
        '/admin', 'admin', '/management', 'admin', '/fwupgrade', 'admin',
        '/logout', 'logout',
        '/login', 'login',
        '/services', 'services', '/ntrip', 'services', '/tcp', 'services', '/tcpo', 'services', '/dyndns', 'services', '/ping', 'services', '/pairing', 'services',
        '/communication', 'communication', '/lan', 'communication', '/uhf',
        'communication', '/extmodem', 'communication', '/gsm', 'communication',
        '/wifi', 'communication', '/bt', 'communication', '/gsetup', 'communication', '/adv',
        'communication')



render = web.template.render('templates/')
app = web.application(urls, globals())


web.webapi.internalerror = web.debugerror




class webiface:
    def GET(self):
        if session.check_session() == False:
            return


        return render.webiface2()



if __name__ == '__main__':

    if os.environ.has_key("DBUS_SESSION_BUS_ADDRESS") == False:
        import subprocess
        p = subprocess.Popen('dbus-launch', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for var in p.stdout:
            sp = var.split('=', 1)
            #print sp
            os.environ[sp[0]] = sp[1][:-1]

    app.run()



