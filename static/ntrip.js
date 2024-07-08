
var cas_ln;
var net_ln;
var str_ln;
var cas=[];
var net=[];
var str=[];

var cur_show;
var cur_mpoint;

function is_digit(d)
{
    for(i = 0; i < d.value.length; i++)
    {
                ch = d.value.charAt(i);
                if(ch < '0' || ch > '9')
                {
                        apprise('This field have illegal characters, must be [ 0 - 9 ]');
                        d.value = d.defaultValue;
                        return false;
                }
        }

        return true;
}



function check_range(d, min, max, field_name)
{
        if (is_digit(d)) {

                dd = parseInt(d.value, 10);
		if (!isNaN(dd)) {
                	if ( !(dd <= max && dd >= min) )
                	{
                        	apprise(field_name +' value is out of range ['+ min + ' - ' + max +']');
                        	d.value = d.defaultValue;
                	} else {
                        	d.value = dd;
                	}
		}
        }
}


function ajax_err(jqXHR, textStatus, errorThrown)
{
    apprise_close_progress_box();
    $("#update_btn").removeAttr("disabled");     
    $("#mpoint_sel option").remove();
    apprise("Error during server connection!");
}


function send_ajax_req(req, callback_fn)   
{
    jQuery.ajax({type: "POST", data: req, dataTypeString: "json", success: callback_fn, error: ajax_err});  
}

function nmea_change(chkbox)
{

    if(chkbox.checked)
    {
        document.getElementById("lat").disabled=false;
        document.getElementById("lng").disabled=false;    
    }
    else
    {
        document.getElementById("lat").disabled=true;
        document.getElementById("lng").disabled=true;        
    }
}



function on_prev()
{
    if(cur_show > 0) 
        cur_show--;
    else
        cur_show = str_ln - 1;

    print_str_item(cur_show);
}

function on_next()
{
    if(cur_show < str_ln - 1) 
        cur_show++;
    else
        cur_show = 0;

    print_str_item(cur_show);
}



function print_str_item(n)
{
    if(n >= str_ln) 
        return;

    var tmp_str;
    var item = str[n];
    var i;
    var network;

    $("#stream div:last-child").remove();       
    $("#stream").append("<div  style=\"font-weight:normal;\">" + item[2] + ",   Stream No:  " + (cur_show + 1) + " of " + str_ln + "</div>");
    $("#src_pars .setting div:last-child").remove();       
    $("#mp_0").append("<div>" + item[1] + "</div>");
    switch(item[16]) 
    {
        case "N": tmp_str = "None";   break;
        case "B": tmp_str = "Basic";  break;
        case "D": tmp_str = "Digest"; break;
    }
    $("#mp_1").append("<div>" + tmp_str + "</div>");
    $("#mp_2").append("<div>" + item[3] + "</div>");
    $("#mp_3").append("<div>" + item[4] + "</div>");
    switch(item[5]) 
    {
        case "0": tmp_str = "No";        break;
        case "1": tmp_str = "L1";        break;
        case "2": tmp_str = "L1 and L2"; break;
    }
    $("#mp_4").append("<div>"  + tmp_str  + "</div>");
    $("#mp_5").append("<div>"  + (item[11]=="0"?"No":"Yes") + "</div>");
    $("#mp_6").append("<div>"  + item[6]  + "</div>");
    $("#mp_7").append("<div>"  + item[8]  + "</div>");
    $("#mp_8").append("<div>"  + item[9]  + "</div>");
    $("#mp_9").append("<div>"  + item[10] + "</div>");
    $("#mp_10").append("<div>" + item[13] + "</div>");
    $("#mp_11").append("<div>" + (item[12]=="0"?"Single base":"Network") + "</div>");
    $("#mp_12").append("<div>" + item[14] + "</div>");
    $("#mp_13").append("<div>" + item[17] + "</div>");
    $("#mp_14").append("<div>" + (item[16]=="N"?"No":"Yes") + "</div>");
    $("#mp_15").append("<div>" + item[item.length - 1] + "</div>");

    network = item[7]; 
    $("#mp_16").append("<div style=\"font-weight:normal;\">" + network + "</div>");

    for(i = 0; i < net_ln; i++)
        if(net[i][1] == network) 
            break;

    if(i < net_ln) 
    {
        $("#mp_17").append("<div>" + net[i][2] + "</div>");
        $("#mp_18").append("<div>" + net[i][5] + "</div>");
        $("#mp_19").append("<div>" + net[i][7] + "</div>");        
    }
    else
    {
        $("#mp_17").append("<div>" + "unknown" + "</div>");
        $("#mp_18").append("<div>" + "unknown" + "</div>");
        $("#mp_19").append("<div>" + "unknown" + "</div>");        
    }
}


function update_mpoint()
{
    var i;
    $("#mpoint_sel option").remove();   

    for(i = 0; i < str_ln; i++) 
        $("#mpoint_sel").append("<option " + ((i == cur_mpoint)?"selected=\"selected\"":"") + ">"+str[i][1]+"/"+str[i][3]+"/"+str[i][6] +"</option>");
    
}


