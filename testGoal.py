def Factor(result):
	int signo=1;	
	if(Expect()):	
			Get("-")	
			signo = -1;	
			
	(	
	result = Number(result)	
	|	
	Get("(")	
	result = Expression(result)	
	Get(")")	
	)	
	result*=signo;	
	return result

def Number(result):
	Get(number)	
	result = int.Parse(lastToken.Value)	
	return result

