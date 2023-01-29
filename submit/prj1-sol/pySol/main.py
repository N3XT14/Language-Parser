import sys, re, json

result = []
lexStack = []
stateDP = []
reservedWords = ["var", "number", "string", "record"]
reservedTypeWordList = ["number", "string", "record"]

def isValidIdentifier(id):
    return id.isidentifier() and id not in reservedWords

def isValidType(id):
    return id in reservedTypeWordList

def multiRegSub(pairs, s):
    def repl_func(m):
        return next(
            repl
            for (patt, repl), group in zip(pairs, m.groups())
            if group is not None
        )
        
    #Generate Pairs 
    pattern = '|'.join("({})".format(patt) for patt, _ in pairs)
    return re.sub(pattern, repl_func, s)

def generateJsonArrayOP(inpList):
    inpList = multiRegSub([("'\[*[\[]'*,", '['),(", '\]'", ']'), (", '\]", ']'), ("\]'", ']'), ("\'","\"")], str(inpList))
    return inpList

def getInputFromStdin():
    inputBucket = [line for line in sys.stdin]
    return inputBucket

def createTokens(*args):
    tokens = []
    
    #Removing whitespaces from the tokens
    for id,tok in enumerate(args[0]):
        tok = tok.strip() #Remove whitespace

        if len(tok) == 0:
            continue
        elif tok.startswith("#"):
            continue
        tokens.append(tok)

    if len(tokens) == 0:
        return []
    print(tokens)
    return tokens

def performLexical(l):
    isVarFound = False
    isIDFound = False
    isColonFound = False
    isTypeFound = False
    isSemiColonFound = False
    recCnt, endCnt = 0,0
    try :
        # raise ValueError('A very specific bad thing happened')
        for i in l:
            if len(i) == 0: continue
            tmp = i.split()
            if len(tmp) == 0: continue
            
            i = 0
            while i < len(tmp):
                if tmp[i].startswith('#'): break
                val = tmp[i]
                
                #Special Case
                if recCnt != endCnt and val == "end;":
                    # print(isIDFound, isColonFound)
                    print("End Check", val)
                    endCnt += 1
                    lexStack.append(']]')
                    i += 1

                elif not isVarFound:
                    print("Var check", val)
                    if val != "var": raise KeyError("Syntax Error Found expected var")
                    isVarFound = True
                    i += 1
                elif isVarFound and not isIDFound:
                    print("Identifier Check ===> ", val)
                    if val.startswith(':'): raise ValueError("Identifier Missing")
                    if val.endswith(':'): 
                        val = val[:-1]
                        isColonFound = True
                    if not isValidIdentifier(val): raise AttributeError("Identifier used is incorrect. It cannot be from a reserverd word")
                    lexStack.append('[')
                    lexStack.append(val)
                    isIDFound = True
                    i += 1
                elif isVarFound and isIDFound and not isColonFound:
                    print("Colon Check ===> ", val)
                    if not val.startswith(':'): raise SyntaxError("Colon Needed")
                    if val == ":":
                        i += 1
                    isColonFound = True
                elif isVarFound and isIDFound and isColonFound and not isTypeFound:
                    print("Type Check ===> ", val)
                    if val.startswith(':'):
                        val = val[1:]
                    if val.endswith(';'):
                        val = val[:-1]
                        isSemiColonFound = True
                    if not isValidType(val): raise TypeError("Invalid value of the Type field")
                    
                    if val == 'record':
                        #Recursion
                        # recurRecord()
                        isRecordFound = True
                        stateDP.append([-1,-1,-1,-1,-1])
                        recCnt += 1
                        lexStack.append('[')

                    if recCnt != endCnt:
                        if val != 'record':
                            lexStack.append(val)
                            lexStack.append(']')
                        isTypeFound = False
                        isIDFound = False
                        isColonFound = False
                        isSemiColonFound = False
                    else:
                        lexStack.append(val)
                        lexStack.append(']')
                        isTypeFound = True
                    i += 1
                elif isVarFound and isIDFound and isColonFound and isTypeFound and not isSemiColonFound:
                    print("Semi Colon Check ===> ", val)
                    if val == ";":
                        isSemiColonFound = True
                    i += 1

                if isVarFound and isIDFound and isColonFound and isTypeFound and isSemiColonFound:
                    isVarFound = False
                    isIDFound = False
                    isColonFound = False
                    isTypeFound = False
                    isSemiColonFound = False
        return lexStack

    except KeyError as e:
        print(e)
    except AttributeError as e:
        print(e)
    except ValueError as e:
        print(e)
    except SyntaxError as e:
        print(e)
    except TypeError as e:
        print(e)

inpBucket = getInputFromStdin()
tokenList = createTokens(inpBucket)
lexStack = performLexical(tokenList)
# print(lexStack)
result = generateJsonArrayOP(lexStack)
# print("Result ====>", result, "\n", type(result))
# print("Result ====>", json.loads(result))
print(result)
print(stateDP)
# print(json.loads(result))
#print(inpBucket)
