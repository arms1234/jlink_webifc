import web
import sys
import json
import os
import time
import session


from menu import build_menu
from xml_db import xml_db
from perror import PageError

data_router_config_script = "/jlinklte/scripts/data_router_init"
dyndns_init_script = "/jlinklte/scripts/dyndns_init"

render = web.template.render('templates/')

src_table_filename  = "/jlinklte/storage/ntrip/ntrip.dat"
ntrip_client = "/jlinklte/utils/ntripclient"

def prepare_src_table_from_file():
    try:
        src_tbl_file = open(src_table_filename)
    except IOError as e:
        return []

    src_table = []
    cas_cnt = 0;
    net_cnt = 0;
    str_cnt = 0;

    line = src_tbl_file.readline()
    while line:
        line = src_tbl_file.readline()
        if len(line) >= 3:
            line = line.rstrip("\r\n")
        if line[0:3] == "CAS":
            cas_cnt = cas_cnt + 1;
            src_table.append(line.split(";"))


        if line[0:3] == "NET":
            net_cnt = net_cnt + 1;
            src_table.append(line.split(";"))


        if line[0:3] == "STR":
            str_cnt = str_cnt + 1;
            src_table.append(line.split(";"))

    src_tbl_file.close()
    return src_table

def make_nmeagga_timeout_select_input(sel_from, sel):
    content = ""
    for sel_item in sel_from:
        if sel_item == sel:
            content = content + "<option selected=\"selected\">" + sel_item + " sec</option>"
        else:
            content = content + "<option>" + sel_item + " sec</option>"
    return content




