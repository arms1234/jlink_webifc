function ajax_err(jqXHR, textStatus, errorThrown)
{
    apprise_close_progress_box();
    apprise("Error during server connection!");
}


function send_ajax_req(req, callback_fn)
{
    $.ajax({type: "POST", data: req, dataTypeString: "json", success: callback_fn, error: ajax_err});
}

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

function destination_dialog_close() {
    $(".mdialog_overlay").remove();
	$(".mdialog").remove();
}


function destination_select(inp) {
    $("#bt_dest").val(inp.value);
    $(".mdialog_overlay").remove();
    $(".mdialog").remove();
}


function save_bluetooth_settings_resp(data)
{
    var resp = eval('(' + data + ')');

    $("#save_btn").removeAttr("disabled");
    apprise_close_progress_box();
    if(resp.err != "0")
        apprise("Error: " + resp.errmsg);
    else
        apprise("Bluetooth settings have been successfully saved.");
}

function bt_mode_change() {
    var check = $("#bt_mode_master:checked").val();
    if (check == "on") {
        $("#discoverable_on").attr("disabled", "disabled");
        $("#discoverable_off").attr("disabled", "disabled");
        $("#bt_dest").removeAttr("disabled");
        $("#bt_scan").removeAttr("disabled");
    } else {
        $("#discoverable_on").removeAttr("disabled");
        $("#discoverable_off").removeAttr("disabled");
        $("#bt_dest").attr("disabled", "disabled");
        $("#bt_scan").attr("disabled", "disabled");
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


var bt_scan_devices_cb =function (data) {
    var resp = eval('(' + data + ')');
    apprise_close_progress_box();
    $("#bt_scan").removeAttr("disabled");

    if(resp.err == "0")
    {
        var result = resp.bt_scan_result;
        if(result != "")
        {
            var content;
            result = result.replace(/\r\n/g, "\t");
            result = result.split("\t");
            content = "<b>Select Destination BT Device Address:</b><div><br /></div>";
            content += "<table style=\"width:340px\" cellspacing=\"0\" cellpadding=\"0\">"
            content += "<tr>"
            content += "<td><b>Name</b></td>"
            content += "<td><b>Address</b></td>"
            content += "</tr>"
            for (i = 1; i < result.length - 1; i+=2) {
                content += "<tr>"
                content += "<td>" + result[i+1] + "</td>"
                content += "<td><input name=\"bt_scan_result\" onClick=\"destination_select(this)\" value=\"" + result[i] + "\" /></td>"
                content += "</tr>"
            }
            content += "</table>"
            content += "<div class=\"scan_buttons\">";
            content += "<button value=\"Close\" onClick=\"destination_dialog_close()\">Close</button>";
            content += "</div>";
            show_mdialog(content);
        } else {
            apprise("There is no any discoverable devices");
        }
    }
    else
    {
        apprise("Can not get response");
    }
}



function bt_scan_devices(){

    $("#bt_scan").attr("disabled", "disabled");
    apprise_progress_box("Scanning destination devices. Please wait...");
    send_ajax_req({cmd:"bt_scan_devices"}, bt_scan_devices_cb);
}

function bt_form_reset(f) {
    f.form.reset();
    bt_mode_change();
}

function save_bluetooth_settings() {
    var bt_name = $("#bt_name").val();
    var bt_pin = $("#bt_pin").val();
    var bt_dest = $("#bt_dest").val();
    var bt_mode = $("#bt_mode_master").attr("checked")? "Master" : "Slave";
    var bt_discoverable = $("#discoverable_on").attr("checked")? "Enable" : "Disable";

    if(bt_name.match(/ /))
    {
        apprise("Device name should not contain space.");
        return false;
    }


    if(bt_pin.match(/ /))
    {
        apprise("PIN code should not contain space.");
        return false;
    }

    for(i = 0; i < bt_pin.length; i++)
    {
       var ch = bt_pin.charAt(i);
       if(ch < '0' || ch > '9') 
       {
           apprise("PIN code has illegal character(s)");
           return false;
       }
    }

    var bt_dest_regexp=new RegExp("^([0-9a-fA-F][0-9a-fA-F]:){5}([0-9a-fA-F][0-9a-fA-F])$");
    if (bt_dest_regexp.test(bt_dest) == false) {
        apprise("Destination address: " + bt_dest + " has illegal length");
        $("#bt_dest").val("");
        return false;
    }


    $("#save_btn").attr("disabled", "disabled");
    apprise_progress_box("Settings applying takes some time. Please wait...");
    send_ajax_req({cmd:"save_bluetooth_settings", bt_name:bt_name, bt_pin:bt_pin, bt_dest:bt_dest, bt_mode:bt_mode, bt_discoverable:bt_discoverable}, save_bluetooth_settings_resp);
    return false;
}



$(document).ready(function(){
    bt_mode_change();
});
