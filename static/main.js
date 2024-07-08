
var menu_selected_item;



var make_select = function(items, sel_item, aux_attr_str)
{
    var code = "<select " + aux_attr_str + ">";

    for(var i = 0; i < items.length; i++) 
        if(sel_item == items[i]) 
            code += "<option selected=\"yes\">" + items[i] + "</option>";
        else
            code += "<option>" + items[i] + "</option>";

    code += "</select>";    
    return code;
}




var sel_change = function(menu_sel_item, par__id, par__val)
{
    //DOMhelp.setDebug(menu_sel_item); 
    //DOMhelp.setDebug(par__id);
    //DOMhelp.setDebug(par__val);

    par_submit(menu_sel_item, par__id, par__val);

    return false;
}



var par_submit = function(node, id, val)
{
    //DOMhelp.setDebug(id); 
    //DOMhelp.setDebug(val);
    //DOMhelp.setDebug(node);

    var req = {cmd:"set"};
    req.node = node;
    req.arg = id;
    req.val = val;

    //return false;

    jQuery.ajax({
            type: "POST",
            data: req,
            dataTypeString: "json",
            success: function(data) {
                DOMhelp.setDebug(data); 

                var resp = eval('(' + data + ')');

                if(resp.val != "0") 
                {
                    jQuery("body").empty();
                    jQuery("body").append("<h1 id=\"status\">" + resp.note + "</h1>");
                }
                else
                {                    
                }
            },
            error: function(jqXHR, textStatus, errorThrown) {
                DOMhelp.setDebug("Error!");
            },
            });


    return false;
}



var expand_menu_item = function(item_id)
{
    DOMhelp.setDebug("Click! " + item_id);

    if(menu_selected_item == item_id) 
        return;

    var req = {cmd:"get"};
    req.arg = item_id;
    menu_selected_item = item_id;

    jQuery.ajax({
            type: "POST",
            data: req,
            dataTypeString: "json",
            success: function(data) {
                DOMhelp.setDebug(data); 

                var resp = eval('(' + data + ')');

                if(resp.val != "0") 
                {
                    jQuery("body").empty();
                    jQuery("body").append("<h1 id=\"status\">" + resp.note + "</h1>");
                }
                else
                {
                    if(!resp.hasOwnProperty("params"))
                        return;

                    var params = resp["params"];
                  
                   

                   jQuery("#workplace").empty();
                  // jQuery(".param").remove();
    
                   
                   var par_title;
                   var par_val;
                   var param, par_id, par_type;
                   var content = "<div class=\"param\"><ul>";

                   for(var i = 0; i < params.length; i++ ) 
                   {
                       param     = params[i];
                       par_val   = param["val"];
                       par_id    = param["id"];
                       par_title = param["title"];
                       par_type  = param["type"];

                       switch(par_type) 
                       {
                            case "text":
                                content += "<li>" + "<form class=\"form\" method=\"post\" onsubmit=\"return par_submit(menu_selected_item, this.id, input_field.value)\" id=\"" + par_id + "\"><span>" + par_title + 
                                           ":</span><div class=\"rounded\"><input  id=\"input_field\" type=\"text\" size=\"20\" value=\"" + par_val + "\" /></div></form></li>";  
                            break;

                            case "select":
                                content += "<li>" + "<span>" + par_title + ":</span>"; 
                                content += make_select(param["select_from"], par_val, "id=\"" + par_id + "\" onchange=\"return sel_change(menu_selected_item, this.id, this.options[selectedIndex].text)\"");
                                content += "</div></form></li>";  
                            break;
                       }  
                   }


                   content += "</ul></div>";
                   //DOMhelp.setDebug(content);                    
                   //jQuery("body").append(content);  
                   jQuery("#workplace").append(content);                                                                          
               }
            },
            error: function(jqXHR, textStatus, errorThrown) {
                DOMhelp.setDebug("Error!");
            },
            });



    return false;
}



var load_frame = function(ref)
{
    menu_selected_item="frame";
    ref = "/ping";// + "?reload=" +Math.random();
    jQuery("#workplace").empty();

    jQuery("#workplace").append("<iframe id=\"i_frame\" src=\"" + ref + "\" width=\"100%\" height=\"300\"></iframe>");
    //jQuery("#workplace").append("<iframe id=\"i_frame\"></iframe>");
    //jQuery('#i_frame').attr('src', ref);
    //jQuery('#i_frame').refresh();

    return false;
}



jQuery(document).ready(function() 
{
    jQuery("body").empty();
    DOMhelp.initDebug();
    DOMhelp.setDebug("Page loaded!");

    //document.body.style.cursor = "wait";
    //document.body.style.cursor = "default";
    //jQuery("body").css("cursor", "progress") ;

    // Prepare initial page
//    jQuery("body").prepend("<h1 id=\"loading\">Loading...</h1>");
    jQuery("body").append("<h1 id=\"status\">Loading...</h1>");

    menu_selected_item = "";


    // Send initial request
    jQuery.ajax({
            type: "POST",
            data: {cmd:"init"},
            dataTypeString: "json",
            success: function(data) {
                jQuery("#status").empty();
                

                var resp = eval('(' + data + ')');
                DOMhelp.setDebug(data); 
          

                if(resp.val != "0") 
                {
                    jQuery("body").append("<h1 id=\"status\">" + resp.note + "</h1>");
                    //jQuery("body").prepend("<h1 id=\"status\">Rea</h1>");
                }
                else
                {
                    if(!resp.hasOwnProperty("menu"))
                        return;

                    var menu_items = resp["menu"];
                    
                    var content = "<div id=\"banner\"></div><div id=\"navigation\"><ul>";
                    var item, id, menu_title, item_type;
                    for(var i = 0; i < menu_items.length; i++)
                    {
                        item       = menu_items[i];
                        id         = item["id"];
                        menu_title = item["title"];
                        item_type  = item["type"];

                        switch(item_type) 
                        {
                            case "params":
                                content += "<li><a href=\"#\" id=\"" + id + "\" onclick=\"return expand_menu_item(this.id)\" >" + menu_title + "</a></li>";                      
                            break;

                            case "ref":
                                href = item["href"];
                                content += "<li><a href=\""+ href +"\">" + menu_title + "</a></li>"; 
                            break;

                            case "frame":
                                href = item["href"];
                                content += "<li><a href=\""+ href +"\" onclick=\"return load_frame(this.href)\">" + menu_title + "</a></li>"; 
                            break;

                        }
                        
                        
                    }

                    //content += "<li><a href=\"#\" id=\"tools\" onclick=\"return tools(this.id)\" >Tools</a></li>"; 

                    content += "</ul></div>";
                    content += "<div id=\"workplace\"></div>";
                    //DOMhelp.setDebug(content); 
                    jQuery("body").append(content);
 
                }
            },
            error: function(jqXHR, textStatus, errorThrown) {
                DOMhelp.setDebug("Error!");
            },
            });

  
});