def make_ntrip_page():
    db = xml_db()
    if db.open() == False:
        raise PageError("Could not open configuration storage")

    ntrip_client_settings = db.get_params_set("ntrip_client")
    if ntrip_client_settings == None:
        serv_name       = ""
        serv_port       = ""
        user            = ""
        pwd             = ""
        nmeagga         = ""
        nmeagga_timeout_sel = ""
        lat             = ""
        lng             = ""
        mpoint          = ""
        src_table       = ""
    else:
        #print ntrip_client_settings
        if ntrip_client_settings.has_key("serv_name") == True:
            serv_name = ntrip_client_settings["serv_name"]["val"]
        else:
            serv_name = ""

        if ntrip_client_settings.has_key("serv_port") == True:
            serv_port = ntrip_client_settings["serv_port"]["val"]
        else:
            serv_port = ""
        if ntrip_client_settings.has_key("user") == True:
            user = ntrip_client_settings["user"]["val"]
        else:
            user = ""
        if ntrip_client_settings.has_key("pwd") == True:
            pwd = ntrip_client_settings["pwd"]["val"]
        else:
            pwd = ""
        nmeagga   = ntrip_client_settings["nmeagga"]["val"]
        nmeagga_timeout_list = ["1", "2", "3", "4", "5", "10", "15", "20", "25", "30", "35", "40", "45", "50", "55", "60"]
        nmeagga_timeout_sel = make_nmeagga_timeout_select_input(nmeagga_timeout_list, ntrip_client_settings["nmeagga_timeout"]["val"])

        if ntrip_client_settings.has_key("mpoint_sel") == True:
            mpoint = ntrip_client_settings["mpoint_sel"]["val"]
        else:
            mpoint = ""
        if ntrip_client_settings.has_key("lat") == True:
            lat = ntrip_client_settings["lat"]["val"]
        else:
            lat = ""

        if ntrip_client_settings.has_key("lng") == True:
            lng = ntrip_client_settings["lng"]["val"]
        else:
            lng = ""


        try:
            src_table = json.dumps(prepare_src_table_from_file())
        except IOError as e:
            src_table = ""


    content = """$def with (serv_name, serv_port, user, pwd, nmeagga, nmeagga_timeout_sel, lat, lng, mpoint, src_table) \n
    <script type="text/javascript" src="/static/ntrip.js"></script>
    <div style="display:none;" id="src_table"><script type="application/json">$src_table</script></div>

    <form>
    <fieldset>
    <legend>NTRIP Client Settings</legend>
    <div class="setting">
        <div class="label">Server name/address:</div>
        <input maxlength="32" size="20" id="serv_name" name="serv_name" value="$serv_name" onblur="check_input(this, 'Server')"/>
    </div>
    <div class="setting">
        <div class="label">Port:</div>
        <input maxlength="63" size="20" value="$serv_port" name="serv_port" onblur="check_range(this,0,65535,'Port')" />
    </div>

    <div class="setting">
        <div class="label">User:</div>
        <input maxlength="63" size="20" value="$user" id="user" name="user" onblur="check_input(this, 'User')" />
    </div>


    <div class="setting">
        <div class="label">Password:</div>
        <input maxlength="63" size="20" value="$pwd" type="password" id="pwd" name="pwd" onblur="check_input(this, 'Password')" />
    </div>



    <div class="setting">
        <input type="hidden" id="mpoint" value="$mpoint"/>
        <div class="label">Mountpoint:</div>
        <select id="mpoint_sel" style="width:200px;text-align:left;" name="mpoint" onchange="mpoint_sel_change()">
        </select>
    </div>



    <div class="setting"><div class="label">NMEAGGA Timeout:</div><select
    name="nmeagga_timeout_str" id="nmeagga_timeout_sel" style="width: 140px">$nmeagga_timeout_sel</select></div>
    </fieldset>
    <br />

    <div class="submitFooter">
    <input id="save_btn" type="button" value="Save Settings" onclick="save_ntrip_settings()" />
    <input type="reset" value="Cancel Changes" />
    </div>
    </form>


    <br />
    <br />


    <fieldset>
    <legend>Sources</legend>

    <h2 id="stream"><div>Stream:</div> <div></div> </h2>
    <div id=src_pars>
    <div class="setting" id="mp_0"> <div class="label">Mountpoint:</div><div></div></div>
    <div class="setting" id="mp_1"> <div class="label">Authentication:</div><div></div></div>

    <div class="setting" id="mp_2"> <div class="label">Format:</div><div></div></div>
    <div class="setting" id="mp_3"> <div class="label">Format-Details:</div><div></div></div>
    <div class="setting" id="mp_4"> <div class="label">Carrier:</div><div></div></div>
    <div class="setting" id="mp_5"> <div class="label">Client must send NMEA-GGA:</div><div></div></div>
    <div class="setting" id="mp_6"> <div class="label">System:</div><div></div></div>
    <div class="setting" id="mp_7"> <div class="label">Country:</div><div></div></div>
    <div class="setting" id="mp_8"> <div class="label">Latitude:</div><div></div></div>
    <div class="setting" id="mp_9"> <div class="label">Longitude:</div><div></div></div>
    <div class="setting" id="mp_10"> <div class="label">Generator:</div><div></div></div>
    <div class="setting" id="mp_11"> <div class="label">Solution:</div><div></div></div>
    <div class="setting" id="mp_12"> <div class="label">Compression:</div><div></div></div>
    <div class="setting" id="mp_13"> <div class="label">Bitrate:</div><div></div></div>
    <div class="setting" id="mp_14"> <div class="label">Charges:</div><div></div></div>
    <div class="setting" id="mp_15"> <div class="label">Miscellaneous:</div><div></div></div>
    <br />

    <div class="setting" id="mp_16" style=\"font-weight:bold;\"> <div class="label">Network:</div><div></div></div>
    <div class="setting" id="mp_17"> <div class="label">Operator:</div><div></div></div>
    <div class="setting" id="mp_18"> <div class="label">Details:</div><div></div></div>
    <div class="setting" id="mp_19"> <div class="label">Registration:</div><div></div></div>
    </div>


    </fieldset>
    <br />


    <div class="submitFooter">
    <input type="button" value="Previous" onClick="on_prev()"/>
    <input type="button" value="Next" onClick="on_next()"/>
    <input type="button" value="Select" onClick="on_select()"/>
    <input id="update_btn" type="button" value="Update" onClick="on_update()"/>
    </div>
    """

    content = web.template.Template(content)
    return content(serv_name, serv_port, user, pwd, nmeagga, nmeagga_timeout_sel, lat, lng, mpoint, src_table)



#    <div class="setting">
#        <div class="label">NMEA:</div>
#        $if nmea != "":
#            <div><input type="checkbox" maxlength="63" size="20" id="nmea" name="nmea" checked="checked" onclick="nmea_change(this)"/>Should be sent</div>
#        $else:
#            <div><input type="checkbox" maxlength="63" size="20" id="nmea" name="nmea" onclick="nmea_change(this)"/>Should be sent</div>
#    </div>
#    <div class="setting" >
#        <div class="label">Latitude:</div>
#        $if nmea == "":
#            <input id="lat" maxlength="63" size="15" name="lat" value="$lat" disabled="disabled" />
#        $else:
#            <input id="lat" maxlength="63" size="15" name="lat" value="$lat"/>
#    </div>
#    <div class="setting">
#        <div class="label">Longitude:</div>
#        $if nmea == "":
#            <input id="lng" maxlength="63" size="15" name="lng" value="$lng" disabled="disabled"/>
#        $else:
#            <input id="lng" maxlength="63" size="15" name="lng" value="$lng" />
#    </div>



