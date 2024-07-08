

import web
import sys
import json
import os
import time
import session
import re
import fcntl
import array

from datetime import datetime
from menu import build_menu
from xml_db import xml_db
from perror import PageError


render = web.template.render('templates/')

printenv_util = "/jlinklte/utils/fw_printenv"



def make_device_status_page():

    db = xml_db()
    if db.open() == False:
        raise PageError("Could not open configuration storage")

    fw_uuid = db.get_params_set("fw_uuid")
    product_id = fw_uuid["product_id"]["val"]

    krnl_ver_env = os.popen(printenv_util  + " kernel_ver 2>/dev/null").read().rstrip("\n")
    if krnl_ver_env != None and krnl_ver_env != "":
        krnl_ver = krnl_ver_env.split("=")[1]
    else:
        krnl_ver = "unknown"


    fs_ver_env   = os.popen(printenv_util  + " fs_ver 2>/dev/null").read().rstrip("\n")
    if fs_ver_env != None and fs_ver_env != "":
        fs_ver = fs_ver_env.split("=")[1]
    else:
        fs_ver = "unknown"


    sn_env   = os.popen(printenv_util  + " sn 2>/dev/null").read().rstrip("\n")
    if sn_env != None and sn_env != "":
        sn = sn_env.split("=")[1]
    else:
        sn = "unknown"

    antpwr_env   = os.popen(printenv_util  + " antpwr 2>/dev/null").read().rstrip("\n")
    if antpwr_env != None and antpwr_env == "antpwr=1":
        anttype = "Active"
    else:
        anttype = "Passive"

    pn_env   = os.popen(printenv_util  + " pn 2>/dev/null").read().rstrip("\n")
    if pn_env != None and pn_env != "":
        pn = pn_env.split("=")[1]
    else:
        pn = "unknown"

    if pn == "01-597520-10" or pn == "01-597520-11" or pn == "01-597520-12" or pn == "01-597520-13" or\
       pn == "01-597520-20" or pn == "01-597520-21" or pn == "01-597520-22" or pn == "01-597520-23" or\
       pn == "01-597520-30" or pn == "01-597520-31" or pn == "01-597520-32" or pn == "01-597520-33" or\
       pn == "01-597520-40" or pn == "01-597520-41" or pn == "01-597520-42" or pn == "01-597520-43" or\
       pn == "01-597520-16" or pn == "01-597520-26" or pn == "01-597520-46" :
        product_name = "JLink LTE"
    elif pn == "01-597521-10" or pn == "01-597521-11" or pn == "01-597521-12" or pn == "01-597521-13" or\
         pn == "01-597521-20" or pn == "01-597521-21" or pn == "01-597521-22" or pn == "01-597521-23" or\
         pn == "01-597521-30" or pn == "01-597521-31" or pn == "01-597521-32" or pn == "01-597521-33" or\
         pn == "01-597521-40" or pn == "01-597521-41" or pn == "01-597521-42" or pn == "01-597521-43" or\
         pn == "01-597521-16" or pn == "01-597521-26" or pn == "01-597521-46" :
        product_name = "JLink LTE BAT"
    elif pn == "01-587300-50" or pn == "01-587300-51" or pn == "01-587300-52" or pn == "01-587300-53" or pn == "01-587300-54" :
        product_name = "HPT404BT"
    elif pn == "01-587100-50" or pn == "01-587100-51" or pn == "01-587100-52" or pn == "01-587100-53" or pn == "01-587100-54" :
        product_name = "HPT435BT"
    elif pn == "01-587400-50" or pn == "01-587400-51" or pn == "01-587400-52" or pn == "01-587400-53" or pn == "01-587400-54" :
        product_name = "HPT135BT"
    elif pn == "01-587500-50" or pn == "01-587500-51" or pn == "01-587500-52" or pn == "01-587500-53" or pn == "01-587500-54" :
        product_name = "HPT104BT"
    elif pn == "01-587800-50" or pn == "01-587800-51" or pn == "01-587800-52" or pn == "01-587800-53" or pn == "01-587800-54" :
        product_name = "HPT225BT"
    else:
        product_name = "Unknown"

    installed_hw_option = db.get_params_set("hw_option")
    hw_uhf = installed_hw_option["hw_uhf"]["val"]
    uhf_version = ""
    if hw_uhf == "installed":
        import dbus
        bus = dbus.SessionBus()
        try:
            remote_object = bus.get_object("jlinklte.uhfd", "/")
            iface = dbus.Interface(remote_object, "jlinklte.uhfd.interface")
            uhf_version = iface.uhf_get_fw_version()

        except dbus.DBusException:
            uhf_version = "unknown"


    try:
        dev_temp = "unknown"
        pwr_voltage = "unknown"

        import dbus
        bus = dbus.SessionBus()
        remote_object = bus.get_object("jlinklte.statusd", "/")
        iface = dbus.Interface(remote_object, "jlinklte.statusd.interface")
        dev_temp = iface.GetParticularStatus("Sensors", "TEMP")
        pwr_voltage = iface.GetParticularStatus("Sensors", "V_IN")
        bat_voltage = iface.GetParticularStatus("Sensors", "V_BAT")
        hw_rev = iface.GetParticularStatus("Info", "HW_REV")

    except IOError as e:
        dev_temp = "unknown"

    try:
        from datetime import timedelta

        with open('/proc/uptime', 'r') as f:
            uptime_seconds = int(float(f.readline().split()[0]))
            uptime_string = str(timedelta(seconds = uptime_seconds))

    except IOError as e:
        uptime_string = "unknown"

    cur_time = datetime.now().strftime("%H:%M:%S")
    date = datetime.now().strftime("%d %B %Y (%A)")

    content = """$def with (product_name, pn, product_id, krnl_ver, fs_ver, hw_rev, cur_time, date, dev_temp, sn, uptime, pwr_voltage, bat_voltage, hw_uhf, uhf_version, anttype) \n
    <h2>Device Information</h2>
    <div class="setting"><div class="label">Product name:</div>$product_name</div>
    <div class="setting"><div class="label">Product ID:</div>$product_id</div>
    <div class="setting"><div class="label">Serial number:</div>$sn</div>
    <div class="setting"><div class="label">Part number:</div>$pn</div>
    <div class="setting"><div class="label">Kernel version:</div>$krnl_ver</div>
    <div class="setting"><div class="label">File system version:</div>$fs_ver</div>
    $if hw_uhf == "installed":
        <div class="setting"><div class="label">Modem version:</div>$uhf_version</div>
    <div class="setting"><div class="label">Hardware revision:</div>$hw_rev</div>
    <div class="setting"><div class="label">GPS Antenna:</div>$anttype</div>
    <div class="setting"><div class="label">Current Time:</div>$cur_time</div>
    <div class="setting"><div class="label">Date:</div>$date</div>
    <div class="setting"><div class="label">Up Time:</div>$uptime</div>
    <div class="setting"><div class="label">Housing temperature:</div>$dev_temp &#8451</div>
    <div class="setting"><div class="label">Ext. power voltage:</div>$pwr_voltage V</div>
    $if bat_voltage != "":
        <div class="setting"><div class="label">BAT voltage:</div>$bat_voltage V</div>
    <br />
    <div class="submitFooter"><input onclick="window.location.replace('/device')" type="button" value="Refresh" /></div>
    """

    content = web.template.Template(content)
    return content(product_name, pn, product_id, krnl_ver, fs_ver, hw_rev, cur_time, date, dev_temp, sn, uptime_string, pwr_voltage, bat_voltage, hw_uhf, uhf_version, anttype)


