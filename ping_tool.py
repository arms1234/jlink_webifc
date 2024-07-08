
#!/usr/bin/python


import os, time
#import tempfile
import signal



interchange_file = "/dev/shm/ping_file"


class TimeoutException(Exception): 
    pass 



def ping_begin(addr, iface):
    if addr == "" or addr == None or iface == "" or iface == None:
        return (False, "")

    def timeout_handler(signum, frame):
        raise TimeoutException()

        
    #interchange_file = tempfile.mktemp()
    pid = os.fork()
    if pid == 0:
        os.execl("/jlinklte/scripts/do_ping", "do_ping", "-c5", "-I" + iface, addr, interchange_file)
        return (True, "")



    time.sleep(1)        


    try:            
        reader = open(interchange_file, 'r')
    except Exception as e:
        return (False, e)



    #old_handler = signal.signal(signal.SIGALRM, timeout_handler) 
    #signal.alarm(5) # triger alarm in x seconds


    try: 
        while 1:
            line = reader.readline() 
            if line !='' and line != None:
                #signal.alarm(0)
                #signal.signal(signal.SIGALRM, old_handler)     
                reader.close() 
                return (True, line)


    except TimeoutException:
        #signal.signal(signal.SIGALRM, old_handler)  
        reader.close()   
        os.kill(pid, 0)
        os.remove(interchange_file)         
        return (False, "Timeout expired")




def ping_next():
    def timeout_handler(signum, frame):
        raise TimeoutException()


    try:            
        reader = open(interchange_file, 'r')
    except Exception as e:
        os.remove(interchange_file)         
        return (False, e)



    #old_handler = signal.signal(signal.SIGALRM, timeout_handler) 
    #signal.alarm(5) # triger alarm in x seconds

    ret_str = ""

    try: 
        while 1:
            line = reader.readline() 
            if line =='' or line == None:
                #signal.alarm(0)
                #signal.signal(signal.SIGALRM, old_handler)     
                reader.close()    
                if prev_line == 'Ok\n':
                    os.remove(interchange_file)         
                    return (2, ret_str)
                return (True, ret_str)
            else:
                prev_line = line
                ret_str = ret_str + line



    except TimeoutException:
        #signal.signal(signal.SIGALRM, old_handler)  
        reader.close()   
        os.remove(interchange_file)         
        return (False, "Timeout expired")






def test_ping():
    res, str = ping_begin("www.ru")
    if res == False:
        print "Error ", str
        return

    print str
   
    time.sleep(1) 

    while 1:
        res, str = ping_next()

        if res == False:
            print "Error ", str
            return

        print str
        if res == 2: 
            return

        print "\n"
        print "\n"


        time.sleep(1)  





if __name__ == '__main__':
    test_ping()

