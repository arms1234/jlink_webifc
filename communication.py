import web
import sys
import json
import os
import time
import session


from menu import build_menu
from xml_db import xml_db
from perror import PageError
from helper import get_value

jlinklte_config_script    = "/jlinklte/scripts/jlinklte_init"
bt_reconfig_script    = "/jlinklte/scripts/bt_init reconfig"
timezone_config_script   = "/jlinklte/scripts/timezone_config"

render = web.template.render('templates/')

printenv_util = "/jlinklte/utils/fw_printenv"
remove_network_script  = "/jlinklte/scripts/wifi/wpa_remove_network"
add_network_script     = "/jlinklte/scripts/wifi/wpa_add_network"
connect_network_script = "/jlinklte/scripts/wifi/wpa_connect_network"
ap_stop_script         = "/jlinklte/scripts/wifi/ap_stop"
client_stop_script     = "/jlinklte/scripts/wifi/client_stop"
ap_init_script         = "/jlinklte/scripts/wifi/ap_init"
client_init_script     = "/jlinklte/scripts/wifi/client_init"
lan_config_script      = "/jlinklte/scripts/lan_config"


def make_lan_page():
    db = xml_db()
    if db.open() == False:
        raise PageError("Could not open configuration storage")

    lan_settings = db.get_params_set("lan")

    if lan_settings == None:
        addr_alloc = "DHCP"
        ip_addr   = ""
        netmask   = ""
        gateway   = ""
        dns1      = ""
        dns2      = ""
    else:
        addr_alloc = lan_settings["addr_alloc"]["val"]
        ip_addr   = lan_settings["ip_addr"]["val"].split('.')
        netmask   = lan_settings["netmask"]["val"].split('.')
        gateway   = lan_settings["gateway"]["val"].split('.')

        if lan_settings.has_key("dns1") == True:
            dns1 = lan_settings["dns1"]["val"].split('.')
        else:
            dns1 = ["", "", "", ""]

        if lan_settings.has_key("dns2") == True:
            dns2 = lan_settings["dns2"]["val"].split('.')
        else:
            dns2 = ["", "", "", ""]


    content = """$def with (addr_alloc, ip_addr, netmask, gateway, dns1, dns2) \n
    <script type="text/javascript" src="/static/utils.js"></script>
    <script type="text/javascript" src="/static/lan.js"></script>
    <h2>LAN Settings</h2>
    <form>
    <div class="setting">
        <div class="label">Address allocation:</div>
        $if addr_alloc == "DHCP":
            <div><input type="radio" id="addr_alloc_dhcp" name="addr_alloc" checked="checked" onchange="lan_mode_change()" /><label>DHCP</label><input type="radio" name="addr_alloc" onchange="lan_mode_change()" /><label>STATIC</label></div>
        $else:
            <div><input type="radio" id="addr_alloc_dhcp" name="addr_alloc" onchange="lan_mode_change()" /><label>DHCP</label> <input type="radio" name="addr_alloc" checked="checked" onchange="lan_mode_change()" /><label>STATIC</label></div>
    </div>
    <div id="static_net_settings">
    <div class="setting">
        <div class="label">IP address:</div>
        <input size="3" maxlength="3" class="num" id="ip_addr_0" onblur="check_range(this,0,255,'IP')" value="$ip_addr[0]" />.
        <input size="3" maxlength="3" class="num" id="ip_addr_1" onblur="check_range(this,0,255,'IP')" value="$ip_addr[1]" />.
        <input size="3" maxlength="3" class="num" id="ip_addr_2" onblur="check_range(this,0,255,'IP')" value="$ip_addr[2]" />.
        <input size="3" maxlength="3" class="num" id="ip_addr_3" onblur="check_range(this,0,255,'IP')" value="$ip_addr[3]" />
    </div>
    <div class="setting">
        <div class="label">Subnet Mask:</div>
        <input size="3" maxlength="3" class="num" id="netmask_0" onblur="check_range(this,0,255,'IP')" value="$netmask[0]" />.
        <input size="3" maxlength="3" class="num" id="netmask_1" onblur="check_range(this,0,255,'IP')" value="$netmask[1]" />.
        <input size="3" maxlength="3" class="num" id="netmask_2" onblur="check_range(this,0,255,'IP')" value="$netmask[2]" />.
        <input size="3" maxlength="3" class="num" id="netmask_3" onblur="check_range(this,0,255,'IP')" value="$netmask[3]" />
    </div>
    <div class="setting">
        <div class="label">Gateway:</div>
        <input size="3" maxlength="3" class="num" id="gateway_0" onblur="check_range(this,0,255,'IP')" value="$gateway[0]" />.
        <input size="3" maxlength="3" class="num" id="gateway_1" onblur="check_range(this,0,255,'IP')" value="$gateway[1]" />.
        <input size="3" maxlength="3" class="num" id="gateway_2" onblur="check_range(this,0,255,'IP')" value="$gateway[2]" />.
        <input size="3" maxlength="3" class="num" id="gateway_3" onblur="check_range(this,0,255,'IP')" value="$gateway[3]" />
    </div>

    <div class="setting">
        <div class="label">DNS 1:</div>
        <input size="3" maxlength="3" class="num" id="dns1_0" onblur="check_range(this,0,255,'IP')" value="$dns1[0]" />.
        <input size="3" maxlength="3" class="num" id="dns1_1" onblur="check_range(this,0,255,'IP')" value="$dns1[1]" />.
        <input size="3" maxlength="3" class="num" id="dns1_2" onblur="check_range(this,0,255,'IP')" value="$dns1[2]" />.
        <input size="3" maxlength="3" class="num" id="dns1_3" onblur="check_range(this,0,255,'IP')" value="$dns1[3]" />
    </div>

    <div class="setting">
        <div class="label">DNS 2:</div>
        <input size="3" maxlength="3" class="num" id="dns2_0" onblur="check_range(this,0,255,'IP')" value="$dns2[0]" />.
        <input size="3" maxlength="3" class="num" id="dns2_1" onblur="check_range(this,0,255,'IP')" value="$dns2[1]" />.
        <input size="3" maxlength="3" class="num" id="dns2_2" onblur="check_range(this,0,255,'IP')" value="$dns2[2]" />.
        <input size="3" maxlength="3" class="num" id="dns2_3" onblur="check_range(this,0,255,'IP')" value="$dns2[3]" />
    </div>
    </div>

    <br/>
    <div class="submitFooter">
    <input type="button" id="save_btn" value="Save Settings" onclick="save_lan_settings()"/>
    <input type="reset" value="Cancel Changes" onClick="lan_form_reset(this)"/>
    </div>
    </form>
    """

    content = web.template.Template(content)
    return content(addr_alloc, ip_addr, netmask, gateway, dns1, dns2)

def save_lan_settings(query):
    db = xml_db()
    if db.open() == False:
        raise PageError("Could not open configuration storage")

    query.pop("cmd")

    res = db.set_params_set("lan", query)

    if res == "":
        db.update()
        import subprocess
        proc = subprocess.Popen(lan_config_script, shell=True, stdout=subprocess.PIPE)
        res = proc.wait()

        return json.dumps({"err":"0", "errmsg":""})
    else:
        return json.dumps({"err":"1", "errmsg":"Could not save settings"})



def make_select_input(sel_from, sel):
    content = ""
    for sel_item in sel_from:
        if sel_item == sel:
            content = content + "<option selected=\"selected\">" + sel_item + "</option>"
        else:
            content = content + "<option>" + sel_item + "</option>"

    return content

def make_protocol_select_input(sel_from, sel):
    content = ""
    for sel_item in sel_from:
        if sel_item == sel:
            content = content + "<option selected=\"selected\">" + sel_item.replace('_', ' ') + "</option>"
        else:
            content = content + "<option>" + sel_item.replace('_', ' ') + "</option>"
    return content

def make_region_select_input(sel_from, sel):
    content = ""
    for sel_item in sel_from:
        if sel_item == sel:
            content = content + "<option selected=\"selected\">" + sel_item.replace('_', ' ') + "</option>"
        else:
            content = content + "<option>" + sel_item.replace('_', ' ') + "</option>"
    return content

