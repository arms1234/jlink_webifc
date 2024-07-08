

import web
import sys
import json
import os
import time
import session


from menu import build_menu
from xml_db import xml_db
from perror import PageError

render = web.template.render('templates/')

fw_dscr_file = "jlinkltefw.dsr"
tmp_dir_path = "/dev/shm/"
get_fw_dscr_file_cmd = "tftp -g -r " +  fw_dscr_file + " -l " + tmp_dir_path + fw_dscr_file +" "

kernel_mtd_dev_pri  = "/dev/mtd3"
kernel_mtd_bdev_pri = "/dev/mtdblock3"
kernel_mtd_dev_sec  = "/dev/mtd4"
kernel_mtd_bdev_sec = "/dev/mtdblock4"
kernel_addr_pri     = "0x280000"
kernel_addr_sec     = "0x780000"


fs_mtd_dev_pri      = "/dev/mtd5"
fs_mtd_bdev_pri     = "/dev/mtdblock5"
fs_mtd_dev_sec      = "/dev/mtd6"
fs_mtd_bdev_sec     = "/dev/mtdblock6"
fs_dev_num_pri      = "5"
fs_dev_num_sec      = "6"


printenv_util       = "/jlinklte/utils/fw_printenv"
setenv_util         = "/jlinklte/utils/fw_setenv"

uhf_upgrade_init_script = "/jlinklte/scripts/uhf_upgrade_init"
pwbrd_upgrade_init_script = "/jlinklte/scripts/pwbrd_upgrade_init"


#update_mode = 3 #update2__mode__common = 0, update2__mode__release = 1, update2__mode__prerelease = 2, update2__mode__testing = 3


def make_management_page():
    db = xml_db()
    if db.open() == False:
        raise PageError("Could not open configuration storage")

    admin_account = db.get_admin_account()
    if admin_account == None:
        raise PageError("There is no Admin Account")

    admin_login = admin_account["username"]
    admin_pwd   = admin_account["password"]


    content = """$def with (admin_login, admin_pwd) \n
    <script type="text/javascript" src="/static/admin.js"></script>

    <form name="setup">
	<fieldset>
	<legend>Admin Account</legend>
	<div class="setting"><div class="label">Device Login:</div><input maxlength="32" size="20" id="admin_login" value="$admin_login" /></div>
	<div class="setting"><div class="label">Device Password:</div><input type="password" maxlength="63" size="20" value="$admin_pwd" id="admin_pwd" onblur="valid_name(this,'Password',SPACE_NO)" /></div>
	<div class="setting"><div class="label">Re-enter to confirm:</div><input type="password" maxlength="63" size="20" value="$admin_pwd" id="admin_pwd_conf" onblur="valid_name(this,'Password',SPACE_NO)" />
    </div>
	</fieldset>
    <br />
    <div class="submitFooter">
    <input type="button" value="Save Settings" onclick=save_admin_settings() />
    <input type="reset" value="Cancel Changes" />
    </div>
    <div class="submitFooter">
    <input type="button" value="Default" onclick=def_cfg() />
    <input type="button" value="Reboot" onclick=reboot_device() />
    <input type="button" value="Switch Off" onclick=switch_off_device() />
    <input type="button" value="Logout" onclick="parent.logout()" />
    </div>
    </form>
    """

    content = web.template.Template(content)


    return content(admin_login, admin_pwd)

# <input type="button" value="Logout" onclick="window.location.replace('/logout')" />

def make_fwupgrade_page_prev():

    content = """
    <script type="text/javascript" src="/static/upgrade.js" ></script>
    <h2>Firmware Upgrade</h2>

    <fieldset>
    <legend>UHF Int.</legend>
    <div class="setting"><div class="label">Firmware filename:</div><input maxlength="32" size="20" id="uhf_fw_name" /></div>
    <br/>
    <div class="submitFooter"><input id="uhf_upgrade_btn" type="button" value="Upgrade" onclick=uhf_upgrade() /></div>
    </fieldset>
    <br/>
    <br/>
    <fieldset>
    <legend>Power board</legend>
    <div class="setting"><div class="label">Firmware filename:</div><input maxlength="32" size="20" id="pwbrd_fw_name" /></div>
    <br/>
    <div class="submitFooter"><input id="pwbrd_upgrade_btn" type="button" value="Upgrade" onclick=pwbrd_upgrade() /></div>
    </fieldset>
    <br/>
    """
    return content


