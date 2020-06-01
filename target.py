from utils.dfa import DFA
from utils.evaluate import evaluate, Node
from utils.evaluate import Node

#CHARACTERS
letter = DFA('U!V!s!M!I!O!i!D!L!H!n!S!t!X!f!K!Q!u!b!F!J!Y!d!y!Z!W!h!x!a!o!k!c!G!p!w!N!m!g!E!r!z!v!e!A!C!B!q!j!T!P!R!l')
digit = DFA('4!7!2!6!5!9!8!0!1!3')
tab = DFA('\t')
eol = DFA('\n')

#KEYWORDS
keywords = {}
keywords["while"] = "while"
keywords["do"] = "do"
keywords["if"] = "if"

#TOKENS
ident = DFA("letter{letter!digit}", {'letter': letter, 'digit': digit})
number = DFA("digit{digit}", {'digit': digit})
part0 = DFA("';'", {})
part1 = DFA("'.'", {})
part2 = DFA("'+'", {})
part3 = DFA("'-'", {})
part4 = DFA("'*'", {})
part5 = DFA("'/'", {})
part6 = DFA("'-'", {})
part7 = DFA("'('", {})
part8 = DFA("')'", {})

tokens = {'ident': (ident, 'A', [], True),'number': (number, 'A', [], False),'part0': (part0, 'A', [], False),'part1': (part1, 'A', [], False),'part2': (part2, 'A', [], False),'part3': (part3, 'A', [], False),'part4': (part4, 'A', [], False),'part5': (part5, 'A', [], False),'part6': (part6, 'A', [], False),'part7': (part7, 'A', [], False),'part8': (part8, 'A', [], False),}

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

	def Aritmetica(self):
		while(self.Expect(part7) or self.Expect(part6) or self.Expect(number)):
			self.Stat()
			self.Get(part0)
		
		self.Get(part1)

	def Stat(self):
		value = None		
		value = self.Expression(value)
		print(value)		

	def Expression(self,result):
		result1 = None		
		result2 = None		
		result1 = self.Term(result1)
		while(self.Expect(part2) or self.Expect(part3)):
			if(self.Expect(part2)):
				self.Get(part2)
				result2 = self.Term(result2)
				result1 += result2		
			elif(self.Expect(part3)):
				self.Get(part3)
				result2 = self.Term(result2)
				result1 -= result2		
		
		result = result1		
		return result

	def Term(self,result):
		result1 = None		
		result2 = None		
		result1 = self.Factor(result1)
		while(self.Expect(part4) or self.Expect(part5)):
			if(self.Expect(part4)):
				self.Get(part4)
				result2 = self.Factor(result2)
				result1 *= result2		
			elif(self.Expect(part5)):
				self.Get(part5)
				result2 = self.Factor(result2)
				result1 /= result2		
		
		result = result1		
		return result

	def Factor(self,result):
		signo = 1		
		if(self.Expect(part6)):
			self.Get(part6)
			signo = -1		
		
		if(self.Expect(number)):
			result = self.Number(result)
		elif(self.Expect(part7)):
			self.Get(part7)
			result = self.Expression(result)
			self.Get(part8)
		result *= signo		
		return result

	def Number(self,result):
		self.Get(number)
		result = int(self.last)		
		return result

file = open('./inputs/sum.txt', 'r')
text = Node(''.join(file.read().splitlines()))
file.close()
words = evaluate(text, tokens, keywords)
test = PRODUCTIONS(words)
test.Aritmetica()