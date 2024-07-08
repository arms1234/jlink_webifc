
import web
import sys
import json
import os
import time


import session
import ping_tool

render = web.template.render('templates/')


def make_resp_hdr(val, note):
    return {"val":val, "note":note}


def make_ping_response(addr):
    res, str = ping_tool.ping_begin(addr)
    if res == False:
        return make_resp_hdr("1", "Can't make ping")


    return make_resp_hdr("0", str)

def make_ping_wait_response():
    res, str = ping_tool.ping_next()
    if res == False:
        return make_resp_hdr("1", "Can't make ping")

    if res == 2:
        return make_resp_hdr("2", str)


    return make_resp_hdr("0", str)




class ping_service:
    def GET(self):
        cookies = web.cookies().get("user__id")  
        if cookies == None or session.check_id(cookies) == False:
            session.clear_id()
            raise web.seeother('/login')
            return


        web.header('Cache-Control', 'no-cache')
        #web.header('Last-Modified', 'Mon, 29 Jun 1998 02:28:12 GMT')
        s = render.ping()       
        #print s
        return s


    def POST(self):
        cookies = web.cookies().get("user__id")  
        if cookies == None or session.check_id(cookies) == False:
            session.clear_id()
            raise web.seeother('/login')
            return

        query = web.input(cmd = "")


        if query.cmd == "ping":
            #print "Ping!"
            #print query.address
            s = make_ping_response(query.address)
            #print s
            return s


        elif query.cmd == "ping_wait":
            #print "Ping Next!"
            s = make_ping_wait_response()
            #print s
            return s






