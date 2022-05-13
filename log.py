
def add_log(order):
    with open('log.txt','r')  as f:
        data =f.read().strip().split(' ')
        data[int(order)] = str(int(data[int(order)]) + 1)
    with open('log.txt', 'w') as f:
        f.write(' '.join(data))
def get_log():
    with open('log.txt','r')  as f:
        return [int(i) for i in f.read().strip().split(' ')]