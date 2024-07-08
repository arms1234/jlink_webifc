
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
    apprise("Error during server connection!");
}

function send_ajax_req(req, callback_fn)
{
    jQuery.ajax({type: "POST", data: req, dataTypeString: "json", success: callback_fn, error: ajax_err});
}

function save_dyndns_settings_resp(data)
{
    var resp = eval('(' + data + ')');

    $("#save_btn").removeAttr("disabled");

    if(resp.err != "0")
        apprise("Error: " + resp.errmsg);
    else
        apprise("Settings have been successfully saved.");
}

function save_dyndns_settings()
{
    $("#save_btn").attr("disabled", "disabled");

    var settings_to_save = jQuery("form").serialize();
    settings_to_save += "&cmd=save_dyndns_settings";
    send_ajax_req(settings_to_save, save_dyndns_settings_resp);
    return false;
}

$(document).ready(function(){});
