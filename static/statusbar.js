
function sb_ajax_err(jqXHR, textStatus, errorThrown)
{
    apprise_close_progress_box();
    apprise("Error during server connection!");
}


function sb_send_ajax_req( req_url, req, callback_fn)
{
    $.ajax({ url:req_url, type: "POST", data: req, dataTypeString: "json", success: callback_fn, error: sb_ajax_err});
}


function ack_next_gsm_status()
{
    if(window.location.pathname != "/gsms")
        setTimeout("sb_send_ajax_req(\"/gsms\", {cmd:\"get_gsm_status\", src:\"sb\"}, sb_get_gsm_status)", 3000);
    else
        setTimeout("ack_next_gsm_status()", 3000);
}


function sb_get_gsm_status(data)
{
    var resp = eval('(' + data + ')');

    if(resp.err != "0") 
    {
        $("#si_gsm").empty();
        $("#si_gsm").append("<a href=\"/gsms\" target=\"content\"><img src=\"/static/GSM_off.png\" title=\"" + resp.errmsg + "\" /></a>");
    }
    else
    {
        var icon_name = "GSM_off.png";
        var status = "";
        var rssi = 1;
        var mode = "";

        var gsm_status = resp["gsm_status"];
        var reg_status = gsm_status["REG"];

        var status = "Disabled";

        if(gsm_status["STATUS"] == "Ready")
        {
            status = reg_status;

            if(reg_status == "Registered")
            {

                if(gsm_status.hasOwnProperty("NET_TYPE"))
                {
                    if(gsm_status["NET_TYPE"] == "CDMA2000 1x" || gsm_status["NET_TYPE"] == "GSM"
                            || gsm_status["NET_TYPE"] == "EDGE" || gsm_status["NET_TYPE"] == "Unknown")
                    {
                        status += ". GSM mode.";
                        mode = "GSM";
                    }
                    else if (gsm_status["NET_TYPE"] == "LTE")
                    {
                        status += ". LTE mode.";
                        mode = "LTE";
                    }
                    else
                    {
                        status += ". 3G mode.";
                        mode = "3G";
                    }
                }

                if(gsm_status.hasOwnProperty("RSSI"))
                {
                    rssi = parseInt(gsm_status["RSSI"]);
                    if(rssi > -50)
                        icon_name = "GSM_6.png";
                    else if(rssi > -55)
                        icon_name = "GSM_5.png";
                    else if(rssi > -65)
                        icon_name = "GSM_4.png";
                    else if(rssi > -75)
                        icon_name = "GSM_3.png";
                    else if(rssi > -85)
                        icon_name = "GSM_2.png";
                    else if(rssi > -100)
                        icon_name = "GSM_1.png";            
                    else
                        icon_name = "GSM_NoSignal.png";

                    status += " RSSI=" + gsm_status["RSSI"];
                }
            }
            else
                icon_name = "GSM_NoSignal.png";           
        }


        $("#si_gsm").empty();
        $("#si_gsm").append("<a href=\"/gsms\" style=\"z-index:-1;\" target=\"content\"><img src=\"/static/" + icon_name + "\" title=\"" + status + "\" /><p id=\"mode_text\">" + mode +"</p></a>");                    
    }

    ack_next_gsm_status();

    //setTimeout("sb_send_ajax_req(\"/gsms\", {cmd:\"get_gsm_net_status\", src:\"sb\"}, sb_get_gsm_net_status)", 3000);   

}


function sb_get_lan_status(data)
{
    var resp = eval('(' + data + ')');

    if(resp.err != "0") 
    {
        $("#si_lan").empty();
        $("#si_lan").append("<a href=\"/lans\" target=\"content\"><img src=\"/static/Disconnected.png\" title=\"" + resp.errmsg + "\" /></a>");
    }
    else
    {
        var status = "";
        var icon_name = "Disconnected.png"
            var lan_status = resp["lan_status"];

        if(lan_status.hasOwnProperty("state"))
        {
            if(lan_status["state"] == "connected")
            {
                icon_name = "Connected.png"
                    status = lan_status["ip_addr"];
            }
            else
                status = "Disconnected";

        }

        $("#si_lan").empty();
        $("#si_lan").append("<a href=\"/lans\" target=\"content\"><img src=\"/static/" + icon_name + "\" title=\"" + status + "\" /></a>");

        setTimeout("sb_send_ajax_req(\"/lans\", {cmd:\"get_lan_status\", src:\"sb\"}, sb_get_lan_status)", 5000);
    }

}


