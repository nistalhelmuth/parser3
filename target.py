from utils.dfa import DFA
from utils.evaluate import evaluate, Node

#CHARACTERS
digit = DFA('0!6!1!8!5!3!9!2!4!7')
tab = DFA('\t')
eol = DFA('\n')
blanco = DFA('\n!\t!\r')
blanco.get_core()

#KEYWORDS
keywords = {}
keywords["while"] = "while"
keywords["do"] = "do"

#TOKENS
number = DFA("digit{digit}", {'digit': digit})
decnumber = DFA('digit{digit}"."digit{digit}', {'digit': digit})
white = DFA("blanco{blanco}", {'blanco': blanco})
part0 = DFA("';'", {})
part1 = DFA("'.'", {})
part2 = DFA("'+'", {})
part3 = DFA("'-'", {})
part4 = DFA("'*'", {})
part5 = DFA("'/'", {})
part6 = DFA("'-'", {})
part7 = DFA("'('", {})
part8 = DFA("')'", {})

tokens = {'number': (number, 'A', [], False),'decnumber': (decnumber, 'A', [], False),'white': (white, 'A', [], False),'part0': (part0, 'A', [], False),'part1': (part1, 'A', [], False),'part2': (part2, 'A', [], False),'part3': (part3, 'A', [], False),'part4': (part4, 'A', [], False),'part5': (part5, 'A', [], False),'part6': (part6, 'A', [], False),'part7': (part7, 'A', [], False),'part8': (part8, 'A', [], False),}

class PRODUCTIONS():
	def __init__(self, tokens):
		self.currentToken =  Node(tokens)
		self.nextToken = self.currentToken
		self.last = None

	def Expect(self, dfa):
		self.last = self.nextToken.value
		if self.last != None and dfa.check(self.last):
			return True
		return False

	def Get(self, dfa):
		self.last = self.currentToken.value
		self.currentToken = self.currentToken.next
		self.nextToken = self.currentToken
		if self.last != None and dfa.check(self.last):
			return self.last
		return False

	def Double(self):
		while(self.Expect(number) or self.Expect(part6) or self.Expect(decnumber) or self.Expect(part7)):
			self.Stat()
			self.Get(part0)
			while(self.Expect(white)):
				self.Get(white)
		
		
		while(self.Expect(white)):
			self.Get(white)
		
		self.Get(part1)

	def Stat(self):
		value=0		
		value = self.Expression(value)
		print("Resultado", value)		

	def Expression(self,result):
		result1=0		
		result2=0		
		result1 = self.Term(result1)
		while(self.Expect(part3) or self.Expect(part2)):
			if(self.Expect(part2)):
				self.Get(part2)
				result2 = self.Term(result2)
				result1+=result2;		
			elif(self.Expect(part3)):
				self.Get(part3)
				result2 = self.Term(result2)
				result1-=result2;		
		
		result=result1;		
		return result

	def Term(self,result):
		result1=0 		
		result2=0		
		result1 = self.Factor(result1)
		while(self.Expect(part5) or self.Expect(part4)):
			if(self.Expect(part4)):
				self.Get(part4)
				result2 = self.Factor(result2)
				result1*=result2		
			elif(self.Expect(part5)):
				self.Get(part5)
				result2 = self.Factor(result2)
				result1/=result2		
		
		result=result1		
		return result

	def Factor(self,result):
		sign=1		
		if(self.Expect(part6)):
			self.Get(part6)
			sign = -1		
		
		if(self.Expect(number) or self.Expect(decnumber)):
			result = self.Number(result)
		elif(self.Expect(part7)):
			self.Get(part7)
			result = self.Expression(result)
			self.Get(part8)
		result*=sign		
		return result

	def Number(self,result):
		if(self.Expect(number)):
			self.Get(number)
		elif(self.Expect(decnumber)):
			self.Get(decnumber)
		result = float(self.last)		
		return result

file = open('./inputs/sum.txt', 'r')
text = Node(''.join(file.read().splitlines()))
file.close()
words = evaluate(text, tokens, keywords)
test = PRODUCTIONS(words)
test.Double()