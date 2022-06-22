from token_ import Token
import sys, os

if len(sys.argv) > 1:
    with open(sys.argv[1]) as file:
        for std_in in file.readlines():
            token = Token(std_in)
            tokenize = token.tokenize()
            tokenize.out()
else:
    os.system("clear" if os.name == "posix" else "cls")
    while True:
        std_in = input("> ")
        token = Token(std_in)
        tokenize = token.tokenize()
        tokenize.out()