def make_lan_status_page():
    db = xml_db()
    if db.open() == False:
        raise PageError("Could not open configuration storage")

    advsetup = db.get_params_set("advsetup")
    bridg_mode = advsetup["eth_mode"]["val"]

    if bridg_mode == "BRIDGE":
        content = """$def with () \n
        <h2>Local Network</h2>
        <div class="setting"><div class="label">Status:</div>Ethernet configured as BRIDGE not as LAN</div>
        <div class="setting"><div class="label">IP Address:</div>10.1.12.1</div>
        <br />
        <div class="submitFooter"><input onclick="window.location.replace('/lans')" type="button" value="Refresh" /></div>
        """
	content = web.template.Template(content)
	return content()

    stream = os.popen("ifconfig eth0")
    str = stream.read()
    mac_addr = re.search("HWaddr (([0-9a-fA-F]+\:){5}[0-9a-fA-F]+)",str).group()[7:]
    is_run = re.search("RUNNING", str)
    if is_run == None or is_run == "":
        content = """$def with (mac_addr) \n
        <h2>Local Network</h2>
	<div class="setting"><div class="label">MAC Address:</div>$:mac_addr</div>
        <div class="setting"><div class="label">Status:</div>There is no connection</div>
        <br />
        <div class="submitFooter"><input onclick="window.location.replace('/lans')" type="button" value="Refresh" /></div>
        """
	content = web.template.Template(content)
	return content(mac_addr)


    ip_addr = re.search("inet addr:(\d+\.\d+\.\d+\.\d+)",str).group()[10:]
    net_mask = re.search("Mask:(\d+\.\d+\.\d+\.\d+)",str).group()[5:]

    dns1 = ""
    dns2 = ""
    stream = os.popen("cat /etc/resolv.conf")
    str = stream.read()
    dns = re.findall("(\d+\.\d+\.\d+\.\d+)",str);
    if dns != []:
        if len(dns) == 1:
            dns1 = dns[0]
        else:
            dns1 = dns[0]
            dns2 = dns[1]


    content = """$def with (ip_addr, net_mask, mac_addr, dns1, dns2) \n
    <h2>Local Network</h2>
    <div class="setting"><div class="label">MAC Address:</div>$:mac_addr</div>
    <div class="setting"><div class="label">IP Address:</div>$:ip_addr</div>
    <div class="setting"><div class="label">Subnet Mask:</div>$:net_mask</div>
    <div class="setting"><div class="label">DNS 1:</div>$:dns1</div>
    <div class="setting"><div class="label">DNS 2:</div>$:dns2</div>
    <br />
    <div class="submitFooter"><input onclick="window.location.replace('/lans')" type="button" value="Refresh" /></div>
    """

    content = web.template.Template(content)
    return content(ip_addr, net_mask, mac_addr, dns1, dns2)


def send_lan_status():
    db = xml_db()
    if db.open() == False:
        raise PageError("Could not open configuration storage")

    advsetup = db.get_params_set("advsetup")
    bridg_mode = advsetup["eth_mode"]["val"]
    if bridg_mode == "BRIDGE":
        status["ip_addr"] = "10.1.12.1"
        status["state"] = "not LAN mode"
        return json.dumps({"err":"0", "errmsg":"", "lan_status":status})

    status = {}
    stream = os.popen("ifconfig eth0")
    str = stream.read()
    is_run = re.search("RUNNING", str)

    if is_run == None or is_run == "":
        status["state"] = "disconnected"
    else:
        status["ip_addr"] = re.search("inet addr:(\d+\.\d+\.\d+\.\d+)",str).group()[10:]
        status["state"] = "connected"

    return json.dumps({"err":"0", "errmsg":"", "lan_status":status})




def make_gsm_status_page():
    db = xml_db()
    if db.open() == False:
        raise PageError("Could not open configuration storage")

    installed_hw_option = db.get_params_set("hw_option")
    hw_gsm = installed_hw_option["hw_gsm"]["val"]
    if hw_gsm != "installed":
        return """<h2>Wireless module</h2><div class="setting"><div class="label">Status:</div>Uninstalled</div>"""

    gsetup = db.get_params_set("gsetup")
    en_gsm = gsetup["en_gsm"]["val"]
    if en_gsm != "Enable":
        return """<h2>Wireless module</h2><div class="setting"><div class="label">Status:</div>Disabled</div><br />
                  <div class="submitFooter"><input onclick="window.location.replace('/gsms')" type="button" value="Refresh" /></div>"""


    import dbus

    dev_info_content   = ""
    net_status_content = ""
    net_reg_content = ""


    bus = dbus.SessionBus()
    try:
        remote_object = bus.get_object("jlinklte.gsmd", "/")
        iface = dbus.Interface(remote_object, "jlinklte.gsmd.interface")
        status = iface.get_full_status()

        status = json.loads(status)

        if status["PWR"] == "Disable":
            content = """
            <h2>Wireless Module</h2>
            <div class="setting"><div class="label">Status:</div>Disabled</div><br />
            <div class="submitFooter"><input onclick="window.location.replace('/gsms')" type="button" value="Refresh" /></div>
            """
            return content

        dev_info_content += "<div class=\"setting\"><div class=\"label\">Status:</div><div id=\"status\">" + status["STATUS"] + "</div></div>"
#         if dev_info.has_key("Revision") == True:
#             dev_info_content += "<div class=\"setting\"><div class=\"label\">Revision:</div><span style=\"width: 370px; display: inline-block;\">" + dev_info["Revision"] + "</span></div>"
#
        if status.has_key("SIM") == True:
            dev_info_content += "<div class=\"setting\"><div class=\"label\">SIM Card:</div><div id=\"sim_card_status\">" + status["SIM"] + "</div></div>"
        if status.has_key("ICCID") == True:
            dev_info_content += "<div class=\"setting\"><div class=\"label\">ICCID:</div><div id=\"sim_card_iccid\">" + status["ICCID"] + "</div></div>"
        if status.has_key("Manufacturer") == True:
            dev_info_content += "<div class=\"setting\"><div class=\"label\">Manufacturer:</div>" + status["Manufacturer"] + "</div>"
        if status.has_key("Model") == True:
            dev_info_content += "<div class=\"setting\"><div class=\"label\">Model:</div>" + status["Model"] + "</div>"
        if status.has_key("Revision") == True:
            dev_info_content += "<div class=\"setting\"><div class=\"label\">Revision:</div>" + status["Revision"] + "</div>"
        if status.has_key("IMEI") == True:
            dev_info_content += "<div class=\"setting\"><div class=\"label\">IMEI:</div>" + status["IMEI"] + "</div>"

#
#         dev_info_content +=  "<div class=\"setting\"><div class=\"label\">Temperature:</div><div id=\"temperature\"></div></div>"
#
#         #if dev_info.has_key("net_reg_status"):
#         #    net_reg_content = "<div class=\"setting\"><div class=\"label\">Status:</div><div id=\"net_reg_status\">" + dev_info["net_reg_status"] + "</div></div>"
#
#         #for key in net_status.iterkeys():
#         #    net_status_content +=  "<div class=\"setting\"><div class=\"label\">"+ key + "</div>" + net_status[key] + "</div>"
#         #
#
#
#
    except dbus.DBusException:
        dev_info_content = "Could not get wireless module info!"

    if status.has_key("REG") == True:
        net_reg_content  = "<div class=\"setting\"><div class=\"label\">Status:</div><div id=\"net_reg_status\">" + status["REG"] + "</div></div>"
    else:
        net_reg_content  = "<div class=\"setting\"><div class=\"label\">Status:</div><div id=\"net_reg_status\"></div></div>"

    if status.has_key("OP") == True:
        net_reg_content += "<div class=\"setting\"><div class=\"label\">Operator:</div><div id=\"operator\">" + status["OP"] + "</div></div>"
    else:
        net_reg_content += "<div class=\"setting\"><div class=\"label\">Operator:</div><div id=\"operator\"></div></div>"

    if status.has_key("APN") == True:
        net_reg_content += "<div class=\"setting\"><div class=\"label\">APN:</div><div id=\"apn\">" + status["APN"] + "</div></div>"
    else:
        net_reg_content += "<div class=\"setting\"><div class=\"label\">APN:</div><div id=\"apn\"></div></div>"



    content = """$def with (dev_info_content, net_status_content, net_reg_content) \n
    <script type="text/javascript" src="/static/gsms.js"></script>
    <h2>Wireless Module</h2>
    <fieldset>
    <legend>Device Info</legend>
    <div id="dev_info">$dev_info_content</div>
    </fieldset>
    <br />
    <fieldset>
    <legend>Network registration</legend>
    <div id="net_reg">$net_reg_content</div>
    </fieldset>
    <br />
    <fieldset>
    <legend>Network Status</legend>
    <div id="net_status">$net_status_content </div>
    </fieldset>
    <br />
    <div class="submitFooter"><input onclick="window.location.replace('/gsms')" type="button" value="Refresh" /></div>
    """
    content = web.template.Template(content)
    return content(dev_info_content, net_status_content, net_reg_content)