def make_fwupgrade_page():

    import dbus
    bus = dbus.SessionBus()
    try:
        remote_object = bus.get_object("jlinklte.updated", "/")
        iface = dbus.Interface(remote_object, "jlinklte.updated.interface")
        updatable_parts = iface.get_updatable_parts()
    except dbus.DBusException:
        updatable_parts = []


    if updatable_parts != []:
        update_mode = updatable_parts["kernel_jlinklte"][3]
    else:
        update_mode = "1"


    content = """$def with (update_mode) \n
    <script type="text/javascript" src="/static/fwupdate.js" ></script>
    <form name="setup">
    <fieldset>
    <legend>Firmware Upgrade</legend>

    <div class="label"><h2>Versions Branch:
        $if update_mode == "1":
                <input type="radio" id="release" name="branch" checked="checked" value="1" onclick="update_mode_changed(this)"/><label>Release(recomended)</label>
                <input type="radio" id="prerelease" name="branch" value="2" onclick="update_mode_changed(this)"/><label>Prerelease</label>
                <input type="radio" id="test" name="branch" value="3" onclick="update_mode_changed(this)"/><label>Test</label>
            </div>
        $elif update_mode == "2":
                <input type="radio" id="release" name="branch" value="1" onclick="update_mode_changed(this)"/><label>Release(recomended)</label>
                <input type="radio" id="prerelease" name="branch" checked="checked" value="2" onclick="update_mode_changed(this)"/><label>Prerelease</label>
                <input type="radio" id="test" name="branch" value="3" onclick="update_mode_changed(this)"/><label>Test</label>
            </div>
        $else:
                <input type="radio" id="release" name="branch" value="1" onclick="update_mode_changed(this)"/><label>Release(recomended)</label>
                <input type="radio" id="prerelease" name="branch" value="2" onclick="update_mode_changed(this)"/><label>Prerelease</label>
                <input type="radio" id="test" name="branch" checked="checked" value="3" onclick="update_mode_changed(this)"/><label>Test</label>
            </h2></div>

    <table id="fw_tbl" class="fw_tbl" width="100%" cellpadding="0" cellspacing="0" style="table-layout:fixed;">
    <thead class="fw_tbl_hdr"><tr><th>Firmware</th><th>Current</th><th>Update</th><th>Size</th><th/></tr></thead>
    <tbody>
    """

    if updatable_parts != []:
         length = len(updatable_parts);
         fw_list_prio = [None] * length;
         for (fw_id, fw_description) in updatable_parts.iteritems():
             prior = int(fw_description[2]);
             if prior >= length:
                 prior = length - 1
             fw_list_prio[prior] = fw_id

         #for (fw_id, fw_description) in updatable_parts.iteritems():
         #    content += "<tr id=\"" + fw_id + "\"><td>" + fw_description[0] + "</td><td>" + fw_description[1] + "</td><td/><td/><td><input type=\"checkbox\"></td></tr>"

         prio = 0;
         for fw_id in fw_list_prio:
             fw_description = updatable_parts[fw_id]
             if fw_id == "kernel_jlinklte" or fw_id == "fs_jlinklte" or fw_id == "gsm":
                 content += "<tr id=\"" + fw_id + "\" uprio=\"" + str(prio) + "\" umode=\""+ fw_description[3] +"\"><td>" + fw_description[0] + "</td><td>" + fw_description[1] + "</td><td/><td/><td><input id=\"in_" + fw_id + "\" type=\"checkbox\" onclick=update_checkbox(\"in_" + fw_id + "\")></td></tr>"
             else:
                 content += "<tr id=\"" + fw_id + "\" uprio=\"" + str(prio) + "\" umode=\""+ fw_description[3] +"\"><td>" + fw_description[0] + "</td><td>" + fw_description[1] + "</td><td/><td/><td><input type=\"checkbox\"></td></tr>"
             prio = prio + 1

    content += """
    </tbody></table>
    </fieldset>
    </form>
    <br/>
    <div class="submitFooter">
    <input id="check_btn" type="button" value="Check for update" onclick=check_for_update() />
    <input id="update_btn" type="button" value="Update" onclick=update() />
    </div>

    """
    content = web.template.Template(content)
    return content(update_mode)


