

import web
import sys
import os

import session
from xml_db import xml_db
from perror import PageError

printenv_util = "/jlinklte/utils/fw_printenv"


class logout:
    def GET(self):
        session.clear_id()

        resp = """\
                <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
        <html>
        <head>
             <link rel="stylesheet" type="text/css" href="/static/webiface.css" />
        </head>
        <body class="gui"><br><h2><span>You have been logged out...</span></h2></body>
        </html>
        """
        return resp



class login:
    def GET(self):
        db = xml_db()
        if db.open() == False:
            raise PageError("Could not open configuration storage")

        fw_uuid = db.get_params_set("fw_uuid")
        product_id = fw_uuid["product_id"]["val"]
        serial_num =  os.popen(printenv_util  + " sn 2>/dev/null").read().rstrip("\n")
        if serial_num != None and serial_num != "":
            serial_num = serial_num.split("=")[1]
        else:
            serial_num = "unknown"
        resp = """$def with (product_id, serial_num)\n
        <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
        <html>
        <head>
             <link rel="stylesheet" type="text/css" href="/static/webiface.css" />
             <link rel="stylesheet" type="text/css" href="/static/apprise.css"/>    
             <script type="text/JavaScript" src="/static/apprise.js" ></script>
             <script type="text/Javascript" src="/static/jquery-1.4.2.min.js" ></script>
             <script>
             var product_id = $product_id;
             var serial_num = $serial_num;
             </script>
             <script type="text/javascript" src="/static/login.js"></script>  
        </head>
        <body class="gui"></body>
        </html>
        """
        resp = web.template.Template(resp)
        return resp(product_id, serial_num)






    #print web.ctx.env

#        auth = web.ctx.env.get('HTTP_AUTHORIZATION')
#
#        sid = web.cookies().get("user__id") 
#         
#        if auth != None or session.get_id():
#            import re
#            import base64
#            auth = re.sub('^Basic ','',auth)
#            username, password = base64.decodestring(auth).split(':')
#            #print username
#            #print password        
#
#            if session.check_admin_account(username, password) == True:                                                
#                session_id = session.assign_id()
#                web.setcookie("user__id", session_id, 3600)
#                session.set_id(session_id)
#
#                raise web.seeother('/')
#                return
#        else:
#            print "No Auth"
#
#         
#


#        session_id = session.get_id()

#        if session_id == None:            
#            session_id = session.assign_id()
#            web.setcookie("user__id", session_id, 3600)
#        else:           
#            auth = web.ctx.env.get('HTTP_AUTHORIZATION')
#            if auth != None:
                #print "autor"

#                import re
#                import base64
#                auth = re.sub('^Basic ','',auth)
#                username, password = base64.decodestring(auth).split(':')
                #print username
                #print password        

#                if session.check_admin_account(username, password) == True:                                
#                    raise web.seeother('/')
#                    return



        web.header('WWW-Authenticate','Basic realm="Login page"')
        web.ctx.status = '401 Unauthorized'
        return


    def POST(self):
        #if session.check_session() == False:
        #    return

        query = web.input()
        print query


        if query.cmd == None:
            return {"err":"1", "errmsg":"There is no cmd field!"}


        if query.cmd == "login":
            if session.check_admin_account(query.login, query.password) == True:                                                
                session_id = session.assign_id()
                print "Update session id ", session_id
                session.set_id(session_id)
                #web.setcookie("user__id", session_id, 3600)
                return {"err":"0", "errmsg":"", "session_id": session_id, "expires": "3600"}
            else:
                print "Wrong password/login"
                return {"err":"1", "errmsg":"Wrong password/login"}
        else:
            return {"err":"1", "errmsg":"There is no correct cmd field!"}


        return {"err":"0", "errmsg":""}

