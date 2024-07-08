function ajax_err(jqXHR, textStatus, errorThrown)
{
    apprise_close_progress_box();
    apprise("Error during server connection!");
}


function send_ajax_req(req, callback_fn)   
{
    jQuery.ajax({type: "POST", data: req, dataTypeString: "json", success: callback_fn, error: ajax_err});  
}


function cmd_resp(data) 
{
    var resp = eval('(' + data + ')');

    if(resp.err != "0") 
        apprise("Error: " + resp.errmsg);
    else
        apprise("Command have been successfully applied.");                               
}


function switch_off_device()
{
    apprise("Switch Off command have been successfully applied. Please wait...");                               
    send_ajax_req({cmd:"switch_off_device"}, cmd_resp);
    return false;
}


function reboot_device()
{
    apprise("Reboot command have been successfully applied. Please wait...");                               
    send_ajax_req({cmd:"reboot_device"}, cmd_resp);
    return false;
}


function def_cfg()
{
    apprise("Default command have been successfully applied. Rebooting  device");
    send_ajax_req({cmd:"def_cfg"}, cmd_resp);
    return false;
}



function save_admin_settings()
{
    var login;
    var pwd, pwd_conf;

    login = $("#admin_login").val();

    if(login == "" || login.match(/ /))
    {
        apprise("Login should not consist space or be empty.");
        return false;
    }

    pwd      = $("#admin_pwd").val();
    pwd_conf = $("#admin_pwd_conf").val();

    if(pwd != pwd_conf)
    {
        apprise("Password confirmation is not matched.");
        return false;
    }

    if(pwd == "" || pwd.match(/ /))
    {
        apprise("Password should not consist space or be empty.");
        return false;
    }

    send_ajax_req({cmd:"save_admin_settings", username:login, password:pwd}, cmd_resp);
    return false;
}



      
