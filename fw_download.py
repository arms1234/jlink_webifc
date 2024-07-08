#!/usr/bin/env python



import gobject

import dbus
import dbus.service
import dbus.mainloop.glib
import shlex
import subprocess
import os

os.environ["DISPLAY"]=":0.0"

class fw_download(dbus.service.Object):

    @dbus.service.method("com.fwdownload.ctrliface", in_signature='a{ss}', out_signature='a{ss}')
    def start_download(self, params):
        self.fname     = params["fname"].encode('ascii') 
        self.fsize     = params["fsize"].encode('ascii')   
        self.tmp_dir   = params["tmp_dir"].encode('ascii') 
        ip_addr        = params["ip_addr"].encode('ascii')  

        self.file_sha256sum = params["fsha256sum"].encode('ascii')  


       
        cmd_line = "/usr/bin/tftp -g -r " + self.fname + " -l " + self.tmp_dir + self.fname + " " + ip_addr; 
        args = shlex.split(cmd_line)
        #print cmd_line
        #print args

        self.p = subprocess.Popen(args) #, shell=True) #, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        #for line in p.stderr.readlines():
        #    print line

        #for line in p.stdout.readlines():
        #    print line

        
        if self.p.poll() ==  None:
            return {"err":"0", "errmsg":""}
        else: 
            mainloop.quit()   
            return {"err":"1", "errmsg":"Can't start downloading!"}



    @dbus.service.method("com.fwdownload.ctrliface", in_signature='', out_signature='a{ss}')
    def check_download_status(self):

        file_name = self.tmp_dir + self.fname
        if os.path.exists(file_name) == True:
            fsize = os.path.getsize(file_name)
            progress_proc = int(100 * float(fsize)/float(self.fsize))
        else:
            progress_proc = int(0);

        ret_code = self.p.poll()       
        if ret_code == None:
            return {"err":"0", "errmsg":"", "status":"download_proc", "progress":str(progress_proc)}

        if ret_code == 0:
            mainloop.quit()
            sha256_sum = os.popen("./sha256sum " + file_name).read().rstrip("\n")

            if (progress_proc == int(100)) and (sha256_sum == self.file_sha256sum):
                return {"err":"0", "errmsg":"", "status":"download_done", "progress":str(progress_proc)}
            else:
                return {"err":"1", "errmsg":"Incorrect CRC!", "status":"download_done", "progress":str(progress_proc)}

        return {"err":"0", "errmsg":""}



    @dbus.service.method("com.fwdownload.ctrliface", in_signature='', out_signature='')
    def Exit(self):
        mainloop.quit()


if __name__ == '__main__':
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    
#    os.system("env")
    
#    p = subprocess.Popen('dbus-launch', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#    for var in p.stdout:
#	sp = var.split('=', 1)
#        print sp
#        os.environ[sp[0]] = sp[1][:-1]    

    session_bus = dbus.SessionBus()   
    name = dbus.service.BusName("com.fwdownload.service", session_bus)
    object = fw_download(session_bus, '/fwdownload')

    mainloop = gobject.MainLoop()
    print "Running firmware download service \n"
    mainloop.run()
