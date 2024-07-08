


import sys
import os
from xml.dom import minidom, Node

class xml_db:

    def __init__(self, xml_filename = "/jlinklte/storage/configs/jlinklte.xml"):
        self.xml_doc      = None
        self.xml_root     = None
        self.xml_filename = xml_filename



    def open(self):
        try:
            self.xml_doc = minidom.parse(self.xml_filename)
        except Exception as e:
            return False
        else:
            self.xml_root = self.xml_doc.documentElement
            return True





    #
    #
    #
    def get_params_set(self, set_id):
        if(self.xml_root == None):
            return {}
        else:
            set_items = self.xml_root.getElementsByTagName("params_set")
            if len(set_items) == 0:
                return {}

            param_list = {}
            for set_item in set_items:
                if set_item.nodeType == Node.ELEMENT_NODE:
                    if set_item.attributes.get('id').value == set_id and set_item.attributes.get('type').value == "params":
                        for child in set_item.childNodes:
                            if child.nodeType == Node.ELEMENT_NODE:

                                param_attr = {}
                                for (name, value) in child.attributes.items():
                                    param_attr[name] = value

                                for chld in child.childNodes:
                                    if chld.nodeType == Node.TEXT_NODE:
                                        param_attr["val"] = chld.nodeValue;

                                if param_attr.has_key("select_from"):
                                    param_attr["select_from"] = param_attr["select_from"].split(" ")

                                if param_attr.has_key("id") and param_attr.has_key("val"):
                                     param_list[param_attr["id"]] = param_attr

            return param_list


    #
    #
    #
    def set_params_set(self, set_id, params):
        if(self.xml_root == None):
            return "DB has not been opened!"
        else:
            set_items = self.xml_root.getElementsByTagName("params_set")
            if len(set_items) == 0:
                return "There is no any params set!"

            for set_item in set_items:
                if set_item.nodeType == Node.ELEMENT_NODE:
                    if set_item.attributes.get('id').value == set_id and set_item.attributes.get('type').value == "params":

                        param_cnt = 0
                        for child in set_item.childNodes:
                            if child.nodeType == Node.ELEMENT_NODE:
                                param_id = child.attributes.get('id').value

                                #print param_id

                                if params.has_key(param_id):
                                    new_child = self.xml_doc.createElement("param")
                                    # Copy child attributes
                                    for (name, value) in child.attributes.items():
                                        new_child.setAttribute(name, value)

                                    new_child.appendChild(self.xml_doc.createTextNode(params[param_id]))

                                    set_item.replaceChild(new_child, child)
                                    param_cnt = param_cnt + 1

                        return ""
                        #if param_cnt == len(params):
                        #    return ""
                        #else:
                        #    return "There is no some param!"

            return "There is no such params set!"


    #
    #
    #
    def set_param_set(self, set_id, param_id, param_val):
        if(self.xml_root == None):
            return "DB has not been opened!"
        else:
            set_items = self.xml_root.getElementsByTagName("params_set")
            if len(set_items) == 0:
                return "There is no any params set!"

            for set_item in set_items:
                if set_item.nodeType == Node.ELEMENT_NODE:
                    if set_item.attributes.get('id').value == set_id and set_item.attributes.get('type').value == "params":

                        for child in set_item.childNodes:
                            if child.nodeType == Node.ELEMENT_NODE:

                                if param_id == child.attributes.get('id').value:
                                    new_child = self.xml_doc.createElement("param")
                                    # Copy child attributes
                                    for (name, value) in child.attributes.items():
                                        new_child.setAttribute(name, value)

                                    new_child.appendChild(self.xml_doc.createTextNode(param_val))

                                    set_item.replaceChild(new_child, child)
                                    return ""
                        return "There is no such param!"
            return "There is no such params set!"

    #
    #
    #
    def set_update_mode(self,umode):
        if(self.xml_root == None):
            return "DB has not been opened!"
        else:
            set_items = self.xml_root.getElementsByTagName("params_set")
            if len(set_items) == 0:
                return "There is no any params set!"
            for set_item in set_items:
                if set_item.nodeType == Node.ELEMENT_NODE:
                    if set_item.attributes.get('id').value == "updatable_parts" and set_item.attributes.get('type').value == "params":
                        for child in set_item.childNodes:
                            if child.nodeType == Node.ELEMENT_NODE:
                                param_id = child.attributes.get('id').value
                                new_child = self.xml_doc.createElement("param")
                                # Copy child attributes
                                for (name, value) in child.attributes.items():
                                    if name == "umode":
                                        new_child.setAttribute(name, umode)
                                    else:
                                        new_child.setAttribute(name, value)
                                new_child.appendChild(self.xml_doc.createTextNode(child.firstChild.nodeValue))
                                set_item.replaceChild(new_child, child)
                        return ""
            return "There is no umode!"



    #
    # Looking for menu items in xml data base
    # Return menu structure in dictionary like this:
    #   { "menu": [ {"name":"Printed menu item name", "attr1_name":"attr_val", ....},
    #               {"name":"Printed menu item name", "attr1_name":"attr_val", ....},
    #               .....
    #             ]
    #
    #
