from dataclasses import dataclass

@dataclass
class TokenType:
    type: any
    value: any
    bytesize: int

    def check_repr(self):
        return f"'{self.value}'" if self.type == "CHAR" else f'"{self.value}"' if self.type == "STRING" else self.value

    def __repr__(self) -> str:
        return f"{self.type}\t\t{self.check_repr()}\t\t{self.bytesize}"