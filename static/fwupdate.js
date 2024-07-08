
var updatable_item_list = [];
var update_list = {};
var update_prio = {};
var update_mode = {};
var update_list_keys = [];
var update_list_index = 0;
var num_updates_to_download = 0;
var cur_fw_name = "";
var downloaded_update_list = {};
var num_updates_to_apply = 0;

function update_checkbox(msg)
{
	if (msg == "in_fs_jlinklte") {
		$("#in_kernel_jlinklte").attr("checked", $("#in_fs_jlinklte").attr("checked"))
		if ($("#in_fs_jlinklte").attr("checked") == true) {
			$("#in_gsm").attr("checked", false)
		}
    }
	if (msg == "in_kernel_jlinklte") {
		$("#in_fs_jlinklte").attr("checked", $("#in_kernel_jlinklte").attr("checked"))
		if ($("#in_kernel_jlinklte").attr("checked") == true) {
			$("#in_gsm").attr("checked", false)
		}
	}
	if (msg == "in_gsm") {
		if (($("#in_gsm").attr("checked") == true) && ($("#in_fs_jlinklte").attr("checked") == true) ) {
			$("#in_fs_jlinklte").attr("checked", false)
			$("#in_kernel_jlinklte").attr("checked", false)
		}
	}
}

function open_wait_dlg(msg)
{
    apprise_progress_box("<div style=\"text-align:center; width: 400px;\"><div id=\"wait_gdl_msg\">" + msg + "</div></div><br /><div id=\"wait_spin\" ></div>");
}

function update_wait_dlg(msg)
{
    $("#wait_gdl_msg").html(msg);
}

function check_prio_0()
{
    alert("changed_0");
}

function check_prio_1()
{
    alert("changed_1");
}

function close_wait_dlg()
{
    apprise_close_progress_box();
}

function update_progress_bar(msg, progress)
{
     var pb  = "<div style=\"text-align:center; width: 400px; \">" + msg + "</div>";
     pb += "<div style=\"text-align:right;font-weight:bold;\">" + progress;
     pb += "%</div></span><div id=\"progress\" style=\"border: 1px solid black;\"> <div style=\"background-color:#11CC00; width:";
     pb += progress + "%\">&nbsp;</div></div>";
     apprise_progress_box_set_text(pb);
}

function open_progress_bar(msg)
{
     var pb  = "<div style=\"text-align:center; width: 400px; \">" + msg + "</div><div style=\"text-align:right;font-weight:bold;\">0%</div></span>";
     pb += "<div id=\"progress\" style=\"border: 1px solid black;\"><div style=\"background-color:#11CC00; width: 0%\">&nbsp;</div></div>";
     apprise_progress_box(pb);
}



function ajax_err(jqXHR, textStatus, errorThrown)
{
    close_wait_dlg();
    apprise("Error during server connection!");
    $("#check_btn").removeAttr("disabled");    
}

function size_dict(d){ c = 0; for (i in d) ++c; return c;}

function send_ajax_req(req, callback_fn)   
{
    $.ajax({type: "POST", data: req, dataTypeString: "json", success: callback_fn, error: ajax_err});  
}


function update_mode_changed_cb(data)
{
    var resp = eval('(' + data + ')');

    if(resp.err != "0") 
        apprise("Error: " + resp.errmsg);
    $("#check_btn").removeAttr("disabled");    
}



function check_for_update_cb(data)
{
    var resp = eval('(' + data + ')');

    if(resp.err != "0") 
        apprise("Error: " + resp.errmsg);
    else
    {
        if(resp.hasOwnProperty("update_info"))   
        {
            var update_info = resp["update_info"];
            var update_available = false;

            update_list = [];

            for(var fw_id in update_info)
            {
                if (update_info.hasOwnProperty(fw_id))
                {
                    var fw_info = update_info[fw_id]; 
                    var cur_ver = $("#fw_tbl #" + fw_id + " td:eq(1)").html();
                    $("#fw_tbl #" + fw_id + " td:eq(2)").html(fw_info[0]);
                    $("#fw_tbl #" + fw_id + " td:eq(3)").html(fw_info[1]);

                    if(fw_info[0] != "not available" && cur_ver != fw_info[0] && cur_ver != "unknown")
                    {
                        if($("#fw_tbl #" + fw_id + " td:eq(4) input[type=checkbox]").is(':checked'))
                        { 
                            $("#fw_tbl #" + fw_id + " td").css({ "color": 'green'});                         
                            update_available = true;
                            update_list[fw_id] = [$("#fw_tbl #" + fw_id + " td:eq(0)").html(), fw_info[0], fw_info[1], update_mode[fw_id]];
                        }
                    }
                    else
                    {
                         $("#fw_tbl #" + fw_id + " td").css({ "color": 'black'});            
                         if($("#fw_tbl #" + fw_id + " td:eq(4) input[type=checkbox]").is(':checked'))
                         {    
                             $("#fw_tbl #" + fw_id + " td").css({ "color": 'green'});                         
                             update_available = true;
                             update_list[fw_id] = [$("#fw_tbl #" + fw_id + " td:eq(0)").html(), fw_info[0], fw_info[1], update_mode[fw_id]];
                         }
                    }
                }                
            }

            if(update_available)
                $("#update_btn").removeAttr("disabled"); 
        }
    }   
    close_wait_dlg();
    $("#check_btn").removeAttr("disabled");    
}


