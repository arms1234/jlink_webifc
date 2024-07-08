function ajax_err(jqXHR, textStatus, errorThrown)
{
    apprise_close_progress_box();
    apprise("Error during server connection!");
}


function send_ajax_req(req, callback_fn)   
{
    $.ajax({type: "POST", data: req, dataTypeString: "json", success: callback_fn, error: ajax_err});  
}

var get_wifi_status = function(data)
{
    var resp = eval('(' + data + ')');
    var content;

    if(resp.err != "0") 
    {
        $("#wifi_status").empty();
        $("#wifi_status").append(resp.errmsg);       
    }
    else
    {

        $("#wifi_status").empty();
        content = resp.wifi_status;
        $("#wifi_status").append(content);

        setTimeout( "send_ajax_req({cmd:\"get_wifi_status\"}, get_wifi_status)", 4000 );
    }
}



$(document).ready(function(){setTimeout( "send_ajax_req({cmd:\"get_wifi_status\"}, get_wifi_status)", 4000 );});