def make_uhf_status_page():
    db = xml_db()
    if db.open() == False:
        raise PageError("Could not open configuration storage")

    installed_hw_option = db.get_params_set("hw_option")
    hw_uhf = installed_hw_option["hw_uhf"]["val"]
    if hw_uhf != "installed":
        return """<h2>UHF/FH Module Info</h2><div class="setting"><div class="label">Status:</div>Uninstalled</div><br />
                  <div class="submitFooter"><input onclick="window.location.replace('/uhfs')" type="button" value="Refresh" /></div>"""

    gsetup = db.get_params_set("gsetup")
    en_uhf = gsetup["en_uhf"]["val"]
    if en_uhf != "Enable":
        return """<h2>UHF/FH Module Info</h2><div class="setting"><div class="label">Status:</div>Disabled</div><br />
                  <div class="submitFooter"><input onclick="window.location.replace('/uhfs')" type="button" value="Refresh" /></div>"""


    import dbus

    dev_info_content   = ""
    dev_status_content = ""


    bus = dbus.SessionBus()
    try:
        remote_object = bus.get_object("jlinklte.uhfd", "/")
        iface = dbus.Interface(remote_object, "jlinklte.uhfd.interface")
        product_id = iface.uhf_get_product_id()
        dev_info = iface.uhf_get_info()
        dev_status = iface.uhf_get_status()

        dev_info_content += "<div class=\"setting\"><div class=\"label\">Product ID:</div>" + str(product_id) + "</div>"

        if dev_info.has_key("Model"):
            dev_info_content += "<div class=\"setting\"><div class=\"label\">Model:</div>" + dev_info["Model"] + "</div>"
        if dev_info.has_key("ProductID"):
            dev_info_content += "<div class=\"setting\"><div class=\"label\">Product ID:</div>" + dev_info["ProductID"] + "</div>"
        if dev_info.has_key("S/N"):
            dev_info_content += "<div class=\"setting\"><div class=\"label\">S/N:</div>" + dev_info["S/N"] + "</div>"
        if dev_info.has_key("Hardware"):
            dev_info_content += "<div class=\"setting\"><div class=\"label\">Hardware:</div>" + dev_info["Hardware"] + "</div>"
        if dev_info.has_key("Software"):
            dev_info_content += "<div class=\"setting\"><div class=\"label\">Software:</div>" + dev_info["Software"] + "</div>"
        if dev_info.has_key("MCU"):
            dev_info_content += "<div class=\"setting\"><div class=\"label\">MCU:</div>" + dev_info["MCU"] + "</div>"
        if dev_info.has_key("BootLoader"):
            dev_info_content += "<div class=\"setting\"><div class=\"label\">BootLoader:</div>" + dev_info["BootLoader"] + "</div>"

        if dev_info.has_key("state"):
            dev_status_content += "<div class=\"setting\"><div class=\"label\">State:</div>" + dev_info["state"] + "</div>"
        if dev_status.has_key("RSSI"):
            dev_status_content += "<div class=\"setting\"><div class=\"label\">RSSI:</div>" + dev_status["RSSI"] + "</div>"
        if dev_status.has_key("BER"):
            dev_status_content += "<div class=\"setting\"><div class=\"label\">BER:</div>" + dev_status["BER"] + "</div>"
        if dev_status.has_key("RXFREQ"):
            dev_status_content += "<div class=\"setting\"><div class=\"label\">RX Frequency:</div>" + dev_status["RXFREQ"] + "</div>"
        if dev_status.has_key("TXFREQ"):
            dev_status_content += "<div class=\"setting\"><div class=\"label\">TX Frequency:</div>" + dev_status["TXFREQ"] + "</div>"
        if dev_status.has_key("RXBYTE"):
            dev_status_content += "<div class=\"setting\"><div class=\"label\">Bytes received:</div>" + dev_status["RXBYTE"] + "</div>"
        if dev_status.has_key("TXBYTE"):
           dev_status_content += "<div class=\"setting\"><div class=\"label\">Bytes transmitted:</div>" + dev_status["TXBYTE"] + "</div>"
        if dev_status.has_key("TEMP"):
           dev_status_content += "<div class=\"setting\"><div class=\"label\">Temperature:</div>" + dev_status["TEMP"] + " C" "</div>"
        if dev_status.has_key("ANTENNA"):
           dev_status_content += "<div class=\"setting\"><div class=\"label\">Antenna:</div>" + dev_status["ANTENNA"] + "</div>"
        if dev_status.has_key("BSP"):
           dev_status_content += "<div class=\"setting\"><div class=\"label\">BSP:</div>" + dev_status["BSP"] + "</div>"
        if dev_status.has_key("RSP"):
           dev_status_content += "<div class=\"setting\"><div class=\"label\">RSP:</div>" + dev_status["RSP"] + "</div>"
        if dev_status.has_key("PER"):
           dev_status_content += "<div class=\"setting\"><div class=\"label\">PER:</div>" + dev_status["PER"] + "</div>"


    except dbus.DBusException:
        dev_info_content   = "Could not get UHF/FH module info!"
        dev_status_content = "Could not get UHF/FH module status!"


    content = """$def with (dev_info_content, dev_status_content) \n
    <script type="text/javascript" src="/static/uhfs.js"></script>
    <h2>UHF/FH Module Info</h2>
    <div id="uhf_info">$dev_info_content</div>
    <br />
    <h2>UHF/FH Module Status</h2>
    <div id="uhf_status">$dev_status_content</div>
    <br />
    <div class="submitFooter"><input onclick="window.location.replace('/uhfs')" type="button" value="Refresh" /></div>
    """


    content = web.template.Template(content)
    return content(dev_info_content, dev_status_content)





def send_gsm_status():

    import dbus

    bus = dbus.SessionBus()
    try:
        remote_object = bus.get_object("jlinklte.gsmd", "/")
        iface = dbus.Interface(remote_object, "jlinklte.gsmd.interface")
        status = iface.get_full_status()
        print status

        status = json.loads(status)

    except dbus.DBusException:
        raise PageError("Could not get GSM module status")

    return json.dumps({"err":"0", "errmsg":"", "gsm_status":status})




def make_wifi_ap_status_content():
    import subprocess

    proc = subprocess.Popen("ifconfig wlan1|grep HWaddr|awk '{print $5}'", shell=True, stdout=subprocess.PIPE)
    res = proc.wait()
    for line in proc.stdout:
        ssid = line
    proc = subprocess.Popen("iw dev wlan1 station dump", shell=True, stdout=subprocess.PIPE)
    res = proc.wait()

    if res != 0:
        return ""

    body = ""
    body = body + "<h2>AP Status</h2>"
    body = body + "<div class=\"setting\"><div class=\"label\">Own BSSID:</div>" + ssid + "</div>"
    body = body + "<h2>Connected Clients</h2>"
    first = 0
    for line in proc.stdout:
        station = line.split()
        if station[0] == "Station":
            if first == 0:
                first = 1
                body = body + "<fieldset>"
            else:
                body = body + "<br /></fieldset><br /><fieldset>"
            body = body + "<legend>Client BSSID:&nbsp;" + station[1].upper() + "</legend>"
        else:
            status_line = line.split(":")
            body = body + "<div class=\"setting\"><div class=\"label\">" + status_line[0].title() + ":" + "</div>" + status_line[1] +"</div>"
    body = body + "<br /></fieldset>"

    return body





