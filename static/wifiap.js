
var adapter_state;

function ajax_err(jqXHR, textStatus, errorThrown)
{
	apprise_close_progress_box();
	apprise("Error during server connection!");
}


function send_ajax_req(req, callback_fn)   
{
	$.ajax({type: "POST", data: req, dataTypeString: "json", success: callback_fn, error: ajax_err});  
}

/*
var set_mode_cb = function(data)
{
	var resp = eval('(' + data + ')');
	if(resp.err == "0") 
		window.location = '/wifi';
	else
		apprise("<b>Error:</b> " + resp.errmsg + " Please reload page.");
}


function set_adapter_mode()
{
	$("#mode_btn").attr("disabled", "disabled");
	send_ajax_req({cmd:"wifi_set_mode", mode:"client"}, set_mode_cb);
}*/

function add_mac()
{
	var mac = document.getElementById("mac_in").value;
	var ip = document.getElementById("ip_in").value;
	var l = document.getElementsByName("ip").length;                
	if (l >= 10) {
		apprise('The table limit is reached, Please remove unused MAC and try again.');
		return;
	}
	if ( mac.length < 17 || ip == "") {
		apprise("invalid MAC or IP address\nPlease anter valid IP and MAC");
	} else {
		var i;                                                          
		var value = "";                                                    
		for(i = 0; i < l; i++) {                                        
			value = document.getElementsByName("ip")[i].innerHTML      
				var range = value.split('.');                              
			if (range[3] == ip) {                                   
				document.getElementById("ip_in").value = "";
				apprise('IP value already exsisting in map');   
				return;
			}                                                       
		}                                   
		send_ajax_req({cmd:"add_wifi_mac", bssid:mac, ip:'10.1.10.' + ip}, add_mac_cb);
	}
}

var add_mac_cb = function(data)                                              
{                                                                               
	var resp = eval('(' + data + ')');                                          
	var mac = resp.bssid;
	var ip = resp.ip;
	if(resp.err == "0") {                                                       
		var row = document.getElementById(mac);                         
		if (row == null) {                                              
			var table = document.getElementById('mac_table');       
			var l = document.getElementsByName("ip").length + 2;    
			row = table.insertRow(l)                                
				row.setAttribute("id", mac);                            
			var cell1 = row.insertCell(0);                          
			var cell2 = row.insertCell(1);                          
			var cell3 = row.insertCell(2);                       
			cell1.innerHTML = mac;                                  
			cell1.setAttribute("name", "mac");                      
			cell2.innerHTML = ip;                      
			cell2.setAttribute("name", "ip")                        
				cell3.innerHTML = '<input id=' + mac + ' type="button" value="Remove" onClick="remove_mac(this)" />';
		} else {                                                        
			row.cells[1].innerHTML = ip;
		}               
	} else {                                                                   
		apprise("<b>Error:</b> " + resp.errmsg + " Please reload page.");       
	}                                                                          
} 

var remove_mac_cb = function(data)                                                
{                                                                               
	var resp = eval('(' + data + ')');                                          
	if(resp.err == "0") {                                                         
		document.getElementById(resp.bssid).remove();;
	} else {                                                                       
		apprise("<b>Error:</b> " + resp.errmsg + " Please reload page.");
	}       
}

function remove_mac(d)
{
	send_ajax_req({cmd:"remove_wifi_mac", bssid:d.id}, remove_mac_cb);
} 

function validate_ip(d, min, max) 
{
	is_digit(d);
	dd = parseInt(d.value, 10);     
	if ( !(dd <= max && dd >= min) ) 
	{           
		apprise('IP value is out of range ['+ min + ' - ' + max +']');
		d.value = d.defaultValue;               
	} else  {
		var l = document.getElementsByName("ip").length;
		var i;
		var ip = "";
		for(i = 0; i < l; i++) {
			ip = document.getElementsByName("ip")[i].innerHTML
				var range = ip.split('.');
			if (range[3] == dd) {
				d.value = d.defaultValue;
				apprise('IP value already exsisting in map');
				return;
			}
		}
		d.value = dd;
	}   
}

function formatMAC(inp) {
	var r = /([A-F0-9]{2})([A-F0-9]{2})/i;
	var str = inp.value.replace(/[^a-fA-F0-9]/ig, "");
	str = str.toUpperCase();
	while (r.test(str)) {
		str = str.replace(r, '$1' + ':' + '$2');
	}
	inp.value = str.slice(0, 17);
}



/*
   var set_state_cb = function(data)
   {
   var resp = eval('(' + data + ')');
   if(resp.err == "0") 
   {
   $("#state_btn").removeAttr("disabled");

   if(adapter_state == "disabled")
   {
   $("#adapter_state").text("Disabled");
   $("#state_btn").attr("value", "Enable adapter");
   }          
   else
   {
   $("#adapter_state").text("Enabled");    
   $("#state_btn").attr("value", "Disable adapter");
   }                       
   }
   else
   apprise("<b>Error:</b> " + resp.errmsg + " Please reload page.");
   }
   */


/*
   function set_adapter_state()
   {
   $("#state_btn").attr("disabled", "disabled");

   if($("#adapter_state").text() == "Enabled")
   adapter_state = "disabled";
   else
   adapter_state = "enabled";

   send_ajax_req({cmd:"wifi_set_state", state:adapter_state}, set_state_cb);
   }
   */


var save_wifiap_settings = function(data)
{
	var resp = eval('(' + data + ')');

	if(resp.err == "0") 
		apprise("Settings have been successfully saved.");
	else
		apprise("Error: " + resp.errmsg);
}



function hwmode_change()
{
    var band = $("#hwmode").val();
    if (band == "a") {                           
        $("#channel").attr("disabled", "disabled");
        $("#channel_5g").removeAttr("disabled");               
    } else {                                                
        $("#channel_5g").attr("disabled", "disabled");
        $("#channel").removeAttr("disabled");               
    }           
}

function save_settings() 
{
	var passphrase; 
	var protection;
	var passphrase_len;

	passphrase = $("#passphrase").val();
	protection = $("#protection").val();
	passphrase_len = passphrase.length;


	if((protection != "OPEN") && passphrase.match(/ /))
	{
		apprise("Passphrase should not contain space.");
		return false;
	}


	if(protection == "WEP")
	{
		if((passphrase_len != 5) && (passphrase_len != 13) && (passphrase_len != 16))
		{
			apprise("Invalid passphrase length (expected 5, 13, or 16 characters)");
			return false;
		}     
	}
	else if((protection == "WPA") || (protection == "WPA2"))
	{          
		if(passphrase_len < 7 || passphrase_len > 63)
		{
			apprise("Invalid passphrase length (expected 8..63 characters)");
			return false;
		}     
	}

	var data_to_save = jQuery('form').serialize();    
	data_to_save += "&cmd=save_wifiap_settings";

	send_ajax_req(data_to_save, save_wifiap_settings);
	return false;
}



$(document).ready(function(){

	hwmode_change();
	if($("#protection").val() == "OPEN")
		$("#passphrase").attr("disabled", "disabled");

	$("#protection").change(function()                             
			{
				if($(this).attr('value') == "OPEN")
					$("#passphrase").attr("disabled", "disabled");
				else
					$("#passphrase").removeAttr("disabled");
			});
});

