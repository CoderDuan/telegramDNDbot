import re
import random

nat = '[1-9][0-9]*'
dice = nat + 'd' + nat
kdice = dice + 'k' + nat
command_format = '\.r.*'

# Check if the expression starts with '.r'
def check_command(exp):
	result = re.match(command_format, exp)
	if result:
		return True
	else:
		print "Invalid input"
		return False

# Check character set
def check_char_set(exp):
	char_set = set(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9','+', '-', '*', '/', '(', ')', 'k', 'd'))
	if set(exp).issubset(char_set):
		return True
	else:
		print "Invalid characters"
		return False

# Roll dices with 'k's.
# For example, 5d6k3.
def roll_kdice(exp):
	match = re.search(kdice, exp)
	if match:
		roll = match.group()
		n1 = re.search(nat, roll).group()
		rest = re.sub(n1+'d', '', roll)
		n2 = re.search(nat, rest).group()
		rest = re.sub(n2+'k', '', rest)
		n3 = re.search(nat, rest).group()
		arr = []
		for i in range(0, int(n1)):
			arr.append(random.randint(1, int(n2)))
		arr.sort(reverse = True)
		result = 0
		for i in range(0, min(int(n1), int(n3))):
			result += arr[i]
		return roll_kdice(re.sub(roll, str(result), exp))
	else:
		return exp

# Roll dices. First roll dices with 'k's. Then ones without 'k's.
# For example, 5d6, 5d6k3.
def roll_dice(exp):
	exp = roll_kdice(exp)
	match = re.search(dice, exp)
	if match:
		roll = match.group()
		n1 = re.search(nat, roll).group()
		rest = re.sub(n1+'d', '', roll)
		n2 = re.search(nat, rest).group()
		result = 0
		for i in range(0, int(n1)):
			result += random.randint(1, int(n2))
		return roll_dice(re.sub(roll, str(result), exp))
	else:
		return exp

# Calculate multiply and divide.
# First match the first 'nat*nat' (or 'nat/nat') expression,
# Then parse it and calculate it.
# Next, find the next 'nat*nat' expression by recursion.
# If can't find such expression, return input expression.
def cal_mul_div(exp):
	match = re.search(r'\d+[\*\/]\d+', exp)
	if match:
		content = match.group()
		if len(content.split('*')) > 1:
			n1, n2 = content.split('*')
			value = int(n1)*int(n2)
			exp = exp.replace(content, str(value))
			return cal_mul_div(exp)
		elif len(content.split('/')) > 1:
			n1, n2 = content.split('/')
			value = int(n1)/int(n2)
			exp = exp.replace(content, str(value))
			return cal_mul_div(exp)
		else:
			return exp
	else:
		return exp

# Calculate addition and substraction.
# First match the first 'nat+nat' (or 'nat-nat') expression,
# Then parse it and calculate it.
# Next, find the next 'nat+nat' expression by recursion.
# If can't find such expression, return input expression. 
def cal_add_sub(exp):
	match = re.search(r'\d+[\+\-]\d+', exp)
	if match:
		content = match.group()
		if len(content.split('+')) > 1:
			n1, n2 = content.split('+')
			value = int(n1)+int(n2)
			exp = exp.replace(content, str(value))
			return cal_add_sub(exp)
		elif len(content.split('-')) > 1:
			n1, n2 = content.split('-')
			value = int(n1)-int(n2)
			exp = exp.replace(content, str(value))
			return cal_add_sub(exp)
		else:
			return exp
	else:
		return exp

# Calculate all parentheses by bottom-up recursion.
# In each recursion, find the innerest pair of parentheses, 
# by matching the a pair of parentheses between which there is no more '(' or ')' symbols.
# Then, calculate the expression between these parentheses,
# and replace the expression including paretheses with the calculation result.
# Repeat by recursion until there is no more parentheses
def cal_parentheses(exp):
	match = re.search(r'\([0-9dk\+\-\*\/]*\)', exp)
	if match:
		content = match.group()
		replace_content = content[1:-1]
		value = roll_dice(replace_content)
		replace_content = cal_mul_div(replace_content)
		replace_content = cal_add_sub(replace_content)
		exp = exp.replace(content, replace_content)
		return cal_parentheses(exp)
	else:
		exp = roll_dice(exp)
		exp = cal_mul_div(exp)
		exp = cal_add_sub(exp)
		return exp

# check and parse the command
def parse_command(command):
	if not check_command(command):
		return "Invalid Command"
	line = re.sub(r'\.r\s*', '', command)
	line = re.sub(r'\s+', '', line)
	if check_char_set(line) == False:
		return "Invalid Characters"
	after_rolled = roll_dice(line)
	line = cal_parentheses(after_rolled)
	#print line
	return after_rolled + '=' + line

def main():
	command = ".r (1+2*(3+4)+(6/3))"
	if check_command(command) == False:
		return
	line = re.sub(r'\.r\s*', '', command)
	line = re.sub(r'\s+', '', line)
	if check_char_set(line) == False:
		return
	print line
	line = cal_parentheses(line)
	print line

#main()

