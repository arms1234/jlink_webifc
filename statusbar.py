
import web
import sys
import json
import os
import time
import session
import re


from perror import PageError


render = web.template.render('templates/')


#def make_statusbar_page()
#    return ""

class statusbar:
    def GET(self):
        #if session.check_session() == False:
        #    return
        path = web.ctx.path
        content = ""

        #try:
        #    if (path == "/statusbar"):
        #        content = make_statusbar_page()
        #    else:
        #        raise PageError("Error!")
        #
        #except PageError as perr:
        #    content = perr.errmsg

        return render.statusbar()



    def POST(self):
        #if session.check_session() == False:
        #    return

        query = web.input()
        print query


        return {"err":"0", "errmsg":""}



