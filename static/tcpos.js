
function ajax_err(jqXHR, textStatus, errorThrown)
{
    apprise_close_progress_box();
    apprise("Error during server connection!");
}


function send_ajax_req(req, callback_fn)   
{
    $.ajax({type: "POST", data: req, dataTypeString: "json", success: callback_fn, error: ajax_err});  
}

var get_tcpo_status = function(data)
{
    var resp = eval('(' + data + ')');

    if(resp.err != "0") 
    {
        $("#tcpo_status").empty();
        $("#tcpo_status").append(resp.errmsg);       
    }
    else
    {

        $("#tcpo_status").empty();
        $("#tcpo_status").append(resp.tcpo_status);

        setTimeout( "send_ajax_req({cmd:\"get_tcpo_status\"}, get_tcpo_status)", 2000 );
    }
}

$(document).ready(function(){setTimeout( "send_ajax_req({cmd:\"get_tcpo_status\"}, get_tcpo_status)", 2000 );});



