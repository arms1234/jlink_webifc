
var cur_fw_ver;
var avl_fw_ver;
var fw__type;
var fw_sha256sum_s;
var fw_fname_s;
var fw_size_s;
var server_ip_addr;
var uhf_flashing;
var uhf_preparing;
var uhf_loading;


function enable_button()
{
    document.getElementById("krnl_upgrd_id").disabled = "";
    document.getElementById("fs_upgrd_id").disabled   = "";   
}

function ajax_err(jqXHR, textStatus, errorThrown)
{
    apprise_close_progress_box();
    apprise("Error during server connection!");
    enable_button();
}

function upgrade_error(errmsg)
{
    apprise_close_progress_box();
    apprise(errmsg);
    enable_button();
}

function update_progress_bar(progress)
{
     pb  = "<div style=\"text-align:center;\">Downloading...</div>";
     pb += "<div style=\"text-align:right;font-weight:bold;\">";
     pb += progress;
     pb += "%</div></span><div id=\"progress\" style=\"border: 1px solid black;\"> <div style=\"background-color:#1aa; width:";
     pb += progress;
     pb += "%\">&nbsp;</div> </div>";
     apprise_progress_box_set_text(pb);
}


function send_ajax_req(req, callback_fn)   
{
    req.sub_title = "fwupgrade";
    jQuery.ajax({type: "POST", data: req, dataTypeString: "json", success: callback_fn, error: ajax_err, });  
}


var fw_upgrade_stage_4 = function(data)
{
    var resp = eval('(' + data + ')'); 

    if(resp.err != "0") 
        upgrade_error("Error: " + resp.errmsg);     
    else   
    {
        apprise_close_progress_box();
        apprise("Please reboot IP Radio.");
        enable_button();
    }
}

var fw_upgrade_stage_3 = function(data)
{
    var resp = eval('(' + data + ')'); 

    if(resp.err != "0") 
        upgrade_error("Error: " + resp.errmsg);     
    else   
    {
        if(resp.status == "download_done") 
        {
             apprise_progress_box_set_text("Saving firmware...");
             send_ajax_req({cmd:"save_fw", fver:avl_fw_ver ,fname:fw_fname_s, fsize:fw_size_s, fsha256sum:fw_sha256sum_s, fw_type:fw__type}, fw_upgrade_stage_4);
             //apprise_close_progress_box();
             //apprise("Done");
             //enable_button();
        }
        else
        {
            update_progress_bar(resp.progress);          
            setTimeout( "send_ajax_req({cmd:\"check_fw_downloading\"}, fw_upgrade_stage_3)", 1000 );
        }
    }
}


var fw_upgrade_stage_2 = function(data)
{
    var resp = eval('(' + data + ')'); 
   
    if(resp.err != "0") 
        upgrade_error("Error: " + resp.errmsg);     
    else  
    {        
        update_progress_bar("0");
        send_ajax_req({cmd:"check_fw_downloading"}, fw_upgrade_stage_3);
    }
}


var fw_upgrade_stage_1 = function(data)
{
    var resp = eval('(' + data + ')'); 

    if(resp.err != "0") 
    {
        upgrade_error("Error: " + resp.errmsg);     
    }
    else
    {   
        apprise_close_progress_box();
        var str  = "<pre style=\"text-align:left;\">" 
            
        if(fw__type == "krnl") 
        {            
            if(resp.hasOwnProperty("kernel_fname") && resp.hasOwnProperty("kernel_size") && resp.hasOwnProperty("kernel_sha256sum"))                          
            {
                fw_fname_s     = resp["kernel_fname"];       
                fw_size_s      = resp["kernel_size"];       
                fw_sha256sum_s = resp["kernel_sha256sum"];       
            }
            else
            {
                upgrade_error("Firmware's parametrs is not defined");
                return;
            }                                                

            if(resp.hasOwnProperty("cur_fw_ver"))                          
                cur_fw_ver = resp.cur_fw_ver;       
            if(resp.hasOwnProperty("kernel_ver"))                          
                avl_fw_ver = resp.kernel_ver;


            str += "Current firmware version:<br/>--Kernel:       " + cur_fw_ver + "<br/><br/>"
            str += "Available firmware version:<br/>--Kernel:       " + avl_fw_ver + "<br/><br/>"
        }
        else if(fw__type == "fs") 
        {
            if(resp.hasOwnProperty("fs_fname") && resp.hasOwnProperty("fs_size") && resp.hasOwnProperty("fs_sha256sum"))                          
            {
                fw_fname_s     = resp["fs_fname"];       
                fw_size_s      = resp["fs_size"];       
                fw_sha256sum_s = resp["fs_sha256sum"];       
            }
            else
            {
                upgrade_error("Firmware's parametrs isn't defined");
                return;
            }                                                

            if(resp.hasOwnProperty("cur_fw_ver"))                          
                cur_fw_ver = resp.cur_fw_ver;                   
            if(resp.hasOwnProperty("fs_ver"))                          
                avl_fw_ver = resp.fs_ver;       

            str += "Current firmware version:<br/>--File system:  " + cur_fw_ver + "<br/><br/>"
            str += "Available firmware version:<br/>--File system:  " + avl_fw_ver + "<br/><br/>"
        }


        if(fw_fname_s == "" || fw_size_s == "" || fw_sha256sum_s == "") 
        {
            upgrade_error("Firmware's parametrs is not defined correctly");
            return;
        }
                  


//      str += "Current firmware version:<br/>--Kernel:       " + cur_fw_ver + "<br/>--File system:  " + cur_fs_ver + "<br/><br />"
//      str += "Available firmware version:<br/>--Kernel:       " + avl_fw_ver + "<br/>--File system:  " + avl_fs_ver + "<br/><br />"
        str += "Do you want to continue upgrading?<br/>"
        str += "</pre>"


        apprise(str, {'verify':true}, function(r)   
        {
            if(r)
            {   
                apprise_progress_box("Please wait..."); 
                send_ajax_req({cmd:"download_fw", ip_addr:server_ip_addr, fname:fw_fname_s, fsize:fw_size_s, fsha256sum:fw_sha256sum_s}, fw_upgrade_stage_2);  
            }
            else
                enable_button();
        });
    }
}


