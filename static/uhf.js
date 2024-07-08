

var protocol_details;
var cur_protocol;
var user_freqs;
var is_freq_rx;

var col_per_row = 4

var user_freqs_need_update       = false;
var protocol_details_need_update = false;

var baud_rate_tbl =
{
    'GMSK':  {'25.0':'9600',  '20.0':'7500',  '12.5':'4800',  '6.25':'2400'},
    'DBPSK': {'25.0':'9600',  '20.0':'7500',  '12.5':'4800',  '6.25':'2400'},    
    'DQPSK': {'25.0':'19200', '20.0':'15000', '12.5':'9600',  '6.25':'4800'},    
    '4FSK':  {'25.0':'19200', '20.0':'15000', '12.5':'9600',  '6.25':'4800'},    
    'D8PSK': {'25.0':'28800', '20.0':'22500', '12.5':'14499', '6.25':'7200'},    
    'D16QAM':{'25.0':'38400', '20.0':'30000', '12.5':'19200', '6.25':'9600'}    
};
		 




function show_mdialog(content)
{	
	var doc_height = $(document).height();
	var doc_width = $(document).width();
	$("body").append("<div class=\"mdialog_overlay\" id=\"overlay\"></div>");    
    $(".mdialog_overlay").css("height", doc_height).css("width", doc_width).fadeIn(50); 
    $("body").append("<div class=\"mdialog\"></div>");
    $(".mdialog").css("left", ( $(window).width()  - $(".mdialog").width() ) / 2+$(window).scrollLeft() + "px");
    $(".mdialog").css("top",  ( $(window).height() - $(".mdialog").height() ) / 2 + "px");
    $(".mdialog").append("<div id=\"mdialog_inner\" class=\"mdialog_inner\"></div>");
    $(".mdialog_inner").append(content);   
    $(".mdialog").fadeIn(50);
}






function update_freqs_table_style()
{
    $("#user_freqs_tbl tr:even").addClass("even");
    $("#user_freqs_tbl tr:odd").addClass("odd");

    $("#user_freqs_tbl td").mouseover(function(){
        if($(this).hasClass('selected') == false)
            $(this).addClass("over");
    });

    $("#user_freqs_tbl td").mouseout(function(){
        if($(this).hasClass('selected') == false)
            $(this).removeClass("over");
    });

    $("#user_freqs_tbl td").click(function(){
        if($(this).html() != "") 
        {       
            $("#user_freqs_tbl .selected").removeClass("over selected");     
            $(this).addClass("selected");
        }
    });
}


function split_freq_val(freq)
{
    if(freq.search(/\d{9}/) == -1)
        return "";

    return freq.slice(0,3) + "." + freq.slice(3,6) + "." + freq.slice(6);
}


function comb_freq_val(freq)
{
    if(freq.search(/\d{3}\.\d{3}\.\d{3}/) == -1)
        return "";

    freq = freq.replace(".", "");
    freq = freq.replace(".", "");

    return freq;
}



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


function make_freq_table()
{
    var row;
    var tbl_cont;
    var i,tbl_index, num_items;

    tbl_cont = "<table id=\"user_freqs_tbl\" cellspacing=\"0\" cellpadding=\"0\">";
    num_items = user_freqs.length;
    tbl_index = 0;
    if(num_items) 
    {
        
        while(num_items) 
        {
            tbl_cont += "<tr>";
            if(num_items >= col_per_row) 
            {
                for(i = 0; i < col_per_row; i++) 
                    tbl_cont += "<td>" + split_freq_val(user_freqs[tbl_index++]) + "</td>";

                num_items -= col_per_row;
            }
            else
            {
                for(i = 0; i < col_per_row; i++) 
                    if(num_items) 
                    {
                        tbl_cont += "<td>" + split_freq_val(user_freqs[tbl_index++]) + "</td>";
                        num_items--;
                    }
                    else
                        tbl_cont += "<td></td>";
            }
            tbl_cont += "</tr>";
        }
    }
    else
    {
        tbl_cont += "<tr>";
        for(i = 0; i < col_per_row; i++) 
            tbl_cont += "<td></td>";
        tbl_cont += "</tr>";
    }

    tbl_cont += "</table>";
    return tbl_cont;    
}


function make_freqs_dlg_content()
{
    var content;
    
    content = "<b>Select or enter new frequency:</b><div><br /></div>";
    content += make_freq_table();
    content += "<div class=\"freq_buttons\">";
    content += "<button value=\"Add\" onClick=\"freqs_tbl_add()\">Add</button>";
    content += "<button value=\"Delete\" onClick=\"freqs_tbl_delete()\">Delete</button>";
    content += "<button value=\"Close\" onClick=\"freqs_tbl_close()\">Close</button>";
    content += "</div>";

    return content;
}




