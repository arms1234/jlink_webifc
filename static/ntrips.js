
function ajax_err(jqXHR, textStatus, errorThrown)
{
    apprise_close_progress_box();
    apprise("Error during server connection!");
}


function send_ajax_req(req, callback_fn)   
{
    $.ajax({type: "POST", data: req, dataTypeString: "json", success: callback_fn, error: ajax_err});  
}

var get_ntrip_status = function(data)
{
    var resp = eval('(' + data + ')');

    if(resp.err != "0") 
    {
        $("#ntrip_status").empty();
        $("#ntrip_status").append(resp.errmsg);       
    }
    else
    {

        $("#ntrip_status").empty();
        $("#ntrip_status").append(resp.ntrip_status);

        setTimeout( "send_ajax_req({cmd:\"get_ntrip_status\"}, get_ntrip_status)", 2000 );
    }
}

$(document).ready(function(){setTimeout( "send_ajax_req({cmd:\"get_ntrip_status\"}, get_ntrip_status)", 2000 );});