def update_mode_changed(query):
    fw_mode = query["fw_mode"]

    db = xml_db()
    if db.open() == False:
        raise PageError("Could not open configuration storage!")

    res = db.set_update_mode(fw_mode)

    if res == "":
        db.update()
        return {"err":"0", "errmsg":""}
    else:
        return {"err":"1", "errmsg":"Could not save settings"}



def check_for_update(query):
    fw_id_list = json.loads(query["fw_id"])
    fw_mode = json.loads(query["fw_mode"])

    import dbus
    update_info_resp = {}
    bus = dbus.SessionBus()
    try:
        remote_object = bus.get_object("jlinklte.updated", "/")
        iface = dbus.Interface(remote_object, "jlinklte.updated.interface")

        for fw_id in fw_id_list:
            update_mode = int(fw_mode[fw_id])
            update_info = iface.part_check_for_update(fw_id, update_mode)
            print update_info

            if update_info.has_key("Error"):
                update_info_resp[fw_id] = ["not available", "", ""]
            else:
                ver = update_info["VMajor"] + "." + update_info["VMinor"] + "." + update_info["VMaintanence"] + "." + update_info["VBuild"]
                update_info_resp[fw_id] = [ver, update_info["Size"], update_info["Name"]]

    except dbus.DBusException:
        return {"err":"1", "errmsg":"Could not perform update checking!"}


    #print  json.dumps({"err":"0", "update_info": update_info_resp})

    return json.dumps({"err":"0", "update_info": update_info_resp})


def update_download_initiate(query):

    update_info = json.loads(query["update_info"])
    fw_id = query["fw_id"]

    print fw_id
    print update_info

    import dbus
    bus = dbus.SessionBus()
    try:
        remote_object = bus.get_object("jlinklte.updated", "/")
        iface = dbus.Interface(remote_object, "jlinklte.updated.interface")

        size = update_info[2]
        ver  = update_info[1].split(".")
        update_mode = int(update_info[3])

        ret = iface.part_download_update(fw_id, int(ver[0]), int(ver[1]), int(ver[2]), int(ver[3]), int(size) , update_mode)

        if ret != 0:
            return {"err":"1", "errmsg":"Could not perform update initiate!"}


    except dbus.DBusException:
        return {"err":"1", "errmsg":"Could not perform update initiate!"}

    return {"err":"0"};


def get_download_status(query):
    import dbus
    bus = dbus.SessionBus()
    try:
        remote_object = bus.get_object("jlinklte.updated", "/")
        iface = dbus.Interface(remote_object, "jlinklte.updated.interface")

        status = iface.get_download_status()

        print status

    except dbus.DBusException:
        return {"err":"1", "errmsg":"Could not get download status!"}

    return json.dumps({"err":"0", "status":status});


def get_completion_status(query):
    import dbus
    bus = dbus.SessionBus()
    try:
        remote_object = bus.get_object("jlinklte.updated", "/")
        iface = dbus.Interface(remote_object, "jlinklte.updated.interface")

        status = iface.get_download_res()

    except dbus.DBusException:
        return {"err":"1", "errmsg":"Could not get completion status!"}

    return json.dumps({"err":"0", "cstatus":status});


def update_apply_initiate(query):
    import dbus
    bus = dbus.SessionBus()
    try:
        remote_object = bus.get_object("jlinklte.updated", "/")
        iface = dbus.Interface(remote_object, "jlinklte.updated.interface")

        update_info = json.loads(query["update_info"])
        update_info_files = list(update_info.keys())

        ##if len(update_info_files) != 1:
        ##    return {"err":"1", "errmsg":"Update info is incorrect!"}

        update_file_name = update_info_files[0]
        update_file_md5  = update_info[update_file_name]
        res = iface.update_apply({"fw_id":query["fw_id"], "fw_size":query["fw_size"], "fw_ver":query["fw_ver"], "fname":update_file_name, "md5":update_file_md5})

        if res != 0:
            return {"err":"1", "errmsg":"Could not update apply initiate!"}

    except dbus.DBusException:
        return {"err":"1", "errmsg":"Could not update apply initiate!"}

    return json.dumps({"err":"0"});