def make_wifi_client_status_content():
    import subprocess

    proc = subprocess.Popen("wpa_cli -i wlan0 status", shell=True, stdout=subprocess.PIPE)
    res = proc.wait()

    body=""
    body = body + "<h2>Client Status</h2>"
    if res != 0:
        return body

    status = {}
    for line in proc.stdout:
        spl=line.rstrip().split("=")
        if len(spl) == 2:
            status[spl[0]] = spl[1]


    if status.has_key("address"):
        body = body + "<div class=\"setting\"><div class=\"label\">Own MAC:</div>" + status["address"].upper() +"</div>"

    if status.has_key("ip_address"):
        body = body + "<div class=\"setting\"><div class=\"label\">Assigned IP address:</div>" + status["ip_address"] +"</div>"

    if status.has_key("wpa_state"):
        body = body + "<div class=\"setting\"><div class=\"label\">WPA State:</div>" + status["wpa_state"] +"</div>"

    if status.has_key("ssid"):
        body = body + "<div class=\"setting\"><div class=\"label\">SSID:</div>" + status["ssid"] +"</div>"

    if status.has_key("bssid"):
        body = body + "<div class=\"setting\"><div class=\"label\">BSSID:</div>" + status["bssid"] +"</div>"

    if status.has_key("pairwise_cipher"):
        body = body + "<div class=\"setting\"><div class=\"label\">Pairwise Cipher:</div>" + status["pairwise_cipher"] +"</div>"

    if status.has_key("group_cipher"):
        body = body + "<div class=\"setting\"><div class=\"label\">Group Cipher:</div>" + status["group_cipher"] +"</div>"

    if status.has_key("key_mgmt"):
        body = body + "<div class=\"setting\"><div class=\"label\">Key Management:</div>" + status["key_mgmt"] +"</div>"

    proc = subprocess.Popen("wpa_cli -i wlan0 signal_poll", shell=True, stdout=subprocess.PIPE)
    res = proc.wait()

    if res != 0:
        return body


    signal_status = {}
    for line in proc.stdout:
        spl=line.rstrip().split("=")
        if len(spl) == 2:
            signal_status[spl[0]] = spl[1]

    if signal_status.has_key("FREQUENCY"):
        body = body + "<div class=\"setting\"><div class=\"label\">Frequency:</div>" + signal_status["FREQUENCY"] +" MHz</div>"

    if signal_status.has_key("RSSI"):
        body = body + "<div class=\"setting\"><div class=\"label\">RSSI:</div>" + signal_status["RSSI"] +" dBm</div>"

    #if signal_status.has_key("NOISE"):
    #    body = body + "<div class=\"setting\"><div class=\"label\">Noise:</div>" + signal_status["NOISE"] +" dBm</div>"

    if signal_status.has_key("LINKSPEED"):
        body = body + "<div class=\"setting\"><div class=\"label\">Link rates:</div>" + signal_status["LINKSPEED"] +" Mbps</div>"

#    stream = os.popen("ifconfig wlan0")
#    str = stream.read()
#    ip_addr = re.search("inet addr:(\d+\.\d+\.\d+\.\d+)",str).group()[10:]

#    if ip_addr == "":
#        body = body + "<div class=\"setting\"><div class=\"label\">IP Address:</div>Not assigned</div>"
#    else:
#        body = body + "<div class=\"setting\"><div class=\"label\">IP Address:</div>" + ip_addr + "</div>"


    return body


def make_wifi_status_page():
    db = xml_db()
    if db.open() == False:
        raise PageError("Could not open configuration storage")


    installed_hw_option = db.get_params_set("hw_option")
    hw_wifi = installed_hw_option["hw_wifi"]["val"]
    if hw_wifi != "installed":
        return "<h2>Wi-Fi Module</h2>There is no Wi-Fi module on this device."

    gsetup = db.get_params_set("gsetup")
    adapter_state  = gsetup["en_wifi"]["val"]

    wifi_settings = db.get_params_set("wifi_adapter")
    if wifi_settings == None or wifi_settings.has_key("mode") == False:
        raise PageError("Could not define adapter mode")

    adapter_mode  = wifi_settings["mode"]["val"]

    if adapter_state == "Enable":
        body = "<div class=\"setting\"><div class=\"label\">Status:</div>Enabled</div>"
	body = body + "<div class=\"setting\"><div class=\"label\">Mode:</div>"+adapter_mode+"</div>"
	body = body + "<div id=\"wifi_status\">"
    	body = body + make_wifi_client_status_content();
        body = body + make_wifi_ap_status_content();
    else:
        body = ""
        body = body + "<div class=\"setting\"><div class=\"label\">Status:</div>Disabled</div>"
        body = body + "<div class=\"setting\"><div class=\"label\">Mode:</div>"+adapter_mode+"</div>"
	body = body + "<div id=\"wifi_status\">"


    content = """$def with (body, adapter_state, adapter_mode) \n
    <script type="text/javascript" src="/static/wifis.js"></script>
    <h2>Wi-Fi Adapter</h2>
    $body</div>
    <br />
    <div class="submitFooter"><input onclick="window.location.replace('/wifis')" type="button" value="Refresh" /></div>
    """

    content = web.template.Template(content)
    return content(body, adapter_state, adapter_mode)


def make_bluetooth_status_page():
    db = xml_db()
    if db.open() == False:
        raise PageError("Could not open configuration storage")


    installed_hw_option = db.get_params_set("hw_option")
    hw_bt = installed_hw_option["hw_bt"]["val"]
    if hw_bt != "installed":
        return "<h2>Bluetooth Module</h2>There is no Bluetooth module on this device."

    gsetup = db.get_params_set("gsetup")
    adapter_state  = gsetup["en_bt"]["val"]
    bt_adapter = db.get_params_set("bt_adapter")
    bt_mode  = bt_adapter["bt_mode"]["val"]

    body = ""

    if adapter_state == "Enable":
        body = body + "<div class=\"setting\"><div class=\"label\">Status:</div>Enabled</div>"
        body = body + "<div class=\"setting\"><div class=\"label\">Mode:</div>" + bt_mode + "</div>"
        stream = os.popen("hcitool dev|awk '{print $2}'")
        bt_mac_addr = stream.read()
        body = body + "<div class=\"setting\"><div class=\"label\">Device Address:</div>" + bt_mac_addr + "</div>"
        stream = os.popen("hcitool con|grep ACL|awk '{print $3}'")
        dest_address = stream.read()
        stream = os.popen("hcitool con|grep ACL|awk '{print $5}'")
        dest_con = stream.read()
        if dest_con == "1\n":
            body = body + "<div class=\"setting\"><div class=\"label\">State:</div>Connected</div>"
            #destination device info
            stream = os.popen("hcitool name " + dest_address)
            dest_name = stream.read()
            stream = os.popen("hcitool rssi " + dest_address)
            dest_rssi = stream.read().split(":")
            stream = os.popen("hcitool lq " + dest_address)
            dest_lq = stream.read().split(":")
            stream = os.popen("hcitool tpl " + dest_address)
            dest_tpl = stream.read().split(":")
            body = body + "<h2>Destination Adapter</h2>"
            body = body + "<fieldset><legend>Device Name:&nbsp;" + dest_name + "</legend>"
            body = body + "<div class=\"setting\"><div class=\"label\">Device Address :</div>" + dest_address.upper() +"</div>"
            body = body + "<div class=\"setting\"><div class=\"label\">RSSI Return Value :</div>" + dest_rssi[1] + "</div>"
            body = body + "<div class=\"setting\"><div class=\"label\">Link Quality :</div>" + dest_lq[1] + "</div>"
            body = body + "<div class=\"setting\"><div class=\"label\">Transmit Power Level :</div>" + dest_tpl[1] + "</div>"
            body = body + "<br /></fieldset>"
        else:
            body = body + "<div class=\"setting\"><div class=\"label\">State:</div>Disconnected</div>"
    else:
        body = body + "<div class=\"setting\"><div class=\"label\">Status:</div>Disabled</div>"
    content = """$def with (body) \n
    <h2>Bluetooth Adapter</h2>
    <div id="bt_status">$body</div>
    <br />
    <div class="submitFooter"><input onclick="window.location.replace('/bts')" type="button" value="Refresh" /></div>
    """

    content = web.template.Template(content)
    return content(body)




