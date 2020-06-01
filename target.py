from utils.dfa import DFA
from utils.evaluate import evaluate, Node
from utils.evaluate import Node

#CHARACTERS
letter = DFA('o!s!e!A!t!W!Ñ!r!T!a!S!R!b!C!F!I!Y!G!w!z!d!K!E!N!k!P!H!L!f!ñ!u!q!Z!O!m!U!h!J!D!v!g!x!i!V!c!l!j!Q!M!X!p!n!B!y')
digit = DFA('6!3!4!2!5!9!7!8!1!0')
cr = DFA('\r')
lf = DFA('\n')
tab = DFA('\t')
ignore = DFA('\t!\n!\r')
comillas = DFA('"')
stringletter = DFA('')
operadores = DFA('=!-![!]!{!.!+!)!}!<!>!(!|')
MyANY = DFA('')

#TOKENS
ident = DFA("letter{letter!digit}", {'letter': letter, 'digit': digit})
string = DFA("comillasstringletter{stringletter}comillas", {'comillas': comillas, 'stringletter': stringletter})
char = DFA(""'"["/"]letter"'"", {'letter': letter})
charnumber = DFA(""CHR("digit{digit}")"", {'digit': digit})
charinterval = DFA(""CHR("digit{digit}")""..""CHR("digit{digit}")"", {'digit': digit})
nontoken = DFA("MyANY", {'MyANY': MyANY})
startcode = DFA(""(."", {})
endcode = DFA("".)"", {})
part0 = DFA("'COMPILER'", {})
part1 = DFA("'END'", {})
part2 = DFA("'CHARACTERS'", {})
part3 = DFA("'='", {})
part4 = DFA("'+'", {})
part5 = DFA("'-'", {})
part6 = DFA("'.'", {})
part7 = DFA("'KEYWORDS'", {})
part8 = DFA("'='", {})
part9 = DFA("'.'", {})
part10 = DFA("'TOKENS'", {})
part11 = DFA("'='", {})
part12 = DFA("'.'", {})
part13 = DFA("'PRODUCTIONS'", {})
part14 = DFA("'='", {})
part15 = DFA("'.'", {})
part16 = DFA("'EXCEPT'", {})
part17 = DFA("'KEYWORDS'", {})
part18 = DFA("'|'", {})
part19 = DFA("'('", {})
part20 = DFA("')'", {})
part21 = DFA("'['", {})
part22 = DFA("']'", {})
part23 = DFA("'{'", {})
part24 = DFA("'}'", {})
part25 = DFA("'<.'", {})
part26 = DFA("'.>'", {})
part27 = DFA("'|'", {})
part28 = DFA("'('", {})
part29 = DFA("')'", {})
part30 = DFA("'['", {})
part31 = DFA("']'", {})
part32 = DFA("'{'", {})
part33 = DFA("'}'", {})
part34 = DFA("'ANY'", {})

