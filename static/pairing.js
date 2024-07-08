
function ajax_err(jqXHR, textStatus, errorThrown)
{
    apprise_close_progress_box();
    apprise("Error during server connection!");
}


function send_ajax_req(req, callback_fn)
{
    jQuery.ajax({type: "POST", data: req, dataTypeString: "json", success: callback_fn, error: ajax_err});
}




function pairing_start_cb(data)
{
    var resp = eval('(' + data + ')');

    $("#pairing_start_btn").removeAttr("disabled");
    $("#unpairing_start_btn").removeAttr("disabled");
    apprise_close_progress_box();

    if(resp.err == "0")
    {
        var result;
        var content = "";
        result = resp.pairing_res.replace(/\n/g, "<br />");
        result = "<pre>" + result + "</pre>";
        apprise(result);
    }
    else
    {
        apprise("Error: " + resp.errmsg);
    }
}




function pairing_start(id)
{

    var iface = $("#iface").val();
    $("#pairing_result").empty();

    $("#unpairing_start_btn").attr("disabled", "disabled");
    $("#pairing_start_btn").attr("disabled", "disabled");

    apprise_progress_box("Pairing takes some time. Please wait...");
    send_ajax_req({cmd:"pairing_start", iface:iface}, pairing_start_cb);
    return false;
}

function unpairing_start(id)
{

    var iface = $("#iface").val();
    $("#pairing_result").empty();

    $("#unpairing_start_btn").attr("disabled", "disabled");
    $("#pairing_start_btn").attr("disabled", "disabled");

    apprise_progress_box("UnPairing takes some time. Please wait...");
    send_ajax_req({cmd:"unpairing_start", iface:iface}, pairing_start_cb);
    return false;
}




$("body").ready(function(){});

