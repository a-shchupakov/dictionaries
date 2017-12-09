import argparse
import random
import string

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--string', action='store_true')
parser.add_argument('-i', '--int', action='store_true')
parser.add_argument('-r', '--replies', type=int)
parser.add_argument('-p', '--path', type=str)

args = parser.parse_args()

string_gen = args.string
int_gen = args.int
replies = args.replies
path = args.path

if not string_gen and not int_gen or path is None:
    exit()


chars = string.ascii_lowercase + string.ascii_uppercase if string_gen else ""
chars += string.digits if int_gen else ""


def generate_random(chars_, number):
    for _ in range(0, number):
        length = random.randint(29, 127)
        yield ''.join(random.choices(chars_, k=length))


def generate_in_file(file, chars_, number):
    with open(file, "w", newline="") as text_file:
        for x in generate_random(chars_, number):
            text_file.write(x + '\n')

generate_in_file(path, chars, replies)