#    def get_menu_items(self):
#        if(self.xml_root == None):
#            return {}
#        else:
#            menu_items = self.xml_root.getElementsByTagName("menu_item")
#            if len(menu_items) == 0:
#                return {}
#
#            menu_list = []
#            for menu_item in menu_items:
#                if menu_item.nodeType == Node.ELEMENT_NODE:
#                    menu_record = {}
#                    for (name, value) in menu_item.attributes.items():
#                        #print '    Attr -- Name: %s  Value: %s' % (name, value)
#                        menu_record[name] = value
#
#
#                    if menu_record.has_key("id") == True:
#                        if menu_record.has_key("title") == False:
#                            menu_record["title"] = menu_record["id"]
#
#                        menu_list.append(menu_record)
#
#            return {"menu":menu_list}
#
#
#

    #
    #
    #  Return list of parameters for menu item with type="params"
    #
    #
    #
    #
#    def get_params_for_menu_item(self, item_id):
#        if(self.xml_root == None):
#            return {}
#        else:
#            menu_items = self.xml_root.getElementsByTagName("menu_item")
#            if len(menu_items) == 0:
#                return {}
#
#            param_list = []
#            for menu_item in menu_items:
#                if menu_item.nodeType == Node.ELEMENT_NODE:
#                    if menu_item.attributes.get('id').value == item_id and menu_item.attributes.get('type').value == "params":
#                        for child in menu_item.childNodes:
#                            if child.nodeType == Node.ELEMENT_NODE:
#
#                                param_record = {}
#                                for (name, value) in child.attributes.items():
#                                    param_record[name] = value
#
#                                for chld in child.childNodes:
#                                    if chld.nodeType == Node.TEXT_NODE:
#                                        param_record["val"] = chld.nodeValue;
#
#                                if param_record.has_key("select_from"):
#                                    param_record["select_from"] = param_record["select_from"].split(" ")
#
#
#                                if param_record.has_key("id") and param_record.has_key("val") and param_record.has_key("title"):
#                                     param_list.append(param_record)
#
#            return {"params":param_list}
#
#
    #
    #
    # Change value of a parameter
    #
    #
    #
    #
