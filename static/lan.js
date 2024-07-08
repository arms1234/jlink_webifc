function ajax_err(jqXHR, textStatus, errorThrown)
{
    apprise_close_progress_box();
    apprise("Error during server connection!");
}


function send_ajax_req(req, callback_fn)   
{
    $.ajax({type: "POST", data: req, dataTypeString: "json", success: callback_fn, error: ajax_err});  
}



function save_lan_settings_resp(data) 
{
    var resp = eval('(' + data + ')');

    $("#save_btn").removeAttr("disabled");     
    if(resp.err != "0") 
        apprise("Error: " + resp.errmsg);
    else
        apprise("LAN settings have been successfully saved.");                               
}



function save_lan_settings()
{
 
    if($("#addr_alloc_dhcp").attr("checked"))
    {
        $("#save_btn").attr("disabled", "disabled");
        send_ajax_req({cmd:"save_lan_settings", addr_alloc:"DHCP"}, save_lan_settings_resp);   
        return false;
    }

    var ip_addr = read_from_fields("ip_addr", 4);
    var netmask = read_from_fields("netmask", 4); 
    var gateway = read_from_fields("gateway", 4); 
    var dns1    = read_from_fields("dns1", 4); 
    var dns2    = read_from_fields("dns2", 4); 

    if(check_ip(ip_addr, "IP address") == false)
        return false;

    if(check_netmask(netmask, "Subnet Mask ") == false)
        return false;

    if(check_gateway(gateway, ip_addr, netmask) == false)
        return false;

    $("#save_btn").attr("disabled", "disabled");
    send_ajax_req({cmd:"save_lan_settings", addr_alloc:"STATIC", ip_addr:addr_to_str(ip_addr), netmask:addr_to_str(netmask), 
                                    gateway:addr_to_str(gateway), dns1:addr_to_str(dns1), dns2:addr_to_str(dns2)}, save_lan_settings_resp);

    return false;
}

function lan_mode_change() {
        var check = $("#addr_alloc_dhcp").attr("checked");
        if (check)
            $("#static_net_settings input").attr('disabled', 'disabled');
        else
            $("#static_net_settings input").removeAttr("disabled");
}


function lan_form_reset(f) {
    f.form.reset();
    lan_mode_change();
}


$(document).ready(function(){
    lan_mode_change();
});


