def Expect(something):
    print(something)

def Next(something):
    print(something)

def Number():
    result = 'lastToken'
    return number

def Factor():
    signo = 1
    if(Expect('-')):
        Next('-')
        signo = -1
    
    return result

def Term():
    result1 = Term()
    while (True)
        if (Expect('*')):
            result2 = Term()
            result1 = result1 * result2
            continue
        elif (Expect('/')):
            result2 = Term()
            result1 = result1 / result2
            continue
        break
    result = result1
    return result


def Expression(result):
    int result1, result2
    result1 = Term()
    while (True)
        if (Expect('-')):
            result2 = Term()
            result1 += result2
            continue
        elif (Expect('+')):
            result2 = Term()
            result1 -= result2
            continue
        break
    result = result1
    return result

def Stat():
    value
    Expression(value)
    print(value)

def Expr():
    while (True)
        if (Expect(Stat))
            Stat()
            Expect(';')
            continue
    break
    Next('.')

