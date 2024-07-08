function ajax_err(jqXHR, textStatus, errorThrown)
{
    apprise_close_progress_box();
    apprise("Error during server connection!");
}


function send_ajax_req(req, callback_fn)   
{
    $.ajax({type: "POST", data: req, dataTypeString: "json", success: callback_fn, error: ajax_err});  
}

var get_uhf_status = function(data)
{
    var resp = eval('(' + data + ')');

    if(resp.err != "0") 
    {
        $("#uhf_status").empty();
        $("#uhf_status").append(resp.errmsg);       
    }
    else
    {

        $("#uhf_status").empty();
        $("#uhf_status").append(resp.uhf_status);

        setTimeout( "send_ajax_req({cmd:\"get_uhf_status\"}, get_uhf_status)", 3000 );
    }
}

$(document).ready(function(){setTimeout( "send_ajax_req({cmd:\"get_uhf_status\"}, get_uhf_status)", 3000 );});