def make_power_select_input(sel_from, sel):
    content = ""
    for sel_item in sel_from:
        pwr = 10**(float(sel_item)/10)
        if sel_item == sel:
            content = content + "<option selected=\"selected\">" + sel_item + "dBm (" + '%4.1f'%pwr + " mW)</option>"
        else:
            content = content + "<option>" + sel_item + "dBm (" + '%4.1f'%pwr + " mW)</option>"

#### test    content = content + "<option>45dBm (35000 mW)</option>"

    return content




def make_uhf_page():
    db = xml_db()
    if db.open() == False:
        raise PageError("Could not open configuration storage")
    installed_hw_option = db.get_params_set("hw_option")
    hw_uhf = installed_hw_option["hw_uhf"]["val"]
    if hw_uhf != "installed":
        return "<h2>UHF modem</h2>There is no UHF module in this device"

    import dbus

    product_id = ""
    bus = dbus.SessionBus()
    try:
        remote_object = bus.get_object("jlinklte.uhfd", "/")
        iface = dbus.Interface(remote_object, "jlinklte.uhfd.interface")
        product_id = iface.uhf_get_product_id()

    except dbus.DBusException:
        raise PageError("Could not get Product ID!")
    if product_id == "unknown" :
        raise PageError("Product ID is unknown!")

    if product_id == "138" :
        fh_settings     = db.get_params_set("fh")
        region_details = db.get_fh_region_details()


        region_details_payload = json.dumps(region_details)
        region_sel = make_region_select_input(fh_settings["region"]["select_from"], fh_settings["region"]["val"])

        protocol_list = ["Receiver", "Transmitter", "Transceiver"]
        protocol_sel = make_select_input(protocol_list, fh_settings["protocol"]["val"])
        repeater_list = ["On", "Off"]
        repeater_sel = make_select_input(repeater_list, fh_settings["repeater"]["val"])
        power_list = ["15", "16", "17", "18", "19", "20", "21", "22", "23","24", "25", "26", "27", "28", "29", "30"]
        power_sel = make_power_select_input(power_list, fh_settings["power"]["val"])
        fec = get_value(fh_settings, "fec", "val")
        fec_on  = "checked=\"checked\"" if fec == "Enable" else ""
        fec_off = "checked=\"checked\"" if fec == "Disable" else ""
        scrambling = get_value(fh_settings, "scrambling", "val")
        scrambling_on  = "checked=\"checked\"" if scrambling == "Enable" else ""
        scrambling_off = "checked=\"checked\"" if scrambling == "Disable" else ""
        fan_control = get_value(fh_settings, "fan_control", "val")
        fan_control_on  = "checked=\"checked\"" if fan_control == "Enable" else ""
        fan_control_off = "checked=\"checked\"" if fan_control == "Disable" else ""
        status_info = get_value(fh_settings, "status_info", "val")
        status_info_on  = "checked=\"checked\"" if status_info == "Enable" else ""
        status_info_off = "checked=\"checked\"" if status_info == "Disable" else ""


        content = """$def with (region_details_payload, region_sel, protocol_list, protocol_sel, repeater_list, repeater_sel, power_list, power_sel, fec_on, fec_off, scrambling_on, scrambling_off, fan_control_on, fan_control_off, status_info_on, status_info_off) \n
        <script type="text/javascript" src="/static/fh.js"></script>
        <link rel="stylesheet" type="text/css" href="/static/wizard.css"/>
        <script type="text/javascript" src="/static/wizard.js"></script>

        <div style="display:none;" id="region_details"><script type="application/json">$region_details_payload</script></div>
        <h2>UHF modem</h2>
        <form>
        <div class="setting"><div class="label">Region:</div><select style="width: 100px" name="region" id="region_sel" onchange="region_change()">$region_sel</select></div>
        <div class="setting"><div class="label">Protocol:</div><select name="protocol" id="protocol_sel" style="width: 140px">$protocol_sel</select></div>
        <div class="setting"><div class="label">Repeater:</div><select name="repeater" id="repeater_sel" style="width: 140px">$repeater_sel</select></div>
        <div class="setting"><div class="label">Output power:</div><select name="power" id="power_sel" style="width: 140px">$power_sel</select></div>
        <div class="setting"><div class="label">FEC:</div>
        <div>
            <input type="radio" id="fec_on" name="fec" $fec_on /><label>Enable</label>
            <input type="radio" id="fec_off" name="fec" $fec_off /><label>Disable</label>
        </div>
        <div class="setting"><div class="label">Scrambling:</div>
        <div>
            <input type="radio" id="scrambling_on" name="scrambling" $scrambling_on /><label>Enable</label>
            <input type="radio" id="scrambling_off" name="scrambling" $scrambling_off /><label>Disable</label>
        <div>
        <div class="setting"><div class="label">Fan control:</div>
        <div>
            <input type="radio" id="fan_control_on" name="fan_control" $fan_control_on /><label>Enable</label>
            <input type="radio" id="fan_control_off" name="fan_control" $fan_control_off /><label>Disable</label>
        </div>
        <div class="setting"><div class="label">Status info:</div>
        <div>
            <input type="radio" id="status_info_on" name="status_info" $status_info_on /><label>Enable</label>
            <input type="radio" id="status_info_off" name="status_info" $status_info_off /><label>Disable</label>
        </div>
        <br />
        <h2>Region details</h2>
        <div class="setting"><div class="label">Modulation:</div><div class="label" id="modulation"></div></div>
        <div class="setting"><div class="label">Freq TX:</div><div class="label" id="freq_tx"></div></div>
        <div class="setting"><div class="label">Freq RX:</div><div class="label" id="freq_rx"></div></div>
        <div class="setting"><div class="label" id="channel_spacing_label"></div><div class="label" id="channel_spacing"></div></div>
        <div class="setting"><div class="label" id="f_rule_label"></div><div class="label" id="f_rule"></div></div>
        <div class="setting"><div class="label" id="redundancy_label"></div><div class="label" id="redundancy"></div></div>

        <br />
        <div class="submitFooter">
        <input id="save_btn" type="button" value="Save Settings" onClick="save_uhf_settings()" />
        <input type="reset" value="Cancel Changes" onClick="uhf_form_reset(this)" />
        </div>
        </form>
        """

        content = web.template.Template(content)
        return content(region_details_payload, region_sel, protocol_list, protocol_sel, repeater_list, repeater_sel, power_list, power_sel, fec_on, fec_off, scrambling_on, scrambling_off, fan_control_on, fan_control_off, status_info_on, status_info_off)

    else:
        uhf_settings     = db.get_params_set("uhf")
        protocol_details = db.get_uhf_protocol_details()
        user_freqs       = db.get_uhf_freqs()
        #print uhf_settings
        #print protocol_details

        freq_rx = uhf_settings["freq_rx"]["val"]
        freq_tx = uhf_settings["freq_tx"]["val"]

        freq_rx_str = freq_rx[0:3] + "." + freq_rx[3:6] + "." + freq_rx[6:] + " Hz"
        freq_tx_str = freq_tx[0:3] + "." + freq_tx[3:6] + "." + freq_tx[6:] + " Hz"

        prot_sel  = make_protocol_select_input(uhf_settings["protocol"]["select_from"], uhf_settings["protocol"]["val"])

        protocol_details_payload = json.dumps(protocol_details)
        user_freqs_payload = json.dumps(user_freqs)


        power_list = ["15", "16", "17", "18", "19", "20", "21", "22", "23","24", "25", "26", "27", "28", "29", "30"]
        if (product_id == "761") or (product_id == "991"):
            power_list = ["15", "16", "17", "18", "19", "20", "21", "22", "23","24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36"]
        elif (product_id == "751") or (product_id == "97"):
            power_list = ["25", "26", "27", "28", "29", "30", "31", "32", "33","34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46"]
        elif (product_id == "98"):
            power_list = ["25", "26", "27", "28", "29", "30", "31", "32", "33","34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44"]

        min_freq = 406000000;
        max_freq = 470000000;
        if (product_id == "97") or (product_id == "991"):
            min_freq = 138000000;
            max_freq = 176000000;
        elif (product_id == "98"):
            min_freq = 215000000;
            max_freq = 255000000;

        power_sel = make_power_select_input(power_list, uhf_settings["power"]["val"])

        csign = get_value(uhf_settings, "csign", "val")
        snrm = get_value(uhf_settings, "snrm", "val")
        snrm_on  = "checked=\"checked\"" if snrm == "Enable" else ""
        snrm_off = "checked=\"checked\"" if snrm == "Disable" else ""
        fan_control = get_value(uhf_settings, "fan_control", "val")
        fan_control_on  = "checked=\"checked\"" if fan_control == "Enable" else ""
        fan_control_off = "checked=\"checked\"" if fan_control == "Disable" else ""
        antenna_detect = get_value(uhf_settings, "antenna_detect", "val")
        antenna_detect_on  = "checked=\"checked\"" if antenna_detect == "Enable" else ""
        antenna_detect_off = "checked=\"checked\"" if antenna_detect == "Disable" else ""
        tx_delay = get_value(uhf_settings, "tx_delay", "val")
        status_info = get_value(uhf_settings, "status_info", "val")
        status_info_on  = "checked=\"checked\"" if status_info == "Enable" else ""
        status_info_off = "checked=\"checked\"" if status_info == "Disable" else ""


        content = """$def with (freq_rx_str, freq_tx_str, min_freq, max_freq, power_sel, prot_sel, protocol_details_payload, user_freqs_payload, csign, snrm_on, snrm_off, fan_control_on, fan_control_off, antenna_detect_on, antenna_detect_off, status_info_on, status_info_off, tx_delay) \n
        <script type="text/javascript" src="/static/uhf.js"></script>
        <script>
            var min_uhf_freq = $min_freq;
            var max_uhf_freq = $max_freq;
        </script>
        <link rel="stylesheet" type="text/css" href="/static/wizard.css"/>
        <script type="text/javascript" src="/static/wizard.js"></script>

        <div style="display:none;" id="protocol_details"><script type="application/json">$protocol_details_payload</script></div>
        <div style="display:none;" id="user_freqs"><script type="application/json">$user_freqs_payload</script></div>
        <h2>UHF modem</h2>
        <form>
        <div class="setting"><div class="label">Frequency RX:</div><div><div class="label" id="freq_rx_val" style="width: 90px">$freq_rx_str</div><input type="button" style="width: 30px; height: 15px;" value="..." onClick="set_freq_rx_event()"/></div></div>
        <div class="setting"><div class="label">Frequency TX:</div><div><div class="label" id="freq_tx_val" style="width: 90px">$freq_tx_str</div><input type="button" style="width: 30px; height: 15px;" value="..." onClick="set_freq_tx_event()"/></div></div>
        <div class="setting"><div class="label">Output power:</div><select name="power" id="power_sel" style="width: 140px">$power_sel</select></div>
        <div class="setting"><div class="label">Protocol:</div><select style="width: 100px" name="protocol" id="protocol_sel" onchange="protocol_change()">$prot_sel</select></div>
        <div class="setting"> <div class="label">Call Sign:</div> <input maxlength="10" size="10" id="csign" onkeyup="format_csign(this)" value="$csign" />
        </div>
        <div class="setting">
            <div class="label">Tx Delay: ( in range 0 - 650 ms ) </div>

            <input maxlength="63" size="20" value="$tx_delay" name="tx_delay" id="tx_delay" onblur="check_range(this,0,650,'Tx Delay')" />
        </div>
        <div class="setting"><div class="label">SNRM:</div>
        <div>
            <input type="radio" id="snrm_on" name="snrm" $snrm_on /><label>Enable</label>
            <input type="radio" id="snrm_off" name="snrm" $snrm_off /><label>Disable</label>
        </div>
        <div class="setting"><div class="label">Fan control:</div>
        <div>
            <input type="radio" id="fan_control_on" name="fan_control" $fan_control_on /><label>Enable</label>
            <input type="radio" id="fan_control_off" name="fan_control" $fan_control_off /><label>Disable</label>
        </div>
        <div class="setting"><div class="label">Antenna detect:</div>
        <div>
            <input type="radio" id="antenna_detect_on" name="antenna_detect" $antenna_detect_on /><label>Enable</label>
            <input type="radio" id="antenna_detect_off" name="antenna_detect" $antenna_detect_off /><label>Disable</label>
        </div>
        <div class="setting"><div class="label">Status info:</div>
        <div>
            <input type="radio" id="status_info_on" name="status_info" $status_info_on /><label>Enable</label>
            <input type="radio" id="status_info_off" name="status_info" $status_info_off /><label>Disable</label>
        </div>
        <br />
        <h2>Protocol details</h2>
        <div class="setting"><div class="label" id="mode_label"></div><div class="label" id="mode_val"></div></div>
        <div class="setting"><div class="label">Modulation:</div><div class="label" id="modulation"></div></div>
        <div class="setting"><div class="label">Channel spacing:</div><div class="label" id="channel_spacing"></div></div>
        <div class="setting"><div class="label">FEC:</div><div class="label" id="fec"></div></div>
        <div class="setting"><div class="label">Scrambling:</div><div class="label" id="scrambling"></div></div>
        <div class="setting"><div class="label">Scrambling seed:</div><div class="label" id="scram_num_val"></div></div>
        <div class="setting"><div class="label">Link rate:</div><div class="label" id="link_rate"></div></div>
        <div class="setting"><div class="label" id="aux_label"></div><div class="label" id="aux_val"></div></div>
        <div class="setting"><div class="label" id="compartibility_label"></div><div class="label" id="compartibility_val"></div></div>

        <br />
        <div class="submitFooter">
        <input id="save_btn" type="button" value="Save Settings" onClick="save_uhf_settings()" />
        <input type="reset" value="Cancel Changes" onClick="uhf_form_reset(this)" />
        </div>
        </form>
        """

        content = web.template.Template(content)
        return content(freq_rx_str, freq_tx_str, min_freq, max_freq, power_sel, prot_sel, protocol_details_payload, user_freqs_payload, csign, snrm_on, snrm_off, fan_control_on, fan_control_off, antenna_detect_on, antenna_detect_off, status_info_on, status_info_off, tx_delay)



