function ajax_err(jqXHR, textStatus, errorThrown)
{
    apprise_close_progress_box();
    apprise("Error during server connection!");
}


function send_ajax_req(req, callback_fn)   
{
    $.ajax({type: "POST", data: req, dataTypeString: "json", success: callback_fn, error: ajax_err});  
}

var get_gps_status = function(data)
{
    var resp = eval('(' + data + ')');

    if(resp.err != "0") 
    {
        $("#sat").empty();
        $("#loc").empty();
        $("#loc").append(resp.errmsg);       
    }
    else
    {

        $("#sat").empty();
        $("#loc").empty();
        $("#loc").append(resp.loc_cont);
        $("#sat").append(resp.sat_cont);

        $("#sat_tbl tr:even").addClass("even");
        $("#sat_tbl tr:odd").addClass("odd");

        setTimeout( "send_ajax_req({cmd:\"get_gps_status\"}, get_gps_status)", 1000 );
    }
}

$(document).ready(function()
{
    $("#sat_tbl tr:even").addClass("even");
    $("#sat_tbl tr:odd").addClass("odd");
    setTimeout( "send_ajax_req({cmd:\"get_gps_status\"}, get_gps_status)", 1000 );
});



