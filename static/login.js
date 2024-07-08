
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


function open_login_dialog()
{
    var content;
    var device_info = "";
    serial_num = ("00000" + serial_num).slice(-5);

    switch(product_id){
        case 115:
            device_info = "JLinkLTE_" + serial_num;
            break;
        case 116:
            device_info = "HPT404BT_" + serial_num;
            break;
        case 117:
            device_info = "HPT435BT_" + serial_num;
            break;
        case 118:
            device_info = "HPT104BT_" + serial_num;
            break;
        case 119:
            device_info = "HPT135BT_" + serial_num;
            break;
        case 120:
            device_info = "HPT225BT_" + serial_num;
            break;
        default:
            device_info = "UNKNOWN DEVICE" + serial_num;
    }
    content = "";
    content += "<div><b>" + device_info + "</b></div></br>";
    content += "<div><b>Login:&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</b><input id=\"login\" maxlength=\"32\" size=\"20\" value=\"\"/></div></br>";
    content += "<div><b>Password:&nbsp&nbsp</b><input id=\"password\" type=\"password\" maxlength=\"64\" size=\"20\" value=\"\"/></div>";
    content += "<button value=\"Ok\" onclick=\"login()\">Ok</button>";
    show_mdialog(content);
}




var login_cb = function(data)
{
    var resp = eval('(' + data + ')');

    if(resp.err != "0") 
    {
        apprise_close_progress_box();
        apprise("Login/password is incorrect!", {}, function(r) {open_login_dialog();});
    }
    else
    {
        document.cookie = "session__id=" + encodeURIComponent(resp.session_id);
        window.location.replace('/');
    }
}


function login()
{
    var login = $("#login").val();
    var password = $("#password").val();

    apprise_progress_box("Please wait..."); 

    send_ajax_req({cmd:"login", login:login, password:password}, login_cb); 

    $(".mdialog_overlay").remove();
	 $(".mdialog").remove();
}





$(document).ready(function(){
    if(typeof(parent.reload) == 'function')
        parent.reload();
    else
        open_login_dialog();
});