#    def set_param_for_menu_item(self, menu_item_id, par_id, par_val):
#        if(self.xml_root == None):
#            return "DB has not been opened!"
#        else:
#            menu_items = self.xml_root.getElementsByTagName("menu_item")
#            if len(menu_items) == 0:
#                return "There isn't such item id!"
#
#            for menu_item in menu_items:
#                if menu_item.nodeType == Node.ELEMENT_NODE:
#                    if menu_item.attributes.get('id').value == menu_item_id and menu_item.attributes.get('type').value == "params":
#
#                        for child in menu_item.childNodes:
#                            if child.nodeType == Node.ELEMENT_NODE and child.attributes.get('id').value == par_id:
#
#                                new_child = self.xml_doc.createElement("param")
#                                # Copy child attributes
#                                for (name, value) in child.attributes.items():
#                                     new_child.setAttribute(name, value)
#
#                                new_child.appendChild(self.xml_doc.createTextNode(par_val))
#
#                                menu_item.replaceChild(new_child, child)
#
#                                return ""
#            return "Can't change this param!"
#




    def get_session_id(self):
        session_id = None
        if(self.xml_root == None):
            return session_id
        else:
            user_settings = self.xml_root.getElementsByTagName("session")
            if user_settings[0] == None:
                return session_id

            session_id = user_settings[0].attributes.get("id").value
            return session_id


    def set_session_id(self, session_id):
        if(self.xml_root == None):
            return False
        else:
            user_settings = self.xml_root.getElementsByTagName("session")
            if user_settings[0] == None:
                print "Could not set session_id"
                return False

            user_settings[0].setAttribute("id", session_id)
            print "session_id has been updated"
            return True


    def get_admin_account(self):
        if(self.xml_root == None):
            return None
        else:
            admin_account = self.get_params_set("admin_account")

            print admin_account


            if admin_account.has_key("username") == True:
                username = admin_account["username"]["val"]
            else:
                username = ""

            if admin_account.has_key("password") == True:
                password = admin_account["password"]["val"]
            else:
                password = ""

            account = {}
            account["username"] = username
            account["password"] = password
            return account




    def update(self):
        #print self.xml_doc.toxml('utf-8')
        try:
            import re
            pretty_xml = self.xml_doc.toprettyxml(indent = "    ", encoding = "utf-8")
            text_re = re.compile(">\n\s+([^<>\s].*?)\n\s+</", re.DOTALL)
            pretty_xml = re.sub("\n[\s]+\n","\n", pretty_xml)
            formated_pretty_xml = text_re.sub(">\g<1></", pretty_xml)
            formated_pretty_xml = re.sub(">\n[\s]+</param>","></param>", formated_pretty_xml)
            f = open(self.xml_filename, 'w')
            f.write(formated_pretty_xml)
            f.close()
            os.system("sync")
        except Exception as e:
            return False
        else:
            self.xml_root = self.xml_doc.documentElement
            return True


    def update_compact(self):
        #print self.xml_doc.toxml('utf-8')
        try:
            import re
            xmlstr = re.sub(r">[\n\s\t]+<", "><",  self.xml_doc.toxml('utf-8'))
            xmlstr = re.sub(r"[\n\s\t]+<", "<",  xmlstr)
            xmlstr = re.sub(r">[\n\s\t]+", ">",  xmlstr)
            f = open(self.xml_filename, 'w')
            f.write(xmlstr)
            f.close()
            os.system("sync")
        except Exception as e:
            return False
        else:
            self.xml_root = self.xml_doc.documentElement
            return True

    #
    #
    #
    def get_wifi_networks(self):
        if(self.xml_root == None):
            return {}
        else:
            wifi_networks_record = self.xml_root.getElementsByTagName("wifi_networks")
            if len(wifi_networks_record) != 1:
                return []

            wifi_networks = wifi_networks_record[0].childNodes

            network_list = []
            for item in wifi_networks:
                if item.nodeType == Node.ELEMENT_NODE:

                    network_list_item = {}
                    for wifi_network_item in item.childNodes:
                        if wifi_network_item.nodeType == Node.ELEMENT_NODE:
                            if wifi_network_item.firstChild == None:
                                network_list_item[wifi_network_item.nodeName] = ""
                            else:
                                network_list_item[wifi_network_item.nodeName] = wifi_network_item.firstChild.nodeValue
                    network_list.append(network_list_item)
            return network_list

    #
    #
    #
    def add_wifi_network(self, network):
        if self.xml_root == None:
            return "DB has not been opened!"
        else:
            if network.has_key("bssid") == False:
                return "BSSID isn't defined!"

            wifi_networks_record = self.xml_root.getElementsByTagName("wifi_networks")
            if len(wifi_networks_record) != 1:
                return "DB can't find wifi_networks record!"


            new_network = self.xml_doc.createElement("record")
            for key in network:
                param = self.xml_doc.createElement(key)
                param.appendChild(self.xml_doc.createTextNode(network[key]))
                new_network.appendChild(param)



            # Check for network with the same BSSID
            wifi_networks = wifi_networks_record[0].childNodes
            for item in wifi_networks:
                if item.nodeType == Node.ELEMENT_NODE:
                    for wifi_network_item in item.childNodes:
                        if wifi_network_item.nodeType == Node.ELEMENT_NODE:
                            if wifi_network_item.nodeName == "bssid" and wifi_network_item.firstChild.nodeValue == network["bssid"]:
                                # Replace duplicate item
                                wifi_networks_record[0].replaceChild(new_network, item)
                                return ""

            wifi_networks_record[0].appendChild(new_network)
            return ""

    #
    #
    #
    def remove_wifi_network(self, bssid):
        if self.xml_root == None:
            return "DB has not been opened!"
        else:
            if bssid == "":
                return "BSSID isn't defined!"

            wifi_networks_record = self.xml_root.getElementsByTagName("wifi_networks")
            if len(wifi_networks_record) != 1:
                return "DB can't find wifi_networks record!"

            wifi_networks = wifi_networks_record[0].childNodes
            for item in wifi_networks:
                if item.nodeType == Node.ELEMENT_NODE:
                    for wifi_network_item in item.childNodes:
                        if wifi_network_item.nodeType == Node.ELEMENT_NODE:
                            if wifi_network_item.nodeName == "bssid" and wifi_network_item.firstChild.nodeValue == bssid:
                                wifi_networks_record[0].removeChild(item)
                                return ""

            return "Can't find network to remove!"


    def get_mac_map(self):
        if(self.xml_root == None):
            return []
        else:
            mac_record = self.xml_root.getElementsByTagName("mac_map")
            if len(mac_record) != 1:
                return []

            mac_map = mac_record[0].childNodes
            mac_list = {}
            for item in mac_map:
                if item.nodeType == Node.ELEMENT_NODE:
                    mac = "";
                    ip = "";
                    for mac_item in item.childNodes:
                        if mac_item.nodeType == Node.ELEMENT_NODE:
                            if mac_item.nodeName == "bssid":
                                mac = mac_item.firstChild.nodeValue
                            else:
                                ip = mac_item.firstChild.nodeValue

                    mac_list[mac] = ip
            return mac_list


    #
    #
    #
    def get_fh_region_details(self):
        if(self.xml_root == None):
            return []
        else:
            fh_region_details_record = self.xml_root.getElementsByTagName("fh_region_details")
            if len(fh_region_details_record) != 1:
                return []

            region_details = fh_region_details_record[0].childNodes

            region_details_list = {}
            for item in region_details:
                if item.nodeType == Node.ELEMENT_NODE:

                    region_name = "";
                    region_details = {}
                    for region_detail_item in item.childNodes:
                        if region_detail_item.nodeType == Node.ELEMENT_NODE:

                            if region_detail_item.nodeName == "name":
                                region_name = region_detail_item.firstChild.nodeValue
                            else:
                                detail = {}
                                detail["value"] = region_detail_item.firstChild.nodeValue
                                for (name, value) in region_detail_item.attributes.items():
                                    if name == "select_from":
                                        detail["select_from"] = value.split(" ")
                                    else:
                                        detail[name] = value

                                region_details[region_detail_item.nodeName] = detail

                    region_details_list[region_name] = region_details
            return region_details_list


    #
    #
    #
    def set_fh_region_details(self, region, details):
        if(self.xml_root == None):
            return "DB has not been opened!"
        else:
            fh_region_details_record = self.xml_root.getElementsByTagName("fh_region_details")
            if len(fh_region_details_record) != 1:
                return "There is no region details record"

            region_details = fh_region_details_record[0].childNodes

            for item in region_details:
                if item.nodeType == Node.ELEMENT_NODE:  # record

                    for region_detail_item in item.childNodes:
                        if region_detail_item.nodeType == Node.ELEMENT_NODE:

                            if region_detail_item.nodeName == "name":
                                if region_detail_item.firstChild.nodeValue == region:

                                    for rd_item in item.childNodes:
                                        if rd_item.nodeType == Node.ELEMENT_NODE and rd_item.nodeName != "name":

                                            if details.has_key(rd_item.nodeName):
                                                new_val = details[rd_item.nodeName]

                                                new_rd_item = self.xml_doc.createElement(rd_item.nodeName)
                                                # Copy child attributes
                                                for (name, value) in rd_item.attributes.items():
                                                    new_rd_item.setAttribute(name, value)

                                                new_rd_item.appendChild(self.xml_doc.createTextNode(new_val))
                                                item.replaceChild(new_rd_item, rd_item)
                                break
            return ""




    #
    #
    #
    def get_uhf_protocol_details(self):
        if(self.xml_root == None):
            return []
        else:
            uhf_protocol_details_record = self.xml_root.getElementsByTagName("uhf_protocol_details")
            if len(uhf_protocol_details_record) != 1:
                return []

            protocol_details = uhf_protocol_details_record[0].childNodes

            protocol_details_list = {}
            for item in protocol_details:
                if item.nodeType == Node.ELEMENT_NODE:

                    protocol_name = "";
                    protocol_details = {}
                    for protocol_detail_item in item.childNodes:
                        if protocol_detail_item.nodeType == Node.ELEMENT_NODE:

                            if protocol_detail_item.nodeName == "name":
                                protocol_name = protocol_detail_item.firstChild.nodeValue
                            else:
                                detail = {}
                                detail["value"] = protocol_detail_item.firstChild.nodeValue
                                for (name, value) in protocol_detail_item.attributes.items():
                                    if name == "select_from":
                                        detail["select_from"] = value.split(" ")
                                    else:
                                        detail[name] = value

                                protocol_details[protocol_detail_item.nodeName] = detail

                    protocol_details_list[protocol_name] = protocol_details
            return protocol_details_list


    #
    #
    #
    def set_uhf_protocol_details(self, protocol, details):
        if(self.xml_root == None):
            return "DB has not been opened!"
        else:
            uhf_protocol_details_record = self.xml_root.getElementsByTagName("uhf_protocol_details")
            if len(uhf_protocol_details_record) != 1:
                return "There is no protocol details record"

            protocol_details = uhf_protocol_details_record[0].childNodes

            for item in protocol_details:
                if item.nodeType == Node.ELEMENT_NODE:  # record

                    for protocol_detail_item in item.childNodes:
                        if protocol_detail_item.nodeType == Node.ELEMENT_NODE:

                            if protocol_detail_item.nodeName == "name":
                                if protocol_detail_item.firstChild.nodeValue == protocol:

                                    for pd_item in item.childNodes:
                                        if pd_item.nodeType == Node.ELEMENT_NODE and pd_item.nodeName != "name":

                                            if details.has_key(pd_item.nodeName):
                                                new_val = details[pd_item.nodeName]

                                                new_pd_item = self.xml_doc.createElement(pd_item.nodeName)
                                                # Copy child attributes
                                                for (name, value) in pd_item.attributes.items():
                                                    new_pd_item.setAttribute(name, value)

                                                new_pd_item.appendChild(self.xml_doc.createTextNode(new_val))
                                                item.replaceChild(new_pd_item, pd_item)
                                break
            return ""




    #
    #
    #
    def get_uhf_freqs(self):
        if(self.xml_root == None):
            return []
        else:
            uhf_freqs_record = self.xml_root.getElementsByTagName("uhf_freqs")
            if len(uhf_freqs_record) != 1:
                return []

            uhf_freqs = uhf_freqs_record[0].childNodes

            freqs_list = []
            for item in uhf_freqs:
                if item.nodeType == Node.ELEMENT_NODE:
                    if item.nodeName == "freq":
                        freqs_list.append(item.firstChild.nodeValue)

            return freqs_list

    #
    #
    #
    def set_uhf_freqs(self, freqs_list):
        if(self.xml_root == None):
            return "DB has not been opened!"
        else:
            uhf_freqs_record = self.xml_root.getElementsByTagName("uhf_freqs")
            if len(uhf_freqs_record) != 1:
                return "There is no uhf_freqs record!"

            uhf_freqs = uhf_freqs_record[0].childNodes

            for i in range(len(uhf_freqs)):
                uhf_freqs_record[0].removeChild(uhf_freqs[0])

            for freq in freqs_list:
                 new_freq = self.xml_doc.createElement("freq")
                 new_freq.appendChild(self.xml_doc.createTextNode(freq))
                 uhf_freqs_record[0].appendChild(new_freq)

            return ""







def main():
    db = xml_db("./db.xml")
    if db.open() == False:
        print "Can't open XML data base\n"
        return

#    print db.get_menu_items()
#    print db.get_param_item("modem")


#    res = db.get_params_set("ntrip_client")
#    print res

#    print res["serv_name"]["val"]

#    print db.set_params_set("ntrip_client", {"lat":"99", "lng":"120"})
 #  db.update()
 #
 #   db.update_compact()

#    print db.get_uhf_freqs()
    #print db.set_uhf_freqs(["123456789", "345345"])
#    print db.xml_doc.toxml('utf-8')
    print db.set_uhf_protocol_details("Javad", {"channel_spacing":"35", "fec":"test"})
    print db.xml_doc.toxml('utf-8')
    #db.update()

#    print db.get_wifi_networks()

    #net = {"bssid":"00:11:22:00:44:55", "ssid":"tets"}
    #print db.add_wifi_network(net)
    #print db.remove_wifi_network("00:11:22:33:44:55")

    #print db.xml_doc.toxml('utf-8')


if __name__ == '__main__':
    main()


