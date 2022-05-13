from itertools import count
from flask import Flask, json, request, jsonify
import os
import temp_mail_store
import hot_mail_store
import mail_thread
import threading

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

app = Flask(__name__)


@app.route("/", methods=['GET'])
def helloworld():
    return '''<h1>Mail server</h1>'''

@app.route("/api/create-request", methods=['GET'])
def get_mail():
    serviceId_list = [1,2] # 1 tempmail
    # action=create-request&serviceId=3&count=1
    args_dict = request.args.to_dict()
    params = list(args_dict.keys())
    if 'serviceId' not in params:
        return jsonify({'status': 401, 'message': 'serviceId is not exist'})
    if not args_dict['serviceId'].isdigit() or int(args_dict['serviceId']) not in serviceId_list:
        return jsonify({'status': 402, 'message': 'serviceId is invalid'})
    count = 1
    if 'count' in params and args_dict['count'].isdigit() and int(args_dict['count']) > 1:
        count = int(args_dict['count']) 
    # get temp mail
    serviceId = int(args_dict['serviceId'])
    if serviceId == 1:
        mail_list = temp_mail_store.run_gen_mail(count)
        return jsonify({'status': 200, 'message': mail_list})
    elif serviceId == 2:
        status,message = hot_mail_store.get_mail()
        return jsonify({'status': status, 'message': message})



@app.route("/api/get-request", methods=['GET'])
def get_message():
    serviceId_list = [1,2] # 1 tempmail
    args_dict = request.args.to_dict()
    params = list(args_dict.keys())
    if 'serviceId' not in params:
        return jsonify({'status': 401, 'message': 'serviceId is not exist'})
    if 'orderid' not in params:
        return jsonify({'result': 401, 'message': 'orderid is not exist'})
    if not args_dict['serviceId'].isdigit() or int(args_dict['serviceId']) not in serviceId_list:
        return jsonify({'status': 402, 'message': 'serviceId is invalid'})
    if not args_dict['orderid'].isdigit():
        return jsonify({'status': 402, 'message': 'orderid is invalid'})
    serviceId = int(args_dict['serviceId'])
    if serviceId == 1:
        orderid = args_dict['orderid']
        status, message = temp_mail_store.read_mail(int(orderid))
        return jsonify({'status': status, 'message': message})
    elif serviceId == 2:
        orderid = int(args_dict['orderid'])
        status, message = hot_mail_store.get_code(orderid)
        return jsonify({'status': status, 'message': message})


@app.route('/api/add-hotmail',methods=['POST'])
def add_hot_mail():
    try:
        data = request.json
        mail = data['mail']
        password = data['password']
        hot_mail_store.add_mail(mail,password)
        return jsonify({'status':200,'message': 'post add mail successfully'})
    except:
        return jsonify({'status':100,'message': 'unknown error'})

@app.route('/api/start-get-code',methods=['GET'])
def start_get_task():
    args_dict = request.args.to_dict()
    params = list(args_dict.keys())
    if 'orderid' not in params or not args_dict['orderid'].isdigit():
        return jsonify({'result': 401, 'message': 'orderid is not exist'})
    status,message = hot_mail_store.get_request_code(args_dict['orderid'])
    return jsonify({'status':status,'message': message})

@app.route('/api/get-task',methods=['GET'])
def get_task():
    status,message = hot_mail_store.get_task()
    return jsonify({'status':status,'message': message})


@app.route('/api/post-code',methods=['POST'])
def post_code():
    try:
        data = request.json
        id = data['id']
        code = data['code']
        hot_mail_store.post_code(id,code)
        return jsonify({'status':200,'message': 'post code successfully'})
    except:
        return jsonify({'status':100,'message': 'unknown error'})

if __name__ == "__main__":
    # threading.Thread(target=mail_thread.run_gen).start()
    # threading.Thread(target=mail_thread.run_clear).start()
    #threading.Thread(target=customer_thread.run_gen).start()
    app.run(host='0.0.0.0', port=105)