def save_uhf_settings(query):
    import dbus
    db = xml_db()
    if db.open() == False:
        raise PageError("Could not open configuration storage")

    res = ""

    if query.has_key("csign"):
        uhf_params = {}
        uhf_params["csign"] = query["csign"]
        if query.has_key("freq_rx"):
            uhf_params["freq_rx"] = query["freq_rx"]
        if query.has_key("freq_tx"):
            uhf_params["freq_tx"] = query["freq_tx"]
        if query.has_key("power"):
            uhf_params["power"] = query["power"]
        if query.has_key("protocol"):
            uhf_params["protocol"] = query["protocol"]
        if query.has_key("fan_control"):
            uhf_params["fan_control"] = query["fan_control"]
        if query.has_key("snrm"):
            uhf_params["snrm"] = query["snrm"]
        if query.has_key("antenna_detect"):
            uhf_params["antenna_detect"] = query["antenna_detect"]
        if query.has_key("tx_delay"):
            uhf_params["tx_delay"] = query["tx_delay"]
        if query.has_key("status_info"):
            uhf_params["status_info"] = query["status_info"]

        if len(uhf_params) != 0:
            res = db.set_params_set("uhf", uhf_params)
            if res != "":
                raise PageError("Could not save settings")

    if query.has_key("region"):
        fh_params = {}
        fh_params["region"] = query["region"]
        if query.has_key("protocol"):
            fh_params["protocol"] = query["protocol"]
        if query.has_key("repeater"):
            fh_params["repeater"] = query["repeater"]
        if query.has_key("power"):
            fh_params["power"] = query["power"]
        if query.has_key("fec"):
            fh_params["fec"] = query["fec"]
        if query.has_key("scrambling"):
            fh_params["scrambling"] = query["scrambling"]
        if query.has_key("fan_control"):
            fh_params["fan_control"] = query["fan_control"]
        if query.has_key("status_info"):
            fh_params["status_info"] = query["status_info"]

        if len(fh_params) != 0:
            res = db.set_params_set("fh", fh_params)
            if res != "":
                raise PageError("Could not save settings")

    if query.has_key("protocol_details"):
        protocol_details = json.loads(query["protocol_details"])
        for protocol_name in protocol_details:
            details = protocol_details[protocol_name]
            details_to_save = {}
            for detail in details:
                if details[detail].has_key("select_from"):
                    details_to_save[detail] = details[detail]["value"]
                if details[detail].has_key("type"):
                    details_to_save[detail] = details[detail]["value"]
            if len(details_to_save):
                res = db.set_uhf_protocol_details(protocol_name, details_to_save)
                if res != "":
                    raise PageError("Could not save settings")

    if query.has_key("region_details"):
        region_details = json.loads(query["region_details"])
        for region_name in region_details:
            details = region_details[region_name]
            details_to_save = {}
            for detail in details:
                if details[detail].has_key("select_from"):
                    details_to_save[detail] = details[detail]["value"]
                if details[detail].has_key("type"):
                    details_to_save[detail] = details[detail]["value"]
            if len(details_to_save):
                res = db.set_fh_region_details(region_name, details_to_save)
                if res != "":
                    raise PageError("Could not save settings")

    if query.has_key("user_freqs"):
        res = db.set_uhf_freqs(eval(query["user_freqs"]))
        if res != "":
            raise PageError("Could not save settings")

    if res == "":
        db.update()
        gsetup = db.get_params_set("gsetup")
        en_uhf = gsetup["en_uhf"]["val"]
        if en_uhf == "Enable":
            bus = dbus.SessionBus()
            try:
                remote_object = bus.get_object("jlinklte.uhfd", "/")
                iface = dbus.Interface(remote_object, "jlinklte.uhfd.interface")
                iface.uhf_disable()
                iface.uhf_enable()
                import time
                time.sleep(20)
            except dbus.DBusException:
                raise PageError("Could not restart UHF/FH module!")
        return json.dumps({"err":"0", "errmsg":""})
    else:
        return json.dumps({"err":"1", "errmsg":"Could not save settings"})




