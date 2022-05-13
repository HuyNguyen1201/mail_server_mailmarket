anchor_id = 100000
def get_id():
    global anchor_id
    anchor_id += 1
    if anchor_id >= 999999:
        anchor_id = 100000
    return anchor_id
