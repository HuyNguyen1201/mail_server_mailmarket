import threading
import gen_mail
import time
import mail_thread
import copy
import threading
from id_order import get_id

mail_dict = dict()
clear_time = 30*60

def gen_mail_thread(mail_list):
    global mail_dict
    mail, token = gen_mail.gen_mail()
    id = get_id()
    mail_dict[id] = [time.time(), token,'',0]
    mail_list.append([id,mail])

def run_gen_mail(count):
    mail_list = []
    threads = []
    for i in range(count):
        thread = threading.Thread(target=gen_mail_thread,args=(mail_list,))
        threads.append(thread)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return mail_list


def clear_mail():
    global mail_dict, clear_time
    try:
        keys = list(mail_dict.keys())
        for k in keys:
            if time.time()-mail_dict[k][0] > clear_time:
                del mail_dict[k]
    except:
        print('delete mail fail')


def read_mail(id):
    global mail_dict
    if id in mail_dict.keys():
        # if time.time() - mail_dict[mail][2] > 3:
        # mail_dict[mail][2] = time.time()
        return gen_mail.read_mail(mail_dict,id)
        # mail_dict[mail][2] = time.time()
        # return False, 'please slow down, preferably every 3 seconds'
    else:
        return 202, 'mail is not available or expired'
