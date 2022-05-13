import threading
import time
import os
import id_order
import log
mail_list = []
mail_dict = dict()
time_life = 12*60*60

def add_mail(mail,password,n_time=0):
    mail_list.append([mail,password,int(time.time()),n_time,-600])

def get_mail():
    global mail_list,mail_dict
    while True:
        if len(mail_list)<=0:
            return 300,'mail is out of stock'
        mail,password, start_time,n_time,use_time = mail_list.pop(0)
        if time.time()-use_time>0:#6*63:
            break
        continue
    if n_time <1:
        mail_list.append([mail,password,start_time,n_time + 1,int(time.time())])
    # save idorder
    id = id_order.get_id()
    mail_dict[id] = {'time': time.time(),
                        'code': 0,
                        'ready_get_code': False,
                        'is_getting_code': False,
                        'mail': mail,
                        'password': password,
                        'n_get_code': 5}
    print(mail_list)
    return 200,id

def get_request_code(orderid):
    global mail_dict
    orderid = int(orderid)
    if orderid not in mail_dict.keys():
        return 401, 'orderid is not exist'
    if mail_dict[orderid]['code'] != 0:
        return 405, 'mail is got an otp'
    mail_elm = mail_dict[orderid]
    if mail_elm['n_get_code'] <=0:
        return 402, 'get code many times'
    if mail_dict[orderid]['is_getting_code'] or mail_dict[orderid]['ready_get_code']:
        return 403,'a request is being processed'
    mail_dict[orderid]['ready_get_code'] = True
    mail_dict[orderid]['n_get_code'] -= 1
    return 200,'starting get code'

def save_mail():
    global mail_list,time_life
    for i in range(len(mail_list)-1,-1,-1):
        if time.time() - mail_list[i][2] >time_life:
            del mail_list[i]
    with open('mail_list.txt', 'w') as f:
        mail_list_str = []
        for m in mail_list:
            mail_list_str.append('|'.join([str(i) for i in m]))
        f.write('\n'.join(mail_list_str))

def get_log():
    global mail_list
    zero = 0
    one = 0
    for m in mail_list:
        if m[3] == 0:
            zero += 1
        elif m[3] == 1:
            one +=1
    return {'zero':zero,'one':one,'sum':zero + one}

def get_code(id):
    global mail_dict
    id = int(id)
    if id in mail_dict.keys():
        if mail_dict[id]['code'] == 0 and mail_dict[id]['ready_get_code'] == False and not mail_dict[id]['is_getting_code']:
            return 401, 'you have to post a request to start getting code first'
        if mail_dict[id]['code'] == 0:
            return 300,"mail is logging in to get code"
        elif mail_dict[id]['code'] == -1:
            return 400,"mail has died"
        elif mail_dict[id]['code'] == 1:
            return 600,"get code fail"
        else:
            return 200,mail_dict[id]['code']
    return 500, "order id is not exist"


def post_code(id, code):  # local
    id = int(id)
    global mail_dict
    try:
        if id in mail_dict.keys():
            mail_dict[id]['is_getting_code'] = False
            mail_dict[id]['ready_get_code'] = False
            if mail_dict[id]['code'] != 0:
                return 300, 'added code before'
            if code != -1 and code != 1:
                log.add_log(1)
                mail_dict[id]['code'] = code
            else:
                if code == -1:
                    log.add_log(3)
                else:
                    log.add_log(2)
                mail_dict[id]['code'] = code
        return 200, 'post code successfully'
    except:
        return 100, 'unknown error'


def get_task():
    global mail_dict
    for i in range(3):
        id_list = list(mail_dict.keys())
        for id in id_list:
            if id in mail_dict.keys():
                detail = mail_dict[id]
                if detail['ready_get_code']:
                    mail_dict[id]['ready_get_code'] = False
                    mail_dict[id]['is_getting_code'] = True
                    return 200, str(id) + '|' + detail['mail'] +'|' +  detail['password'] + '|' + str(detail['code'])
    return 100, 'there is not any new task'



def run_save_mail():
    while True:
        time.sleep(20)
        save_mail()


def run_clear_mail():
    global mail_dict
    while True:
        time.sleep(10)
        keys = list(mail_dict.keys())
        for key in keys:
            date = mail_dict[key]['time']
            if time.time()-date > 6*60:
                del mail_dict[key]




if os.path.exists('mail_list.txt'):
    with  open('mail_list.txt', 'r') as f:
        data = f.read().strip().split('\n')
        if data[0] != '':
            for d in data:
                d = d.split('|')
                mail_list.append([d[0],d[1],int(d[2]),int(d[3]),int(d[4])])

threading.Thread(target=run_clear_mail).start()
threading.Thread(target=run_save_mail).start()