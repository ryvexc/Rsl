from token_ import Token
from instruction_ import Instruction, Function, Variable, _Static
import sys, os
import functions_
from colorama import Fore, Back, Style

##### LOAD BUILTINS FUNCTION #####
for lines in [fun_name.split("\n") for fun_name in functions_.DEFAULT]:
    for line in lines:
        token = Token(line)
        token.tokenize()
        Instruction(token.nodes).parse()
##### END #####


if sys.argv.__len__() > 1:
    if sys.argv[1] == "-v":
        print("Rsl 0.82")
    elif ".rsl" in sys.argv[1]: 
        with open(sys.argv[1]) as fileinput:
            for std_in in fileinput.readlines():
                _Static.line += 1
                token = Token(std_in)
                token.tokenize()
                
                Instruction(token.nodes).parse()
                # print([node.type for node in token.nodes])

        # print(Function.funcdo[1]
    else:
        print("error: Filename should have '.rsl' format")
        print("       Example:")
        print("           main.rsl")
        print("           helloworld.rsl")

else:
    print("RSL v0.82, release: 22 June 2022")
    print("Rsl ver 0.82 22-06-22")
    while True:
        _Static.line += 1
        function_mode = _Static.onfunction_build
        if function_mode:   
            instruction_input = input(Fore.YELLOW + "["+str(_Static.line)+"] ....     " + Fore.WHITE)
        else:
            instruction_input = input(Fore.LIGHTGREEN_EX + "["+str(_Static.line)+"] rsl-shl> " + Fore.WHITE)
        token = Token(instruction_input)
        token.tokenize()

        Instruction(token.nodes).parse()
        
            