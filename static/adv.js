function ajax_err(jqXHR, textStatus, errorThrown)
{
    apprise_close_progress_box();
    apprise("Error during server connection!");
}


function send_ajax_req(req, callback_fn)
{
    jQuery.ajax({type: "POST", data: req, dataTypeString: "json", success: callback_fn, error: ajax_err});
}


function save_advanced_settings_resp(data)
{
    var resp = eval('(' + data + ')');

    $("#save_btn").removeAttr("disabled");
    if(resp.err != "0")
        apprise("Error: " + resp.errmsg);
    else
        apprise("Settings have been successfully saved, Please reboot the device.");
}


function save_advanced_settings()
{
    var settings_to_save = jQuery("form").serialize();
    settings_to_save += "&cmd=save_advanced_settings";
    var serial_port_sel = document.getElementById("serial_port_sel").value;
    settings_to_save += "&ser_mode="+serial_port_sel;
    var bt_port_sel = document.getElementById("bt_port_sel").value;
    settings_to_save += "&bt_ser_mode="+bt_port_sel;
    var inet_sel = document.getElementById("first_priority_sel").value;
    settings_to_save += "&internet_first_prior="+inet_sel;
    var eth_sel = document.getElementById("eth_sel").value;        
    settings_to_save += "&eth_mode="+eth_sel; 
    var elt = document.getElementById("time_shift");
    var time_shift = elt.options[elt.selectedIndex].text;
    settings_to_save += "&time_shift="+encodeURIComponent(time_shift);


    $("#save_btn").attr("disabled", "disabled");
    send_ajax_req(settings_to_save, save_advanced_settings_resp);
    return false;
}
