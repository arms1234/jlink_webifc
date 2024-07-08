
function ajax_err(jqXHR, textStatus, errorThrown)
{
    apprise_close_progress_box();
    apprise("Error during server connection!");
}


function send_ajax_req(req, callback_fn)   
{
    $.ajax({type: "POST", data: req, dataTypeString: "json", success: callback_fn, error: ajax_err});  
}

var get_tcp_status = function(data)
{
    var resp = eval('(' + data + ')');

    if(resp.err != "0") 
    {
        $("#tcp_status").empty();
        $("#tcp_status").append(resp.errmsg);       
    }
    else
    {

        $("#tcp_status").empty();
        $("#tcp_status").append(resp.tcp_status);

        setTimeout( "send_ajax_req({cmd:\"get_tcp_status\"}, get_tcp_status)", 2000 );
    }
}

$(document).ready(function(){setTimeout( "send_ajax_req({cmd:\"get_tcp_status\"}, get_tcp_status)", 2000 );});