def send_sourcetable():
    db = xml_db()
    if db.open() == False:
        raise PageError("Could open data base")

    ntrip_client_settings = db.get_params_set("ntrip_client")
    if ntrip_client_settings == None:
        raise PageError("NTRIP server isn't defined")
    else:
        serv_name = ntrip_client_settings["serv_name"]["val"]
        serv_port = ntrip_client_settings["serv_port"]["val"]

        if serv_name == None or serv_name == "":
            raise PageError("NTRIP server address isn't defined")

        if serv_port == None or serv_port == "":
            serv_port = "2101"


    import subprocess
    proc = subprocess.Popen(ntrip_client + " -s " + serv_name + " -r " + serv_port + " >" + src_table_filename, shell=True)
    res = proc.wait()

    if res != 0:
        raise PageError("Could not update source table!")

    try:
        src_table = prepare_src_table_from_file()
    except IOError as e:
        return json.dumps({"err":"2", "errmsg":"There is no actual source table!"})

    nmeagga = "Disable"
    mpoint = ""
    for mp in src_table:
        if mp[0] == "STR":
            mpoint = mp[1] + "/" + mp[3] + "/" + mp[6]
            if mp[11] == "1":
                nmeagga = "Enable"
            break;

    res = db.set_params_set("ntrip_client", {"mpoint_sel":"0", "mpoint": mpoint, "nmeagga": nmeagga})
    if res == "":
        db.update()

    #print "Send source table"
    return json.dumps({"err":"0", "errmsg":"", "stbl":src_table})


def save_ntrip_settings(query):
    db = xml_db()
    if db.open() == False:
        raise PageError("Could not open data base")

    query.pop("cmd")
#    if not query.has_key("nmea"):
#        query["nmea"] = "off"
    print "*************************************"
    print query

    res = db.set_params_set("ntrip_client", query)

    if res == "":
        db.update()
        import subprocess
        proc = subprocess.Popen(data_router_config_script, shell=True)
        res = proc.wait()
        return {"err":"0", "errmsg":""}
    else:
        return {"err":"1", "errmsg":"Could not save settings"}


def make_tcpo_page():
    db = xml_db()
    if db.open() == False:
        raise PageError("Could not open configuration storage")

    tcp_output_settings = db.get_params_set("tcp_output")
    if tcp_output_settings == None:
        server_port = ""
    else:
        #print tcp_output_settings
        if tcp_output_settings.has_key("server_port") == True:
            server_port = tcp_output_settings["server_port"]["val"]
        else:
            server_port = ""

    content = """$def with (server_port) \n
    <script type="text/javascript" src="/static/tcpo.js"></script>
    <h2>TCP Output Settings</h2>
    <form>
    <div class="setting">
        <div class="label">Port: ( in range 8100 - 8200 ) </div>

        <input maxlength="63" size="20" value="$server_port" name="server_port" onblur="check_range(this,8100,8200,'Port')" />
    </div>
    <div class="submitFooter">
    <input id="save_btn" type="button" value="Save Settings" onclick="save_tcpo_settings()" />
    <input type="reset" value="Cancel Changes" />
    </div>
    </form>
    """

    content = web.template.Template(content)
    return content(server_port)

def save_tcpo_settings(query):
    db = xml_db()
    if db.open() == False:
        raise PageError("Could not open data base")

    query.pop("cmd")

    res = db.set_params_set("tcp_output", query)

    if res == "":
        db.update()
        import subprocess
        proc = subprocess.Popen(data_router_config_script, shell=True)
        res = proc.wait()
        return {"err":"0", "errmsg":""}
    else:
        return {"err":"1", "errmsg":"Could not save settings"}