def make_bluetooth_page():
    db = xml_db()
    if db.open() == False:
        raise PageError("Could not open configuration storage")

    installed_hw_option = db.get_params_set("hw_option")
    hw_bt = installed_hw_option["hw_bt"]["val"]
    if hw_bt != "installed":
        return "<h2>Bluetooth Module</h2>There is no Bluetooth module in this device"

    bt_settings         = db.get_params_set("bt_adapter")
    bt_discoverable     = get_value(bt_settings,"bt_discoverable","val")
    bt_name             = get_value(bt_settings,"bt_name","val")
    bt_pin              = get_value(bt_settings,"bt_pin","val")
    bt_mode             = get_value(bt_settings,"bt_mode","val")
    bt_dest             = get_value(bt_settings,"bt_dest","val")
    bt_mode_master      = "checked=\"checked\"" if bt_mode == "Master" else ""
    bt_mode_slave       = "checked=\"checked\"" if bt_mode == "Slave" else ""
    bt_discoverable_on  = "checked=\"checked\"" if bt_discoverable == "Enable" else ""
    bt_discoverable_off = "checked=\"checked\"" if bt_discoverable == "Disable" else ""

    content = """$def with (bt_discoverable, bt_name, bt_pin, bt_mode, bt_dest, bt_mode_master, bt_mode_slave, bt_discoverable_on, bt_discoverable_off) \n
    <script type="text/javascript" src="/static/bt.js"></script>
    <h2>Bluetooth adapter</h2>

    <form>
    <div class="setting"><div class="label">Device Name:</div><input maxlength="32" size="20" id="bt_name" name="bt_name" value="$bt_name"/></div>
    <div class="setting"><div class="label">Device Mode:</div>
    <div>
        <input type="radio" id="bt_mode_master" name="bt_mode" $bt_mode_master onchange="bt_mode_change()" /><label>Master</label>
        <input type="radio" name="bt_mode" $bt_mode_slave onchange="bt_mode_change()" /><label>Slave</label>
    </div>
    </div>
    <div class="setting"><div class="label">Destination Address:</div>
        <input maxlength="17" size="20" id="bt_dest" name="bt_dest" onkeyup="formatMAC(this)"value="$bt_dest" />
        <input id="bt_scan" name="bt_scan" type="button" value="Scan" onclick="bt_scan_devices()" /></div>
    <div class="setting"><div class="label">Discoverable:</div>
    <div>
        <input type="radio" id="discoverable_on" name="discoverable" $bt_discoverable_on /><label>Enable</label>
        <input type="radio" id="discoverable_off" name="discoverable" $bt_discoverable_off /><label>Disable</label>
    </div>
    <div class="setting"><div class="label">PIN:</div><input maxlength="4" size="4" id="bt_pin" name="bt_pin" value="$bt_pin"/></div>
    <br />
    <div class="submitFooter">
        <input id="save_btn" type="button" value="Save Settings" onclick="save_bluetooth_settings()" />
        <input type="reset" value="Cancel Changes" onClick="bt_form_reset(this)" />
    </div>
    </form>
    """

    content = web.template.Template(content)
    return content(bt_discoverable, bt_name, bt_pin, bt_mode, bt_dest, bt_mode_master, bt_mode_slave, bt_discoverable_on, bt_discoverable_off)

def bt_scan_devices(query):
    query.pop("cmd")
    stream = os.popen("hcitool scan|grep  '[0-9A-F]'")
    result = stream.read()
    print result
    return json.dumps({"err":"0", "errmsg":"", "bt_scan_result":result})


def save_bluetooth_settings(query):
    db = xml_db()
    if db.open() == False:
        raise PageError("Could not open configuration storage")

    query.pop("cmd")
    res = db.set_params_set("bt_adapter", query)
    if res == "":
        db.update()
        import subprocess
        proc = subprocess.Popen(bt_reconfig_script, shell=True)
        res = proc.wait()
        return {"err":"0", "errmsg":""}
    else:
        return {"err":"1", "errmsg":"Could not save settings"}




