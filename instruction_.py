from error_ import Error
from token_ import Token

def find(arr, fd) -> list:
	return [i for i in arr if fd in i]

def skip(arr, fd) -> list:
	return [i for i in arr if fd not in i]

def joinall(arr, sepr) -> str:
	string = ""
	for i in arr:
		string += str(i) + sepr
	return string

class Variable:
	varname = []
	varvalue = []
	vartype = []

	def __repr__():
		return f"Var: {Variable.varname}\nValue: {Variable.varvalue}\nType: {Variable.vartype}"

	def register(name, value, type):
		Variable.varname.append(name)
		Variable.varvalue.append(value)
		Variable.vartype.append(type)

	def get(varname):
		return Variable.varvalue[Variable.varname.index(varname)]

	def typeof(varname):
		return Variable.vartype[Variable.varname.index(varname)]

	def changeValue(varname, newvalue, newtype):
		try:
			Variable.varvalue[Variable.varname.index(varname)] = newvalue
			Variable.vartype[Variable.varname.index(varname)] = newtype
		except ValueError:
			pass # Error

	def delete(name):
		location = Variable.varname.index(name)
		del Variable.varname[location]
		del Variable.varvalue[location]
		del Variable.vartype[location]

	def find(varname):
		return len(find(Variable.varname, varname)) != 0

	def parseValue(nodevalue: list, nodetype: list) -> list:
		value: any
		value_type = ""
		parsed = []
		current_instruction = []
		instruction_active = False
		__waitpos = 0
		pos = 0
		while pos <= len(nodetype):
			if pos == len(nodetype):
				instruction_active = False
				# print("ev:", current_instruction)
				if len(current_instruction) != 0: parsed.append(eval(joinall(current_instruction, "")))
				else: parsed.append(joinall(current_instruction, ""))
				current_instruction.clear()
			elif nodetype[pos] in ("STRING"):
				parsed.append(nodevalue[pos])
			elif nodetype[pos] == "VARNAME":
				__waitpos = pos
				instruction_active = True
				current_instruction.append(Variable.get(nodevalue[pos]))
			elif nodetype[pos] in ("INT", "FLOAT", "CHAR", "LONG", "LPAREN", "RPAREN"):
				__waitpos = pos
				instruction_active = True
				current_instruction.append(nodevalue[pos])
			elif nodetype[pos] in ("PLUS", "MINUS", "MUL", "DIV"):
				if instruction_active and nodetype[pos + 1] != "STRING":
					current_instruction.append(nodevalue[pos])
				elif instruction_active and nodetype[pos + 1] == "STRING":
					instruction_active = False
					# print("ev:", current_instruction)
					parsed.append(eval(joinall(current_instruction, "")))
					pos = __waitpos + 1
					current_instruction.clear()
			elif nodetype[pos] == "UNKNOWN":
				print(nodevalue)
				print(nodetype)
				Error(_Static.line).IllegalCharError()
				print()
			pos += 1

		value = joinall(parsed, "")
		for node in nodetype:
			if node == "STRING":
				value_type = "STRING"
				break
			elif node != "STRING" and node in ("LONG", "FLOAT", "INT", "CHAR"):
				if node == "LONG":
					value_type = "LONG"
				elif node == "INT":
					value_type = "INT"
				elif node == "FLOAT":
					value_type = "FLOAT"
				elif node == "CHAR":
					value_type = "CHAR"
					
		return [value, value_type]

class Function:
	funcname = []
	funcparam = []
	funcdo = []
	funcreturntype = []
	funcreturnvalue = []

	def __repr__():
		return f"Name: {Function.funcname}\nFuncparam: {Function.funcparam}\nFuncdo: {Function.funcdo}\nFuncret: {Function.funcreturnvalue}\nFuncrettyp: {Function.funcreturntype}"

	def register(name, param: list, funcdo):
		Function.funcname.append(name)
		Function.funcparam.append(param)
		Function.funcdo.append(funcdo)
		Function.funcreturnvalue.append("NOVALUE")
		Function.funcreturntype.append("VOID")
		[Variable.register(parameter, "null", "NULL") for parameter in param]

	def find(name):
		return len(find(Function.funcname, name)) != 0

	def rewriteFunction(name, param: list, funcdo):
		function_location = Function.funcname.index(_Static.funcname)
		Function.funcname[function_location] = name
		Function.funcparam[function_location] = param
		Function.funcdo[function_location] = funcdo
		Function.funcreturnvalue[function_location] = "NOVALUE"
		Function.funcreturntype[function_location] = "VOID"
		[Variable.changeValue(parameter, "null", "NULL") for parameter in param]

	def call(name, args: list, args_type: list) -> list:
		for i in range(len(args)):
			varname_reg = Function.funcparam[Function.funcname.index(name)][i]
			varvalue_reg = args[i]
			Variable.changeValue(varname_reg, varvalue_reg, args_type[i])

		try:
			for instruction in Function.funcdo[Function.funcname.index(name)]:
				Instruction(instruction, name).parse()
			
			for i in range(len(args)):
				varname_reg = Function.funcparam[Function.funcname.index(name)][i]
				varvalue_reg = "Require Arguments!"
				Variable.changeValue(varname_reg, varvalue_reg, args_type[i])
			# print("res: ", [Function.funcreturnvalue[Function.funcname.index(name)], Function.funcreturntype[Function.funcname.index(name)]])
			# return [Function.funcreturnvalue[Function.funcname.index(name)], Function.funcreturntype[Function.funcname.index(name)]]
		except ValueError:
			pass
			# Error(_Static.line).NoFunctionFound()

