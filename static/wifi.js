

var sel_network_bssid = "";
var sel_network_ssid = "";
var sel_network_protection = "";
var sel_network_slvl = "";
var wifi_networks = [];
var adapter_state;


function ajax_err(jqXHR, textStatus, errorThrown)
{
    apprise_close_progress_box();
    apprise("Error during server connection!");
}


function send_ajax_req(req, callback_fn)
{
    $.ajax({type: "POST", data: req, dataTypeString: "json", success: callback_fn, error: ajax_err});
}


var forget_wifi_network = function(data)
{
    var resp = eval('(' + data + ')');

    apprise_close_progress_box();
    if(resp.err != "0")
        apprise("<b>Error:</b> " + resp.errmsg + " Please reload page.");

}


var update_known_wifi_networks = function(data)
{
    var resp = eval('(' + data + ')');
    var i;
    var content = "";

    wifi_networks = [];
    var wifi_net = resp.wifi_networks;
    for(i = 0; i < wifi_net.length; i++)
    {
        var item = [];
        if(wifi_net[i].hasOwnProperty("bssid"))
            item["bssid"] = wifi_net[i]["bssid"];
        if(wifi_net[i].hasOwnProperty("ssid"))
            item["ssid"] = wifi_net[i]["ssid"];
        if(wifi_net[i].hasOwnProperty("protection"))
            item["protection"] = wifi_net[i]["protection"];

        wifi_networks[i] = item;
    }
}



var add_wifi_network = function(data)
{
    var resp = eval('(' + data + ')');

    apprise_close_progress_box();
    if(resp.err != "0")
        apprise("<b>Error:</b> " + resp.errmsg + " Please reload page.");
    else
        send_ajax_req({cmd:"get_wifi_networks"}, update_known_wifi_networks);
}


var connect_wifi_network = function(data)
{
    var resp = eval('(' + data + ')');

    apprise_close_progress_box();
    if(resp.err != "0")
        apprise("<b>Error:</b> " + resp.errmsg);
}


function remove_known_network(bssid)
{
    for(var i = 0; i < wifi_networks.length; i++)
        if(bssid == wifi_networks[i]["bssid"])
        {
            wifi_networks.splice(i,1);
            break;
        }
}

function check_known_network(bssid)
{
    for(var i = 0; i < wifi_networks.length; i++)
        if(bssid == wifi_networks[i]["bssid"])
            return true;
    return false;
}



function update_events()
{
    $("#wifi_networks_tbl tbody.scroll_body tr").click(function(){
        $("#wifi_networks_tbl tbody.scroll_body tr.selected").removeClass("over selected");
        sel_network_bssid = $(this).find("td").eq(2).find("#bssid").html();

        if(sel_network_bssid != "")
    {
        sel_network_ssid  = $(this).find("td").eq(2).find("b").html();
        sel_network_slvl  = $(this).find("td").eq(3).find("b").html();
        sel_network_protection = $(this).find("td").eq(1).html();

        $(this).addClass("selected");

        if(check_known_network(sel_network_bssid))
    {
        apprise("<b>"+sel_network_ssid+"</b>", (sel_network_protection == "OPEN")?{'select':["Connect", "Forget", "Cancel"]}:{'select':["Connect", "Forget", "Change Password", "Cancel"]}, function(r)
            {
                if(typeof(r) == 'string')
            if(r == 'Forget')
        {
            $("#wifi_networks_tbl tbody.scroll_body tr.selected").remove();
            apprise_progress_box("Please wait...");
            remove_known_network(sel_network_bssid);
            send_ajax_req({cmd:"forget_wifi_network", "bssid":sel_network_bssid}, forget_wifi_network);
            sel_network_bssid = "";
        }
            else if(r == 'Connect')
        {
            apprise_progress_box("Please wait...");
            send_ajax_req({cmd:"connect_wifi_network", "bssid":sel_network_bssid}, connect_wifi_network);
            sel_network_bssid = "";
        }
            else if(r == 'Change Password')
        {
            apprise("Enter new password for <b>"+sel_network_ssid+"</b> ?", {'input':true, 'prompt':"Password: "} , function(r)
                {
                    if(r)
            {
                apprise_progress_box("Please wait...");
                send_ajax_req({cmd:"add_wifi_network", bssid:sel_network_bssid, passphrase:r, ssid:sel_network_ssid, protection:sel_network_protection }, add_wifi_network);
            }
            sel_network_bssid = "";
                });
        }
            else
                sel_network_bssid = "";
        $("#wifi_networks_tbl tbody.scroll_body tr.selected").removeClass("over selected");
            });
    }
        else
        {
            apprise("Connect to <b>"+sel_network_ssid+"</b> ?", (sel_network_protection == "OPEN")?{'confirm':true}:{'input':true, 'prompt':"Password: "} , function(r)
                    {
                        if(r)
            {
                apprise_progress_box("Please wait...");
                send_ajax_req({cmd:"add_wifi_network", bssid:sel_network_bssid, passphrase:r, ssid:sel_network_ssid, protection:sel_network_protection }, add_wifi_network);

            }
            $("#wifi_networks_tbl tbody.scroll_body tr.selected").removeClass("over selected");
            sel_network_bssid = "";
                    });
        }
    }
    });
}






