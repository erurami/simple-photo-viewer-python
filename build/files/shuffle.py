import random

def shuffle(list):
    already_selected = []
    never_selected = list
    retval = []
    for index in range(len(list)):
        select = random.choice(never_selected)
        never_selected.remove(select)
        retval.append(select)
    return retval

a = [1,2,3,4,5,6]
print(shuffle(a))