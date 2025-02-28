import random
import string

def random_char(char_num):
       return ''.join(random.choice(string.ascii_letters) for _ in range(char_num))

print (random_char(7)+"@cybered.com")