def send_wifi_status():
    body = make_wifi_client_status_content();
    body = body + make_wifi_ap_status_content();

    if body == None:
        body = "<div>Could not get status of interface!</div>"

#    print body

    return json.dumps({"err":"0", "errmsg":"", "wifi_status":body})




def send_uhf_status():
    import dbus

    dev_status_content = ""

    bus = dbus.SessionBus()
    try:
        remote_object = bus.get_object("jlinklte.uhfd", "/")
        iface = dbus.Interface(remote_object, "jlinklte.uhfd.interface")
        dev_status = iface.uhf_get_status()

        if dev_status.has_key("state"):
            dev_status_content += "<div class=\"setting\"><div class=\"label\">State:</div>" + dev_status["state"] + "</div>"
        if dev_status.has_key("RSSI"):
            dev_status_content += "<div class=\"setting\"><div class=\"label\">RSSI:</div>" + dev_status["RSSI"] + "</div>"
        if dev_status.has_key("BER"):
            dev_status_content += "<div class=\"setting\"><div class=\"label\">BER:</div>" + dev_status["BER"] + "</div>"
        if dev_status.has_key("RXFREQ"):
            dev_status_content += "<div class=\"setting\"><div class=\"label\">RX Frequency:</div>" + dev_status["RXFREQ"] + "</div>"
        if dev_status.has_key("TXFREQ"):
            dev_status_content += "<div class=\"setting\"><div class=\"label\">TX Frequency:</div>" + dev_status["TXFREQ"] + "</div>"
        if dev_status.has_key("RXBYTE"):
            dev_status_content += "<div class=\"setting\"><div class=\"label\">Bytes received:</div>" + dev_status["RXBYTE"] + "</div>"
        if dev_status.has_key("TXBYTE"):
            dev_status_content += "<div class=\"setting\"><div class=\"label\">Bytes transmitted:</div>" + dev_status["TXBYTE"] + "</div>"
        if dev_status.has_key("TEMP"):
            dev_status_content += "<div class=\"setting\"><div class=\"label\">Temperature:</div>" + dev_status["TEMP"] + " C" "</div>"
        if dev_status.has_key("ANTENNA"):
            dev_status_content += "<div class=\"setting\"><div class=\"label\">Antenna:</div>" + dev_status["ANTENNA"] + "</div>"
        if dev_status.has_key("BSP"):
           dev_status_content += "<div class=\"setting\"><div class=\"label\">BSP:</div>" + dev_status["BSP"] + "</div>"
        if dev_status.has_key("RSP"):
           dev_status_content += "<div class=\"setting\"><div class=\"label\">RSP:</div>" + dev_status["RSP"] + "</div>"
        if dev_status.has_key("PER"):
           dev_status_content += "<div class=\"setting\"><div class=\"label\">PER:</div>" + dev_status["PER"] + "</div>"

    except dbus.DBusException:
        dev_status_content = "Could not get UHF/FH module status!"


    return json.dumps({"err":"0", "errmsg":"", "uhf_status":dev_status_content})




def send_uhf_lite_status():
    #TODO add output power value
    db = xml_db()
    if db.open() == False:
        raise PageError("Could not open configuration storage")
    
    uhf_params = db.get_params_set("uhf")
    power = uhf_params["power"]["val"]
    
    import dbus
    bus = dbus.SessionBus()
    try:
        remote_object = bus.get_object("jlinklte.uhfd", "/")
        iface = dbus.Interface(remote_object, "jlinklte.uhfd.interface")
        uhf_status = iface.uhf_get_lite_status()
        dev_status = iface.uhf_get_status()

    except dbus.DBusException:
        raise PageError("UHF/FH module is not ready or not installed!")
    status = {}
    status["state"] = uhf_status["state"]
    status["sync"] = dev_status["SYNC"]
    status["rssi"] = dev_status["RSSI"]
    status["power"] = power;

    #print status
    return json.dumps({"err":"0",  "errmsg":"", "uhf_status":status})



def signal_handler(signum, frame):
    raise Exception("Timeout!")

def make_gps_content():
    import gps

    try:
        session = gps.gps(mode=gps.WATCH_ENABLE)
        session.stream(flags=gps.WATCH_JSON)

        sky_rcved = False
        tpv_rcved = False
        sky_cnt = 0;
        tpv_cnt = 0;

        for report in session:

            #print report.keys()
            #print report

            if report["class"] == "SKY":
                satellites = report
                sky_cnt = sky_cnt + 1
                sky_rcved = True
            elif report["class"] == "TPV":
                location = report
                if location["mode"] == 0 or location["mode"] == 1:
                    if sky_cnt > 0:
                        del session
                        break

                tpv_cnt = tpv_cnt + 1
                tpv_rcved = True
            else:
                print report
            if sky_rcved == True and tpv_rcved == True:
                del session
                break

            if sky_cnt > 1 or tpv_cnt > 1:
                del session
                break
           # if session.waiting():
            #    del session
             #   break

        location_content   = ""
        satellites_content = ""

        if sky_rcved == True:
            satellites_content += "<table id=\"sat_tbl\" class=\"sat_tbl\" width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" style=\"table-layout:fixed;\">"
            satellites_content += "<thead class=\"sat_hdr\"><tr>"
            satellites_content += "<th>PRN</th>"
            satellites_content += "<th>Elevation</th>"
            satellites_content += "<th>Azimut</th>"
            satellites_content += "<th>SNR</th>"
            satellites_content += "<th>Use</th>"
            satellites_content += "</tr></thead>"
            satellites_content += "<tbody>"
            for item in satellites["satellites"]:
                satellites_content += "<tr>"
                satellites_content += "<td>" + str(item["PRN"]) + "</td>"
                satellites_content += "<td>" + str(item["el"]) + "</td>"
                satellites_content += "<td>" + str(item["az"]) + "</td>"
                satellites_content += "<td>" + str(item["ss"]) + "</td>"
                if item["used"] == True:
                    satellites_content += "<td>Y</td>"
                else:
                    satellites_content += "<td>N</td>"
                satellites_content += "</tr>"
            satellites_content += "</tbody></table>"


        if tpv_rcved == True:
            if location["mode"] == 0 or location["mode"] == 1:
                location_content += "<div class=\"setting\"><div class=\"label\">Status:</div>No valid data from GNSS</div>"
                #location_content += "<div class=\"setting\"><div class=\"label\">Time:</div>" +  "" + "</div>"
            else:
                if location["mode"] == 2:
                    location_content += "<div class=\"setting\"><div class=\"label\">Status:</div>2D fix</div>"
                elif location["mode"] == 3:
                    location_content += "<div class=\"setting\"><div class=\"label\">Status:</div>3D fix</div>"

                #print location


                #location_content += "<div class=\"setting\"><div class=\"label\">Time:</div>" +  time.asctime(time.localtime(location["time"])) + "</div>"
                if location.__dict__.has_key("time") == True:
                    location_content += "<div class=\"setting\"><div class=\"label\">Time:</div>" + location["time"] + "</div>"

                if location["lat"] > 0:
                    lat = "%f N"%(location["lat"])
                elif location["lat"] < 0:
                    lat = "%f S"%(abs(location["lat"]))
                else:
                    lat = "%f"%(location["lat"])

                if location["lon"] > 0:
                    lon = "%f E"%(location["lon"])
                elif location["lon"] < 0:
                    lon = "%f W"%(abs(location["lon"]))
                else:
                    lon = "%f"%(location["lon"])

                location_content += "<div class=\"setting\"><div class=\"label\">Latitude:</div>" + lat + "</div>"
                location_content += "<div class=\"setting\"><div class=\"label\">Longitude:</div>" + lon  + "</div>"
                location_content += "<div class=\"setting\"><div class=\"label\">Altitude:</div>" + "%.2f"%(location["alt"]) + " m</div>"
                if location.__dict__.has_key("speed") == True:
                    location_content += "<div class=\"setting\"><div class=\"label\">Speed:</div>" + "%.2f"%(location["speed"]) + " m/sec</div>"
                if location.__dict__.has_key("climb") == True:
                    location_content += "<div class=\"setting\"><div class=\"label\">Climb:</div>" + "%.2f"%(location["climb"]) + " m/sec</div>"
        else:
            location_content += "<div class=\"setting\"><div class=\"label\">Status:</div>No valid location data from GNSS</div>" 

        return {"loc_cont": location_content, "sat_cont":satellites_content}
    except Exception, msg:
        print "No valid data from GNSS"
        location_content = "<div class=\"setting\"><div class=\"label\">Status:</div>No valid location data from GNSS</div>"
        satellites_content = ""
        return {"loc_cont": location_content, "sat_cont":satellites_content}





