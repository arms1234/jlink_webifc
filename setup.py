import web
import sys
import json
import os
import time
import session
import re


from menu import build_menu
from xml_db import xml_db
from perror import PageError


data_router_config_script = "/jlinklte/scripts/data_router_init"

render = web.template.render('templates/')



def make_data_router_setup_page():
    db = xml_db()
    if db.open() == False:
        raise PageError("Could not open configuration storage")

    data_router_map = db.get_params_set("data_router_map")
    gsetup = db.get_params_set("gsetup")
    advsetup = db.get_params_set("advsetup")

    ntrip_src     = "checked=\"checked\"" if data_router_map["ntrip_src"]["val"] == "Enable" else ""
    ntrip_uhf_dst = "checked=\"checked\"" if data_router_map["ntrip_uhf_dst"]["val"] == "Enable" else ""
    ntrip_bt_dst  = "checked=\"checked\"" if data_router_map["ntrip_bt_dst"]["val"] == "Enable" else ""
    ntrip_ser_dst = "checked=\"checked\"" if data_router_map["ntrip_ser_dst"]["val"] == "Enable" else ""
    tcp_src       = "checked=\"checked\"" if data_router_map["tcp_src"]["val"] == "Enable" else ""
    tcp_uhf_dst   = "checked=\"checked\"" if data_router_map["tcp_uhf_dst"]["val"] == "Enable" else ""
    tcp_bt_dst    = "checked=\"checked\"" if data_router_map["tcp_bt_dst"]["val"] == "Enable" else ""
    tcp_ser_dst   = "checked=\"checked\"" if data_router_map["tcp_ser_dst"]["val"] == "Enable" else ""
    uhf_src       = "checked=\"checked\"" if data_router_map["uhf_src"]["val"] == "Enable" else ""
    uhf_bt_dst    = "checked=\"checked\"" if data_router_map["uhf_bt_dst"]["val"] == "Enable" else ""
    uhf_ser_dst   = "checked=\"checked\"" if data_router_map["uhf_ser_dst"]["val"] == "Enable" else ""
    uhf_soc_dst   = "checked=\"checked\"" if uhf_ser_dst == "" and uhf_bt_dst == "" else ""

    uhf_en = "true" if gsetup["en_uhf"]["val"] == "Enable" else "false"
    ser_en = "true" if advsetup["ser_mode"]["val"] == "Terminal" else "false"
    bt_en = "true" if gsetup["en_bt"]["val"] == "Enable" and advsetup["bt_ser_mode"]["val"] == "Terminal"  else "false"

    tcpo_src       = data_router_map["tcpo_src"]["val"]
    if ser_en == "true":
	serial_option = "<option>SERIAL"
    else:
        serial_option = ""

    if bt_en == "true":                                                                                               
        bt_option = "<option>BT"                                                                               
    else:                                                                                                               
        bt_option = ""
    
    if uhf_en == "true":                                                                                                
        uhf_option = "<option>UHF"                                                                                       
    else:                                                                                                              
        uhf_option = ""
    
    if tcpo_src == "SERIAL":
       tcpo_list = serial_option + "<option>NONE" + bt_option + "<option>UHF<option>TCPC<option>NTRIP";  
    elif tcpo_src == "BT":
       tcpo_list = bt_option + "<option>NONE" + serial_option + "<option>UHF<option>TCPC<option>NTRIP";
    elif tcpo_src == "UHF":                                                                                                                                                                  
       tcpo_list = uhf_option + "<option>NONE" + serial_option + bt_option + "<option>TCPC<option>NTRIP";
    elif tcpo_src == "TCPC":                                                                                                                                                                 
       tcpo_list = "<option>TCPC<option>NONE" + serial_option + bt_option + uhf_option + "<option>NTRIP";
    elif tcpo_src == "NTRIP":                                                                                                                                                                 
       tcpo_list = "<option>NTRIP<option>NONE" + serial_option + bt_option + uhf_option + "<option>TCPC";
    else:                                                                                                                                                                 
       tcpo_list = "<option>NONE" + serial_option + bt_option + uhf_option + "<option>TCPC<option>NTRIP";


    content = """$def with (ntrip_src, ntrip_uhf_dst, ntrip_ser_dst, ntrip_bt_dst, tcp_src, tcp_uhf_dst, tcp_ser_dst, tcp_bt_dst, uhf_src, uhf_ser_dst,uhf_bt_dst, uhf_soc_dst, ser_en, uhf_en, bt_en, tcpo_list) \n
    <script>
    var ser_en = $ser_en;
    var uhf_en = $uhf_en;
    var bt_en = $bt_en;
    </script>
    <script type="text/javascript" src="/static/rou.js"></script>
    <h2>NTRIP Client Data Router Setup</h2>
    <form>
    <table class="cor_map_tbl" border="0">
      <tr>
        <th>Source</th>
        <th>Destination</th>
      </tr>
      <tr>
        <td>
        </td>
        <td>
          <input type="checkbox" id="ntrip_uhf_dst" $ntrip_uhf_dst onchange="ntrip_uhf_dest_()" /><label>UHF Modem</label>
        </td>
      </tr>
      <tr>
        <td>
          <input type="checkbox" id="ntrip_src" $ntrip_src onchange="ntrip_src_()" /><label>NTRIP Client</label>
        </td>
        <td>
          <input type="checkbox" id="ntrip_ser_dst" $ntrip_ser_dst onchange="ntrip_ser_dest_()" /><label>Serial port</label>
        </td>
      </tr>
      <tr>
        <td>
        </td>
        <td>
          <input type="checkbox" id="ntrip_bt_dst" $ntrip_bt_dst onchange="ntrip_bt_dest_()" /><label>BT Serial port</label>
        </td>
      </tr>
    </table>
    <h2>TCP Client Data Router Setup</h2>
    <form>
    <table class="cor_map_tbl" border="0">
      <tr>
        <th>Source</th>
        <th>Destination</th>
      </tr>
      <tr>
        <td>
        </td>
        <td>
          <input type="checkbox" id="tcp_uhf_dst" $tcp_uhf_dst onchange="tcp_uhf_dest_()" /><label>UHF Modem</label>
        </td>
      </tr>
      <tr>
        <td>
          <input type="checkbox" id="tcp_src" $tcp_src onchange="tcp_src_()" /><label>TCP Client</label>
        </td>
        <td>
          <input type="checkbox" id="tcp_ser_dst" $tcp_ser_dst onchange="tcp_ser_dest_()" /><label>Serial port</label>
        </td>
      </tr>
      <tr>
        <td>
        </td>
        <td>
          <input type="checkbox" id="tcp_bt_dst" $tcp_bt_dst onchange="tcp_bt_dest_()" /><label>BT Serial port</label>
        </td>
      </tr>
    </table>
    <h2>UHF Modem Data Router Setup</h2>
    <table class="cor_map_tbl" border="0">
      <tr>
        <th>Source</th>
        <th>Destination</th>
      </tr>
      <tr>
        <td>
          <input type="checkbox" id="uhf_src" $uhf_src onchange="uhf_src_()"/><label>UHF Modem</label>
        </td>
        <td>
          <input type="radio" id="uhf_ser_dst" name="src" $uhf_ser_dst onchange="uhf_ser_dest_()"  /><label>Serial port</label>
        </td>
      </tr>
      <tr>
        <td>
        </td>
        <td>
          <input type="radio" id="uhf_bt_dst" name="src" $uhf_bt_dst onchange="uhf_bt_dest_()" /><label>BT Serial port</label>
        </td>
      </tr>
      <tr>                                                                                                                                                                                                  
        <td>                                                                                                                                                                                                
        </td>                                                                                                                                                                                               
        <td>                                                                                                                                                                                                
          <input type="radio" id="uhf_soc_dst" name="src" $uhf_soc_dst onchange="uhf_soc_dest_()" /><label>Socket 1101</label>                                                                              
        </td>                                                                                                                                                                                               
      </tr> 
    </table>
    <h2>TCP Output Data Router Setup</h2>
    <table class="cor_map_tbl" border="0">
      <tr>                                                                                                                                                                                                  
        <th>Source</th>                                                                                                                                                                                     
        <th></th>                                                                                                                                                                                
      </tr> 
           </select></div>
           <td><select id="tcpo_sel" style="width: 80px">$tcpo_list
           </select></div></td>
    </table>
    <br />
    <div class="submitFooter">
      <input id="save_btn" type="button" value="Save Settings"  onclick="save_data_router_settings()" />
      <input type="reset" value="Cancel Changes" onClick="router_form_reset(this)" />
    </div>
    </form>
    """

    content = web.template.Template(content)
    return content(ntrip_src, ntrip_uhf_dst, ntrip_ser_dst, ntrip_bt_dst, tcp_src, tcp_uhf_dst, tcp_ser_dst, tcp_bt_dst, uhf_src, uhf_ser_dst, uhf_bt_dst, uhf_soc_dst, ser_en, uhf_en, bt_en, tcpo_list)


def save_data_router_settings(query):
    db = xml_db()
    if db.open() == False:
        raise PageError("Could not open configuration storage")

    query.pop("cmd")
    res = db.set_params_set("data_router_map", query)

    if res == "":
        db.update()
        import subprocess
        proc = subprocess.Popen(data_router_config_script, shell=True)
        res = proc.wait()
        return {"err":"0", "errmsg":""}
    else:
        return {"err":"1", "errmsg":"Could not save settings"}




class setup:
    def GET(self):
        if session.check_session() == False:
            return
        path = web.ctx.path
        content = ""
        try:
            if (path == "/" or path == "/rou"):
                menu = build_menu("Setup", "Router")
                content = make_data_router_setup_page()


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
            if query.cmd == "save_data_router_settings":
                save_data_router_settings(query)
            else:
                return {"err":"1", "errmsg":"There is no correct cmd field!"}

        except PageError as perr:
            return {"err":"1", "errmsg":perr.errmsg}

        return {"err":"0", "errmsg":""}


