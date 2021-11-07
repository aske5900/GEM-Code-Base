import string

# ------------------------------------------------------------------------------

def error(str):
    error = "\033[1;31m" + str.capitalize() + "\033[0;30m"  # red and bold
    print(error)

# ------------------------------------------------------------------------------

# functions for formatting in the main file

def b_bold(str):  # bold black
    bold = "\033[1;30m" + str + "\033[0;30m"
    return bold

def r_bold(str):  # bold red
    bold = "\033[1;31m" + str + "\033[0;30m"
    return bold

def r(s):
    red = "\033[0;31m" + s + "\033[0;30m"
    return red

def line():
    return "-"*70 #200

# ------------------------------------------------------------------------------

def to_string(partition):
    s = str(partition)
    return s.replace(",", " ")

def make_dict(perm, dataset):
    perm_dict = {}
    for s in dataset:
        permutation = s[perm][1:-1].split(")(")
        if len(permutation) in perm_dict:
            perm_dict[len(permutation)] += 1
        else:
            perm_dict[len(permutation)] = 1
    return perm_dict

def factorial(n):
    num = 1

    if(n <= 1):
        return num
    for i in range(1, n + 1):
        num *= i
    return num