def make_tcp_page():
    db = xml_db()
    if db.open() == False:
        raise PageError("Could not open configuration storage")

    tcp_client_settings = db.get_params_set("tcp_client")
    if tcp_client_settings == None:
        serv_name = ""
        serv_port = ""
        user      = ""
        pwd       = ""
        nmeagga      = "Disable"
    else:
        #print tcp_client_settings
        if tcp_client_settings.has_key("serv_name") == True:
            serv_name = tcp_client_settings["serv_name"]["val"]
        else:
            serv_name = ""
        if tcp_client_settings.has_key("serv_port") == True:
            serv_port = tcp_client_settings["serv_port"]["val"]
        else:
            serv_port = ""
        if tcp_client_settings.has_key("user") == True:
            user = tcp_client_settings["user"]["val"]
        else:
            user = ""
        if tcp_client_settings.has_key("pwd") == True:
            pwd = tcp_client_settings["pwd"]["val"]
        else:
            pwd = ""
        nmeagga = tcp_client_settings["nmeagga"]["val"]


    content = """$def with (serv_name, serv_port, user, pwd, nmeagga) \n
    <script type="text/javascript" src="/static/tcp.js"></script>
    <h2>TCP Client Settings</h2>
    <form>
    <div class="setting">
        <div class="label">Server name/address:</div>
        <input maxlength="32" size="20" id="serv_name" name="serv_name" value="$serv_name" onblur="check_input(this, 'Server')"/>
    </div>
    <div class="setting">
        <div class="label">Port:</div>
        <input maxlength="63" size="20" value="$serv_port" name="serv_port" onblur="check_range(this,0,65535,'Port')" />
    </div>
    <div class="setting">
        <div class="label">User:</div>
        <input maxlength="63" size="20" value="$user" id="user" name="user" onblur="check_input(this, 'User')" />
    </div>
    <div class="setting">
        <div class="label">Password:</div>
        <input maxlength="63" size="20" value="$pwd" type="password" id="pwd" name="pwd" onblur="check_input(this, 'Password')" />
    </div>
    <div class="setting">
        <div class="label">NMEA:</div>
        $if nmeagga == "Enable":
            <div><input type="checkbox" maxlength="63" size="20" id="nmeagga" name="nmeagga" checked="checked" onclick="nmea_change(this)"/></div>
        $else:
           <div><input type="checkbox" maxlength="63" size="20" id="nmeagga" name="nmeagga" onclick="nmea_change(this)"/></div>
    </div>
    <div class="submitFooter">
    <input id="save_btn" type="button" value="Save Settings" onclick="save_tcp_settings()" />
    <input type="reset" value="Cancel Changes" />
    </div>
    </form>
    """


    content = web.template.Template(content)
    return content(serv_name, serv_port, user, pwd, nmeagga)


def save_tcp_settings(query):
    db = xml_db()
    if db.open() == False:
        raise PageError("Could not open data base")

    query.pop("cmd")
    if not query.has_key("nmeagga"):
        query["nmeagga"] = "Disable"
    else:
        print "DBG: NMEA=" + query["nmeagga"]
        if query["nmeagga"] == "on":
            query["nmeagga"] =  "Enable"
        else:
            query["nmeagga"] =  "Disable"

    res = db.set_params_set("tcp_client", query)

    if res == "":
        db.update()
        import subprocess
        proc = subprocess.Popen(data_router_config_script, shell=True)
        res = proc.wait()
        return {"err":"0", "errmsg":""}
    else:
        return {"err":"1", "errmsg":"Could not save settings"}


