

function ajax_err(jqXHR, textStatus, errorThrown)
{
    apprise_close_progress_box();
    apprise("Error during server connection!");
}


function send_ajax_req(req, callback_fn)
{
    jQuery.ajax({type: "POST", data: req, dataTypeString: "json", success: callback_fn, error: ajax_err});
}


function save_gsm_settings_resp(data)
{
    var resp = eval('(' + data + ')');

    if(resp.err != "0")
        apprise("Error: " + resp.errmsg);
    else
        apprise("Settings have been successfully saved.");
}


function to_submit(F)
{
    var data_to_save = jQuery('form').serialize();
    data_to_save += "&cmd=save_gsm_settings";

    send_ajax_req(data_to_save, save_gsm_settings_resp);
    return false;
}


function restart_gsm_cb(data)
{
    var resp = eval('(' + data + ')');

    if(resp.err != "0")
        apprise("Error: " + resp.errmsg);
    else
        apprise("GSM Module has been successfully restarted");
}

function restart_gsm()
{
    send_ajax_req({cmd:"restart_gsm"}, restart_gsm_cb);
    return false;
}