def get_update_apply_status(query):
    import dbus
    bus = dbus.SessionBus()
    try:
        remote_object = bus.get_object("jlinklte.updated", "/")
        iface = dbus.Interface(remote_object, "jlinklte.updated.interface")

        status = iface.get_update_apply_status()
    except dbus.DBusException:
        return {"err":"1", "errmsg":"Could not update apply status!"}

    print status

    return json.dumps({"err":"0", "status": status});



#    <fieldset>
#    <legend>Firmware server</legend>
#    <div class="setting">
#        <div class="label">Firmware server IP address:</div>
#        <input size="3" maxlength="3" class="num" name="fw_server_ip_0" onblur="valid_range(this,0,255,'IP')" value="192" />.
#        <input size="3" maxlength="3" class="num" name="fw_server_ip_1" onblur="valid_range(this,0,255,'IP')" value="168" />.
#        <input size="3" maxlength="3" class="num" name="fw_server_ip_2" onblur="valid_range(this,0,255,'IP')" value="0" />.
#        <input size="3" maxlength="3" class="num" name="fw_server_ip_3" onblur="valid_range(this,0,255,'IP')" value="1" />
#    </div>
#    </fieldset>
#    <br/>
#
#    <div class="submitFooter">
#    <input id="krnl_upgrd_id" type="button" value="Upgrade Kernel" onClick=fw_upgrade(\"krnl\") />
#    <input id="fs_upgrd_id" type="button" value="Upgrade File system" onClick=fw_upgrade(\"fs\") />
#    </div>




def save_admin_settings(query):
    db = xml_db()
    if db.open() == False:
        raise PageError("Could not open configuration storage!")

    query.pop("cmd")

    res = db.set_params_set("admin_account", query)

    if res == "":
        db.update()
        return {"err":"0", "errmsg":""}
    else:
        return {"err":"1", "errmsg":"Could not save settings"}




def parse_fw_descriptor_file(filename):
    res={}
    try:
        f = open(filename)
        line = f.readline()
        while line:
            #print line
            spl=line.split("=")
            if len(spl) == 2:
                res[spl[0]] = spl[1].rstrip("\n")

            line = f.readline()
    except IOError as e:
        raise PageError("Could not read firmware descriptor file!")

    f.close()
    return res

#
# Convert dbus dictionary to normal dictionary
#
def dbus_dict_to_dict(dbus_dict):
    out_dict = {}
    keys = list(dbus_dict)
    for key in keys:
        out_dict[str(key)] = str(dbus_dict[key])

    return out_dict






