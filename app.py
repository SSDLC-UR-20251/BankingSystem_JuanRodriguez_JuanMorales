import random

def write_random_to_file():
    no = random.randint(1, 10)
    with open("random.txt", "w") as file:
        file.write(str(no))
    return no

def write_random():
    random_no = write_random_to_file()
    print "A random number was written to random.txt"

def surplus_argument():
    the_format = "{spam} {eggs}" # Used to be "{spam} {eggs} {chips}"
    return the_format.format(spam = "spam", eggs="eggs", chips="chips")
