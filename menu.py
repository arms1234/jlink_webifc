
import os

import session
from xml_db import xml_db
from perror import PageError

printenv_util = "/jlinklte/utils/fw_printenv"

SetupSubMenu         = [{"title":"Router", "ref":"/rou"}]
StatusSubMenu        = [{"title":"Device", "ref":"/device"}, {"title":"LAN", "ref":"/lans"}, {"title":"UHF Int.", "ref":"/uhfs"}, {"title":"GSM", "ref":"/gsms"}, {"title":"Wi-Fi", "ref":"/wifis"},
        {"title":"Bluetooth", "ref":"/bts"}, {"title":"GNSS", "ref":"/gpss"},
        {"title":"NTRIP", "ref":"/ntrips"}, {"title":"TCP", "ref":"/tcps"}, {"title":"TCPO", "ref":"/tcpos"}, {"title":"DYNDNS", "ref":"/dyndnss"}, {"title":"Power", "ref":"/power"}]
AdminSubMenu         = [{"title":"Management", "ref":"/management"}, {"title":"Firmware Update", "ref":"/fwupgrade"}]
ServicesSubMenu      = [{"title":"NTRIP", "ref":"/ntrip"}, {"title":"TCP", "ref":"/tcp"}, {"title":"TCPO", "ref":"/tcpo"},  {"title":"DYNDNS", "ref":"/dyndns"}, {"title":"Ping", "ref":"/ping"}, {"title":"Pairing", "ref":"/pairing"}]
CommunicationSubMenu = [{"title":"LAN", "ref":"/lan"}, {"title":"UHF Int.", "ref":"/uhf"}, {"title":"GSM", "ref":"/gsm"},
        {"title":"Wi-Fi", "ref":"/wifi"},{"title":"Bluetooth",
            "ref":"/bt"}, {"title":"Power Management", "ref":"/gsetup"}, {"title":"Advanced", "ref":"/adv"}]
        #                        {"title":"UHF Ext.", "ref":"/extmodem"},



MainMenu = [{"title":"Setup",       "ref":"/rou",             "subMenu":SetupSubMenu},
        {"title":"Status",          "ref":"/status",          "subMenu":StatusSubMenu},
        {"title":"Communication",   "ref":"/communication",   "subMenu":CommunicationSubMenu},
        {"title":"Services",        "ref":"/services",        "subMenu":ServicesSubMenu},
        {"title":"Administration",  "ref":"/admin",           "subMenu":AdminSubMenu},
        ]

def build_menu(main__title, sub__title):
    menu_str = ""
    for main_item in MainMenu:
        title = main_item["title"]
        ref   = main_item["ref"]
        sub   = main_item["subMenu"]

        #print main_item
        #print title
        #print ref
        #print sub

        if title == main__title:
            menu_str = menu_str + "<li class=\"current\"><span>" + title + "</span>\n"
            if sub != None:
                menu_str = menu_str + "<div id=\"menuSub\"><ul id=\"menuSubList\">\n"
                for sub_item in sub:
                    sub_title = sub_item["title"]
                    sub_ref   = sub_item["ref"]
                    if sub_title == sub__title:
                        menu_str = menu_str + "<li><span>" + sub_title + "</span></li>\n"
                    else:
                        if sub_ref == None:
                            menu_str = menu_str + "<li><span>" + sub_title + "</span></li>\n"
                        else:
                            menu_str = menu_str + "<li><a href=\"" + sub_ref + "\">" + sub_title + "</a></li>\n"

                menu_str = menu_str + "</ul></div>\n"
            menu_str = menu_str + "</li>\n"
        else:
            if ref == None:
                menu_str = menu_str + "<li><span>" + title + "</span></li>\n"
            else:
                menu_str = menu_str + "<li><a href=\"" + ref + "\">" + title + "</a></li>\n"

    db = xml_db()
    if db.open() == False:
        raise PageError("Could not open configuration storage")

    fw_uuid = db.get_params_set("fw_uuid")
    product_id = fw_uuid["product_id"]["val"]
    serial_num =  os.popen(printenv_util  + " sn 2>/dev/null").read().rstrip("\n")
    if serial_num != None and serial_num != "":
        serial_num = serial_num.split("=")[1]
    else:
        serial_num = "Unknown"

    pn_env   = os.popen(printenv_util  + " pn 2>/dev/null").read().rstrip("\n")
    if pn_env != None and pn_env != "":
        pn = pn_env.split("=")[1]
    else:
        pn = "unknown"

    if pn == "01-597520-10" or pn == "01-597520-11" or pn == "01-597520-12" or pn == "01-597520-13" or\
       pn == "01-597520-20" or pn == "01-597520-21" or pn == "01-597520-22" or pn == "01-597520-23" or\
       pn == "01-597520-30" or pn == "01-597520-31" or pn == "01-597520-32" or pn == "01-597520-33" or\
       pn == "01-597520-40" or pn == "01-597520-41" or pn == "01-597520-42" or pn == "01-597520-43" or\
       pn == "01-597520-16" or pn == "01-597520-26" or pn == "01-597520-46" :
        product_name = "JLinkLTE"
    elif pn == "01-597521-10" or pn == "01-597521-11" or pn == "01-597521-12" or pn == "01-597521-13" or\
         pn == "01-597521-20" or pn == "01-597521-21" or pn == "01-597521-22" or pn == "01-597521-23" or\
         pn == "01-597521-30" or pn == "01-597521-31" or pn == "01-597521-32" or pn == "01-597521-33" or\
         pn == "01-597521-40" or pn == "01-597521-41" or pn == "01-597521-42" or pn == "01-597521-43" or\
         pn == "01-597521-16" or pn == "01-597521-26" or pn == "01-597521-46" :
        product_name = "JLinkLTE_BAT"
    elif pn == "01-587300-50" or pn == "01-587300-51" or pn == "01-587300-52" or pn == "01-587300-53" or pn == "01-587300-54" :
        product_name = "HPT404BT"
    elif pn == "01-587100-50" or pn == "01-587100-51" or pn == "01-587100-52" or pn == "01-587100-53" or pn == "01-587100-54" :
        product_name = "HPT435BT"
    elif pn == "01-587400-50" or pn == "01-587400-51" or pn == "01-587400-52" or pn == "01-587400-53" or pn == "01-587400-54" :
        product_name = "HPT135BT"
    elif pn == "01-587500-50" or pn == "01-587500-51" or pn == "01-587500-52" or pn == "01-587500-53" or pn == "01-587500-54" :
        product_name = "HPT104BT"
    elif pn == "01-587800-50" or pn == "01-587800-51" or pn == "01-587800-52" or pn == "01-587800-53" or pn == "01-587800-54" :
        product_name = "HPT225BT"
    else:
        product_name = "Unknown"

    device_name = product_name + "_" + serial_num
    menu_str = menu_str + "<li><h1 style=\"margin-left:240px\">" + device_name + "</h1></li>"
    return menu_str