def make_gps_status_page():

    try:
        gps_content = make_gps_content()
    except Exception as e:
        content = """
                  <h2>Location</h2>
                  <b>Error: Could not connect to GSP stream socket!</b>
                  <br/>
                  <div class="submitFooter"><input onclick="window.location.replace('/gpss')" type="button" value="Refresh" /></div>
                  """
        content = web.template.Template(content)
        return content()


    content = """$def with (location_content, satellites_content) \n
    <script type="text/javascript" src="/static/gpss.js"></script>

    <h2>Location</h2>
    <div id="loc">$location_content</div>
    <br/>
    <h2>Satellites</h2>
    <br/>
    <div id="sat">$satellites_content</div>
    <br/>
    <div class="submitFooter"><input onclick="window.location.replace('/gpss')" type="button" value="Refresh" /></div>
    """

    content = web.template.Template(content)
    return content(gps_content["loc_cont"], gps_content["sat_cont"])



def send_gps_status():
    gps_content = make_gps_content()
    return json.dumps({"err":"0", "errmsg":"", "loc_cont":gps_content["loc_cont"], "sat_cont":gps_content["sat_cont"]})



def make_ntrip_status_page():
    import dbus

    ntrip_status_content = ""

    bus = dbus.SessionBus()
    try:
        remote_object = bus.get_object("jlinklte.ntripcd", "/")
        iface = dbus.Interface(remote_object, "jlinklte.ntripcd.interface")
        ntrip_status = iface.get_status()

        if ntrip_status.has_key("state") == True:

            ntrip_status_content = "<div class=\"setting\"><div class=\"label\">Status:</div>" + ntrip_status["state"] + "</div>"

            if ntrip_status.has_key("error"):
                ntrip_status_content += "<div class=\"setting\"><div class=\"label\">Error description:</div>" + ntrip_status["error"] + "</div>"
            else:
                if ntrip_status.has_key("totalbytes"):
                    ntrip_status_content += "<div class=\"setting\"><div class=\"label\">Bytes transfered:</div>" + ntrip_status["totalbytes"] + "</div>"
                if ntrip_status.has_key("bitrate"):
                    ntrip_status_content += "<div class=\"setting\"><div class=\"label\">Bitrate:</div>" + ntrip_status["bitrate"] + "</div>"
        else:
            ntrip_status_content = "Could not get NTRIP Client Status!"

    except dbus.DBusException:
        ntrip_status_content = "Could not get NTRIP Client Status!"


    content = """$def with (ntrip_status_content) \n
    <script type="text/javascript" src="/static/ntrips.js"></script>
    <h2>NTRIP client status</h2>
    <div id="ntrip_status">$ntrip_status_content</div>
    <br />
    <div class="submitFooter"><input onclick="window.location.replace('/ntrips')" type="button" value="Refresh" /></div>
    """
    content = web.template.Template(content)
    return content(ntrip_status_content)


def send_ntrip_status():
    import dbus

    ntrip_status_content = ""

    bus = dbus.SessionBus()
    try:
        remote_object = bus.get_object("jlinklte.ntripcd", "/")
        iface = dbus.Interface(remote_object, "jlinklte.ntripcd.interface")
        ntrip_status = iface.get_status()

        if ntrip_status.has_key("state") == True:

            ntrip_status_content = "<div class=\"setting\"><div class=\"label\">Status:</div>" + ntrip_status["state"] + "</div>"

            if ntrip_status.has_key("error"):
                ntrip_status_content += "<div class=\"setting\"><div class=\"label\">Error description:</div>" + ntrip_status["error"] + "</div>"
            else:
                if ntrip_status.has_key("totalbytes"):
                    ntrip_status_content += "<div class=\"setting\"><div class=\"label\">Bytes transfered:</div>" + ntrip_status["totalbytes"] + "</div>"
                if ntrip_status.has_key("bitrate"):
                    ntrip_status_content += "<div class=\"setting\"><div class=\"label\">Bitrate:</div>" + ntrip_status["bitrate"] + "</div>"
        else:
            ntrip_status_content = "Could not get NTRIP client status!"
    except dbus.DBusException:
        ntrip_status_content = "Could not get NTRIP client status!"

    return json.dumps({"err":"0", "errmsg":"", "ntrip_status":ntrip_status_content})



def make_tcpo_status_page():                                                                                                                              
    import dbus                                                                                                                                      
                                                                                                                                                     
    tcpo_status_content = ""                                                                                                                          
                                                                                                                                                     
    bus = dbus.SessionBus()                                                                                                                          
    try:                                                                                                                                             
        remote_object = bus.get_object("jlinklte.tcpod", "/")                                                                                        
        iface = dbus.Interface(remote_object, "jlinklte.tcpod.interface")                                                                            
        tcpo_status = iface.get_status()                                                                                                              
                                                                                                                                                     
        if tcpo_status.has_key("state") == True:                                                                                                      
                                                                                                                                                     
            tcpo_status_content = "<div class=\"setting\"><div class=\"label\">Status:</div>" + tcpo_status["state"] + "</div>"                        
                                                                                                                                                     
            if tcpo_status.has_key("error"):                                                                                                          
                tcpo_status_content += "<div class=\"setting\"><div class=\"label\">Error description:</div>" + tcpo_status["error"] + "</div>"        
            else:                                                                                                                                    
                if tcpo_status.has_key("numofclients"):                                                                                                 
                    tcpo_status_content += "<div class=\"setting\"><div class=\"label\">Number of connected clients:</div>" + tcpo_status["numofclients"] + "</div>"
                if tcpo_status.has_key("totalbytes"):                                                                                                 
                    tcpo_status_content += "<div class=\"setting\"><div class=\"label\">Bytes transfered:</div>" + tcpo_status["totalbytes"] + "</div>"
                if tcpo_status.has_key("bitrate"):                                                                                                    
                    tcpo_status_content += "<div class=\"setting\"><div class=\"label\">Bitrate:</div>" + tcpo_status["bitrate"] + "</div>"            
        else:                                                                                                                                        
            tcpo_status_content = "Could not get TCP Output Status!"                                                                                  
                                                                                                                                                     
    except dbus.DBusException:                                                                                                                       
        tcpo_status_content = "Could not get TCP Output Status!"                                                                                      
                                                                                                                                                     
                                                                                                                                                     
    content = """$def with (tcpo_status_content) \n                                                                                                   
    <script type="text/javascript" src="/static/tcpos.js"></script>                                                                                   
    <h2>TCP output status</h2>                                                                                                                       
    <div id="tcpo_status">$tcpo_status_content</div>                                                                                                   
    <br />                                                                                                                                           
    <div class="submitFooter"><input onclick="window.location.replace('/tcpos')" type="button" value="Refresh" /></div>                               
    """                                                                                                                                              
    content = web.template.Template(content)                                                                                                         
    return content(tcpo_status_content)                                                                                                               
                                                                                                                                                     
                    


