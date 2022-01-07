import itertools as itrt

def modus_ponens(p, p2):
	if not isinstance(p, Implication):
		return modus_ponens(p2, p)
	if (hasattr(p2, "origin")):
		p2 = p2.origin
		print("aa")
	if hasattr(p.left, "origin"):
		if p2 == p.left.origin:
			p.right.set_true()
			return p.right
	if p.truth_value:
		if p2 == p.left:
				p.right.set_true()
				return p.right

def modus_tollens(p, p2):
	if not isinstance(p, Implication):
		return modus_tollens(p2, p)
	if (hasattr(p2, "origin")):
		p2 = p2.origin
	if hasattr(p.right, "origin"):
		if p2 == p.right.origin.neg():
			p.left.set_false()
			return p.left
	if p.truth_value:
		if p2 == p.right:
			if not p2.truth_value:
				p.left.truth_value = False
				return p.left

def disj_syll(p, p2):
	if not isinstance(p, Disjunction):
		return disj_syll(p2, p)
	if type(p.right) is Negation:
		p.right = p.right.origin
	if type(p.left) is Negation:
		p.left = p.left.origin
	if p.truth_value:
		if not p.right.truth_value:
			p.left.truth_value = True
			return p.left
		elif not p.left.truth_value:
			p.right.truth_value = True
			return p.right

def conj_(conju):
	if type(conju) is Conjunction and conju.truth_value:
		return conju.args

def hyp_syll(*ps):
	p_not_imp = tuple(filter(lambda x: type(x) is not Implication and x.truth_value, ps))
	ps = tuple(filter(lambda x: type(x) is Implication and x.truth_value, ps))
	ret_val = []
	sorted_ps = sorted(ps)
	

	while True:
		p_not_imp_ = []
		for p in p_not_imp:
			for p2 in sorted_ps:
				if p == p2.left:
					ret_val.append(p2.right)
					p_not_imp_.append(p2.right)
		if not p_not_imp_: break
		p_not_imp = p_not_imp_

	return ret_val


def hyp_toll(*ps):
	p_not_imp = tuple(filter(lambda x: type(x) is not Implication and ((not x.truth_value) if type(x) is not Negation else not(x.origin.truth_value)), ps))
	p_not_imp = tuple(((x.origin if type(x) is Negation else x) for x in p_not_imp))
	ps = tuple(filter(lambda x: type(x) is Implication and x.truth_value, ps))
	ret_val = []
	sorted_ps = sorted(ps)
	

	while True:
		p_not_imp_ = []
		for p in p_not_imp:
			for p2 in sorted_ps: #CHANGE HERE
				if p == neg(p2.right): #
					ret_val.append(not(p2.left))
					p_not_imp_.append(not(p2.left))
		if not p_not_imp_: break
		p_not_imp = p_not_imp_

	return ret_val



def apply_logical_rules(p, p2):
	s1, s2, s3, s4, s5, s6, = None,None,None,None,None,None,
	if isinstance(p, Implication):
		s1 = modus_ponens(p, p2)
		s2 = modus_tollens(p, p2)
	if isinstance(p2, Implication):
		s3 = modus_ponens(p2, p)
		s4 = modus_tollens(p2, p)

	#if any is a disjunction
	if isinstance(p, Disjunction):
		s5 = disj_syll(p, p2)
	elif isinstance(p2, Disjunction):
		s6 = disj_syll(p2, p)

	s8 = conj_(p); s9 = conj_(p2)
	ret_val = [s1, s2, s3, s4, s5, s6, s8, s9]
	ret_val2 = list(filter(lambda x: isinstance(x, Proposition), ret_val))
	for s in ret_val:
		if type(s) in [list,tuple]:
			ret_val2.extend(s)
	return ret_val2