function freqs_tbl_add()
{  
    apprise("Enter new frequency", {'input':true}, function(r) 
    {
        if(r) 
        {
            if(r.search(/\d{9}/) == -1 && r.search(/\d{3}\.\d{3}\.\d{3}/) == -1)
            {
                apprise("Incorrect frequency format!");
            }
            else
            {   
                if(r.search(/\d{3}\.\d{3}\.\d{3}/) != -1)
                    r = comb_freq_val(r);
                
                var freq = parseInt(r);

                if(freq < min_uhf_freq || freq > max_uhf_freq)
                {
                    apprise("Incorrect frequency value!");
                    return;
                }
                
                 
                user_freqs.push(r);  
                var content = make_freqs_dlg_content();
    
                $("#mdialog_inner").empty();
                $("#mdialog_inner").append(content);
                update_freqs_table_style();
                user_freqs_need_update = true;
            }
        }            
    });      
}


function freqs_tbl_delete()
{
     var col = $("#user_freqs_tbl .selected").index();
     if(col == -1) 
         return;

     var cl_tr = $("#user_freqs_tbl .selected").closest('tr');
     var row = cl_tr.index();     
     var index = row * col_per_row + col;
     user_freqs.splice(index, 1);

     var content = make_freqs_dlg_content();

     $("#mdialog_inner").empty();
     $("#mdialog_inner").append(content);
     update_freqs_table_style();

     user_freqs_need_update = true;
}


function freqs_tbl_close()
{
    var col = $("#user_freqs_tbl .selected").index();
    if(col != -1) 
    {
        var cl_tr = $("#user_freqs_tbl .selected").closest('tr');
        var row = cl_tr.index();     
        var index = row * col_per_row + col;
        if (is_freq_rx)
            $("#freq_rx_val").html(split_freq_val(user_freqs[index]) + " Hz");
        else
            $("#freq_tx_val").html(split_freq_val(user_freqs[index]) + " Hz");
    }


    $(".mdialog_overlay").remove();
	$(".mdialog").remove();
}



function make_dropdown_list(sel_from, sel)
{
    var list = "";
    var i;
    for(i in sel_from)
        if(sel_from[i] == sel)
            list += "<option selected=\"selected\">" + sel_from[i] + "</option>";
        else
            list += "<option>" + sel_from[i] + "</option>";

    return list;
}


var mod_change_event = function()
{
    var mod = $("#mod_sel option:selected").val();
    var possible_rates = baud_rate_tbl[mod];
    var details = protocol_details[cur_protocol];
    var channel_spacing = details["channel_spacing"];

    details["modulation"]["value"] = mod;

    protocol_details_need_update = true;

    $("#link_rate").html(possible_rates[channel_spacing["value"]] + " bps");
}


var ch_spacing_change_event = function()
{
    var channel_spacing = $("#ch_spacing_sel option:selected").val();
    var details = protocol_details[cur_protocol];
    var modulation = details["modulation"];
    var possible_rates = baud_rate_tbl[modulation["value"]];

    details["channel_spacing"]["value"] = channel_spacing;

    protocol_details_need_update = true;

    $("#link_rate").html(possible_rates[channel_spacing] + " bps");
}


var fec_change_event = function()
{
    var details = protocol_details[cur_protocol];
    details["fec"]["value"] = $("input[name='fec']:checked").val();   
    protocol_details_need_update = true;
}


var scr_change_event = function()
{
    var details = protocol_details[cur_protocol];
    value = $("input[name='scrambling']:checked").val();
        if (value == "Disable")
            $("#scram_num").attr("disabled", true);
        else
            $("#scram_num").attr("disabled", false);
    details["scrambling"]["value"] = value
    protocol_details_need_update = true;
}


var scr_num_change_event = function()
{
    var details = protocol_details[cur_protocol];
    value = document.getElementById("scram_num").value;
    if (Number(value) !=NaN) {
        if ((Number(value) < 256)&&(Number(value) >= 0)) {
            details["scram_num"]["value"] = value;
        } else {
            apprise("Scrambling Seed must in range 0..255");
            document.getElementById("scram_num").value = details["scram_num"]["value"];
        }
    } else {
        apprise("Scrambling Seed must in range 0..255");
        document.getElementById("scram_num").value = details["scram_num"]["value"];
    }
    protocol_details_need_update = true;
}

var aux_change_event = function()
{
    var aux = $("#aux_sel option:selected").val();
    var details = protocol_details[cur_protocol];

    details["aux"]["value"] = aux;

    protocol_details_need_update = true;
}

