try:
    import sys
    import string
    import random
except ImportError as exception:
    print("%s - Please install the necessary libraries." % exception)
    sys.exit(0)

#
alphabet62 = string.digits + string.ascii_letters
alphabet16_upper = string.digits + string.ascii_uppercase[:6]


#
def random_str(length):
    return ''.join(random.choice(alphabet62) for _ in range(length))
