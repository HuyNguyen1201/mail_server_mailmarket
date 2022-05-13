import threading
import temp_mail_store
import time
max_number = 2000

n_mail_per_loop = 200


def run_gen():
    global n_mail_per_loop
    while True:
        if server_processor.get_number_mail() < max_number:
            print('run gen')
            threads = []
            for i in range(n_mail_per_loop):
                threads.append(threading.Thread(
                    target=temp_mail_store.run_gen_mail))
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
        else:
            time.sleep(10)


def run_clear():
    while True:
        time.sleep(30)
        temp_mail_store.clear_mail()