function on_select()
{
    cur_mpoint = cur_show;
    update_mpoint();
}


function parse_src_table(stbl)
{
    var item;
    var i;


    cas_ln = 0;
    net_ln = 0;
    str_ln = 0;

    cas = [];
    net = [];
    str = [];    
    for(i = 0; i < stbl.length; i++) 
    {
        item = stbl[i];
        switch(item[0]) 
        {
            case "CAS": cas.push(item); cas_ln++; break;
            case "NET": net.push(item); net_ln++; break;
            case "STR": str.push(item); str_ln++; break;
        }
    }    
}


var get_src_tbl = function(data)
{
    var resp = eval('(' + data + ')');
 
    apprise_close_progress_box();

    $("#update_btn").removeAttr("disabled");     
   
    if(resp.err != "0") 
    {
       if(resp.err == "2")
       {
           $("#stream div:last-child").remove();       
           $("#stream").append("<div  style=\"font-weight:normal; color:red;\">" + resp.errmsg + "</div>");
       }
       else       
           apprise(resp.errmsg);       
    }
    else  
    {
        cur_show = 0;
        cur_mpoint = 0;
        parse_src_table(resp.stbl);
        print_str_item(cur_show);
        update_mpoint();                    
    }
}

function mpoint_sel_change()
{
    cur_show = document.getElementById("mpoint_sel").selectedIndex;
    print_str_item(cur_show);
}


function save_ntrip_settings_resp(data) 
{
    var resp = eval('(' + data + ')');

    $("#save_btn").removeAttr("disabled");     

    if(resp.err != "0") 
        apprise("Error: " + resp.errmsg);
    else
        apprise("Settings have been successfully saved.");
                                
}

function save_ntrip_settings() 
{ 
    $("#save_btn").attr("disabled", "disabled");
       
/*    if($("#serv_name").val() == "")
    {
        apprise("Server is not defined!");
        return false;
    }*/

    if($("#user").val() != "" && $("#pwd").val() == "")
    {
        apprise("Password is not defined!");
        return false;
    }

    if($("#user").val() == "" && $("#pwd").val() != "")
    {
        apprise("User is not defined!");
        return false;
    }


    var nmeagga = "Disable";
    if(str_ln != 0)
    {
		if (!Number.isNaN(cur_mpoint)) {
			var cur_mp_item = str[cur_mpoint];
			nmeagga = (cur_mp_item[11] == "0")?"Disable":"Enable";
		}
    }

    var nmeagga_timeout = $("#nmeagga_timeout_sel option:selected").val();
    nmeagga_timeout = nmeagga_timeout.split(" ")[0];


/*
    if($("#nmeagga").attr("checked"))
    {
        if($("#lat").val() == "")
        {
            apprise("Latitude is not defined!");
            return false;
        }
        if($("#lng").val() == "")
        {
            apprise("Longitude is not defined!");
            return false;
        }
    }
*/

    var mpoint_sel = document.getElementById("mpoint_sel").selectedIndex;
	 if(mpoint_sel == -1)
	     mpoint_sel = 0;

    var data_to_save = $('form').serialize();    
    data_to_save += "&cmd=save_ntrip_settings" + "&mpoint_sel=" + mpoint_sel + "&nmeagga=" + nmeagga + "&nmeagga_timeout=" + nmeagga_timeout; 
    send_ajax_req(data_to_save, save_ntrip_settings_resp);
    return false;
}


function on_update() 
{
    $("#update_btn").attr("disabled", "disabled");
    apprise_progress_box("Downloading Source Information. Please wait...");
    send_ajax_req({cmd:"get_src_tbl"}, get_src_tbl);
}



$(document).ready(function(){

    //jQuery(".setting:last").remove();  doesn't work
    //jQuery(".setting div:last-child").remove();


    cur_mpoint = parseInt($("#mpoint").val());

    cur_show = cur_mpoint;
	 str_ln = 0;


    var src_table_str = $("#src_table script").html();
    if(src_table_str == "" || src_table_str == "[]")
    {
         $("#stream div:last-child").remove();       
         $("#stream").append("<div  style=\"font-weight:normal; color:red;\">There is no actual source table!</div>");
    }
    else
    {
        var src_table = eval('(' + src_table_str + ')');
        parse_src_table(src_table);
        print_str_item(cur_show);
        update_mpoint();                    
    }
});


function check_input(d, name)
{
    var dd = d.value.replace(/^\s*/,"");
    var ddd = dd.replace(/\s*$/,"");

    d.value = ddd;

	for(i = 0; i < d.value.length; i++)
    {
        ch = d.value.charAt(i);
		if(ch == ' ') 
        {
			apprise(name +' is not allow space!');
			d.value = d.defaultValue;	
			return;
		}
	}
}
