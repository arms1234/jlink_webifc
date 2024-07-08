function ajax_err(jqXHR, textStatus, errorThrown)
{
    apprise_close_progress_box();
    apprise("Error during server connection!");
}

function send_ajax_req(req, callback_fn)
{
    jQuery.ajax({type: "POST", data: req, dataTypeString: "json", success: callback_fn, error: ajax_err});
}

function save_data_router_settings_resp(data)
{
    var resp = eval('(' + data + ')');

    $("#save_btn").removeAttr("disabled");
    if(resp.err != "0")
        apprise("Error: " + resp.errmsg);
    else
        apprise("Settings have been successfully saved.");
}

function save_data_router_settings()
{
    ntrip_src = $("#ntrip_src").attr("checked")? "Enable" : "Disable";
    ntrip_ser_dst = $("#ntrip_ser_dst").attr("checked")? "Enable" : "Disable";
    ntrip_uhf_dst = $("#ntrip_uhf_dst").attr("checked")? "Enable" : "Disable";
    ntrip_bt_dst = $("#ntrip_bt_dst").attr("checked")? "Enable" : "Disable";
    tcp_src = $("#tcp_src").attr("checked")? "Enable" : "Disable";
    tcp_ser_dst = $("#tcp_ser_dst").attr("checked")? "Enable" : "Disable";
    tcp_uhf_dst = $("#tcp_uhf_dst").attr("checked")? "Enable" : "Disable";
    tcp_bt_dst = $("#tcp_bt_dst").attr("checked")? "Enable" : "Disable";
    uhf_src = $("#uhf_src").attr("checked")? "Enable" : "Disable";
    uhf_ser_dst = $("#uhf_ser_dst").attr("checked")? "Enable" : "Disable";
    uhf_bt_dst = $("#uhf_bt_dst").attr("checked")? "Enable" : "Disable";
    var tcpo_sel = document.getElementById("tcpo_sel").value;

    $("#save_btn").attr("disabled", "disabled");
    send_ajax_req({cmd:"save_data_router_settings", ntrip_src:ntrip_src, ntrip_uhf_dst:ntrip_uhf_dst, ntrip_ser_dst:ntrip_ser_dst, ntrip_bt_dst:ntrip_bt_dst, tcp_src:tcp_src, tcp_uhf_dst:tcp_uhf_dst, tcp_ser_dst:tcp_ser_dst, tcp_bt_dst:tcp_bt_dst, uhf_src:uhf_src,uhf_ser_dst:uhf_ser_dst, uhf_bt_dst:uhf_bt_dst, tcpo_src:tcpo_sel}, save_data_router_settings_resp);
    return false;
}