var mode_change_event = function()
{
    var mode = $("#mode_sel option:selected").val();
    var details = protocol_details[cur_protocol];
    details["mode"]["value"] = mode;

    protocol_details_need_update = true;
}


var compartibility_change_event = function()
{
    var compartibility = $("#compartibility_sel option:selected").val();
    var details = protocol_details[cur_protocol];
    details["compartibility"]["value"] = compartibility;

    protocol_details_need_update = true;
}




function update_protocol_details(protocol_name)
{
    if(!protocol_details.hasOwnProperty(protocol_name))
        return;

    var details = protocol_details[protocol_name];

    if(details.hasOwnProperty("modulation"))
    {
        var modulation = details["modulation"];
        if(modulation.hasOwnProperty("select_from"))
            $("#modulation").html("<select id=\"mod_sel\" style=\"width: 80px\" onchange=\"mod_change_event()\">" + make_dropdown_list(modulation["select_from"], modulation["value"]) + "</select>");
        else
            $("#modulation").html(modulation["value"]);
    }

    if(details.hasOwnProperty("channel_spacing"))
    {
        var channel_spacing = details["channel_spacing"];
        if(channel_spacing.hasOwnProperty("select_from"))
            $("#channel_spacing").html("<select id=\"ch_spacing_sel\" style=\"width: 80px\" onchange=\"ch_spacing_change_event()\">" + make_dropdown_list(channel_spacing["select_from"], channel_spacing["value"]) + "</select>");
        else
            $("#channel_spacing").html(channel_spacing["value"]);
    }

    if(details.hasOwnProperty("fec"))
    {
        var fec = details["fec"];
        var tmp;

        if(fec["value"] == "Enable")
            tmp = "<div><input type=\"radio\" name=\"fec\" checked=\"checked\" value=\"Enable\" onchange=\"fec_change_event()\">Enable</input><input type=\"radio\" name=\"fec\" value=\"Disable\" onchange=\"fec_change_event()\">Disable</input></div>";
        else
            tmp = "<div><input type=\"radio\" name=\"fec\" value=\"Enable\" onchange=\"fec_change_event()\">Enable</input><input type=\"radio\" name=\"fec\" checked=\"checked\" value=\"Disable\" onchange=\"fec_change_event()\">Disable</input></div>";

        $("#fec").html(tmp);
    }

    if(details.hasOwnProperty("scrambling"))
    {
        var scrambling = details["scrambling"];
        var tmp;

        if(scrambling["value"] == "Enable")
            tmp = "<div><input type=\"radio\" name=\"scrambling\" value=\"Enable\" checked=\"checked\" onchange=\"scr_change_event()\">Enable</input><input type=\"radio\" name=\"scrambling\" value=\"Disable\" onchange=\"scr_change_event()\">Disable</input></div>";
        else
            tmp = "<div><input type=\"radio\" value=\"Enable\" name=\"scrambling\" onchange=\"scr_change_event()\">Enable</input><input type=\"radio\" name=\"scrambling\" checked=\"checked\" value=\"Disable\" onchange=\"scr_change_event()\">Disable</input></div>";

        $("#scrambling").html(tmp);
    }

    if(details.hasOwnProperty("scram_num"))
    {
        var scrambling = details["scrambling"];
        var scram_num = details["scram_num"];
        var tmp;
        if(scrambling["value"] == "Enable")
            tmp = "<div><input type=\"text\" id=\"scram_num\" style=\"width: 80px\" onchange=\"scr_num_change_event()\" value=" + scram_num["value"]+" ></input></div>";
        else
            tmp = "<div><input type=\"text\" id=\"scram_num\" style=\"width: 80px\" onchange=\"scr_num_change_event()\" value=" + scram_num["value"] + " disabled ></input></div>";

        $("#scram_num_val").html(tmp);
    }

    if(details.hasOwnProperty("channel_spacing") && details.hasOwnProperty("modulation"))
    {
        var possible_rates = baud_rate_tbl[modulation["value"]];
        $("#link_rate").html(possible_rates[channel_spacing["value"]] + " bps");
    }


    if(details.hasOwnProperty("aux"))
    {
        var aux = details["aux"];
        $("#aux_label").html("Aux:");

        if(aux.hasOwnProperty("select_from"))
            $("#aux_val").html("<select id=\"aux_sel\" style=\"width: 80px\" onchange=\"aux_change_event()\">" + make_dropdown_list(aux["select_from"], aux["value"]) + "</select>");
        else
            $("#aux_val").html(aux["value"]);
    }
    else
    {
        $("#aux_label").html("");
        $("#aux_val").html("");
    }

    if(details.hasOwnProperty("mode"))
    {
        var mode = details["mode"];
        $("#mode_label").html("Mode:");

        if(mode.hasOwnProperty("select_from"))
            $("#mode_val").html("<select id=\"mode_sel\" style=\"width: 120px\" onchange=\"mode_change_event()\">" + make_dropdown_list(mode["select_from"], mode["value"]) + "</select>");
        else
            $("#mode_val").html(mode["value"]);
    }
    else
    {
        $("#mode_label").html("");
        $("#mode_val").html("");
    }

    if(details.hasOwnProperty("compartibility"))
    {
        var compartibility = details["compartibility"];
        $("#compartibility_label").html("Compartibility:");

        if(compartibility.hasOwnProperty("select_from"))
            $("#compartibility_val").html("<select id=\"compartibility_sel\" style=\"width: 100px\" onchange=\"compartibility_change_event()\">" + make_dropdown_list(compartibility["select_from"], compartibility["value"]) + "</select>");
        else
            $("#compartibility_val").html(compartibility["value"]);
    }
    else
    {
        $("#compartibility_label").html("");
        $("#compartibility_val").html("");
    }

}


