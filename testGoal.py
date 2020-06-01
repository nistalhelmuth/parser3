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
		while(self.Expect(number) or self.Expect("-") or self.Expect("(")):
			self.Stat()
			self.Get(";")
		
		self.Get(".")

