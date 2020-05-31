from utils.evaluate import Node

class PRODUCTIONS():
	def __init__(self, tokens):
		self.currentToken =  Node(tokens)
		self.nextToken = self.currentToken

	def Expect(self, dfa):
		token = self.nextToken.value
		if dfa.check(token):
			return True
		return False

	def Get(self, dfa):
		token = self.currentToken.value
		self.currentToken = self.currentToken.next
		self.nextToken = self.currentToken
		if dfa.check(token):
			return token
		return False

	def Expr(self):
		while(self.Expect("(") or self.Expect(number) or self.Expect("-")):
			self.Stat()
			self.Get(";")
		
		self.Get(".")

	def Stat(self):
		value = None		
		value = self.Expression(value)
		print(value)		

	def Expression(self,result):
		result1 = None		
		result2 = None		
		result1 = self.Term(result1)
		while(self.Expect("+") or self.Expect("-")):
			if(self.Expect("+")):
				self.Get("+")
				result2 = self.Term(result2)
				result1 += result2		
			elif(self.Expect("-")):
				self.Get("-")
				result2 = self.Term(result2)
				result1 -= result2		
		
			result = result1		

	def Term(self,result):
		result1 = None		
		result2 = None		
		result1 = self.Factor(result1)
		while(self.Expect("/") or self.Expect("*")):
			if(self.Expect("*")):
				self.Get("*")
				result2 = self.Factor(result2)
				result1 *= result2		
			elif(self.Expect("/")):
				self.Get("/")
				result2 = self.Factor(result2)
				result1 /= result2		
		
			result = result1		

	def Factor(self,result):
		signo = 1		
		if(self.Expect("-")):
			self.Get("-")
			signo = -1		
		
		if(self.Expect(number)):
			result = self.Number(result)
		elif(self.Expect("(")):
			self.Get("(")
			result = self.Expression(result)
			self.Get(")")
			result *= signo		

	def Number(self,result):
		self.Get(number)
		result = lastToken.Value		