def send_tcpo_status():                                                                                                                                 
    import dbus                                                                                                                                        
                                                                                                                                                       
    tcpo_status_content = ""                                                                                                                            
                                                                                                                                                       
    bus = dbus.SessionBus()                                                                                                                            
    try:                                                                                                                                               
        remote_object = bus.get_object("jlinklte.tcpod", "/")                                                                                          
        iface = dbus.Interface(remote_object, "jlinklte.tcpod.interface")                                                                              
        tcpo_status = iface.get_status()                                                                                                                
                                                                                                                                                       
        if tcpo_status.has_key("state") == True:                                                                                                        
                                                                                                                                                       
            tcpo_status_content = "<div class=\"setting\"><div class=\"label\">Status:</div>" + tcpo_status["state"] + "</div>"                          
                                                                                                                                                       
            if tcpo_status.has_key("error"):                                                                                                            
                tcpo_status_content += "<div class=\"setting\"><div class=\"label\">Error description:</div>" + tcpo_status["error"] + "</div>"          
            else:                                                                                                                                      
                if tcpo_status.has_key("numofclients"):                                                                                                   
                    tcpo_status_content += "<div class=\"setting\"><div class=\"label\">Number of connected clients:</div>" + tcpo_status["numofclients"] + "</div>"
                if tcpo_status.has_key("totalbytes"):                                                                                                   
                    tcpo_status_content += "<div class=\"setting\"><div class=\"label\">Bytes transfered:</div>" + tcpo_status["totalbytes"] + "</div>"  
                if tcpo_status.has_key("bitrate"):                                                                                                      
                    tcpo_status_content += "<div class=\"setting\"><div class=\"label\">Bitrate:</div>" + tcpo_status["bitrate"] + "</div>"              
        else:                                                                                                                                          
            tcpo_status_content = "Could not get TCP output status!"                                                                                    
    except dbus.DBusException:                                                                                                                         
        tcpo_status_content = "Could not get TCP output status!"                                                                                        
                                                                                                                                                       
    return json.dumps({"err":"0", "errmsg":"", "tcpo_status":tcpo_status_content}) 






def make_tcp_status_page():
    import dbus

    tcp_status_content = ""

    bus = dbus.SessionBus()
    try:
        remote_object = bus.get_object("jlinklte.tcpcd", "/")
        iface = dbus.Interface(remote_object, "jlinklte.tcpcd.interface")
        tcp_status = iface.get_status()

        if tcp_status.has_key("state") == True:

            tcp_status_content = "<div class=\"setting\"><div class=\"label\">Status:</div>" + tcp_status["state"] + "</div>"

            if tcp_status.has_key("error"):
                tcp_status_content += "<div class=\"setting\"><div class=\"label\">Error description:</div>" + tcp_status["error"] + "</div>"
            else:
                if tcp_status.has_key("totalbytes"):
                    tcp_status_content += "<div class=\"setting\"><div class=\"label\">Bytes transfered:</div>" + tcp_status["totalbytes"] + "</div>"
                if tcp_status.has_key("bitrate"):
                    tcp_status_content += "<div class=\"setting\"><div class=\"label\">Bitrate:</div>" + tcp_status["bitrate"] + "</div>"
        else:
            tcp_status_content = "Could not get TCP Client Status!"

    except dbus.DBusException:
        tcp_status_content = "Could not get TCP Client Status!"


    content = """$def with (tcp_status_content) \n
    <script type="text/javascript" src="/static/tcps.js"></script>
    <h2>TCP client status</h2>
    <div id="tcp_status">$tcp_status_content</div>
    <br />
    <div class="submitFooter"><input onclick="window.location.replace('/tcps')" type="button" value="Refresh" /></div>
    """
    content = web.template.Template(content)
    return content(tcp_status_content)


def send_tcp_status():
    import dbus

    tcp_status_content = ""

    bus = dbus.SessionBus()
    try:
        remote_object = bus.get_object("jlinklte.tcpcd", "/")
        iface = dbus.Interface(remote_object, "jlinklte.tcpcd.interface")
        tcp_status = iface.get_status()

        if tcp_status.has_key("state") == True:

            tcp_status_content = "<div class=\"setting\"><div class=\"label\">Status:</div>" + tcp_status["state"] + "</div>"

            if tcp_status.has_key("error"):
                tcp_status_content += "<div class=\"setting\"><div class=\"label\">Error description:</div>" + tcp_status["error"] + "</div>"
            else:
                if tcp_status.has_key("totalbytes"):
                    tcp_status_content += "<div class=\"setting\"><div class=\"label\">Bytes transfered:</div>" + tcp_status["totalbytes"] + "</div>"
                if tcp_status.has_key("bitrate"):
                    tcp_status_content += "<div class=\"setting\"><div class=\"label\">Bitrate:</div>" + tcp_status["bitrate"] + "</div>"
        else:
            tcp_status_content = "Could not get TCP client status!"
    except dbus.DBusException:
        tcp_status_content = "Could not get TCP client status!"

    return json.dumps({"err":"0", "errmsg":"", "tcp_status":tcp_status_content})



def send_wifi_lite_status():
    db = xml_db()
    if db.open() == False:
        raise PageError("Could not open configuration storage")


    installed_hw_option = db.get_params_set("hw_option")
    hw_wifi = installed_hw_option["hw_wifi"]["val"]
    if hw_wifi != "installed":
        raise PageError("Wi-Fi module is not installed")

    gsetup = db.get_params_set("gsetup")
    adapter_state  = gsetup["en_wifi"]["val"]

    wifi_settings = db.get_params_set("wifi_adapter")
    if wifi_settings == None or wifi_settings.has_key("mode") == False:
        raise PageError("Could not define adapter mode")

    adapter_mode  = wifi_settings["mode"]["val"]

    status = {}

    if (adapter_mode == "AP"):
        status["mode"] = adapter_mode
        status["state"] = adapter_state
    elif adapter_mode == "client" or adapter_mode == "AP+client":
        status["mode"] = adapter_mode
        status["state"] = adapter_state

        if adapter_state == "Enable":

            import subprocess
            proc = subprocess.Popen("wpa_cli -i wlan0 signal_poll", shell=True, stdout=subprocess.PIPE)
            res = proc.wait()

            if res == 0:
                signal_status = {}
                for line in proc.stdout:
                    spl=line.rstrip().split("=")
                    if len(spl) == 2:
                        signal_status[spl[0]] = spl[1]

                if signal_status.has_key("RSSI"):
                    status["rssi"] = signal_status["RSSI"]

            proc = subprocess.Popen("wpa_cli -i wlan0 status", shell=True, stdout=subprocess.PIPE)
            res = proc.wait()

            if res == 0:
                for line in proc.stdout:
                    spl=line.rstrip().split("=")
                    if len(spl) == 2:
                        signal_status[spl[0]] = spl[1]

                if signal_status.has_key("wpa_state"):
                    status["wpa_state"] = signal_status["wpa_state"]

    #print status
    return json.dumps({"err":"0", "wifi_status":status})



def send_bt_status():
    db = xml_db()
    if db.open() == False:
        raise PageError("Could not open configuration storage")


    installed_hw_option = db.get_params_set("hw_option")
    hw_bt = installed_hw_option["hw_bt"]["val"]
    if hw_bt != "installed":
        raise PageError("Bluetooth module is not installed")

    gsetup = db.get_params_set("gsetup")
    bt_adapter_state  = gsetup["en_bt"]["val"]


    status = {"state":bt_adapter_state}

    if bt_adapter_state == "Enable":
        import subprocess

        proc = subprocess.Popen("ifconfig bnep0 2>/dev/null | grep -q RUNNING", shell=True, stdout=subprocess.PIPE)
        res = proc.wait()

        if res == 0:
            status["connection_state"] = "connected"
        else:
            status["connection_state"] = "disconnected"




    #print status
    return json.dumps({"err":"0", "bt_status":status})



def send_gps_lite_status():
    db = xml_db()
    if db.open() == False:
        raise PageError("Could not open configuration storage")


    installed_hw_option = db.get_params_set("hw_option")
    hw_gps = installed_hw_option["hw_gps"]["val"]
    if hw_gps != "installed":
        raise PageError("GNSS module is not installed")

    gsetup = db.get_params_set("gsetup")
    gps_state  = gsetup["en_gps"]["val"]


    status = {"state":gps_state}

    return json.dumps({"err":"0", "gps_lite_status":status})