function update_apply_initiate()
{
    var fw_id_val = update_list_keys[update_list_index];
    var update_info_val = JSON.stringify(downloaded_update_list[fw_id_val]);
    var fw_size_val = update_list[fw_id_val][2]; 
    var fw_ver_val = update_list[fw_id_val][1];    
    send_ajax_req({cmd:"update_apply_initiate", fw_id:fw_id_val, fw_size:fw_size_val, fw_ver:fw_ver_val, update_info:update_info_val}, update_apply_initiate_cb);                 
    cur_fw_name = update_list[fw_id_val][0];
}

function update_download_initiate()
{
    var fw_id_val = update_list_keys[update_list_index];
    var update_info_val = JSON.stringify(update_list[fw_id_val]);                    
    send_ajax_req({cmd:"update_download_initiate", fw_id:fw_id_val, update_info:update_info_val}, update_download_initiate_cb);
}



var get_update_apply_status_cb = function(data)
{
    var resp = eval('(' + data + ')'); 

    if(resp.err != "0") 
    {
        close_wait_dlg();  
        apprise("Error: " + resp.errmsg);
    }
    else   
    {
        var status = resp["status"];

        if(status["Status"] == "Done")
        {
            num_updates_to_apply--;
            if(status.hasOwnProperty("Error"))
            {
                close_wait_dlg();  
                apprise(status["Error"]);
            }
            else if(num_updates_to_apply == 0)
            {
                close_wait_dlg();  
                apprise("Update has been successfuly done. Please reboot the device.");
            }
            else
            {
                update_list_index++;
                update_apply_initiate();
                update_wait_dlg("Applying " + cur_fw_name + " firmware");
            }
        }
        else
        {
            if(status["Status"] != "In progress")
            {
                var wait_dlg_msg = "Applying " + cur_fw_name + " firmware";
                wait_dlg_msg += "<br>" + status["Status"];
                if(status.hasOwnProperty("Progress"))
                {
                    wait_dlg_msg += " " + status["Progress"] + "%";
                }

                update_wait_dlg(wait_dlg_msg);                
            }

            setTimeout( "send_ajax_req({cmd:\"get_update_apply_status\"}, get_update_apply_status_cb)", 2000);  
        }
    }
}



var update_apply_initiate_cb = function(data)
{
    var resp = eval('(' + data + ')'); 

    if(resp.err != "0") 
    {
        close_wait_dlg();  
        apprise("Error: " + resp.errmsg);
    }
    else   
        setTimeout( "send_ajax_req({cmd:\"get_update_apply_status\"}, get_update_apply_status_cb)", 1000);  
}



var get_completion_status_cb = function(data)
{
    var resp = eval('(' + data + ')'); 

    if(resp.err != "0") 
    {
        apprise_close_progress_box();   
        apprise("Error: " + resp.errmsg);
    }
    else   
    {
        if (resp.hasOwnProperty("cstatus"))
        {
            var cstatus = resp["cstatus"];

            if(cstatus.hasOwnProperty("Error") )
            {
                 apprise_close_progress_box();   
                 apprise("Could not download " + cur_fw_name + "firmware correctly");
                 $("#check_btn").removeAttr("disabled");  
                 $("#update_btn").removeAttr("disabled");  
            }
            else
            {
                num_updates_to_download--;

                downloaded_update_list[update_list_keys[update_list_index]] = cstatus;

                if(num_updates_to_download)
                {
                    update_list_index++;
                    update_download_initiate();
                }
                else
                {
                    num_updates_to_apply = size_dict(downloaded_update_list);
                    update_list_keys = [];
                    for(var key in downloaded_update_list)  
                        update_list_keys.push(key);

                    update_list_index = 0;
                    update_apply_initiate();
                    apprise_close_progress_box();   
                    open_wait_dlg("Applying " + cur_fw_name + " firmware");
                }
            }
        }
    }
}