def make_dyndns_page():
    db = xml_db()
    if db.open() == False:
        raise PageError("Could not open configuration storage")

    dyndns_client_settings = db.get_params_set("dyndns_client")
    if dyndns_client_settings == None:
        user        = ""
        pwd         = ""
        host_name   = ""
        en_client   = "Disable"
    else:
        if dyndns_client_settings.has_key("user") == True:
            user = dyndns_client_settings["user"]["val"]
        else:
            user = ""
        if dyndns_client_settings.has_key("pwd") == True:
            pwd = dyndns_client_settings["pwd"]["val"]
        else:
            pwd = ""
        if dyndns_client_settings.has_key("host_name") == True:
            host_name = dyndns_client_settings["host_name"]["val"]
        else:
            host_name = ""
        if dyndns_client_settings.has_key("en_client") == True:
            en_client = dyndns_client_settings["en_client"]["val"]
        else:
            en_client = "Disable"

    content = """$def with (host_name, user, pwd, en_client) \n
    <script type="text/javascript" src="/static/dyndns.js"></script>
    <h2>DYNDNS Client Settings</h2>
    <form>
    <div class="setting">
        <div class="label">User:</div>
        <input maxlength="63" size="20" value="$user" id="user" name="user" onblur="check_input(this, 'User')" />
    </div>
    <div class="setting">
        <div class="label">Password:</div>
        <input maxlength="63" size="20" value="$pwd" type="password" id="pwd" name="pwd" onblur="check_input(this, 'Password')" />
    </div>
    <div class="setting">
        <div class="label">Host name:</div>
        <input maxlength="63" size="20" value="$host_name" id="host_name" name="host_name" onblur="check_input(this, 'Server')" />
    </div>
    <div class="setting">
        <div class="label">Enable Client:</div>
        $if en_client == "Enable":
            <div><input type="checkbox" maxlength="63" size="20" id="en_client" name="en_client" checked="checked" onclick="nmea_change(this)"/></div>
        $else:
           <div><input type="checkbox" maxlength="63" size="20" id="en_client" name="en_client" onclick="nmea_change(this)"/></div>
    </div>
    <div class="submitFooter">
    <input id="save_btn" type="button" value="Save Settings" onclick="save_dyndns_settings()" />
    <input type="reset" value="Cancel Changes" />
    </div>
    </form>
    """

    content = web.template.Template(content)
    return content(host_name, user, pwd, en_client)



def save_dyndns_settings(query):
    db = xml_db()
    if db.open() == False:
        raise PageError("Could not open data base")

    query.pop("cmd")
    if not query.has_key("en_client"):
        query["en_client"] = "Disable"
    else:
        if query["en_client"] == "on":
            query["en_client"] =  "Enable"
        else:
            query["en_client"] =  "Disable"

    res = db.set_params_set("dyndns_client", query)
    if res == "":
        db.update()
        import subprocess
        proc = subprocess.Popen(dyndns_init_script, shell=True)
        res = proc.wait()
        return {"err":"0", "errmsg":""}
    else:
        return {"err":"1", "errmsg":"Could not save settings"}


def make_ping_page():
    import subprocess

    proc = subprocess.Popen("ifconfig | grep -E \"^\w+  \" | cut -f1 -d\" \"", shell=True, stdout=subprocess.PIPE)
    res = proc.wait()

    ifaces = ""
    if res == 0:
        for line in proc.stdout:
            net_iface = line.rstrip()
            net_iface_name = ""
            if net_iface == "lo":
                net_iface_name = "Local"
            elif net_iface == "br0":
                net_iface_name = "Bluetooth"
            elif net_iface == "eth0":
                net_iface_name = "Ethernet"
            elif net_iface == "eth1":
                net_iface_name = "GSM"
            elif net_iface == "wlan0":
                net_iface_name = "Wi-Fi"
            if net_iface_name != "":
                ifaces = ifaces + "<option>" + net_iface_name + "</option>"




    content = """$def with (ifaces) \n
    <script type="text/javascript" src="/static/ping.js"></script>
    <h2>Ping Service</h2>
    <div>
       <div class="setting"><div class="label">Destination (URL/IP address):</div><input id="ip_addr" maxlength="63" size="20" type="text" value="" style="text-align: right;"/></div>
       <div class="setting"><div class="label">Network interface:</div><select
       id="iface" style="width: 100px; text-align: center;">$ifaces</select></div>
       <h2></h2>
       <div id="ping_result" style="height: 200px;">
       </div>
       <br />
       <form>
       <div class="submitFooter">
       <input id="ping_start_btn" type="button" value="Go" onClick="ping_start(this)"/>
       <input onclick="window.location.replace('/ping')" type="button" value="Refresh" />
       </div>
       </form>
     </div>
    """


    content = web.template.Template(content)
    return content(ifaces)


def ping_start(query):
    import ping_tool
    #print query

    if query.iface == "Local":
        iface = "lo"
    elif query.iface == "Bluetooth":
        iface = "br0"
    elif query.iface == "Ethernet":
        iface = "eth0"
    elif query.iface == "GSM":
        iface = "eth1"
    elif query.iface == "Wi-Fi":
        iface = "wlan0"

    res, ping_res = ping_tool.ping_begin(query.addr, iface)
    if res == False:
        return {"err":"1", "errmsg":"Could not do ping"}
    else:
        #print ping_res
        return json.dumps({"err":"0", "errmsg":"", "ping_res":ping_res})

