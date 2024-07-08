



function ajax_err(jqXHR, textStatus, errorThrown)
{
    apprise_close_progress_box();
    apprise("Error during server connection!");
}


function send_ajax_req(req, callback_fn)   
{
    $.ajax({type: "POST", data: req, dataTypeString: "json", success: callback_fn, error: ajax_err});  
}

var get_net_status = function(data)
{
    var resp = eval('(' + data + ')');
    var content;
    var status;

    if(resp.err != "0") 
    {
        $("div#net_reg_status").html("Unknown");
        $("#net_status").empty();
        $("#net_status").append("<div class=\"setting\"><div class=\"label\">Status:</div>" + resp.errmsg + "</div>");       
    }
    else
    {
        content = "";


	     status = resp["gsm_status"];

        if(status["REG"] == "Disable")
	     {
		 $("div#status").html("Disabled"); 
	     }
        else
	     {
		 if(status.hasOwnProperty("SIM"))
		     $("div#sim_card_status").html(status["SIM"]);
		 else
		     $("div#sim_card_status").html("");


		 if(status.hasOwnProperty("REG"))
		     $("div#net_reg_status").html(status["REG"]);
		 else
		     $("div#net_reg_status").html("");

		 if(status.hasOwnProperty("OP"))
		     $("div#operator").html(status["OP"]);
		 else
		     $("div#operator").html("");

		 if(status.hasOwnProperty("APN"))
		     $("div#apn").html(status["APN"]);
		 else
		     $("div#apn").html("");


		 content = "";


		 if(status.hasOwnProperty("NET_TYPE"))
		     content += "<div class=\"setting\"><div class=\"label\">Network Type:</div>" + status["NET_TYPE"] + "</div>";

		 if(status.hasOwnProperty("RSSI"))
		     content += "<div class=\"setting\"><div class=\"label\">RSSI:</div>" + status["RSSI"] + "</div>";


		 if(status.hasOwnProperty("PPP"))
		 {
   	     if(status["PPP"] == "Connected")
		     {
			 content += "<div class=\"setting\"><div class=\"label\">Data connection:</div>Connected</div>";
			 content += "<div class=\"setting\"><div class=\"label\">Assigned address:</div>" + status["IP_ADDR"] + "</div>";			 
		     }
   	     else
			 content += "<div class=\"setting\"><div class=\"label\">Data connection:</div>Disconnected</div>";
		 }




	 /*




		 if(net_status["wm_status"] == "wm is in connection state")
		 {
		     content = "<div class=\"setting\"><div class=\"label\">Status:</div>Wireles Module is in connection state - network status is not available</div>";
		 }
		 else
		 {
		 
		     $("div#temperature").html(net_status["Temperature"] + "&#x2103");
		     if(net_status.hasOwnProperty("System mode"))
			 content += "<div class=\"setting\"><div class=\"label\">System mode:</div>" + net_status["System mode"] + "</div>";
		     if(net_status.hasOwnProperty("PS state"))
			 content += "<div class=\"setting\"><div class=\"label\">PS state:</div>" + net_status["PS state"] + "</div>";
		     if(net_status.hasOwnProperty("Mode"))
			 content += "<div class=\"setting\"><div class=\"label\">Mode:</div>" + net_status["Mode"] + "</div>";
	     
	     
		     if(net_status.hasOwnProperty("GSM band"))
		     {
			 content += "<div class=\"setting\"><div class=\"label\">GSM band:</div>" + net_status["GSM band"] + "</div>";
			 content += "<div class=\"setting\"><div class=\"label\">GSM channel:</div>" + net_status["GSM channel"] + "</div>";
			 content += "<div class=\"setting\"><div class=\"label\">RX level (dBm):</div>" + net_status["RX level (dBm)"] + "</div>";
			 content += "<div class=\"setting\"><div class=\"label\">Serving Cell:</div>" + net_status["Serving Cell"] + "</div>";
			 content += "<div class=\"setting\"><div class=\"label\">GMM (PS) state:</div>" + net_status["GMM (PS) state"] + "</div>";   
			 content += "<div class=\"setting\"><div class=\"label\">MM (CS) state:</div>" + net_status["MM (CS) state"] + "</div>";
			 content += "<div class=\"setting\"><div class=\"label\">GPRS State:</div>" + net_status["GPRS State"] + "</div>";                                                
		     }
		    
		 }
*/

		 $("#net_status").empty();
		 $("#net_status").append(content);


		 if(window.location.pathname == "/gsms")
		     sb_get_gsm_net_status(data);
	     }

        setTimeout( "send_ajax_req({cmd:\"get_gsm_status\"}, get_net_status)", 2000 );
    }
}


$(document).ready(function(){send_ajax_req({cmd:"get_gsm_status"}, get_net_status);});

