precedence = {'º':3, '?':3, '&':3, '_':2, '!':1, ' ':2} 

def conversionToPostfix(expresion):
    def pop(top, array):
        if not top == -1:
            top -= 1
            return array.pop()
        else:
            return "$"
    
    def notGreater(i, array):
        try: 
            a = precedence[i] 
            b = precedence[array[-1]] 
            return True if a  <= b else False
        except KeyError:  
            return False

    top = -1
    array = []
    output = []
    exp = expresion
    exp = '_'.join(expresion.split())
    i = 0
    while i < len(exp):
        if i < len(exp)-2 and exp[i] == "'" and exp[i+2] == "'":
            output.append(exp[i+1])
            i += 2
        elif exp[i].isalnum() or exp[i] in ['#', '.', '+', '-', ',', '=', '"', "'", '|', '>', '<']:
            count = 0
            buff = exp[i]
            while i+count+1 < len(exp) and ( exp[i+count+1].isalnum() or exp[i+count+1] in ['#', '.', '+', '-', ',', '=', '|']):
                count += 1
                buff = buff + exp[i+count]
            output.append(buff) 
            i += count
            
        elif exp[i] in ['(' ,'[' ,'{']: 
            top += 1
            if exp[:i] != '':
                top += 1
                array.append('_')
            array.append(exp[i])

        elif exp[i] in [')' ,']' ,'}'] and len(array) == 0: 
            top += 1
            array.append(exp[i])
        elif exp[i] == ')': 
            while((not top == -1) and array[-1]  != '('): 

                #a = pop(top, array) 
                if not top == -1:
                    top -= 1
                    a =  array.pop()
                else:
                    a = "$"

                output.append(a) 
            if (not top == -1 and array[-1]  != '('): 
                return -1
            elif not top == -1:
                    top -= 1
                    array.pop()
            if exp[i+1:] != '':
                top += 1
                array.append('_')
        elif exp[i] == ']': 
            while((not top == -1) and array[-1]  != '['): 

                #a = pop(top, array) 
                if not top == -1:
                    top -= 1
                    a =  array.pop()
                else:
                    a = "$"

                output.append(a) 
            output.append('?') 
            if (not top == -1 and array[-1]  != '['): 
                return -1
            elif not top == -1:
                    top -= 1
                    array.pop()
            if exp[i+1:] != '':
                top += 1
                array.append('_')
        elif exp[i] == '}': 
            while((not top == -1) and array[-1]  != '{'): 

                #a = pop(top, array) 
                if not top == -1:
                    top -= 1
                    a =  array.pop()
                else:
                    a = "$"

                output.append(a) 
            output.append('º')
            if (not top == -1 and array[-1]  != '{'): 
                return -1
            elif not top == -1:
                    top -= 1
                    array.pop()
            if exp[i+1:] != '':
                top += 1
                array.append('_')
        
        else: 
            while(not top == -1 and notGreater(exp[i], array) and exp[i] != 'º'): 
                top -= 1
                if exp[i] != 'º':
                    count -= 1
                b = array.pop()
                output.append(b) 

            top += 1
            array.append(exp[i])
        i += 1
    #print(array)
    #print(output)
    while not top == -1: 
        if not top == -1:
            top -= 1
            c =  array.pop()
        else:
            c = "$"
        output.append(c) 
    #print(output)
    return output


#print(conversionToPostfix("º"))
#print(conversionToPostfix('< .'))