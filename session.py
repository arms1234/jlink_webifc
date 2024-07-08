
from xml_db import xml_db
import web


## {{{ http://code.activestate.com/recipes/52252/ (r1)
# create a unique session id
# input - string to use as part of the data used to create the session key.
#         Although not required, it is best if this includes some unique 
#         data from the site, such as it's IP address or other environment 
#         information.  For ZOPE applications, pass in the entire ZOPE "REQUEST"
#         object.

def makeSessionId(st):
    import time, base64, string, hashlib

    md = hashlib.md5()
    md.update('this is a test of the emergency broadcasting system')
    md.update(str(time.time()))
    md.update(str(st))
    return string.replace(base64.encodestring(md.digest())[:-3], '/', '$')


## end of http://code.activestate.com/recipes/52252/ }}}




def check_id(sid):
    db = xml_db()
    if db.open() == False:
        return False

    session_id = db.get_session_id()
    if session_id == None:
        return False


    print session_id
    print sid

    if session_id == sid:
        return True

    return False


def get_id():
    db = xml_db()
    if db.open() == False:
        return False

    session_id = db.get_session_id()
    if session_id == "":
        session_id = None
    return session_id

def set_id(sid):
    db = xml_db()
    if db.open() == False:
        return False

    if db.set_session_id(sid) == True:
        db.update()

    return False



def clear_id():
    db = xml_db()
    if db.open() == False:
        return False

    if db.set_session_id("") == True:
        db.update()

    return False



def assign_id():
    session_id = makeSessionId("")

    #db = xml_db()
    #if db.open() == False:
    #    return session_id 

    #if db.set_session_id(session_id) == True:
    #    db.update()

    return session_id 



def check_admin_account(user, pwd):
    db = xml_db()
    if db.open() == False:
        return False

    account = db.get_admin_account()
    if account == None:
        return False

    #print "Account: ", account

    if account["username"] == "" or account["password"] == "":
        return True

    if user == account["username"] and pwd == account["password"]:
        return True

    return False



def check_session ():

    #sid = web.cookies().get("user__id")
    sid = web.cookies().get("session__id")
    print "Session ID to check: ", sid  
    if sid == None or check_id(sid) == False:
        clear_id()
        raise web.seeother('/login')
        return False

    return True