function wifi_networks_tbl_hdr()
{
    var content = "";

    content = "<div id=\"tbl_cont\" class=\"tbl_cont\">";

    content += "<table id=\"wifi_networks_tbl\" class=\"scroll_tbl\">";

    content += "<tr><td>";
    content += "<table id=\"wifi_networks_tbl_hdr\" class=\"scroll_tbl_hdr\" >";
    content += "<thead class=\"fixed_hdr\"><tr>";
    content += "<th>" + "  " + "</th>";
    content += "<th>" + "Protection" + "</th>";
    content += "<th>" + "Access point" + "</th>";
    content += "<th>" + "Signal level" + "</th>";
    content += "<th>" + "Channel" + "</th>";
    content += "</tr></thead>";
    content += "</table>";
    content += "</td></tr>";

    content += "<tr><td>";
    content += "<div style=\"width:100%; height:210px; overflow:auto; overflow-y: scroll; overflow-x:hidden;\">";
    content += "<table id=\"wifi_networks_tbl_body\" class=\"scroll_tbl_body\">";
    content += "<tbody class=\"scroll_body\">";
    return content;
}

function wifi_networks_tbl_fin(content)
{
    content += "</tbody>";
    content += "</table>";
    content += "</td></tr>";
    content += "</div>";
    content += "</table>";
    content += "</div>";
    return content;
}


function wifi_networks_tbl_body(content, networks)
{
    var protection;

    for(i = 0; i < networks.length; i++)
    {
        bssid = networks[i]["bssid"];
        if(sel_network_bssid == bssid)
            content += "<tr class=\"selected\">";
        else
            content += "<tr>";
        favorite = check_known_network(bssid)? "_fav" : ""

        if(networks[i].hasOwnProperty("protection"))
        {
            protection = networks[i]["protection"];
            if(protection == "OPEN")
            {
                content += "<td><img src=\"/static/lock_open" + favorite + ".png\"/></td>";
            }
            else
                content += "<td><img src=\"/static/lock" + favorite + ".png\"/></td>";
        }
        else
        {
            protection = "";
            content += "<td><img src=\"/static/lock_open" + favorite + ".png\"/></td>";
        }


        content += "<td>" + protection + "</td>";

        var state_str = "";
        if(networks[i].hasOwnProperty("state"))
        {
            if(networks[i]["state"] == "COMPLETED")
                state_str = "<b>(Connected)</b>";
            //    content += "<td>" + "<div><b>" + networks[i]["ssid"] + "</b><b>(connected)</b></div>" + "<div id=\"bssid\">" + networks[i]["bssid"] + "</div>" + "</td>";
        }
        content += "<td><div><b>" + networks[i]["ssid"] + "</b>" + state_str +"</div><div id=\"bssid\">" + networks[i]["bssid"] + "</div></td>";

        if(networks[i].hasOwnProperty("slvl"))
            content += "<td id=\"slvl\">" + networks[i]["slvl"] + "</td>";
        else
            content += "<td id=\"slvl\">" + "<b>Not in range</b>" + "</td>";


        if(networks[i].hasOwnProperty("channel") && networks[i].hasOwnProperty("freq"))
            content += "<td><div><b>" + networks[i]["channel"] + "</b></div><div>(" + networks[i]["freq"] +")</div></td>";
        else
            content += "<td>" + " " + "</td>";

        content += "</tr>";
    }

    return content;
}


