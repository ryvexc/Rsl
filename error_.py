from colorama import Fore, Back, Style

class Error:
    def __init__(self, linepos):
        self.linepos = linepos

    def NoVariableFound(self):
        print(f"{Fore.RED}error:{Fore.WHITE} NoVariableFound at line {self.linepos}")
        
    def NoFunctionFound(self):
        print(f"{Fore.RED}error:{Fore.WHITE} NoFunctionFound at line {self.linepos}")
    
    def IllegalCharError(self):
        print(f"{Fore.RED}error:{Fore.WHITE} IllegalCharError at line {self.linepos}")