class World:
	def __init__(self, *propositions):
		self.propositions = list(propositions)

	def add_proposition(p):
		self.propositions.append(p)

	def evaluate(self):
		added = False
		#will loop through all propositions and add statements whose truth value are now known
		for p, p2 in itrt.combinations(  list(filter(lambda p_: p_.truth_value is not None,self.propositions)), 2):
			new_props = apply_logical_rules(p, p2)
			if new_props:
				#print("yyy",new_props,p,p2)
				for new_prop in new_props:
					if new_prop not in self.propositions:
						added = True
						self.propositions.append(new_prop)
		for p in self.propositions:
			if type(p) is Negation:
				p.truth_value = not(p.origin.truth_value) if p.origin.truth_value is not None else None
		return added

	def print_props(self):
		for p in self.propositions:
			print(p, p.truth_value)
		print()

	def __repr__(self):
		return f"World({len(self.propositions)} propositions)"

class Entity:
	"""a simple entity"""
	@classmethod
	def init_many(cls, names):
		return [Entity(x) for x in names.split()]

	def __init__(self, name):
		if ' ' not in name:
			self.name = name
		else:
			Entity.init_many(name)
	def __repr__(self):
		return self.name
		

class Proposition:
	"""Will accept an ordered bunch of args"""
	def __init__(self, *args, name=None, truth_val = None):
		self.name = name
		self.args = tuple(((a if type(a) is not Negation else a.origin) for a in args))
		
		self.truth_value = truth_val
	def __repr__(self):
		return f"{self.name}{self.args}"
	def __eq__(self, other):
		return (self.name == other.name) and (self.args == other.args) and (self.truth_value == other.truth_value)
	def copy(self):
		T = type(self)
		return T(*self.args,name=self.name,truth_val=self.truth_value)
	def neg(self):
		T = type(self)
		if self.truth_value is None:
			raise ValueError(f"Truth value of {self} is None")
		return T(*self.args,name=self.name,truth_val=not(self.truth_value))
	def set_true(self):
		self.truth_value = True
	def set_false(self):
		self.truth_value = False

class Negation(Proposition):
	def __init__(self,p):
		self.origin = p
		super().__init__(*p.args,name="not "+p.name,truth_val=None if p.truth_value is None else not(p.truth_value))
	def set_true(self):
		self.origin.truth_value = False
		self.truth_value = True

class BinomialProposition(Proposition):
	def __init__(self, left, right, name=None, truth_val=None):
		self.left = left
		self.right = right
		super().__init__(left, right, name=name, truth_val=truth_val)
	def __repr__(self):
		return f"{self.name}({self.left}, {self.right})"

class Conjunction(BinomialProposition):
	def __init__(self, left, right, name="And", truth_val=None):
		c_ = False
		if type(left) is Conjunction:
			other = right
			c = left
			c_ = True
		elif type(right) is Conjunction:
			other = left
			c = right
			c_ = True
		if c_:
			if other == c.left:
				new = c.right
			elif other == c.right:
				new = c.left
			else:
				new = c
		else:
			new = left; other = right
		super().__init__(new, other, name="And", truth_val=truth_val)
	def set_true(self):
		self.left.set_true()
		self.right.set_true()
		self.truth_value = True

class Disjunction(BinomialProposition):
	def __init__(self, left, right, name="Or", truth_val=None):
		super().__init__(left, right, name="Or", truth_val=truth_val)


class Implication(BinomialProposition):
	def __init__(self, left, right, name="Implies", truth_val=None):
		super().__init__(left, right, name="Implies", truth_val=truth_val)
	def __lt__(self, nxt):
		return self.right == nxt.left

class Equivalence(BinomialProposition):
	def __init__(self, left, right, name="Is", truth_val=None):
		super().__init__(left, right, name="Is", truth_val=truth_val)



if __name__ == '__main__':
	l = [Proposition(let, name=let) for let in "pqrst"]
	p,q,r,s,t = l
	p1 = Conjunction(Negation(p), q)
	p2 = Implication(r,p)
	p3 = Implication(Negation(r), s)
	p4 = Implication(s,t)
	l2 = [p1,p2,p3,p4]
	for x in l2: x.set_true()
	w = World(*l2)
	print(w)

	i = 0
	while w.evaluate():
		i += 1
		print(i)
		pass
	w.print_props()

		