function sb_get_wifi_status(data)
{
    var resp = eval('(' + data + ')');

    if(resp.err != "0") 
    {
        $("#si_wifi").empty();
        $("#si_wifi").append("<a href=\"/wifis\" target=\"content\"><img src=\"/static/WiFi_Off.png\" title=\"" + resp.errmsg + "\" /></a>");
    }
    else
    {
        var icon_name = "WiFi_Off.png";
        var status = "Disabled";
        var rssi = 1;

        var wifi_status = resp["wifi_status"];

        if(wifi_status["state"] == "Enable")
        {
            if(wifi_status["mode"] == "AP")
            {
                icon_name = "WiFi_3.png";
                status = "AP mode.";
            }
            else
            {
                rssi = parseInt(wifi_status["rssi"]);
                icon_name = "WiFi_NoSignal.png";
                if(wifi_status["wpa_state"] == "COMPLETED")
                {
                    if(rssi > -67)
                        icon_name = "WiFi_3.png";
                    else if(rssi > -71)
                        icon_name = "WiFi_2.png";
                    else if(rssi > -81)
                        icon_name = "WiFi_1.png";
                    else
                        icon_name = "WiFi_0.png";
                }

                status = wifi_status["mode"] + " mode. RSSI=" + rssi.toString() + " dBm";
            }
        }


        $("#si_wifi").empty();
        $("#si_wifi").append("<a href=\"/wifis\" target=\"content\"><img src=\"/static/" + icon_name + "\" title=\"" + status + "\" /></a>");

        //if(window.location.pathname != "/wifis")
        //if(wifi_status["state"] == "Enable")
        setTimeout("sb_send_ajax_req(\"/wifis\", {cmd:\"get_wifi_lite_status\", src:\"sb\"}, sb_get_wifi_status)", 3000);
    }
}


function sb_get_uhf_status(data)
{
    var resp = eval('(' + data + ')');

    if(resp.err != "0") 
    {
        $("#si_uhf_tx").empty();
        $("#si_uhf_tx").append("<a href=\"/uhfs\" target=\"content\"><img src=\"/static/UHF_NoModem.png\" title=\"" + resp.errmsg + "\" /></a>");
        $("#si_uhf_rx").empty();
        $("#si_uhf_rx").append("<a href=\"/uhfs\" target=\"content\"><img src=\"/static/UHF_rx_NoModem.png\" title=\"" + resp.errmsg + "\" /></a>");
    }
    else
    {
        var icon_name_tx = "UHF_NoModem.png";
        var icon_name_rx = "UHF_rx_NoModem.png";
        var status_tx = "Disabled";
        var status_rx = "Disabled";
        var uhf_status = resp["uhf_status"];
        var rssi;
        var power;


        if(uhf_status["state"] == "txing")
        {
            power = uhf_status["power"];
            if (power < 20) {
                icon_name_tx = "UHF_1.png";
            } else if (power > 27) {
                icon_name_tx = "UHF_3.png";
            } else {
                icon_name_tx = "UHF_2.png";
            }
            status_tx = "Transmitting";
        }
        else if(uhf_status["state"] == "idle")
        {
            icon_name_tx = "UHF_NoSignal.png";
            status_tx = "Idle";
        }

        if(uhf_status["state"] != "disabled")
        {
            if(uhf_status["sync"] == "1")
            {
                rssi = parseInt(uhf_status["rssi"]);
                if (rssi <= -90) {
                    icon_name_rx = "UHF_rx_1.png";
                } else if (rssi < -50){
                    icon_name_rx = "UHF_rx_2.png";
                } else if (rssi < -30) {
                    icon_name_rx = "UHF_rx_3.png";
                } else if (rssi < -20) {
                    icon_name_rx = "UHF_rx_4.png";
                } else if (rssi < -10) {
                    icon_name_rx = "UHF_rx_5.png";
                } else {
                    icon_name_rx = "UHF_rx_6.png";
                }
                status_rx = "Receiving"

            } else {
                icon_name_rx = "UHF_rx_NoSignal.png";
                status_rx = "Idle"
            }
        }

        $("#si_uhf_tx").empty();
        $("#si_uhf_tx").append("<a href=\"/uhfs\" target=\"content\"><img src=\"/static/" + icon_name_tx + "\" title=\"" + status_tx + "\" /></a>");
        $("#si_uhf_rx").empty();
        $("#si_uhf_rx").append("<a href=\"/uhfs\" target=\"content\"><img src=\"/static/" + icon_name_rx + "\" title=\"" + status_rx + "\" /></a>");

        setTimeout("sb_send_ajax_req(\"/uhfs\", {cmd:\"get_uhf_lite_status\", src:\"sb\"}, sb_get_uhf_status)", 2000);
    }
}




function sb_get_bt_status(data)
{
    var resp = eval('(' + data + ')');

    if(resp.err != "0") 
    {
        $("#si_bt").empty();
        $("#si_bt").append("<a href=\"/bts\" target=\"content\"><img src=\"/static/BluetoothOff.png\" title=\"" + resp.errmsg + "\" /></a>");
    }
    else
    {        
        var icon_name = "BluetoothOff.png";
        var status = "Disabled";

        var bt_status = resp["bt_status"];

        if(bt_status["state"] == "Enable")
        {
            icon_name = "Bluetooth.png";
            status = "Enabled";

            if(bt_status["connection_state"] == "connected")
            {
                icon_name = "BluetoothConnected.png";
            }
        }

        $("#si_bt").empty();
        $("#si_bt").append("<a href=\"/bts\" target=\"content\"><img src=\"/static/" + icon_name + "\" title=\"" + status + "\" /></a>");        

        setTimeout("sb_send_ajax_req(\"/bts\", {cmd:\"get_bt_status\", src:\"sb\"}, sb_get_bt_status)", 5000);
    }
}


