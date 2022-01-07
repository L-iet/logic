s = "l = [True, False]\n"
sents = input("Enter the letters representing atomic sentences separated by spaces: ").split()
exprs = input("""Enter the logical statements in proper python syntax, separated by commas.
Example: A and B or C,B and C
""").split(",")
c = input("Do you want the output in 'T  F'[y] or 'True False'[n] format?")


for sent in sents:
	s += f"print('    {sent}|',end=' ')\n"
for expr in exprs:
	if exprs[-1] == expr:
		s += f"print('{expr}|')\n"
	else:
		s += f"print('{expr}|',end='  ')\n"
for i, sent in enumerate(sents):
	s += "\t"*i + F"for {sent} in l:\n"

if c == '' or c == 'y':
	sli = "0"
else:
	sli = ":"
rjusts = ','.join([f"str({sent})[{sli}].rjust(5)+'|'" for sent in sents])

ex_strs = ''
for expr in exprs:
	le = len(expr)
	ex_s = "str("+expr+f")[{sli}].rjust("+str(le)+")+'|'"
	ex_strs += ex_s + ','
ex_strs = ex_strs[:-1]
s += "\t"*(i+1)+"print("+rjusts+f",{ex_strs})\n"

exec(s)