function uhf_src_() {
    var check = $("#uhf_src:checked").val();
    if (check == "on") {
        $("#uhf_ser_dst").attr("disabled", !uhf_en||!ser_en);
        $("#uhf_bt_dst").attr("disabled", !uhf_en||!bt_en);
        $("#uhf_soc_dst").attr("disabled", false);
        $("#ntrip_uhf_dst").attr("checked", false);
        $("#tcp_uhf_dst").attr("checked", false);
    } else {
        $("#uhf_ser_dst").attr("disabled", true);
        $("#uhf_bt_dst").attr("disabled", true);
        $("#uhf_soc_dst").attr("disabled", true);
        if (ser_en) $("#uhf_ser_dst").attr("checked", false);
        if (bt_en) $("#uhf_bt_dst").attr("checked", false);
    } 
}
function ntrip_src_() {
    var check = $("#ntrip_src:checked").val();
    if (check == "on") {
        $("#ntrip_bt_dst").attr("disabled", !bt_en);
        $("#ntrip_ser_dst").attr("disabled", !ser_en);
        $("#ntrip_uhf_dst").attr("disabled", !uhf_en);
    } else {
        $("#ntrip_ser_dst").attr("disabled", true);
        $("#ntrip_bt_dst").attr("disabled", true);
        $("#ntrip_uhf_dst").attr("disabled", true);
        $("#uhf_src").attr("disabled", false||!uhf_en);
        if (uhf_en) $("#ntrip_uhf_dst").attr("checked", false);
        if (ser_en) $("#ntrip_ser_dst").attr("checked", false);
        if (bt_en) $("#ntrip_bt_dst").attr("checked", false);
    }
}
function tcp_src_() {
    var check = $("#tcp_src:checked").val();
    if (check == "on") {
        $("#tcp_bt_dst").attr("disabled", !bt_en);
        $("#tcp_ser_dst").attr("disabled", !ser_en);
        $("#tcp_uhf_dst").attr("disabled", !uhf_en);
    } else {
        $("#tcp_ser_dst").attr("disabled", true);
        $("#tcp_bt_dst").attr("disabled", true);
        $("#tcp_uhf_dst").attr("disabled", true);
        $("#uhf_src").attr("disabled", false||!uhf_en);
        if (uhf_en) $("#tcp_uhf_dst").attr("checked", false);
        if (ser_en) $("#tcp_ser_dst").attr("checked", false);
        if (bt_en) $("#tcp_bt_dst").attr("checked", false);
    }
}
function ntrip_uhf_dest_() {
    var check = $("#ntrip_uhf_dst:checked").val();
    if (check == "on") {
        $("#uhf_src").attr("checked", false);
        $("#uhf_ser_dst").attr("checked", false);
        $("#uhf_bt_dst").attr("checked", false);
        $("#uhf_ser_dst").attr("disabled", true);
        $("#uhf_bt_dst").attr("disabled", true);
        $("#uhf_soc_dst").attr("disabled", true);
        $("#tcp_uhf_dst").attr("checked", false);
    }
}
function tcp_uhf_dest_() {
    var check = $("#tcp_uhf_dst:checked").val();
    if (check == "on") {
        $("#uhf_src").attr("checked", false);
        $("#uhf_ser_dst").attr("checked", false);
        $("#uhf_bt_dst").attr("checked", false);
        $("#uhf_ser_dst").attr("disabled", true);
        $("#uhf_bt_dst").attr("disabled", true);
        $("#uhf_soc_dst").attr("disabled", true);
        $("#ntrip_uhf_dst").attr("checked", false);
    }
}
function ntrip_ser_dest_() {
    var check = $("#ntrip_ser_dst:checked").val();
    if (check == "on") {
        $("#uhf_ser_dst").attr("checked", false);
        $("#tcp_ser_dst").attr("checked", false);
    }
}
function tcp_ser_dest_() {
    var check = $("#ntrip_ser_dst:checked").val();
    if (check == "on") {
        $("#uhf_ser_dst").attr("checked", false);
        $("#ntrip_ser_dst").attr("checked", false);
    }
}
function ntrip_bt_dest_() {
    var check = $("#ntrip_bt_dst:checked").val();
    if (check == "on") {
        $("#uhf_bt_dst").attr("checked", false);
        $("#tcp_bt_dst").attr("checked", false);
    }
}
function tcp_bt_dest_() {
    var check = $("#ntrip_bt_dst:checked").val();
    if (check == "on") {
        $("#uhf_bt_dst").attr("checked", false);
        $("#ntrip_bt_dst").attr("checked", false);
    }
}
function uhf_ser_dest_() {
    var check = $("#uhf_ser_dst:checked").val();
    if (check == "on") {
        $("#ntrip_ser_dst").attr("checked", false);
        $("#tcp_ser_dst").attr("checked", false);
    }
}
function uhf_bt_dest_() {
    var check = $("#uhf_bt_dst:checked").val();
    if (check == "on") {
        $("#ntrip_bt_dst").attr("checked", false);
        $("#tcp_bt_dst").attr("checked", false);
    }
}

function uhf_soc_dest_() {                                      
    var check = $("#uhf_bt_dst:checked").val();                
    if (check == "on") {                                       
        $("#ntrip_bt_dst").attr("checked", false);             
        $("#tcp_bt_dst").attr("checked", false);               
    }                                                          
}

function router_disable_state() {
    $("#ntrip_ser_dst").attr("disabled", !ser_en);
    $("#ntrip_uhf_dst").attr("disabled", !uhf_en);
    $("#ntrip_bt_dst").attr("disabled", !bt_en);
    $("#tcp_ser_dst").attr("disabled", !ser_en);
    $("#tcp_uhf_dst").attr("disabled", !uhf_en);
    $("#tcp_bt_dst").attr("disabled", !bt_en);
    $("#uhf_src").attr("disabled", !uhf_en);
    $("#uhf_ser_dst").attr("disabled", !uhf_en||!ser_en);
    $("#uhf_bt_dst").attr("disabled", !uhf_en||!bt_en);
}

function router_form_reset(f) {
    f.form.reset();
    router_disable_state();
    uhf_src_();
    ntrip_src_();
    tcp_src_();
}

$(document).ready(function(){
    router_disable_state();
    uhf_src_();
    ntrip_src_();                                                     
    tcp_src_();
});
