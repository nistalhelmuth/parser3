class PRODUCTIONS():
	def Expr(self):
		while(Expect(Stat)):
			Get(Stat)
			Get(";")
		
		Get(".")

	def Stat(self):
		int value;		
		value = self.Expression(value)
		System.Console.WriteLn(value.ToString());		

	def Expression(result):
		int result1,result2;		
		result1 = self.Term(result1)
		while(Expect("-") or Expect("+")):
			if(Expect("+")):
				Get("+")
				result2 = self.Term(result2)
				result1+=result2;		
			if(Expect("-")):
				Get("-")
				result2 = self.Term(result2)
				result1-=result2;		
		
			result=result1;		

	def Term(result):
		int result1,result2;		
		result1 = self.Factor(result1)
		while(Expect("/") or Expect("*")):
			if(Expect("*")):
				Get("*")
				result2 = self.Factor(result2)
				result1*=result2;		
			if(Expect("/")):
				Get("/")
				result2 = self.Factor(result2)
				result1/=result2;		
		
			result=result1;		

	def Factor(result):
		int signo=1;		
		if(Expect("-")):
			Get("-")
			signo = -1;		
		
		if(Expect(Number<.ref result.>)):
			result = self.Number(result)
		if(Expect("(")):
			Get("(")
			result = self.Expression(result)
			Get(")")
			result*=signo;		

	def Number(intresult):
		Get(number)
		 result = int.Parse(lastToken.Value)		