function get_wifi_env(data)
{
    var resp = eval('(' + data + ')');

    if(adapter_state == "disabled")
        return;

    if(resp.err != "0")
    {
        //$("#wifi_networks").empty();
        //$("#wifi_networks").append(resp.errmsg);
        if(adapter_state == "enabled")
            setTimeout( "send_ajax_req({cmd:\"get_wifi_env\"}, get_wifi_env)", 5000 );
    }
    else
    {
        var content = "";
        var i, j;
        var wifi_env = resp.wifi_env;
        var bssid;
        var incl;
        var known_networks = [];
        var known_networks_cnt = 0;

        for(i = 0; i < wifi_networks.length; i++)
        {
            bssid = wifi_networks[i]["bssid"];

            incl = true;
            for(j = 0; j < wifi_env.length; j++)
                if(bssid == wifi_env[j]["bssid"])
                {
                    incl = false;
                    break;
                }

            if(incl == true)
                known_networks[known_networks_cnt++] = wifi_networks[i];

        }

        $("#wifi_networks").empty();
        content = wifi_networks_tbl_hdr();
        content = wifi_networks_tbl_body(content, wifi_env);
        content = wifi_networks_tbl_body(content, known_networks);
        content = wifi_networks_tbl_fin(content);
        $("#wifi_networks").append(content);

        update_events();

        if(adapter_state == "enabled") {
            setTimeout( "send_ajax_req({cmd:\"get_wifi_networks\"}, update_known_wifi_networks)", 2500 );
            setTimeout( "send_ajax_req({cmd:\"get_wifi_env\"}, get_wifi_env)", 2500 );
        }
    }
}

var get_wifi_networks = function(data)
{
    var resp = eval('(' + data + ')');
    var i;
    var content = "";

    wifi_networks = [];
    var wifi_net = resp.wifi_networks;
    for(i = 0; i < wifi_net.length; i++)
    {
        var item = [];
        if(wifi_net[i].hasOwnProperty("bssid"))
            item["bssid"] = wifi_net[i]["bssid"];
        if(wifi_net[i].hasOwnProperty("ssid"))
            item["ssid"] = wifi_net[i]["ssid"];
        if(wifi_net[i].hasOwnProperty("protection"))
            item["protection"] = wifi_net[i]["protection"];
        wifi_networks[i] = item;
    }

    $("#wifi_networks").empty();
    content = wifi_networks_tbl_hdr();
    content = wifi_networks_tbl_body(content, wifi_networks);
    content = wifi_networks_tbl_fin(content);
    $("#wifi_networks").append(content);


    //update_events();
    send_ajax_req({cmd:"get_wifi_env"}, get_wifi_env);
}




var set_adapter_mode_cb = function(data)
{
    var resp = eval('(' + data + ')');
    if(resp.err == "0")
        window.location = '/wifi';
    else
        apprise("<b>Error:</b> " + resp.errmsg + " Please reload page.");
}


function set_adapter_mode()
{
    $("#mode_btn").attr("disabled", "disabled");
    send_ajax_req({cmd:"wifi_set_mode", mode:$("#mode_btn").val()}, set_adapter_mode_cb);
}


/*
   var set_state_cb = function(data)
   {
   var resp = eval('(' + data + ')');
   if(resp.err == "0")
   {
   $("#state_btn").removeAttr("disabled");

   if(adapter_state == "disabled")
   {
   content = wifi_networks_tbl_hdr();
   content = wifi_networks_tbl_fin(content);
   $("#wifi_networks").empty();
   $("#wifi_networks").append(content);


   $("#adapter_state").text("Disabled");
   $("#state_btn").attr("value", "Enable adapter");

   wifi_networks = [];
   }
   else
   {
   $("#adapter_state").text("Enabled");
   $("#state_btn").attr("value", "Disable adapter");

   send_ajax_req({cmd:"get_wifi_networks"}, get_wifi_networks);
   }
   }
   else
   apprise("<b>Error:</b> " + resp.errmsg + " Please reload page.");
   }
   */

/*
   function set_adapter_state()
   {
   $("#state_btn").attr("disabled", "disabled");

   if($("#adapter_state").text() == "Enabled")
   adapter_state = "disabled";
   else
   adapter_state = "enabled";
   send_ajax_req({cmd:"wifi_set_state", state:adapter_state}, set_state_cb);
   }
   */


$(document).ready(function(){

    var i;
    var content;
    sel_network_bssid = "";

    content = wifi_networks_tbl_hdr();
    content = wifi_networks_tbl_fin(content);
    $("#wifi_networks").empty();
    $("#wifi_networks").append(content);

    if($("#adapter_state").text() == "Enabled")
{
    adapter_state = "enabled";
    send_ajax_req({cmd:"get_wifi_networks"}, get_wifi_networks);
}
else
adapter_state = "disabled";

});

