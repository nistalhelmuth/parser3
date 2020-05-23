def Expr():
	{
	Stat()
	(
	";"
	)
	}
	"."

def Stat():
	int value
	Expression()
	ref value
	print(value)

def Expression(ref int result):
	int result1,result2
	Term()
	ref result1
	{
	"+"
	Term()
	ref result2
	result1+=result2
	|
	"-"
	Term()
	ref result2
	result1-=result2
	}
	result=result1;

