

var region_details;
var cur_region;
var region_details_need_update = false;




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
    var details = region_details[cur_region];
    details["modulation"]["value"] = mod;

    region_details_need_update = true;
}

var channel_spacing_change_event = function()
{
    var channel_spacing = $("#channel_spacing_sel option:selected").val();
    var details = region_details[cur_region];
    details["channel_spacing"]["value"] = channel_spacing;
    region_details_need_update = true;
}



var rule_change_event = function()
{
    var f_rule = $("#f_rule_sel option:selected").val();
    var details = region_details[cur_region];
    details["f_rule"]["value"] = f_rule;
    region_details_need_update = true;
}



var redundancy_change_event = function()
{
	var redundancy = $("#redundancy_sel option:selected").val();
    var details = region_details[cur_region];
    details["redundancy"]["value"] = redundancy;
    region_details_need_update = true;
}


var freq_tx_change_event = function()
{
    var details = region_details[cur_region];
    value = document.getElementById("freq_tx_val").value;
	if (cur_region == "EU"){
        var min_freq = 868000000;
        var max_freq = 870000000;
	} else {
		var min_freq = 902000000;
        var max_freq = 928000000;
	}
    if (Number(value) !=NaN) {
		if ((Number(value) <= max_freq)&&(Number(value) >= min_freq)) {
            details["freq_tx"]["value"] = value;
        } else {
            apprise("TX Frequency should be in range " + min_freq.toString() + ".." + max_freq.toString());
            document.getElementById("freq_tx_val").value = details["freq_tx"]["value"];
        }
    } else {
        apprise("TX Frequency should be in range " + min_freq.toString() + ".." + max_freq.toString());
        document.getElementById("freq_tx_val").value = details["freq_tx"]["value"];
    }
    region_details_need_update = true;
}



var freq_rx_change_event = function()
{
    var details = region_details[cur_region];
    value = document.getElementById("freq_rx_val").value;
	if (cur_region == "EU"){
        var min_freq = 868000000;
        var max_freq = 870000000;
	} else {
		var min_freq = 902000000;
        var max_freq = 928000000;
	}
    if (Number(value) !=NaN) {
        if ((Number(value) <= max_freq)&&(Number(value) >= min_freq)) {
            details["freq_rx"]["value"] = value;
        } else {
            apprise("RX Frequency should be in range " + min_freq.toString() + ".." + max_freq.toString());
            document.getElementById("freq_rx_val").value = details["freq_rx"]["value"];
        }
    } else {
        apprise("RX Frequency should be in range " + min_freq.toString() + ".." + max_freq.toString());
        document.getElementById("freq_rx_val").value = details["freq_rx"]["value"];
    }
    region_details_need_update = true;
}




function update_region_details(region_name)
{
    if(!region_details.hasOwnProperty(region_name))
        return;

    var details = region_details[region_name];

    if(details.hasOwnProperty("modulation"))
    {
        var modulation = details["modulation"];
        if(modulation.hasOwnProperty("select_from"))
            $("#modulation").html("<select id=\"mod_sel\" style=\"width: 80px\" onchange=\"mod_change_event()\">" + make_dropdown_list(modulation["select_from"], modulation["value"]) + "</select>");
        else
            $("#modulation").html(modulation["value"]);
    }

	if(details.hasOwnProperty("freq_tx"))
    {
		var freq_tx = details["freq_tx"];
        $("#freq_tx").html("<div><input type=\"text\" id=\"freq_tx_val\" style=\"width: 80px\" onchange=\"freq_tx_change_event()\" value=" + freq_tx["value"]+" ></input></div>");
    }

	if(details.hasOwnProperty("freq_rx"))
    {
		var freq_rx = details["freq_rx"];
        $("#freq_rx").html("<div><input type=\"text\" id=\"freq_rx_val\" style=\"width: 80px\" onchange=\"freq_rx_change_event()\" value=" + freq_rx["value"]+" ></input></div>");
    }

    if(details.hasOwnProperty("channel_spacing"))
    {
        var channel_spacing = details["channel_spacing"];
		$("#channel_spacing_label").html("Channel Spacing:");
        if(channel_spacing.hasOwnProperty("select_from"))
            $("#channel_spacing").html("<select id=\"channel_spacing_sel\" style=\"width: 80px\" onchange=\"channel_spacing_change_event()\">" + make_dropdown_list(channel_spacing["select_from"], channel_spacing["value"]) + "</select>");
        else
            $("#channel_spacing").html(channel_spacing["value"]);
    }
    else
    {
        $("#channel_spacing_label").html("");
        $("#channel_spacing").html("");
    }

	if(details.hasOwnProperty("f_rule"))
    {
        var f_rule = details["f_rule"];
		$("#f_rule_label").html("Frequency Rule:");
        if(f_rule.hasOwnProperty("select_from"))
            $("#f_rule").html("<select id=\"f_rule_sel\" style=\"width: 80px\" onchange=\"rule_change_event()\">" + make_dropdown_list(f_rule["select_from"], f_rule["value"]) + "</select>");
        else
            $("#f_rule").html(f_rule["value"]);
    }
    else
    {
        $("#f_rule_label").html("");
        $("#f_rule").html("");
    }

	if(details.hasOwnProperty("redundancy"))
    {
        var redundancy = details["redundancy"];
		$("#redundancy_label").html("Redundancy:");
        if(redundancy.hasOwnProperty("select_from"))
            $("#redundancy").html("<select id=\"redundancy_sel\" style=\"width: 80px\" onchange=\"redundancy_change_event()\">" + make_dropdown_list(redundancy["select_from"], redundancy["value"]) + "</select>");
        else
            $("#redundancy").html(redundancy["value"]);
    }
    else
    {
        $("#redundancy_label").html("");
        $("#redundancy").html("");
    }



}


function region_change()
{
    var region = $("#region_sel option:selected").val();
    region= region.replace(" ", "_");
    cur_region = region;
    update_region_details(region);
}


$(document).ready(function(){

    region_details = eval('(' + $("#region_details script").html() + ')');

    region_change();
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

    var region = $("#region_sel option:selected").val();
    region = region.replace(" ", "_");
    var protocol = $("#protocol_sel option:selected").val();
    protocol = protocol.replace(" ", "_");
    var repeater = $("#repeater_sel option:selected").val();
    repeater = repeater.replace(" ", "_");
    var power = $("#power_sel option:selected").val();
    power = power.slice(0,2);
    var fec = $("#fec_on").attr("checked")? "Enable" : "Disable";
    var scrambling = $("#scrambling_on").attr("checked")? "Enable" : "Disable";
    var fan_control = $("#fan_control_on").attr("checked")? "Enable" : "Disable";
	var status_info = $("#status_info_on").attr("checked")? "Enable" : "Disable";

    req.region      = region;
    req.protocol    = protocol;
	req.repeater    = repeater;
    req.power       = power;
	req.fec         = fec;
	req.scrambling  = scrambling;
    req.fan_control = fan_control;
	req.status_info = status_info;

    if(region_details_need_update)
        req.region_details = JSON.stringify(region_details);

    apprise_progress_box("Settings applying takes some time. Please wait...");
    send_ajax_req(req, save_uhf_settings_resp);
    return false;
}

function uhf_form_reset(f) {
    f.form.reset();
	freq_tx_change_event()
	freq_rx_change_event()
    region_change();
}

function new_profile()
{
	 wizard("Test");
}