function fw_upgrade(fwtype) 
{
    document.getElementById("krnl_upgrd_id").disabled="dis";
    document.getElementById("fs_upgrd_id").disabled="dis";

    
    server_ip_addr  = $(fw_server_ip_0).val() + ".";
    server_ip_addr += $(fw_server_ip_1).val() + ".";
    server_ip_addr += $(fw_server_ip_2).val() + ".";
    server_ip_addr += $(fw_server_ip_3).val();

    fw__type = fwtype;

    cur_fw_ver = "unknown";
    avl_fw_ver = "unknown";

    apprise_progress_box("Checking firmware availability. Please wait...");
    send_ajax_req({cmd:"check_fw_avl", ip_addr:server_ip_addr, fw_type:fwtype}, fw_upgrade_stage_1);
   
    return false;    
}


var uhf_upgrade_get_status_cb = function(data)
{
    var resp = eval('(' + data + ')'); 

    if(resp.err != "0") 
    {
        apprise_close_progress_box();   
        apprise("Error: " + resp.errmsg);
        $("#uhf_upgrade_btn").removeAttr("disabled");   
    }
    else   
    {
        if(resp.status == "1")
        {
            if(uhf_preparing == false)
            {                
                uhf_preparing = true;
            }
        }
        else if(resp.status == "2")
        {
            if(uhf_loading == false)
            {                   
                update_progress_bar("0");             
                uhf_loading = true;
            }
            else
                update_progress_bar(resp.progress);          

        }
        else if(resp.status == "3")
        {
            if(uhf_flashing == false)
            {
                apprise_close_progress_box();
                apprise_progress_box("Flashing firmware. Please wait...");   
                uhf_flashing = true;
            }
        }
        else if(resp.status == "4")
        {
            apprise_close_progress_box();
            $("#uhf_upgrade_btn").removeAttr("disabled");
            apprise("Upgrading has been successfuly done. Please reboot device.");   
            return;
        }
        else if(resp.status == "5")
        {
            apprise_close_progress_box();
            $("#uhf_upgrade_btn").removeAttr("disabled");   
            apprise("Upgrading has failed."); 
            return;
        }
           
        setTimeout( "send_ajax_req({cmd:\"uhf_upgrade_get_status\"}, uhf_upgrade_get_status_cb)", 2000 );
    }
}



var uhf_upgrade_init_cb = function(data)
{
    var resp = eval('(' + data + ')'); 

    if(resp.err != "0") 
    {
        apprise_close_progress_box();
        apprise("Error: " + resp.errmsg);
        $("#uhf_upgrade_btn").removeAttr("disabled");   
    }
    else
    {   
        apprise_close_progress_box();
        apprise_progress_box("Initiate modem for upgrading procedure");       
        setTimeout( "send_ajax_req({cmd:\"uhf_upgrade_get_status\"}, uhf_upgrade_get_status_cb)", 2000 );
    }
}



function uhf_upgrade()
{
    var filename = $("#uhf_fw_name").val();
    uhf_flashing = false;
    uhf_preparing = false;
    uhf_loading = false;

    if(filename == "" || filename.match(/ /))
    {
        apprise("Firmware filename should not consist space or be empty.");
        return false;
    }

    $("#uhf_upgrade_btn").attr("disabled", "disabled");

    apprise_progress_box("Checking firmware availability. Please wait...");
    send_ajax_req({cmd:"uhf_upgrade_init", filename:filename}, uhf_upgrade_init_cb);
}
         
          
                   
                   
var pwbrd_upgrade_init_cb = function(data)
{
    var resp = eval('(' + data + ')'); 

    apprise_close_progress_box();

    if(resp.err != "0") 
    {
        apprise("Error: " + resp.errmsg);        
    }
    else
    {   
        apprise("Upgrading has been successfuly done. Please reboot device.");     
    }

    $("#pwbrd_upgrade_btn").removeAttr("disabled");  
}
                   
                   
                   
                   
                   
function pwbrd_upgrade()
{
    var filename = $("#pwbrd_fw_name").val();
    if(filename == "" || filename.match(/ /))
    {
        apprise("Firmware filename should not consist space or be empty.");
        return false;
    }
    
    $("#pwbrd_upgrade_btn").attr("disabled", "disabled");
    apprise_progress_box("Initiate powerboard upgrading procedure. Please wait...");
    send_ajax_req({cmd:"pwbrd_upgrade_init", filename:filename}, pwbrd_upgrade_init_cb);
}
                   