var get_download_status_cb = function(data)
{
    var resp = eval('(' + data + ')'); 

    if(resp.err != "0") 
    {
        apprise_close_progress_box();   
        apprise("Error: " + resp.errmsg);
    }
    else   
    {
        if (resp.hasOwnProperty("status"))
        {
            var status = resp["status"];
            var state = status["State"];
            var progress = status["Progress"];
            var pace = status["Pace"];

            update_progress_bar("Downloading " + cur_fw_name + " firmware at " + pace + " bps" , progress);
            if(state == "In progress")
                setTimeout( "send_ajax_req({cmd:\"get_download_status\"}, get_download_status_cb)", 2000);
            else
                send_ajax_req({cmd:"get_completion_status"}, get_completion_status_cb);
        }
    }
}



function update_download_initiate_cb(data)
{
    var resp = eval('(' + data + ')');

    if(resp.err != "0") 
    {
        apprise("Error: " + resp.errmsg);
        $("#update_btn").removeAttr("disabled"); 
    }
    else
    {
        cur_fw_name = update_list[update_list_keys[update_list_index]][0];
        send_ajax_req({cmd:"get_download_status"}, get_download_status_cb);
    }
}



function update()
{
    update_list_index = 0;
    downloaded_update_list = {};
    num_updates_to_download = size_dict(update_list);
    if(num_updates_to_download != 0)
    {
        $("#update_btn").attr("disabled", "disabled");


	     var update_prio_list = [];
	     for(var key in update_prio) 
		 update_prio_list[parseInt(update_prio[key])] = key; 


        update_list_keys = [];
	     var i = 0;
        for(var j = 0; j < update_prio_list.length; j++)  
	     {
		 var fw_id = update_prio_list[j];
		 if(update_list.hasOwnProperty(fw_id))
		 {
		     update_list_keys[i] = fw_id;    
		     i++;
		 }
	     }
        open_progress_bar("Downloading " + cur_fw_name + " firmware...");
        update_download_initiate();
    }
}


function update_mode_changed()
{
    $("#check_btn").attr("disabled", "disabled");
    $("#update_btn").attr("disabled", "disabled");
    fw_id_val = JSON.stringify(updatable_item_list);
    var branches = document.getElementsByName('branch');
    var branch;
    for(var i = 0; i < branches.length; i++){
            if(branches[i].checked){
                        branch = branches[i].value;
                            }
    }
    $("#fw_tbl tr").each(function() {
        var fw_id = $(this).attr('id');
        if(fw_id != "")
        {
            update_mode[fw_id] = branch ;
        }
    });

    fw_mode_val = JSON.stringify(update_mode);
    send_ajax_req({cmd:"update_mode_changed", fw_mode:branch}, update_mode_changed_cb);
}

function check_for_update()
{
    $("#check_btn").attr("disabled", "disabled");
    $("#update_btn").attr("disabled", "disabled");
    /*$("body").css("cursor", "progress");*/
    fw_id_val = JSON.stringify(updatable_item_list);
    fw_mode_val = JSON.stringify(update_mode);
    open_wait_dlg("Please wait...");
    send_ajax_req({cmd:"check_for_update", fw_id:fw_id_val, fw_mode:fw_mode_val}, check_for_update_cb);
}


$(document).ready(function()
{
    $("#fw_tbl tr:even").addClass("even");
    $("#fw_tbl tr:odd").addClass("odd");
    $("#update_btn").attr("disabled", "disabled");
    var branches = document.getElementsByName('branch');
    var branch;
    for(var i = 0; i < branches.length; i++){
            if(branches[i].checked){
                        branch = branches[i].value;
                            }
    }


    $("#fw_tbl tr").each(function() {
        var fw_id = $(this).attr('id');
        if(fw_id != "") 
        {
            updatable_item_list.push(fw_id);       
            update_prio[fw_id] = $(this).attr("uprio");
            update_mode[fw_id] = branch;		 
        }
    });
   
});