def make_dyndns_status_page():
    db = xml_db()
    if db.open() == False:
        raise PageError("Could not open configuration storage")

    dyndns_option = db.get_params_set("dyndns_client")
    en_client = dyndns_option["en_client"]["val"]
    if en_client != "Enable":
         content = """
         <h2>DYNDNS Information</h2>
         <div class="setting"><div class="label">Status:</div>DYNDNS Client is Disabled</div><br />
         <div class="submitFooter"><input onclick="window.location.replace('/dyndnss')" type="button" value="Refresh" /></div>
         """
         return content

    last_updated_time=""
    host_name=""
    ip_address=""
    next_check_time=""

    stream = os.popen("jlink status dyndns")
    str = stream.read()
    result = re.search("last updated time.*",str)
    if type(result) != type(None) and result != "":
    	last_updated_time = result.group()[18:]
    result = re.search("host name.*",str)
    if type(result) != type(None) and result != "":
    	host_name = result.group()[10:]
    result = re.search("ip address.*",str)
    if type(result) != type(None) and result != "":
    	ip_address = result.group()[11:]
    result = re.search("next check time.*",str)
    if type(result) != type(None) and result != "":
    	next_check_time = result.group()[16:]

    content = """$def with (last_updated_time, host_name, ip_address, next_check_time) \n
    <h2>DYNDNS Information</h2>
    $if last_updated_time != "":
        <div class="setting"><div class="label">last updated time:</div>$last_updated_time </div>
    $if host_name != "":
        <div class="setting"><div class="label">host name:</div>$host_name </div>
    $if ip_address != "":
        <div class="setting"><div class="label">IP address:</div>$ip_address </div>
    $if next_check_time != "":
        <div class="setting"><div class="label">next check time:</div>$next_check_time </div>
    <div class="submitFooter"><input onclick="window.location.replace('/dyndnss')" type="button" value="Refresh" /></div>
    """
    content = web.template.Template(content)
    return content(last_updated_time, host_name, ip_address, next_check_time)



def make_power_status_page():

    import dbus
    dev_power_content = ""
    pwbrd_info_content = ""

    bus = dbus.SessionBus()
    try:
        remote_object = bus.get_object("jlinklte.statusd", "/")
        iface = dbus.Interface(remote_object, "jlinklte.statusd.interface")
        pwr_voltage = iface.GetParticularStatus("Sensors", "V_IN")
        bat_voltage = iface.GetParticularStatus("Sensors", "V_BAT")
        bat_current = iface.GetParticularStatus("Sensors", "I_BAT")
        bat_temp = iface.GetParticularStatus("Sensors", "TMP_BAT")
        bat_cap = iface.GetParticularStatus("Sensors", "CAP_BAT")
        bat_time = iface.GetParticularStatus("Sensors", "TIME_TO_EMPTY_BAT")
        bat_count = iface.GetParticularStatus("Sensors", "CYCLE_COUNT_BAT")
        wwan_current = iface.GetParticularStatus("Sensors", "WWAN_I")
        uhf_current = iface.GetParticularStatus("Sensors", "UHF_I")
        uhf_ant_current = ""
        #uhf_ant_current = iface.GetParticularStatus("Sensors", "UHF_ANT_I")

    except dbus.DBusException:
        raise PageError("Could not get power info!")


    content = """$def with (pwr_voltage, bat_voltage, bat_current, bat_temp, bat_cap, bat_time, bat_count,uhf_ant_current, wwan_current, uhf_current) \n
    <h2>Power Information</h2>
    <div class="setting"><div class="label">Ext. power voltage:</div>$pwr_voltage V</div>
    $if bat_voltage != "":
        <div class="setting"><div class="label">BAT voltage:</div>$bat_voltage V</div>
    $if bat_current != "":
        <div class="setting"><div class="label">BAT current:</div>$bat_current A</div>
    $if bat_temp != "":
        <div class="setting"><div class="label">BAT temp:</div>$bat_temp C</div>
    $if bat_cap != "":
        <div class="setting"><div class="label">BAT capacity:</div>$bat_cap %</div>
    $if bat_time != "":
        <div class="setting"><div class="label">BAT time to empty:</div>$bat_time M</div>
    $if bat_count != "":
        <div class="setting"><div class="label">BAT cycle count:</div>$bat_count</div>
    <div class="setting"><div class="label">GSM current:</div>$wwan_current A</div>
    <div class="setting"><div class="label">UHF current:</div>$uhf_current A</div>
    $if uhf_ant_current != "":
        <div class="setting"><div class="label">UHF ANT current:</div>$uhf_ant_current A</div>
    <br />
    <div class="submitFooter"><input onclick="window.location.replace('/power')" type="button" value="Refresh" /></div>
    """


    content = web.template.Template(content)
    return content(pwr_voltage, bat_voltage, bat_current, bat_temp, bat_cap, bat_time, bat_count, uhf_ant_current, wwan_current, uhf_current)

def send_pboard_adc_data():

    import dbus

    bus = dbus.SessionBus()
    try:
        remote_object = bus.get_object("jlinklte.statusd", "/")
        iface = dbus.Interface(remote_object, "jlinklte.statusd.interface")
        v_in = iface.GetParticularStatus("Sensors", "V_IN") 
        v_bat = iface.GetParticularStatus("Sensors", "V_BAT") 

    except dbus.DBusException:
        raise PageError("Could not get power info!")

    status = {}
    status["V_IN"] = v_in
    status["V_BAT"] = v_bat

    return json.dumps({"err":"0", "errmsg":"", "pboard_adc_data":status})



class status:
    def GET(self):
        if session.check_session() == False:
            return
        path = web.ctx.path
        content = ""
        try:
            if (path == "/status" or path == "/device"):
                menu = build_menu("Status", "Device")
                content = make_device_status_page()
            elif (path == "/lans"):
                menu = build_menu("Status", "LAN")
                content = make_lan_status_page()
            elif (path == "/uhfs"):
                menu = build_menu("Status", "UHF Int.")
                content = make_uhf_status_page()
            elif (path == "/gsms"):
                menu = build_menu("Status", "GSM")
                content = make_gsm_status_page()
            elif (path == "/wifis"):
                menu = build_menu("Status", "Wi-Fi")
                content = make_wifi_status_page()
            elif (path == "/bts"):
                menu = build_menu("Status", "Bluetooth")
                content = make_bluetooth_status_page()
            elif (path == "/gpss"):
                menu = build_menu("Status", "GNSS")
                content = make_gps_status_page()
            elif (path == "/ntrips"):
                menu = build_menu("Status", "NTRIP")
                content = make_ntrip_status_page()
            elif (path == "/tcps"):
                menu = build_menu("Status", "TCP")
                content = make_tcp_status_page()
            elif (path == "/tcpos"):
                menu = build_menu("Status", "TCPO")
                content = make_tcpo_status_page()
            elif (path == "/dyndnss"):
                menu = build_menu("Status", "DYNDNS")
                content = make_dyndns_status_page()
            elif (path == "/power"):
                menu = build_menu("Status", "Power")
                content = make_power_status_page()


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
            if query.cmd == "get_gsm_status":
                return send_gsm_status()
            elif query.cmd == "get_wifi_status":
                return send_wifi_status()
            elif query.cmd == "get_uhf_status":
                return send_uhf_status()
            elif query.cmd == "get_gps_status":
                return send_gps_status()
            elif query.cmd == "get_gps_lite_status":
                return send_gps_lite_status()
            elif query.cmd == "get_ntrip_status":
                return send_ntrip_status()
            elif query.cmd == "get_tcp_status":
                return send_tcp_status()
            elif query.cmd == "get_tcpo_status":
                return send_tcpo_status()
            elif query.cmd == "get_lan_status":
                return send_lan_status()
            elif query.cmd == "get_wifi_lite_status":
                return send_wifi_lite_status()
            elif query.cmd == "get_uhf_lite_status":
                return send_uhf_lite_status()
            elif query.cmd == "get_bt_status":
                return send_bt_status()
            elif query.cmd == "get_pboard_adc_data":
                return send_pboard_adc_data()



            else:
                return {"err":"1", "errmsg":"There is no correct cmd field!"}

        except PageError as perr:
            return {"err":"1", "errmsg":perr.errmsg}


        return {"err":"0", "errmsg":""}