function sb_get_gps_lite_status(data)
{
    var resp = eval('(' + data + ')');

    if(resp.err != "0") 
    {
        $("#si_gps").empty();
        $("#si_gps").append("<a href=\"/gpss\" target=\"content\"><img src=\"/static/Satellite_Off.png\" title=\"" + resp.errmsg + "\" /></a>");
    }
    else
    {        
        var icon_name = "Satellite_Off.png";
        var status = "Disabled";

        var gps_status = resp["gps_lite_status"];

        if(gps_status["state"] == "Enable")
        {
            icon_name = "Satellite_3.png";
            status = "Enabled";           
        }

        $("#si_gps").empty();
        $("#si_gps").append("<a href=\"/gpss\" target=\"content\"><img src=\"/static/" + icon_name + "\" title=\"" + status + "\" /></a>");        

        setTimeout("sb_send_ajax_req(\"/gpss\", {cmd:\"get_gps_lite_status\", src:\"sb\"}, sb_get_gps_lite_status)", 10000);
    }
}



function sb_get_pboard_adc_data(data)
{
    var resp = eval('(' + data + ')');

    if(resp.err != "0") 
    {
        $("#si_bat").empty();
        $("#si_bat").append("<a href=\"/power\" target=\"content\"><img src=\"/static/BatteryLow.png\" title=\"" + resp.errmsg + "\" /></a>");
    }
    else
    {
        var icon_name = "BatteryLow";
        var status = "";

        var adc_data = resp["pboard_adc_data"];
        var input_voltage = parseFloat(adc_data["V_IN"]);
        var bat_voltage = parseFloat(adc_data["V_BAT"]);

        if(input_voltage > 8.2)
        {
            if(bat_voltage > 8.25)
                icon_name = "BatteryFull";
            else if(bat_voltage > 8.0)
                icon_name = "BatteryHalf";
            else
                icon_name = "BatteryLow";
            icon_name += "Charge";
        } else {
            if(bat_voltage > 7.6)
                icon_name = "BatteryFull";
            else if(bat_voltage > 7.4)
                icon_name = "BatteryHalf";
            else
                icon_name = "BatteryLow";
        }


        status = "Power=" + adc_data["V_IN"];
        icon_name += ".png";
        $("#si_bat").empty();
        $("#si_bat").append("<a href=\"/power\" target=\"content\"  style=\"z-index:-1;\"><img src=\"/static/" + icon_name + "\" title=\"" + status + "\" /><p id=\"pwr_ext_mode\"></p></a>");

        setTimeout("sb_send_ajax_req(\"/power\", {cmd:\"get_pboard_adc_data\", src:\"sb\"}, sb_get_pboard_adc_data)", 30000);
    }
}



$(document).ready(function(){
    var loc = window.location.pathname;

    $("#si_gsm").append("<a href=\"/gsms\" target=\"content\"><img src=\"/static/GSM_off.png\" title=\"\" /></a>");
    $("#si_lan").append("<a href=\"/lans\" target=\"content\"><img src=\"/static/Disconnected.png\" title=\"\" /></a>");
    $("#si_wifi").append("<a href=\"/wifis\" target=\"content\"><img src=\"/static/WiFi_NoSignal.png\" title=\"\" /></a>");  
    $("#si_uhf_tx").append("<a href=\"/uhfs\" target=\"content\"><img src=\"/static/UHF_NoModem.png\" title=\"\" />");
    $("#si_uhf_rx").append("<a href=\"/uhfs\" target=\"content\"><img src=\"/static/EXT_NoModem.png\" title=\"\" />");
    $("#si_bt").append("<a href=\"/bts\" target=\"content\"><img src=\"/static/BluetoothOff.png\" title=\"\" /></a>");
    $("#si_gps").append("<a href=\"/gpss\" target=\"content\"><img src=\"/static/Satellite_Off.png\" title=\"\" /></a>");
    $("#si_bat").append("<a href=\"/power\" target=\"content\"><img src=\"/static/BatteryFull.png\" title=\"\" /></a>");


    sb_send_ajax_req("/lans", {cmd:"get_lan_status", src:"sb"}, sb_get_lan_status);

    if(loc != "/gsms")
    sb_send_ajax_req("/gsms", {cmd:"get_gsm_status", src:"sb"}, sb_get_gsm_status);

//if(loc != "/wifis")
sb_send_ajax_req("/wifis", {cmd:"get_wifi_lite_status", src:"sb"}, sb_get_wifi_status);
sb_send_ajax_req("/uhfs", {cmd:"get_uhf_lite_status", src:"sb"}, sb_get_uhf_status);
sb_send_ajax_req("/power", {cmd:"get_pboard_adc_data", src:"sb"}, sb_get_pboard_adc_data); 
sb_send_ajax_req("/bts", {cmd:"get_bt_status", src:"sb"}, sb_get_bt_status); 
sb_send_ajax_req("/gpss", {cmd:"get_gps_lite_status", src:"sb"}, sb_get_gps_lite_status); 
});