def ping_next(query):
    import ping_tool
    res, ping_res = ping_tool.ping_next()
    if res == False:
        return {"err":"1", "errmsg":"Could not do ping"}

    if res == 2:
        return json.dumps({"err":"2", "errmsg":"", "ping_res":ping_res})   # There is no error. Just ping finish indication.

    return json.dumps({"err":"0", "errmsg":"", "ping_res":ping_res})



def make_pairing_page():

    ifaces = "<option>SER</option><option>BT</option><option>USB</option>"

    content = """$def with (ifaces) \n
    <script type="text/javascript" src="/static/pairing.js"></script>
    <h2>Pairing Service</h2>
    <div>
       <div class="setting"><div class="label">Pairing interface:</div><select
       id="iface" style="width: 100px; text-align: center;">
            <option>Serial</option><option>Bluetooth</option><option>USB</option></select></div>
       <br />
       <form>
       <div class="submitFooter">
       <input id="pairing_start_btn" type="button" value="Pair" onClick="pairing_start(this)"/>
       <input id="unpairing_start_btn" type="button" value="UnPair" onClick="unpairing_start(this)"/>
       </div>
       </form>
     </div>
    """


    content = web.template.Template(content)
    return content(ifaces)



def pairing_start(query):
    import subprocess

    if query.iface == "Bluetooth":
        iface = "BT"
    elif query.iface == "Serial":
        iface = "SER"
    else:
        iface = "USB"

    proc = subprocess.Popen("jlink pairing " + iface, shell=True, stdout=subprocess.PIPE)
    res = proc.wait()
    out = ""
    for line in proc.stdout:
        out += line
    return json.dumps({"err":"0", "errmsg":"", "pairing_res":out})   #There is no error. Just finish indication.



def unpairing_start(query):
    import subprocess

    if query.iface == "Bluetooth":
        iface = "BT"
    elif query.iface == "Serial":
        iface = "SER"
    else:
        iface = "USB"

    proc = subprocess.Popen("jlink unpairing " + iface, shell=True, stdout=subprocess.PIPE)
    res = proc.wait()
    out = ""
    for line in proc.stdout:
        out += line
    return json.dumps({"err":"0", "errmsg":"", "pairing_res":out})   #There is no error. Just finish indication.


class services:
    def GET(self):
        if session.check_session() == False:
            return
        path = web.ctx.path
        content = ""
        try:
            if (path == "/services" or path == "/ntrip"):
                menu = build_menu("Services", "NTRIP")
                content = make_ntrip_page()
            elif (path == "/tcp"):
                menu = build_menu("Services", "TCP")
                content = make_tcp_page()
            elif (path == "/tcpo"):
                menu = build_menu("Services", "TCPO")
                content = make_tcpo_page()
            elif (path == "/dyndns"):
                menu = build_menu("Services", "DYNDNS")
                content = make_dyndns_page()
            elif (path == "/ping"):
                menu = build_menu("Services", "Ping")
                content = make_ping_page()
            elif (path == "/pairing"):
                menu = build_menu("Services", "Pairing")
                content = make_pairing_page()



        except PageError as perr:
            content = perr.errmsg



        return render.webiface(menu, content)



    def POST(self):
        #if session.check_session() == False:
        #    return

        query = web.input()
        #print query


        if query.cmd == None:
            return {"err":"1", "errmsg":"There is no cmd field!"}


        try:
            if query.cmd == "get_src_tbl":
                return send_sourcetable()
            elif query.cmd == "save_ntrip_settings":
                save_ntrip_settings(query)
                return {"err":"0", "errmsg":""}
            elif query.cmd == "save_tcpo_settings":
                save_tcpo_settings(query)
                return {"err":"0", "errmsg":""}
            elif query.cmd == "save_tcp_settings":
                save_tcp_settings(query)
                return {"err":"0", "errmsg":""}
            elif query.cmd == "save_dyndns_settings":
                save_dyndns_settings(query)
                return {"err":"0", "errmsg":""}
            elif query.cmd == "ping_start":
                return ping_start(query)
            elif query.cmd == "ping_next":
                return ping_next(query)
            elif query.cmd == "pairing_start":
                return pairing_start(query)
            elif query.cmd == "unpairing_start":
                return unpairing_start(query)
            else:
                return {"err":"1", "errmsg":"There is no correct cmd field!"}

        except PageError as perr:
            return {"err":"1", "errmsg":perr.errmsg}

        return {"err":"0", "errmsg":""}