class _Static:
	function_do = []
	onfunction_build = False
	funcname = ""
	funcparams = []
	line = 0

class Instruction:
	def __init__(self, nodes, funcallname = None):
		self.pos = 0
		self.nodes = nodes
		self.funcallname = funcallname

	def parse(self):
		node_type = [node.type for node in self.nodes]
		node_value = [node.value for node in self.nodes]
		# print(node_type)
		# print(node_value)

		if not _Static.onfunction_build:
			if len(find(node_type, "VARASSIGN")) == 1:
				varname = node_value[node_type.index("VARNAME")]
				varvalue = []
				vartype = []
				funcall_args = []
				funcall_args_type = []
				cur_pos_ins = node_type.index("EQUAL")+1
				while cur_pos_ins < len(node_type):
					if node_type[cur_pos_ins] == "VARNAME":
						if Function.find(node_value[cur_pos_ins]):
							pos = cur_pos_ins + 1
							while pos < len(node_type):
								if node_type[pos] in ("LPAREN", "COMMA", "RPAREN"):
									pass
								else:
									if node_type[pos] in ("STRING", "CHAR", "INT", "FLOAT", "LONG"):
										funcall_args.append(node_value[pos])
										funcall_args_type.append(node_type[pos])
									elif node_type[pos] in ("VARNAME"):
										try:
											funcall_args.append(Variable.get(node_value[pos]))
											funcall_args_type.append(Variable.typeof(node_value[pos]))
										except:
											# Error(_Static.line).NoVariableFound() 
											pass
								pos += 1
							Function.call(node_value[cur_pos_ins], funcall_args, funcall_args_type)
							fun_pos = Function.funcname.index(node_value[cur_pos_ins])
							varvalue.append(Function.funcreturnvalue[fun_pos])
							vartype.append(Function.funcreturntype[fun_pos])
							cur_pos_ins = pos - 1
						elif Variable.find(node_value[cur_pos_ins]):
							varvalue.append(Variable.get(node_value[cur_pos_ins]))
							vartype.append(Variable.typeof(node_value[cur_pos_ins]))
						else:
							Error(_Static.line).NoVariableFound()
							_Static.line -= 1
					else:
						varvalue.append(node_value[cur_pos_ins])
						vartype.append(node_type[cur_pos_ins])
						# print("VAR", varvalue, vartype)
					cur_pos_ins += 1

				parsedvar = Variable.parseValue(varvalue, vartype)
				if Variable.find(varname):
					Variable.changeValue(varname, parsedvar[0], parsedvar[1])
				else:
					Variable.register(varname, parsedvar[0], parsedvar[1])

			elif len(find(node_type, "STDOUT")) != 0:
				_value = []
				_type = []
				pos = 0
				while pos < node_type.__len__():
					if node_type[pos] == "VARNAME":
						try:
							_value.append(Variable.get(node_value[pos]))
							_type.append(Variable.typeof(node_value[pos]))
						except ValueError:
							Error(_Static.line).NoVariableFound()
							_Static.line -= 1
					elif node_type[pos] in ("STRING", "INT", "FLOAT", "LONG", "CHAR", "PLUS", "MINUS", "MUL", "DIV"):
						_value.append(node_value[pos])
						_type.append(node_type[pos])
					pos += 1
				print(Variable.parseValue(_value, _type)[0])

			elif len(find(node_type, "TYPEOF")) != 0:
				try:
					print(Variable.typeof(node_value[node_type.index("TYPEOF") + 1]))
				except:
					print(node_value[node_type.index("TYPEOF") + 1])

			elif len(find(node_type, "ALLVAR")) != 0:
				print(Variable.__repr__())

			elif len(find(node_type, "FREE")) != 0:
				pos = 0
				while pos != len(node_type):
					if node_type[pos] == "VARNAME":
						Variable.delete(node_value[pos])
					elif node_type[pos] in ("LPAREN", "RPAREN"):
						pass
					pos += 1

			elif len(find(node_type, "REPEAT")) != 0:
				pos = 1
				repeat_onset = False
				repeat_times = 0
				function_name: str
				funcall_args = []
				funcall_args_type = []
				while pos < len(node_type):
					if node_type[pos] in "INT" and not repeat_onset:
						repeat_times = node_value[pos]
						repeat_onset = True
					elif node_type[pos] == "VARNAME":
						if not repeat_onset:
							repeat_times = int(Variable.get(node_value[pos]))
							repeat_onset = True
						else:
							function_name = node_value[pos]
					elif node_type[pos] in ("LPAREN", "RPAREN"):
						pass
					elif node_type[pos] in ("STRING", "CHAR", "INT", "FLOAT", "LONG"):
						funcall_args.append(node_value[pos])
						funcall_args_type.append(node_type[pos])
					elif node_type[pos] in ("VARNAME"):
						try:
							funcall_args.append(Variable.get(node_value[pos]))
							funcall_args_type.append(Variable.typeof(node_value[pos]))
						except:
							pass # Error
					else:
						pass # Error
					pos += 1
				# print(function_name, repeat_times, funcall_args)
				for i in range(repeat_times):
					Function.call(function_name, funcall_args, funcall_args_type)

			elif len(find(node_type, "FUNASSIGN")) != 0:
				_Static.funcname = node_value[node_type.index("FUNASSIGN") + 1];
				
				ins_pos = node_type.index("LPAREN") + 1
				while node_type[ins_pos] != None and node_type[ins_pos] != "RPAREN":
					if "\\" in node_value[ins_pos]:
						print("ERROR")
					elif node_type[ins_pos] != "COMMA": _Static.funcparams.append(node_value[ins_pos])
					ins_pos += 1

				_Static.onfunction_build = True

			elif len(find(node_type, "RETURN")) != 0:
				pos = 1
				ret_args = []
				ret_args_type = []
				while pos < len(node_type):
					if node_type[pos] == "VARNAME":
						if Variable.find(node_value[pos]):
							ret_args.append(Variable.get(node_value[pos]))
							ret_args_type.append(Variable.typeof(node_value[pos]))

					elif node_type[pos] in ("PLUS", "MINUS", "MUL", "DIV", "INT", "FLOAT", "CHAR", "STRING", "LONG"):
						ret_args.append(node_value[pos])
						ret_args_type.append(node_type[pos])
					pos += 1
				fun_pos = Function.funcname.index(self.funcallname)
				parsed = Variable.parseValue(ret_args, ret_args_type)
				Function.funcreturnvalue[fun_pos] = parsed[0]
				Function.funcreturntype[fun_pos] = parsed[1]

			elif len(find(node_type, "VARNAME")) != 0:
				try:
					if node_type[node_type.index("VARNAME") + 1] == "LPAREN":
						funcall_name = node_value[node_type.index("LPAREN") - 1]
						funcall_args = []
						funcall_args_type = []

						ins_pos = node_type.index("LPAREN") + 1
						while node_type[ins_pos] != None and node_type[ins_pos] != "RPAREN":
							if node_type[ins_pos] in ("STRING", "CHAR", "INT", "FLOAT", "LONG"):
								funcall_args.append(node_value[ins_pos])
								funcall_args_type.append(node_type[ins_pos])
							elif node_type[ins_pos] in ("VARNAME"):
								try:
									funcall_args.append(Variable.get(node_value[ins_pos]))
									funcall_args_type.append(Variable.typeof(node_value[ins_pos]))
								except:
									Error(_Static.line).NoVariableFound()
							else:
								pass # Error
							ins_pos += 1
						_Static.onfunction_build = False
						Function.call(funcall_name, funcall_args, funcall_args_type)
					# else:
					#     try:
					#         Variable.get(node_value[node_type.index("STDOUT") + 1])
					#     except:
					#         node_value[node_type.index("STDOUT") + 1]
				except IndexError:
					Error(_Static.line).NoVariableFound()
					_Static.line -= 1

			elif len(find(node_type, "UNKNOWN")) > 0:
				print(node_type)
				Error(_Static.line).IllegalCharError()

			elif len(find(node_type, "THEN")) > 0:
				_Static.onfunction_build = True
			
		else:
			if len(find(node_type, "END")) != 0:
				_Static.onfunction_build = False
				if Function.find(_Static.funcname):
					Function.rewriteFunction(_Static.funcname, _Static.funcparams, _Static.function_do)
				else:
					Function.register(_Static.funcname, _Static.funcparams, _Static.function_do)
				_Static.funcname = []
				_Static.funcparams = []
				_Static.function_do = []

			else:
				_Static.function_do.append(self.nodes)