def make_gsm_page():
    db = xml_db()
    if db.open() == False:
        raise PageError("Could not open configuration storage")

    installed_hw_option = db.get_params_set("hw_option")
    hw_gsm = installed_hw_option["hw_gsm"]["val"]
    if hw_gsm != "installed":
        return "<h2>Wireless module</h2>There is no wireless module on this device"


    gsm_settings = db.get_params_set("gsm")
    #print gsm_settings
    if gsm_settings == None:
        pin  = ""
        apn  = ""
        user = ""
        pwd  = ""
	en_pap = "Disable"
	en_chap = "Disable"
        carrier_profile  = "GENERIC"
	agps = "Off"
    else:
        pin       = get_value(gsm_settings,"pin", "val")
        apn       = get_value(gsm_settings,"apn","val")
        user      = get_value(gsm_settings,"user","val")
        pwd       = get_value(gsm_settings,"pwd","val")
        en_pap    = get_value(gsm_settings,"en_pap","val")
        en_chap   = get_value(gsm_settings,"en_chap","val")
        carrier_profile   = get_value(gsm_settings,"carrier_profile","val")
        agps      = get_value(gsm_settings,"agps","val")
        pn = os.popen(printenv_util  + " pn 2>/dev/null").read().rstrip("\n")
        if pn != None and pn != "":
            pn = pn.split("=")[1]
        else:
            pn = "unknown"
        if pn == "01-597520-10" or pn == "01-597520-11" or pn == "01-597520-12" or\
           pn == "01-597520-13" or pn == "01-597520-14" or pn == "01-597520-15" or\
           pn == "01-597520-16" or pn == "01-597520-17" or pn == "01-597520-18" or\
           pn == "01-597521-10" or pn == "01-597521-11" or pn == "01-597521-12" or\
           pn == "01-597521-13" or pn == "01-597521-14" or pn == "01-597521-15" or\
           pn == "01-597521-16" or pn == "01-597521-17" or pn == "01-597521-18" or\
           pn == "01-587300-51" or pn == "01-587100-51" or pn == "01-597400-51" or\
           pn == "01-587500-51" or pn == "01-587800-51":
            carrier_list = [ 'GENERIC' ]
        else:
            if pn == "01-597520-40" or pn == "01-597520-41" or pn == "01-597520-42" or\
               pn == "01-597520-43" or pn == "01-597520-44" or pn == "01-597520-45" or\
               pn == "01-597520-46" or pn == "01-597520-47" or pn == "01-597520-48" or\
               pn == "01-597521-40" or pn == "01-597521-41" or pn == "01-597521-42" or\
               pn == "01-597521-43" or pn == "01-597521-44" or pn == "01-597521-45" or\
               pn == "01-597521-46" or pn == "01-597521-47" or pn == "01-597521-48" or\
               pn == "01-587300-54" or pn == "01-587100-54" or pn == "01-597400-54" or\
               pn == "01-587500-54" or pn == "01-587800-54":
                carrier_list = [ 'GENERIC', 'VERIZON', 'ATT' ]
            else:
                carrier_list = [ 'GENERIC', 'VERIZON', 'ROGERS', 'TELUS', 'BELL', 'ATT' ]



    content = """$def with (pin, apn, user, pwd, en_pap, en_chap, carrier_profile, carrier_list, agps) \n
    <script type="text/javascript" src="/static/gsm.js"></script>

    <form>

        <div class="setting">
                <div class="label">PIN:</div>
        <input maxlength="32" size="20" name="pin" value="$pin" />
    </div>

        <div class="setting">
                <div class="label">APN Name:</div>
        <input maxlength="32" size="20" name="apn" value="$apn" />
    </div>

        <div class="setting">
                <div class="label">User Name:</div>
        <input maxlength="32" size="20" name="user" value="$user" />
    </div>

        <div class="setting">
                <div class="label">Password:</div>
        <input maxlength="32" size="20" name="pwd" value="$pwd" />
    </div>

        <div class="setting"><div class="label">PAP:</div>
        $if en_pap == "Enable":
            <div><input type="radio" name="en_pap" id="en_pap_id" checked="checked" value="Enable">Enable</input><input type="radio" name="en_pap" value="Disable">Disable</input></div>
        $else:
            <div><input type="radio" name="en_pap" id="en_pap_id" value="Enable">Enable</input><input type="radio" name="en_pap" checked="checked" value="Disable">Disable</input></div>
    </div>

        <div class="setting"><div class="label">CHAP:</div>
        $if en_chap == "Enable":
            <div><input type="radio" name="en_chap" id="en_chap_id" checked="checked" value="Enable">Enable</input><input type="radio" name="en_chap" value="Disable">Disable</input></div>
        $else:
            <div><input type="radio" name="en_chap" id="en_chap_id" value="Enable">Enable</input><input type="radio" name="en_chap" checked="checked" value="Disable">Disable</input></div>
    </div>

    <div class="setting"><div class="label">Carrier Profile:</div>
        <select id="carrier_profile" name="carrier_profile" style="text-align:left;"">
        $for value in carrier_list:
            $if value  == carrier_profile:
               <option selected>$value</option>
            $else:
               <option>$value</option>
        </select></div>
    <div class="setting">

    <div class="setting"><div class="label">AGPS mode:</div>
        <select id="agps" name="agps" style="text-align:left;"">
        $for value in [ 'Off',  'Base', 'Assisted' ] :
            $if value  == agps:
               <option selected>$value</option>
            $else:
               <option>$value</option>
        </select></div>
    <div class="setting">


    <br />
    <div class="submitFooter">
    <input type="button" value="Save Settings" onClick="to_submit(this.form)" />
    <input type="reset" value="Cancel Changes" />
    </div>


    </form>
    """

    content = web.template.Template(content)
    return content(pin, apn, user, pwd, en_pap, en_chap, carrier_profile, carrier_list, agps)

#####    <input type="reset" value="Restart GSM Module" onClick="restart_gsm()"/>




def make_wifi_page():
    db = xml_db()
    if db.open() == False:
        raise PageError("Could not open configuration storage")


    installed_hw_option = db.get_params_set("hw_option")
    hw_wifi = installed_hw_option["hw_wifi"]["val"]
    if hw_wifi != "installed":
        return "<h2>Wi-Fi Module</h2>There is no Wi-Fi module on this device."


    gsetup = db.get_params_set("gsetup")
    state  = gsetup["en_wifi"]["val"]


    wifi_settings = db.get_params_set("wifi_adapter")
    if wifi_settings == None or wifi_settings.has_key("mode") == False:
        raise PageError("Could not define adapter mode")

    #print wifi_settings

    if True:
        mac_map = db.get_mac_map()
        ssid = get_value(wifi_settings,"ssid", "val")

        mode_list = ["client", "AP", "AP+client"]
	m = wifi_settings["mode"]["val"]
        mode       = make_select_input(mode_list, wifi_settings["mode"]["val"])
        hwmode     = make_select_input(wifi_settings["hwmode"]["select_from"], wifi_settings["hwmode"]["val"])
        channel    = make_select_input(wifi_settings["channel"]["select_from"], wifi_settings["channel"]["val"])
        channel_5g = make_select_input(wifi_settings["channel_5g"]["select_from"], wifi_settings["channel_5g"]["val"])
        protection = make_select_input(wifi_settings["protection"]["select_from"], wifi_settings["protection"]["val"])
        if wifi_settings["protection"]["val"] == "OPEN":
            passphrase = ""
        else:
            if wifi_settings.has_key("passphrase"):
                passphrase = wifi_settings["passphrase"]["val"]
            else:
                passphrase = ""

        content = """$def with (state, mode, m, ssid, hwmode, channel, channel_5g, protection,  passphrase, mac_map) \n
        <script type="text/javascript" src="/static/utils.js"></script>
	<script type="text/javascript" src="/static/wifiap.js"></script>
        <script type="text/javascript" src="/static/wifi.js"></script>
        <h2>Wi-Fi adapter</h2>
        <div class="setting"><div class="label">Adapter mode:</div>AP</div>

        <div class="setting"><div class="label">Adapter state:</div>
        $if state == "Enable":
            <div id="adapter_state">Enabled</div>
        $else:
            <div id="adapter_state">Disabled</div>
        </div>

        <div class="submitFooter"><div class="label">Adapter Mode</div><select id="mode_btn" name="mode_btn" style="width: 100px" onchange="set_adapter_mode()">$mode</select></div>

        $if m != "AP":
            <h2>Wi-Fi client</h2>
            <br/>
            <div id="wifi_networks"></div>

        <br/>
        <h2>AP settings</h2>
        <form>
        <div class="setting"><div class="label">SSID:</div><input maxlength="32" size="20" name="ssid" value="$ssid"/></div>
        <div class="setting"><div class="label">Operation mode:</div><select id="hwmode" name="hwmode" style="width: 40px" onchange="hwmode_change()">$hwmode</select></div>
        <div class="setting"><div class="label">Channel 2.4G:</div><select id="channel" name="channel" style="width: 40px">$channel</select></div>
        <div class="setting"><div class="label">Channel 5G:</div><select id="channel_5g" name="channel_5g" style="width: 40px">$channel_5g</select></div>
        <div class="setting"><div class="label">Protection:</div><select id="protection" name="protection" style="width: 70px">$protection</select></div>
        <div class="setting"><div class="label">Secret passphrase:</div><input id="passphrase" maxlength="32" size="20" name="passphrase" value="$passphrase"/></div>

        <br/>
        <h2>MAC MAP</h2>
        <form>
        <table id=mac_table>
            <tr>
                <th>MAC address</th>
                <th>IP address</th>
                <th>Action</th>
            </tr>
            <tr>
                <td><input id="mac_in" maxlength="17" size="12" onkeyup="formatMAC(this)"value="" /></td>
                <td>10.1.10.<input id="ip_in" size="1" onblur="validate_ip(this,101,200)" /></td>
                <td><input type="button" value="Add" onClick="add_mac()" /></td>
            </tr>
            $for key in mac_map:
                <tr id = "$key">
                    <td name="mac">$key</td>
                    <td name="ip" >$mac_map[key]</td>
                    <td><input id=$key type="button" value="Remove" onClick="remove_mac(this)"></td>
                </tr>
        </table>


        <br/>
        <div class="submitFooter">
        <input type="button" value="Save Settings" onClick="save_settings()" />
        <input type="reset" value="Cancel Changes" />
        </div>
        </form>
        """
        content = web.template.Template(content)
        return content(state, mode, m, ssid, hwmode, channel, channel_5g, protection, passphrase, mac_map)



