
function ajax_err(jqXHR, textStatus, errorThrown)
{
    apprise_close_progress_box();
    apprise("Error during server connection!");
}


function send_ajax_req(req, callback_fn)   
{
    jQuery.ajax({type: "POST", data: req, dataTypeString: "json", success: callback_fn, error: ajax_err});  
}




function do_progress() 
{
	var pp = document.getElementById("progress");
	if( !pp ) return false;
	
	if( /\.{10}/.test( pp.innerHTML ) ) 
		pp.innerHTML = "";
	else 
		pp.innerHTML += ".";
	
	setTimeout( "do_progress()", 200 );
}



function ping_next(data)
{   
    var resp = eval('(' + data + ')');

    if(resp.err == "1") 
    {
        jQuery("#ping_result").empty();
        jQuery("#ping_result").append("<h1>" + resp.errmsg + "</h1>");
        $("#ping_start_btn").removeAttr("disabled");     
    }
    else
    {
        var text;
        text = resp.ping_res.replace(/\n/g, "<br />");                    
        text = text.replace(/PING.*data bytes/, "<span style=\"color:#aaaaaa;\">---$&---</span>");          

        if(resp.err == "0")
        {
            if(text != "")
            {
                jQuery("#ping_result").empty();
                jQuery("#ping_result").append(text);    
            }

            setTimeout("send_ajax_req({cmd:\"ping_next\"}, ping_next)", 1000);
        }
        else
        {
            text = text.replace(/--- .* ping statistics ---/, "<span style=\"color:#aaaaaa;\">$&</span>");  
            text = text.replace(/Ok/, "");  
            jQuery("#ping_result").empty();
            jQuery("#ping_result").append(text); 
            $("#ping_start_btn").removeAttr("disabled");     
        }
    }
    

} 



function ping_start_cb(data) 
{
    var resp = eval('(' + data + ')');

    if(resp.err == "0") 
    {
        var text;
        text = resp.ping_res.replace(/\n/g, "<br />");                    
        text = text.replace(/PING.*data bytes/, "<span style=\"color:#aaaaaa;\">---$&---</span>");          
        if(text != "")
        {
            $("#ping_result").empty();
            $("#ping_result").append(text);
        }
        setTimeout("send_ajax_req({cmd:\"ping_next\"}, ping_next)", 10);
    }
    else
    {
        $("#ping_result").empty();
        $("#ping_result").append("<h1>" + resp.errmsg + "</h1>");
        $("#ping_start_btn").removeAttr("disabled");     
    }                                
}




function ping_start(id)
{

    $("#ping_result").empty();
    var ip_addr = $("#ip_addr").val();
    var iface = $("#iface").val();

    if(ip_addr == "")
    {
        apprise("Ping destination isn't defined!");
        return false;
    }

    $("#ping_start_btn").attr("disabled", "disabled");

    $("#ping_result").append("processing <span id=\"progress\"></span>");
    send_ajax_req({cmd:"ping_start", addr:ip_addr, iface:iface}, ping_start_cb); 
    do_progress(); 
    return false;
}




$("body").ready(function() 
{                          
});

