
function ajax_err(jqXHR, textStatus, errorThrown)
{
    apprise_close_progress_box();
    apprise("Error during server connection!");
}
function send_ajax_req(req, callback_fn) {$.ajax({type: "POST", data: req, dataTypeString: "json", success: callback_fn, error: ajax_err});}



function apply_power_management_settings_resp(data)
{
    var resp = eval('(' + data + ')');

    $("#apply_btn").removeAttr("disabled");
    apprise_close_progress_box();
    if(resp.err != "0")
        apprise("Error: " + resp.errmsg);
    else
        apprise("Settings have been successfully applied.");
}

function power_form_reset(f) {
    f.form.reset();
    check_gps_visibility();
}

function apply_power_management_settings()
{

    var settings_to_save = jQuery("form").serialize();
    settings_to_save += "&cmd=apply_power_management_settings";

    $("#apply_btn").attr("disabled", "disabled");
    apprise_progress_box("Settings applying takes some time. Please wait...");
    send_ajax_req(settings_to_save, apply_power_management_settings_resp);

    return false;
}

function check_gps_visibility() {
    var check = $("#en_gsm_id:checked").val();
    if (check == "Enable") {
        $("#en_gps_on_id").attr("disabled", false);
    } else {
        $("#en_gps_on_id").attr("disabled", true);
        jQuery("#en_gps_on_id").attr("checked", '');
        jQuery("#en_gps_off_id").attr("checked", 'checked');
    }
}



$(document).ready(function(){
    check_gps_visibility();
});