def get_wifi_env(query):
    import subprocess

    proc = subprocess.Popen("wpa_cli -i wlan0 status", shell=True, stdout=subprocess.PIPE)
    res = proc.wait()

    status = {}
    if res == 0:
        for line in proc.stdout:
            spl=line.rstrip().split("=")
            if len(spl) == 2:
                status[spl[0]] = spl[1]

    con_bssid = ""
    con_state = ""
    if status.has_key("wpa_state"):
        if status["wpa_state"] != "INACTIVE":
            con_state = status["wpa_state"]

            if status.has_key("bssid"):
                con_bssid = status["bssid"]

    #print  con_bssid, " ", con_state

    proc = subprocess.Popen("iw wlan0 scan", shell=True, stdout=subprocess.PIPE)
    res = proc.wait()

    if res != 0:
        return json.dumps({"err":"1", "errmsg":"Cant' get Wi-Fi environment"})


    wifi_freqs = [2412, 2417, 2422, 2427, 2432, 2437, 2442, 2447, 2452, 2457, 2462, 2467, 2472, 2484]

    wifi_env = []
    scan_item = None


    def freq_to_channel(freq):
        channel = 1;
        for frq in wifi_freqs:
            if freq == frq:
                return str(channel)
            else:
                channel = channel + 1
        return "..."

    def get_ssid(line, scan_res):
        return {"ssid":line[6:]}

    def get_signal_lvl(line, scan_res):
        return {"slvl":line[8:]}


    def get_freq(line, scan_res):
        return {"freq":line[6:] + " MHz", "channel":freq_to_channel(int(line[6:]))}


    def get_rsn(line, scan_res):
        scan_res.readline()
        pairwise_ciphers = scan_res.readline()

        encryp_type = "unknown"
        if pairwise_ciphers.find("CCMP") != -1:
            encryp_type = "CCMP"

        scan_res.readline()
        scan_res.readline()
        return {"rsn":encryp_type}

    def get_wpa(line, scan_res):
        scan_res.readline()
        pairwise_ciphers = scan_res.readline()

        encryp_type = "unknown"
        if pairwise_ciphers.find("TKIP") != -1:
            encryp_type = "TKIP"

        scan_res.readline()
        scan_res.readline()
        return {"wpa":encryp_type}


    def get_capability(line, scan_res):
        if line.find("Privacy") == -1:
            return {"encryp":"off"}
        else:
            return {"encryp":"on"}

    par_list = {"SSID":get_ssid, "freq":get_freq, "signal":get_signal_lvl, "RSN":get_rsn, "WPA":get_wpa, "capability":get_capability}


    line = proc.stdout.readline().rstrip().strip().strip('\t')
    while line:

	if line[0:3] == "BSS" and line[4:5] != "L":
            if scan_item != None:
                wifi_env.append(scan_item)
            scan_item = {}
            scan_item["bssid"] = line[4:21]

            if scan_item["bssid"] == con_bssid:
                scan_item["state"] = con_state
        else:
            for par_name in par_list:
                if par_name == line[0:len(par_name)]:
                    ext_pars = par_list[par_name](line, proc.stdout)
                    for name in ext_pars:
                        scan_item[name] = ext_pars[name]

        line = proc.stdout.readline().rstrip().strip().strip('\t')

    if scan_item != None:
        wifi_env.append(scan_item)

    for item in wifi_env:
        item["protection"] = "OPEN"
        if item.has_key("encryp") and item["encryp"] == "on":
            if item.has_key("rsn"):
                item["protection"] = "WPA2"
                item.pop("rsn")
                if item.has_key("wpa"):
                    item.pop("wpa")
            elif item.has_key("wpa"):
                item["protection"] = "WPA"
                item.pop("wpa")
            else:
                item["protection"] = "WEP"
            item.pop("encryp")

    #print wifi_env

    return json.dumps({"err":"0", "errmsg":"", "wifi_env":wifi_env})


def get_wifi_networks(query):
    db = xml_db()
    if db.open() == False:
        return json.dumps({"err":"0", "errmsg":"", "wifi_networks":{}})

    wifi_networks = db.get_wifi_networks()

    for item in wifi_networks:
        if item.has_key("passphrase"):
            item.pop("passphrase")

    #print wifi_networks

    return json.dumps({"err":"0", "errmsg":"", "wifi_networks":wifi_networks})

def add_wifi_mac(query):
    import subprocess
    proc = subprocess.Popen("jlink add mac " + query["bssid"] + " " + query["ip"], shell=True)
    res = proc.wait()
    if res == 0:
        return json.dumps({"err":"0", "errmsg":"", "bssid":query["bssid"], "ip":query["ip"]})
    else:
        return json.dumps({"err":"Can't add MAC", "errmsg":res})

def remove_wifi_mac(query):
    import subprocess
    proc = subprocess.Popen("jlink remove mac " + query["bssid"], shell=True)
    res = proc.wait()
    if res == 0:
        return json.dumps({"err":"0", "errmsg":"", "bssid":query["bssid"]})
    else:
        return json.dumps({"err":"Can't remove MAC", "errmsg":res})

def forget_wifi_network(query):
    db = xml_db()
    if db.open() == False:
        return PageError("Can't open data base")

    res = db.remove_wifi_network(query["bssid"])

    if res == "":
        db.update()
        import subprocess
        proc = subprocess.Popen(remove_network_script + " " + query["bssid"], shell=True)
        res = proc.wait()

        return json.dumps({"err":"0", "errmsg":""})
    else:
        return json.dumps({"err":"1", "errmsg":res})


def add_wifi_network(query):
    db = xml_db()
    if db.open() == False:
        return PageError("Can't open data base")

    query.pop("cmd")

    res = db.add_wifi_network(query)

    if res == "":
        db.update()

        import subprocess
        proc = subprocess.Popen(add_network_script + " " + query["bssid"] + " " + query["ssid"] + " " + query["protection"] + " " + query["passphrase"], shell=True)
        res = proc.wait()

        return json.dumps({"err":"0", "errmsg":""})
    else:
        return json.dumps({"err":"1", "errmsg":res})


def connect_wifi_network(query):
    import subprocess
    proc = subprocess.Popen(connect_network_script + " " + query["bssid"], shell=True)
    res = proc.wait()

    if res == 0:
        return {"err":"0", "errmsg":""}
    else:
        return {"err":"1", "errmsg":"Couldn't initiate connection to a network"}




def save_gsm_settings(query):
    db = xml_db()
    if db.open() == False:
        raise PageError("Could not open configuration storage")

    query.pop("cmd")

    carrier_profile = "GENERIC"
    if query.has_key("carrier_profile"):
        carrier_profile = query["carrier_profile"]


    res = db.set_params_set("gsm", query)

    if res == "":
        db.update()
        import subprocess
        proc = subprocess.Popen("jlink config gsm -carrier_profile=" + carrier_profile , shell=True, stdout=subprocess.PIPE)
        proc.wait()

        return json.dumps({"err":"0", "errmsg":""})
    else:
        return json.dumps({"err":"1", "errmsg":"Could not save settings"})