tokens = {'ident': (ident, 'A', [], True),'string': (string, 'A', [], False),'char': (char, 'A', [], False),'charnumber': (charnumber, 'A', [], False),'charinterval': (charinterval, 'A', [], False),'nontoken': (nontoken, 'A', [], False),'startcode': (startcode, 'A', [], False),'endcode': (endcode, 'A', [], False),'part0': (part0, 'A', [], False),'part1': (part1, 'A', [], False),'part2': (part2, 'A', [], False),'part3': (part3, 'A', [], False),'part4': (part4, 'A', [], False),'part5': (part5, 'A', [], False),'part6': (part6, 'A', [], False),'part7': (part7, 'A', [], False),'part8': (part8, 'A', [], False),'part9': (part9, 'A', [], False),'part10': (part10, 'A', [], False),'part11': (part11, 'A', [], False),'part12': (part12, 'A', [], False),'part13': (part13, 'A', [], False),'part14': (part14, 'A', [], False),'part15': (part15, 'A', [], False),'part16': (part16, 'A', [], False),'part17': (part17, 'A', [], False),'part18': (part18, 'A', [], False),'part19': (part19, 'A', [], False),'part20': (part20, 'A', [], False),'part21': (part21, 'A', [], False),'part22': (part22, 'A', [], False),'part23': (part23, 'A', [], False),'part24': (part24, 'A', [], False),'part25': (part25, 'A', [], False),'part26': (part26, 'A', [], False),'part27': (part27, 'A', [], False),'part28': (part28, 'A', [], False),'part29': (part29, 'A', [], False),'part30': (part30, 'A', [], False),'part31': (part31, 'A', [], False),'part32': (part32, 'A', [], False),'part33': (part33, 'A', [], False),'part34': (part34, 'A', [], False),}

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

	def MyCOCOR(self):
		string CompilerName = new string(' ',0);		
		string EndName = new string(' ',0);		
		self.Get(part0)
		CompilerName = self.Ident(CompilerName)
		System.Console.WriteLine("Nombre Inicial del Compilador:{0}",CompilerName);		
		if(self.Expect(startcode)):
			self.Codigo()
		
		self.Body()
		self.Get(part1)
		EndName = self.Ident(EndName)
		System.Console.WriteLine("Nombre Final del Compilador:{0}",EndName);		

	def Body(self):
		self.Characters()
		if(self.Expect(part7)):
			self.Keywords()
		
		self.Tokens()
		self.Productions()

	def Characters(self):
		string CharName = new string(' ',0);		
		int Counter = 0;		
		self.Get(part2)
		System.Console.WriteLine("LEYENDO CHARACTERS");		
		while(self.Expect(ident)):
			CharName = self.Ident(CharName)
			Counter++;System.Console.WriteLine("Char Set {0}: {1}",Counter,CharName);		
			self.Get(part3)
			self.CharSet()
			while(self.Expect(part4) or self.Expect(part5)):
				if(self.Expect(part4)):
					self.Get(part4)
					self.CharSet()
				elif(self.Expect(part5)):
					self.Get(part5)
					self.CharSet()
		
				self.Get(part6)
		

	def Keywords(self):
		string KeyName = new string(' ',0);		
		string StringValue = new string(' ',0);		
		int Counter = 0;		
		self.Get(part7)
		System.Console.WriteLine("LEYENDO KEYWORDS");		
		while(self.Expect(ident)):
			KeyName = self.Ident(KeyName)
			Counter++;System.Console.WriteLine("KeyWord {0}: {1}",Counter,KeyName);		
			self.Get(part8)
			StringValue = self.String(StringValue)
			self.Get(part9)
		

	def Tokens(self):
		string TokenName = new string(' ',0);		
		int Counter = 0;		
		self.Get(part10)
		System.Console.WriteLine("LEYENDO TOKENS");		
		while(self.Expect(ident)):
			TokenName = self.Ident(TokenName)
			Counter++;System.Console.WriteLine("Token {0}: {1}",Counter,TokenName);		
			self.Get(part11)
			self.TokenExpr()
			if(self.Expect(part16)):
				self.ExceptKeyword()
		
			self.Get(part12)
		

	def Productions(self):
		int Counter = 0;		
		self.Get(part13)
		string ProdName = new string(' ',0);		
		System.Console.WriteLine("LEYENDO PRODUCTIONS");		
		while(self.Expect(ident)):
			ProdName = self.Ident(ProdName)
			Counter++;System.Console.WriteLine("Production {0}: {1}",Counter,ProdName);		
			if(self.Expect(part25)):
				self.Atributos()
		
			self.Get(part14)
			if(self.Expect(startcode)):
				self.Codigo()
		
			self.ProductionExpr()
			self.Get(part15)
		

	def ExceptKeyword(self):
		self.Get(part16)
		self.Get(part17)

	def ProductionExpr(self):
		self.ProdTerm()
		while(self.Expect(part18)):
			self.Get(part18)
			self.ProdTerm()
		

	def ProdTerm(self):
		self.ProdFactor()
		while(self.Expect(string) or self.Expect(char) or self.Expect(ident) or self.Expect(part23) or self.Expect(part19) or self.Expect(part21)):
			self.ProdFactor()
		

	def ProdFactor(self):
		if(self.Expect(string) or self.Expect(char) or self.Expect(ident)):
			self.SymbolProd()
		elif(self.Expect(part19)):
			self.Get(part19)
			self.Get(ProductionExpr)
			self.Get(part20)
		elif(self.Expect(part21)):
			self.Get(part21)
			self.Get(ProductionExpr)
			self.Get(part22)
		elif(self.Expect(part23)):
			self.Get(part23)
			self.Get(ProductionExpr)
			self.Get(part24)
			if(self.Expect(startcode)):
				self.Codigo()
		

	def SymbolProd(self):
		string SV = new string(' ',0);		
		string IN = new string(' ',0);		
		if(self.Expect(string)):
			SV = self.String(SV)
			System.Console.WriteLine("String en Production: {0}",SV);		
		elif(self.Expect(char)):
			self.Get(char)
		elif(self.Expect(ident)):
			IN = self.Ident(IN)
			System.Console.WriteLine("Identificador en Production: {0}",IN);		
			if(self.Expect(part25)):
				self.Atributos()
		

	def Codigo(self):
		self.Get(startcode)
		while(self.Expect(ANY)):
			self.Get(ANY)
		
		self.Get(endcode)

	def Atributos(self):
		self.Get(part25)
		while(self.Expect(ANY)):
			self.Get(ANY)
		
		self.Get(part26)

	def TokenExpr(self):
		self.TokenTerm()
		while(self.Expect(part27)):
			self.Get(part27)
			self.TokenTerm()
		

	def TokenTerm(self):
		self.TokenFactor()
		while(self.Expect(part30) or self.Expect(part28) or self.Expect(string) or self.Expect(char) or self.Expect(ident) or self.Expect(part32)):
			self.TokenFactor()
		

	def TokenFactor(self):
		if(self.Expect(string) or self.Expect(char) or self.Expect(ident)):
			self.SimbolToken()
		elif(self.Expect(part28)):
			self.Get(part28)
			self.Get(TokenExpr)
			self.Get(part29)
		elif(self.Expect(part30)):
			self.Get(part30)
			self.Get(TokenExpr)
			self.Get(part31)
		elif(self.Expect(part32)):
			self.Get(part32)
			self.Get(TokenExpr)
			self.Get(part33)

	def SimbolToken(self):
		string IdentName = new string(' ',0);		
		string StringValue = new string(' ',0);		
		if(self.Expect(string)):
			StringValue = self.String(StringValue)
		elif(self.Expect(char)):
			self.Get(char)
		elif(self.Expect(ident)):
			IdentName = self.Ident(IdentName)
			System.Console.WriteLine("Identificador en Token: {0}",IdentName);		

	def CharSet(self):
		string IdentName = new string(' ',0);		
		string StringValue = new string(' ',0);		
		if(self.Expect(string)):
			StringValue = self.String(StringValue)
		elif(self.Expect(char) or self.Expect(charinterval) or self.Expect(charnumber)):
			self.Char()
		elif(self.Expect(part34)):
			self.Get(part34)
		elif(self.Expect(ident)):
			IdentName = self.Ident(IdentName)
			System.Console.WriteLine("Identificador en CharSet: {0}",IdentName);		

	def Char(self):
		if(self.Expect(char)):
			self.Get(char)
		elif(self.Expect(charnumber)):
			self.Get(charnumber)
		elif(self.Expect(charinterval)):
			self.Get(charinterval)

	def String(self,S):
		self.Get(string)
		S = LastToken.Value;		
		return S

	def Ident(self,S):
		self.Get(ident)
		S = LastToken.Value;		
		return S

file = open('./inputs/sum.txt', 'r')
text = Node(''.join(file.read().splitlines()))
file.close()
words = evaluate(text, tokens, keywords)
test = PRODUCTIONS(words)
test.MyCOCOR()