function set_freq_rx_event()
{
    is_freq_rx=true;
    show_mdialog(make_freqs_dlg_content());
    update_freqs_table_style();
}


function set_freq_tx_event()
{
    is_freq_rx=false;
    show_mdialog(make_freqs_dlg_content());
    update_freqs_table_style();
}


function protocol_change()
{
    var protocol = $("#protocol_sel option:selected").val();
    protocol= protocol.replace(" ", "_");
    cur_protocol = protocol;
    update_protocol_details(protocol);
}


function format_csign(inp) {
    var str = inp.value.replace(/[^A-Z0-9]/ig, "");
    str = str.toUpperCase();
    inp.value = str.slice(0, 11);
}


$(document).ready(function(){

    protocol_details = eval('(' + $("#protocol_details script").html() + ')');
    user_freqs       = eval('(' + $("#user_freqs script").html() + ')');

    protocol_change();
});





function ajax_err(jqXHR, textStatus, errorThrown)
{
    apprise_close_progress_box();
    apprise("Error during server connection!");
}


function send_ajax_req(req, callback_fn)   
{
    jQuery.ajax({type: "POST", data: req, dataTypeString: "json", success: callback_fn, error: ajax_err});  
}


function save_uhf_settings_resp(data) 
{
    var resp = eval('(' + data + ')');

    apprise_close_progress_box();
    $("#save_btn").removeAttr("disabled");  

    if(resp.err != "0") 
        apprise("Error: " + resp.errmsg);
    else
        apprise("Settings have been successfully save.");
}





function save_uhf_settings()
{
    var req = {cmd:"save_uhf_settings"};
    $("#save_btn").attr("disabled", "disabled");

    var freq_rx = $("#freq_rx_val").html();
    freq_rx = comb_freq_val(freq_rx.match(/\d{3}\.\d{3}\.\d{3}/)[0]);
    var freq_tx = $("#freq_tx_val").html();
    freq_tx = comb_freq_val(freq_tx.match(/\d{3}\.\d{3}\.\d{3}/)[0]);
    var protocol = $("#protocol_sel option:selected").val();
    protocol = protocol.replace(" ", "_");
    var power = $("#power_sel option:selected").val();
    power = power.slice(0,2);
    var csign = $("#csign").val();
    var fan_control = $("#fan_control_on").attr("checked")? "Enable" : "Disable";
    var snrm = $("#snrm_on").attr("checked")? "Enable" : "Disable";
    var antenna_detect = $("#antenna_detect_on").attr("checked")? "Enable" : "Disable";
    var status_info = $("#status_info_on").attr("checked")? "Enable" : "Disable";
	var tx_delay = document.getElementById("tx_delay").value;

    if(user_freqs_need_update)
        req.user_freqs = JSON.stringify(user_freqs);

    req.freq_rx        = freq_rx;
    req.freq_tx        = freq_tx;
    req.protocol       = protocol;
    req.power          = power;
    req.csign          = csign;
    req.snrm           = snrm;
    req.fan_control    = fan_control;
    req.antenna_detect = antenna_detect;
    req.status_info    = status_info;
    req.tx_delay       = tx_delay;

    if(protocol_details_need_update)
        req.protocol_details = JSON.stringify(protocol_details);

    apprise_progress_box("Settings applying takes some time. Please wait...");
    send_ajax_req(req, save_uhf_settings_resp);
    return false;
}

function uhf_form_reset(f) {
    f.form.reset();
    scr_change_event();
    protocol_change();
}

function new_profile()
{
	 wizard("Test");
}