def wifi_set_mode(query):

    db = xml_db()
    if db.open() == False:
        raise PageError("Could not open configuration storage")

    import subprocess

    if query["mode"] == "AP":
        proc = subprocess.Popen(client_stop_script + ";" + ap_init_script, shell=True, stdout=subprocess.PIPE)
        res = db.set_param_set("wifi_adapter", "mode", "AP")

    elif query["mode"] == "client":
        proc = subprocess.Popen(ap_stop_script + ";" + client_init_script, shell=True, stdout=subprocess.PIPE)
        res = db.set_param_set("wifi_adapter", "mode", "client")
    else:
        proc = subprocess.Popen(ap_stop_script + ";" + client_stop_script + ";" + client_init_script + ";" + ap_init_script, shell=True, stdout=subprocess.PIPE)
        res = db.set_param_set("wifi_adapter", "mode", "AP+client")

    proc.wait()
    if res == "":
        db.update()

    return {"err":"0", "errmsg":""}


#def wifi_set_state(query):
#    db = xml_db()
#    if db.open() == False:
#        raise PageError("Could not open configuration storage")


#    if query["state"] == "enabled":
#        res = db.set_param_set("wifi_adapter", "state", "enabled")
#    elif query["state"] == "disabled":
#        res = db.set_param_set("wifi_adapter", "state", "disabled")


#    if res == "":
#        db.update()

#        import subprocess
#        if query["state"] == "enabled":
#            proc = subprocess.Popen(adapter_start_script, shell=True, stdout=subprocess.PIPE)
#        elif query["state"] == "disabled":
#            proc = subprocess.Popen(adapter_stop_script, shell=True, stdout=subprocess.PIPE)
#        proc.wait()

#        return {"err":"0", "errmsg":""}
#    else:
#        return {"err":"1", "errmsg":"Could not set state"}



def save_wifiap_settings(query):
    db = xml_db()
    if db.open() == False:
        raise PageError("Could not open configuration storage")

    query.pop("cmd")

    res = db.set_params_set("wifi_adapter", query)

    if res == "":
        db.update()
        import subprocess
	proc = subprocess.Popen(ap_stop_script + ";" + ap_init_script,
                shell=True, stdout=subprocess.PIPE)
	proc.wait()
        return {"err":"0", "errmsg":""}
    else:
        return {"err":"1", "errmsg":"Could not save settings"}


def restart_gsm(query):
    import dbus

    bus = dbus.SessionBus()
    try:
        remote_object = bus.get_object("gsm.modem.service", "/obj")
        iface = dbus.Interface(remote_object, "gsm.modem.interface")
        status = iface.gsm_modem_restart()

    except dbus.DBusException:
        raise PageError("Could not restart GSM module!")

    return {"err":"0", "errmsg":""}


def make_power_management_page():
    db = xml_db()
    if db.open() == False:
        raise PageError("Could not open configuration storage")

    installed_hw_option = db.get_params_set("hw_option")

    hw_gps  = installed_hw_option["hw_gps"]["val"]
    hw_gsm  = installed_hw_option["hw_gsm"]["val"]
    hw_uhf  = installed_hw_option["hw_uhf"]["val"]
    hw_wifi = installed_hw_option["hw_wifi"]["val"]
    hw_bt   = installed_hw_option["hw_bt"]["val"]

    gsetup = db.get_params_set("gsetup")

    en_gps  = gsetup["en_gps"]["val"]
    en_gsm  = gsetup["en_gsm"]["val"]
    en_uhf  = gsetup["en_uhf"]["val"]
    en_wifi = gsetup["en_wifi"]["val"]
    en_bt   = gsetup["en_bt"]["val"]


    content = """$def with (hw_gps, hw_gsm, hw_uhf, hw_wifi, hw_bt, en_gps, en_gsm, en_uhf, en_wifi, en_bt) \n
    <script type="text/javascript" src="/static/gsetup.js"></script>
    <h2>Peripheries setup</h2>
    <form>
        $if hw_gsm == "installed":
            <div class="setting"><div class="label">GSM:</div>
            $if en_gsm == "Enable":
                <div><input type="radio" name="en_gsm" id="en_gsm_id" checked="checked" onchange="check_gps_visibility()" value="Enable">Enable</input><input type="radio" name="en_gsm" onchange="check_gps_visibility()" value="Disable">Disable</input></div>
            $else:
                <div><input type="radio" name="en_gsm" id="en_gsm_id" onchange="check_gps_visibility()" value="Enable">Enable</input><input type="radio" name="en_gsm" onchange="check_gps_visibility()" checked="checked" value="Disable">Disable</input></div>
            </div>
        $if hw_uhf == "installed":
            <div class="setting"><div class="label">UHF:</div>
            $if en_uhf == "Enable":
                <div><input type="radio" name="en_uhf" checked="checked" value="Enable">Enable</input><input type="radio" name="en_uhf" value="Disable">Disable</input></div>
            $else:
                <div><input type="radio" name="en_uhf" value="Enable">Enable</input><input type="radio" name="en_uhf" checked="checked" value="Disable">Disable</input></div>
            </div>
        $if hw_gps == "installed":
            <div class="setting"><div class="label">GNSS:</div>
            $if en_gps == "Enable":
                <div><input type="radio" name="en_gps" id="en_gps_on_id"
                checked="checked" value="Enable">Enable</input><input type="radio" name="en_gps" id="en_gps_off_id" value="Disable">Disable</input></div>
            $else:
                <div><input type="radio" name="en_gps" id="en_gps_on_id" value="Enable">Enable</input><input type="radio" name="en_gps" id="en_gps_off_id" checked="checked" value="Disable">Disable</input></div>
            </div>

       $if hw_wifi == "installed":
            <div class="setting"><div class="label">Wi-Fi:</div>
            $if en_wifi == "Enable":
                <div><input type="radio" name="en_wifi" checked="checked" value="Enable">Enable</input><input type="radio" name="en_wifi" value="Disable">Disable</input></div>
            $else:
                <div><input type="radio" name="en_wifi" value="Enable">Enable</input><input type="radio" name="en_wifi" checked="checked" value="Disable">Disable</input></div>
            </div>

       $if hw_bt == "installed":
            <div class="setting"><div class="label">BT:</div>
            $if en_bt == "Enable":
                <div><input type="radio" name="en_bt" checked="checked" value="Enable">Enable</input><input type="radio" name="en_bt" value="Disable">Disable</input></div>
            $else:
                <div><input type="radio" name="en_bt" value="Enable">Enable</input><input type="radio" name="en_bt" checked="checked" value="Disable">Disable</input></div>
            </div>

    <div class="submitFooter">
    <input id="apply_btn" type="button" value="Apply Settings" onclick="apply_power_management_settings()" />
    <input type="reset" value="Cancel Changes" onClick="power_form_reset(this)" />
    </div>
    </form>
    """

    content = web.template.Template(content)
    return content(hw_gps, hw_gsm, hw_uhf, hw_wifi, hw_bt, en_gps, en_gsm, en_uhf, en_wifi, en_bt)


def apply_power_management_settings(query):
    db = xml_db()
    if db.open() == False:
        raise PageError("Could not open configuration storage")

    query.pop("cmd")

    res = db.set_params_set("gsetup", query)

    if res == "":
        db.update()
        import subprocess
        proc = subprocess.Popen(jlinklte_config_script, shell=True)
        res = proc.wait()
        return {"err":"0", "errmsg":""}
    else:
        return {"err":"1", "errmsg":"Could not save settings"}