def fw_upgrade_proc(query):
    if query.cmd == None:
        raise PageError("Type of operation is not defined!")

    if query.cmd == "check_fw_avl":
        #print get_fw_dscr_file_cmd + query.ip_addr
        res = os.system(get_fw_dscr_file_cmd + query.ip_addr + " > /dev/null 2>&1")
        if res != 0:
            raise PageError("Could not get Device firmware descriptor file!")
        else:
            # Parse firmware descriptor file
            fw_info = parse_fw_descriptor_file(tmp_dir_path + fw_dscr_file)
            resp = {"err":"0", "errmsg":""}
            resp.update(fw_info)

            # Acquire current firmware info
            if query.fw_type == "krnl":
                cur_fw_ver = os.popen("./fw_printenv kernel_ver 2>/dev/null").read().rstrip("\n")
            elif query.fw_type == "fs":
                cur_fw_ver = os.popen("./fw_printenv fs_ver 2>/dev/null").read().rstrip("\n")
            else:
                raise PageError("Type of firmware is not defined!")

            if cur_fw_ver != None and cur_fw_ver != "":
                 spl = cur_fw_ver.split("=")
                 if len(spl) == 2:
                     resp["cur_fw_ver"] = spl[1]

            #print resp
            return resp

    elif query.cmd == "download_fw":
        #print query
        res = os.system("/usr/bin/python fw_download.py > /dev/null &")
        if res != 0:
            return {"err":"1", "errmsg":"Could not start download daemon!"}


        time.sleep(4.0)

        import dbus

        bus = dbus.SessionBus()
        try:
            remote_object = bus.get_object("com.fwdownload.service", "/fwdownload")
            iface = dbus.Interface(remote_object, "com.fwdownload.ctrliface")
            query.update({"tmp_dir":tmp_dir_path})
            res = iface.start_download(query)
            return dbus_dict_to_dict(res)

        except dbus.DBusException:
            return {"err":"1", "errmsg":"Can't communicate with download daemon!"}

        return {"err":"0", "errmsg":""}

    elif query.cmd == "check_fw_downloading":

        import dbus
        bus = dbus.SessionBus()
        try:
            remote_object = bus.get_object("com.fwdownload.service", "/fwdownload")
            iface = dbus.Interface(remote_object, "com.fwdownload.ctrliface")
            res = iface.check_download_status()
            return dbus_dict_to_dict(res)

        except dbus.DBusException:
            return {"err":"1", "errmsg":"Can't communicate with download daemon!"}

        return {"err":"0", "errmsg":""}


    elif query.cmd == "save_fw":
        fname          = query["fname"].encode('ascii')
        fsize          = query["fsize"].encode('ascii')
        fver           = query["fver"].encode('ascii')
        file_sha256sum = query["fsha256sum"].encode('ascii')
        fw_type        = query["fw_type"].encode('ascii')


        if fw_type == "krnl":
            cur_kernel_addr = os.popen("./fw_printenv kernel_addr 2>/dev/null").read().rstrip("\n")

            if cur_kernel_addr != None:
                tmp = cur_kernel_addr.split("=")
                if len(tmp) == 2:
                    cur_kernel_addr = tmp[1]
                else:
                    cur_kernel_addr = ""
            else:
                cur_kernel_addr = ""


            if cur_kernel_addr == kernel_addr_pri:
                mtd_dev  = kernel_mtd_dev_sec
                mtd_bdev = kernel_mtd_bdev_sec
                new_kernel_addr = kernel_addr_sec
            else:
                mtd_dev  = kernel_mtd_dev_pri
                mtd_bdev = kernel_mtd_bdev_pri
                new_kernel_addr = kernel_addr_pri

        elif fw_type == "fs":
            cur_fs_dev_num = os.popen("./fw_printenv fs_dev_num 2>/dev/null").read().rstrip("\n")


            if cur_fs_dev_num != None:
                tmp = cur_fs_dev_num.split("=")
                if len(tmp) == 2:
                    cur_fs_dev_num = tmp[1]
                else:
                    cur_fs_dev_num = ""
            else:
                cur_fs_dev_num = ""


            if cur_fs_dev_num == fs_dev_num_pri:
                mtd_dev  = fs_mtd_dev_sec
                mtd_bdev = fs_mtd_bdev_sec
                new_fs_dev_num = fs_dev_num_sec
            else:
                mtd_dev  = fs_mtd_dev_pri
                mtd_bdev = fs_mtd_bdev_pri
                new_fs_dev_num = fs_dev_num_pri
        else:
            raise PageError("Type of firmware is not defined!")


        # Erase NAND flash
        res = os.system("flash_eraseall " + mtd_dev + "> /dev/null 2>&1")
        if res != 0:
            raise PageError("Could not erase MTD partition!")


        # Save loaded firmware in NAND
        res = os.system("nandwrite -p " + mtd_dev + " " + tmp_dir_path + fname + "> /dev/null 2>&1")
        if res != 0:
            raise PageError("Could not save firmware in MTD partition!")

        # Checksum verifycation
        sha256_sum = os.popen("./sha256sum " + "-n " + fsize + " " + mtd_bdev).read().rstrip("\n")

        if file_sha256sum != sha256_sum:
            raise PageError("Could not save firmware in MTD partition correctly!")

        os.system("rm " + tmp_dir_path + fname)
        os.system("rm " + tmp_dir_path + fw_dscr_file)


        if fw_type == "krnl":

            res = os.system("./fw_setenv kernel_ver " + fver)
            if res != 0:
                raise PageError("Can't save kernel version in environment!")

            res = os.system("./fw_setenv kernel_size " + hex(int(fsize)))
            if res != 0:
                raise PageError("Could not save kernel size in environment!")

            #res = os.system("./fw_setenv kernel_chsum " + file_sha256sum)
            #if res != 0:
            #    raise PageError("Can't save kernel checksum in environment!")

            res = os.system("./fw_setenv kernel_addr " + new_kernel_addr)
            if res != 0:
                raise PageError("Could not save kernel address in environment!")


        elif fw_type == "fs":

            res = os.system("./fw_setenv fs_ver " + fver)
            if res != 0:
                raise PageError("Could not save file system version in environment!")

            #res = os.system("./fw_setenv fs_size " + hex(int(fsize)))
            #if res != 0:
            #    raise PageError("Can't save file system size in environment!")

            #res = os.system("./fw_setenv fs_chsum " + file_sha256sum)
            #if res != 0:
            #    raise PageError("Can't save file system checksum in environment!")

            res = os.system("./fw_setenv fs_dev_num " + new_fs_dev_num)
            if res != 0:
                raise PageError("Could not save FS MTD device number in environment!")


        return {"err":"0", "errmsg":""}


