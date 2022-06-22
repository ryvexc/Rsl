from tokentype import TokenType

class Token():
	character: str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
	number: str = "0123456789"

	def __init__(self, std_in):
		self.std_in = std_in
		self.nodes = []
		self.pos = 0
		self.mov()

	def __repr__(self):
		return [node for node in self.nodes].join("\n")
 
	def mov(self):
		if self.pos < len(self.std_in):
			self.current_char = self.std_in[self.pos]
			self.pos += 1
		else:
			self.current_char = None

	def out(self):
		for node in self.nodes:
			print(node) if node.type != "NEWLINE" else print(node, "\n")

	def getTypeNodes(self) -> list:
		return [node.type for node in self.nodes]
		
	def tokenize(self):
		WHITESPACE = " \t"
		while self.current_char != None:
			if self.current_char in WHITESPACE:
				self.mov()
				continue
			elif self.current_char == "\n":
				self.nodes.append(TokenType("NEWLINE", "\\n", 2))
				self.mov()
			elif self.current_char in (self.character+"'"+'"'):
				self.nodes.append(self.make_str())
			elif self.current_char in self.number:
				self.nodes.append(self.make_number())
			elif self.current_char == "+":
				self.nodes.append(TokenType("PLUS", "+", ""))
				self.mov()
			elif self.current_char == "-":
				self.nodes.append(TokenType("MINUS", "-", ""))
				self.mov()
			elif self.current_char == "*":
				self.nodes.append(TokenType("MUL", "*", ""))
				self.mov()
			elif self.current_char == "/":
				self.nodes.append(TokenType("DIV", "/", ""))
				self.mov()
			elif self.current_char == "\\":
				self.nodes.append(TokenType("ESCAPECHAR", "\\", ""))
				self.mov()
			elif self.current_char == "(":
				self.nodes.append(TokenType("LPAREN", "(", ""))
				self.mov()
			elif self.current_char == ")":
				self.nodes.append(TokenType("RPAREN", ")", ""))
				self.mov()
			elif self.current_char == "=":
				self.nodes.append(TokenType("EQUAL", "=", ""))
				self.mov()
			elif self.current_char == ",":
				self.nodes.append(TokenType("COMMA", ",", ""))
				self.mov()
			elif self.current_char == "#":
				break
			else:
				self.nodes.append(TokenType("UNKNOWN", self.current_char, "?"))
				self.mov()

		return self

	def make_str(self):
		_byte = 1
		_stream = self.current_char
		self.mov()

		if _stream == '"':
			while self.current_char != None and self.current_char != '"':
				_stream += str(self.current_char)
				_byte += 1
				self.mov()
			_stream += str(self.current_char)
			self.mov()
			_byte += 1
		else:
			while self.current_char != None and self.current_char in (self.character+self.number+"'"+"_"):
				_stream += str(self.current_char)
				_byte += 1
				self.mov()

		# KEYWORD DECLARATOR
		if _stream == "var":
			return TokenType("VARASSIGN", _stream, 0)
		elif _stream == "\\n":
			return TokenType("NEWLINE", _stream, 0)
		elif _stream in ("true", "false"):
			return TokenType("BOOLEAN", _stream[1:_byte-1], 0)
		elif _stream == "stdout":
			return TokenType("STDOUT", _stream, 0)
		elif _stream == "typeof":
			return TokenType("TYPEOF", _stream, 0)
		elif _stream == "then":
			return TokenType("THEN", _stream, 0)
		elif _stream == "end":
			return TokenType("END", _stream, 0)
		elif _stream == "fun":
			return TokenType("FUNASSIGN", _stream, 0)
		elif _stream == "repeat":
			return TokenType("REPEAT", _stream, 0)
		elif _stream == "free":
			return TokenType("FREE", _stream, 0)
		elif _stream == "allvar":
			return TokenType("ALLVAR", _stream, 0)
		elif _stream == "return":
			return TokenType("RETURN", _stream, 0)
		elif _stream == "print":
			return TokenType("STDOUT", _stream, 0)

		if _stream[0] == "'"  and _stream[_byte-1] == "'":
			if _byte <= 3: return TokenType("CHAR", str(_stream[1:_byte-1]), _byte-2)
			else: return TokenType("STRING", str(_stream[1:_byte-1]), _byte-2)
		elif _stream[0] == '"'  and _stream[_byte-1] == '"':
			return TokenType("STRING", str(_stream[1:_byte-1]), _byte-2)
		elif _stream[0] == '"'  and _stream[_byte+1] == '"':
			return TokenType("STRING", str(_stream[1:_byte-1]), _byte-2)
		return TokenType("VARNAME", str(_stream), _byte)

	def make_number(self):
		_byte = 4
		_stream = self.current_char
		self.mov()

		while self.current_char != None and (self.current_char == "." or self.current_char in self.number):
			_stream += self.current_char
			self.mov()

		if "." in _stream:
			_byte = 4
			if _stream[0] == ".":
				_stream = "0" + _stream
			elif _stream[len(_stream) - 1]:
				_stream += "0"
			elif len(_stream.split(".")[1]) == 2:
				_byte = 8
				return TokenType("DOUBLE", _stream. _byte)
			return TokenType("FLOAT", float(_stream), _byte)
		
		else:
			if int(_stream) <= 2_147_483_647:
				return TokenType("INT", int(_stream), _byte)
			else:
				return TokenType("LONG", _stream, 8)
			

		
		