def make_advanced_setup_page():
    db = xml_db()
    if db.open() == False:
        raise PageError("Could not open configuration storage")

    adv = db.get_params_set("advsetup")

    ser_mode  = adv["ser_mode"]["val"]

    if ser_mode == "Network":
       ser_list = "<option>Network<option>Terminal<option>Console";
    elif ser_mode == "Terminal":
       ser_list = "<option>Terminal<option>Console<option>Network";
    else:
       ser_list = "<option>Console<option>Terminal<option>Network";

    bt_mode  = adv["bt_ser_mode"]["val"]

    if bt_mode == "Console":
       bt_list = "<option>Console<option>Terminal";
    else:
       bt_list = "<option>Terminal<option>Console";


    inet_first_prior = adv["internet_first_prior"]["val"]

    if inet_first_prior == "LAN":
       inet_list = "<option>LAN<option>WIFI<option>GSM";
    elif inet_first_prior == "WIFI":
       inet_list = "<option>WIFI<option>LAN<option>GSM";
    else:
       inet_list = "<option>GSM<option>LAN<option>WIFI";

    net_gps  = get_value(adv,"net_gps","val")

    eth_mode  = adv["eth_mode"]["val"]
    if eth_mode == "LAN":
       eth_list = "<option>LAN<option>BRIDGE";
    else:
       eth_list = "<option>BRIDGE<option>LAN";

    time_shift = adv["time_shift"]["val"]
    timezone_list =  [  'GMT-12:00', 'GMT-11:30', 'GMT-11:00', 'GMT-10:30', 'GMT-10:00', 'GMT-9:30',
                        'GMT-9:00', 'GMT-8:30', 'GMT-8:00', 'GMT-7:30', 'GMT-7:00', 'GMT-6:30',
                        'GMT-6:00', 'GMT-5:30', 'GMT-5:00', 'GMT-4:30', 'GMT-4:00', 'GMT-3:30',
                        'GMT-3:00', 'GMT-2:30', 'GMT-2:00', 'GMT-1:30', 'GMT-1:00', 'GMT-0:30',
                        'GMT', 'GMT+0:30', 'GMT+1:00', 'GMT+1:30', 'GMT+2:00', 'GMT+2:30',
                        'GMT+3:00', 'GMT+3:30', 'GMT+4:00', 'GMT+4:30', 'GMT+5:00', 'GMT+5:30',
                        'GMT+6:00', 'GMT+6:30', 'GMT+7:00', 'GMT+7:30', 'GMT+8:00', 'GMT+8:30',
                        'GMT+9:00', 'GMT+9:30', 'GMT+10:00', 'GMT+10:30', 'GMT+11:00', 'GMT+11:30',
                        'GMT+12:00' ]
    content = """$def with (ser_list, bt_list,inet_list, eth_list, net_gps, time_shift, timezone_list)\n
    <script type="text/javascript" src="/static/adv.js"></script>
    <h2>Console Port Setup</h2>
    <form>
    <div>
           <div class="setting"><div class="label">Serial port as:
           </div><select id="serial_port_sel" style="width: 80px">$ser_list
           </select></div>
           <div class="setting"><div class="label">BT port as:
           </div><select id="bt_port_sel" style="width: 80px">$bt_list
           </select></div>
    </div>

    <h2>Internet First Priority Setup</h2>
    <form>
    <div>
           <div class="setting"><div class="label">First Pririty:
           </div><select id="first_priority_sel" style="width: 80px">$inet_list
           </select></div>
    </div>

    <h2>Ethernet Mode Setup</h2>
    <form>
    <div>
           <div class="setting"><div class="label">Ethernet Mode:
           </div><select id="eth_sel" style="width: 80px">$eth_list
           </select></div>
    </div>

    <h2>External Network GPS PATH</h2>
    <form>
        <div class="setting">
                <div class="label">Net GPS IP:PORT</div>
        <input maxlength="32" size="20" name="net_gps" value="$net_gps" />
    </div>


    <h2>Time Setting</h2>
        <div class="setting"><div class="label">Time zone:</div>
			<select id="time_shift" name="time_shift" style="text-align:left;"">
                        $for value in timezone_list:
                            $if value  == time_shift:
                              <option selected>$value</option>
                            $else:
                              <option>$value</option>
                        </select></div>
            <div class="setting">
    <br />

    <div class="submitFooter">
    <input id="save_btn" type="button" value="Save Settings"
    onclick="save_advanced_settings()" />
    <input type="reset" value="Cancel Changes" />
    </div>
    </form>
    """

    content = web.template.Template(content)
    return content(ser_list, bt_list,inet_list, eth_list, net_gps, time_shift, timezone_list)


def save_advanced_settings(query):
    db = xml_db()
    if db.open() == False:
        raise PageError("Could not open configuration storage")

    query.pop("cmd")

    res = db.set_params_set("advsetup", query)

    if res == "":
        import subprocess
        import os
        from subprocess import Popen, PIPE
        from os import environ

        db.update()
        proc = subprocess.Popen(". %s; env" % timezone_config_script,stdout=PIPE, shell=True)
        data=proc.communicate()[0]
        env = dict((line.split("=", 1) for line in data.splitlines()))
        environ.update(env)
        return {"err":"0", "errmsg":"Please reboot the device"}
    else:
        return {"err":"1", "errmsg":"Could not save settings"}



class communication:
    def GET(self):
        if session.check_session() == False:
            return
        path = web.ctx.path
        content = ""
        try:
            if (path == "/communication" or path == "/lan"):
                menu = build_menu("Communication", "LAN")
                content = make_lan_page()
            elif (path == "/uhf"):
                menu = build_menu("Communication", "UHF Int.")
                content = make_uhf_page()
            elif (path == "/extmodem"):
                menu = build_menu("Communication", "UHF Ext.")
                content = make_uhf_page()
            elif (path == "/gsm"):
                menu = build_menu("Communication", "GSM")
                content = make_gsm_page()
            elif (path == "/wifi"):
                menu = build_menu("Communication", "Wi-Fi")
                content = make_wifi_page()
            elif (path == "/bt"):
                menu = build_menu("Communication", "Bluetooth")
                content = make_bluetooth_page()
            elif (path == "/gsetup"):
                menu = build_menu("Communication", "Power Management")
                content = make_power_management_page()
            elif (path == "/adv"):
                menu = build_menu("Communication", "Advanced")
                content = make_advanced_setup_page()
        except PageError as perr:
            content = perr.errmsg


        return render.webiface(menu, content)



    def POST(self):
        #if session.check_session() == False:
        #    return

        query = web.input()
        print query


        if query.cmd == None:
            return {"err":"1", "errmsg":"There is no cmd field!"}


        try:
            if query.cmd == "save_gsm_settings":
                save_gsm_settings(query)
                return {"err":"0", "errmsg":""}
            elif query.cmd == "get_wifi_env":
                return get_wifi_env(query)
            elif query.cmd == "get_wifi_networks":
                return get_wifi_networks(query)
            elif query.cmd == "forget_wifi_network":
                return forget_wifi_network(query)
            elif query.cmd == "add_wifi_network":
                return add_wifi_network(query)
            elif query.cmd == "connect_wifi_network":
                return connect_wifi_network(query)
            elif query.cmd == "wifi_set_mode":
                return wifi_set_mode(query)
            elif query.cmd == "add_wifi_mac":
                return add_wifi_mac(query)
            elif query.cmd == "remove_wifi_mac":
                return remove_wifi_mac(query)
#            elif query.cmd == "wifi_set_state":
#                return wifi_set_state(query)
            elif query.cmd == "save_wifiap_settings":
                return save_wifiap_settings(query)
            elif query.cmd == "restart_gsm":
                return restart_gsm(query)
            elif query.cmd == "save_uhf_settings":
                return save_uhf_settings(query)
            elif query.cmd == "save_lan_settings":
                return save_lan_settings(query)
            elif query.cmd == "save_bluetooth_settings":
                return save_bluetooth_settings(query)
            elif query.cmd == "bt_scan_devices":
                return bt_scan_devices(query)
            elif query.cmd == "apply_power_management_settings":
                apply_power_management_settings(query)
            elif query.cmd == "save_advanced_settings":
                save_advanced_settings(query)

            else:
                return {"err":"1", "errmsg":"There is no correct cmd field!"}

        except PageError as perr:
            return {"err":"1", "errmsg":perr.errmsg}


        return {"err":"0", "errmsg":""}