def switch_off_device(query):
    os.system("jlink shutdown")
    return {"err":"0", "errmsg":""}


def reboot_device(query):
    os.system("jlink reboot")
    return {"err":"0", "errmsg":""}


def def_cfg(query):
    os.system("jlink def_cfg; jlink reboot")
    return {"err":"0", "errmsg":""}


#mmcblk0p1
def uhf_upgrade_init(query):
    import os.path
    if os.path.exists("/media/card/" + query["filename"]) == True:
        import subprocess
        proc = subprocess.Popen(uhf_upgrade_init_script + " /media/card/" + query["filename"], shell=True)
        res = proc.wait()
        if res != 0:
            return {"err":"1", "errmsg":"Could not initiate firmware upgrading"}
        else:
            return {"err":"0", "errmsg":""}
    else:
        return {"err":"1", "errmsg":"Could not find firmware file"}

def uhf_upgrade_get_status(query):
    import dbus

    bus = dbus.SessionBus()
    try:
        remote_object = bus.get_object("jlinklte.uhfd.service", "/obj")
        iface = dbus.Interface(remote_object, "jlinklte.uhfd.interface")
        update_status = iface.uhf_get_fw_update_status()

    except dbus.DBusException:
        raise PageError("Could not get upgrading status!")

    ret_status = {"err":"0", "errmsg":"", "status":update_status["update_state"]}

    if update_status.has_key("loading_progress") == True:
        ret_status["progress"] = update_status["loading_progress"]


    #print json.dumps(ret_status)

    return json.dumps(ret_status)


def pwbrd_upgrade_init(query):
    import os.path
    if os.path.exists("/media/card/" + query["filename"]) == True:
        import subprocess
        proc = subprocess.Popen(pwbrd_upgrade_init_script + " /media/card/" + query["filename"], shell=True)
        res = proc.wait()
        if res != 0:
            return {"err":"1", "errmsg":"Could not initiate firmware upgrading"}
        else:
            return {"err":"0", "errmsg":""}
    else:
        return {"err":"1", "errmsg":"Could not find firmware file"}



cmd_handlers = {"save_admin_settings": save_admin_settings,
                  "switch_off_device": switch_off_device,
                      "reboot_device": reboot_device,
                      "def_cfg": def_cfg,
                   "uhf_upgrade_init": uhf_upgrade_init,
             "uhf_upgrade_get_status": uhf_upgrade_get_status,
                 "pwbrd_upgrade_init": pwbrd_upgrade_init,
                   "check_for_update": check_for_update,
                   "update_mode_changed": update_mode_changed,
           "update_download_initiate": update_download_initiate,
                "get_download_status": get_download_status,
              "get_completion_status": get_completion_status,
              "update_apply_initiate": update_apply_initiate,
            "get_update_apply_status": get_update_apply_status }

class admin:
    def GET(self):
        if session.check_session() == False:
            return
        path = web.ctx.path
        content = ""
        try:
            if (path == "/admin" or path == "/management"):
                menu = build_menu("Administration", "Management")
                content = make_management_page()
            elif (path == "/fwupgrade"):
                menu = build_menu("Administration", "Firmware Upgrade")
                content = make_fwupgrade_page()


        except PageError as perr:
            content = perr.errmsg

        return render.webiface(menu, content)



    def POST(self):
        #if session.check_session() == False:
        #    return

        query = web.input()
        print query

        if query.has_key("cmd") == None:
            return {"err":"1", "errmsg":"There is no cmd field!"}


        try:
            if cmd_handlers.has_key(query.cmd) != None:
                return cmd_handlers[query.cmd](query)
            else:
                return {"err":"1", "errmsg":"There is no correct cmd field!"}

        except PageError as perr:
            return {"err":"1", "errmsg":perr.errmsg}

        return {"err":"0", "errmsg":""}








