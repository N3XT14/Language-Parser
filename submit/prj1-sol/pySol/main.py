import sys, re, json

result = []
lexStack = []
reservedWords = ["var", "number", "string", "record"]
reservedTypeWordList = ["number", "string", "record"]

def isValidIdentifier(id):
    if id.endswith(':'): id = id[:-1]
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

    return tokens

def performLexical(l):
    isVarFound = False
    isIDFound = False
    isColonFound = False
    isTypeFound = False
    isSemiColonFound = False
    recCnt, endCnt = 0,0
    tmp = []
    try :

        for i in l:
            if len(i) == 0: continue
            stmp = i.split()
            
            if len(stmp) == 0: continue

            for ele in stmp:
                if ele.startswith('#'):
                    break
                else:
                    tmp.extend([ele])
            
        i = 0
        while i < len(tmp):
            if tmp[i].startswith('#'): break
            val = tmp[i]
            
            #Special Case
            if recCnt != endCnt and val == "end;":
                endCnt += 1
                lexStack.append(']]')
                i += 1
            elif recCnt != endCnt and val == "end":
                if i >= len(tmp) - 1 or tmp[i+1] != ';':
                    raise SyntaxError("Semicolon Missing")
                endCnt += 1
                lexStack.append(']]')
                i += 1
            elif not isVarFound:
                if val != "var": raise KeyError("Syntax Error Found expected var")
                if i >= len(tmp) - 1:
                    raise ValueError("Identifier Missing")
                isVarFound = True
                i += 1
            elif isVarFound and not isIDFound:
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
                if not val.startswith(':'): raise SyntaxError("Colon Needed")
                if val == ":":
                    i += 1
                isColonFound = True
            elif isVarFound and isIDFound and isColonFound and not isTypeFound:
                if val.startswith(':'):
                    val = val[1:]
                if val.endswith(';'):
                    val = val[:-1]
                    isSemiColonFound = True
                if not isValidType(val): raise TypeError("Invalid value of the Type field")
                
                if not isSemiColonFound:
                    if i >= len(tmp) - 1: 
                        raise SyntaxError("Semicolon Missing")
                    if not tmp[i+1].startswith(';') and val != 'record':
                        raise SyntaxError("Semicolon Missing")
                
                #Perform Lookahead
                if val == 'record':
                    if not isValidIdentifier(tmp[i+1]):
                        print(tmp[i+1])
                        raise SyntaxError('Identifier expected after record')
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
                # print("Semi Colon Check ===> ", val)
                if val == ";":
                    isSemiColonFound = True
                else:
                    raise SyntaxError("Semicolon Missing")
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
        sys.exit(1)
    except AttributeError as e:
        print(e)
        sys.exit(1)
    except ValueError as e:
        print(e)
        sys.exit(1)
    except SyntaxError as e:
        print(e)
        sys.exit(1)
    except TypeError as e:
        print(e)
        sys.exit(1)

inpBucket = getInputFromStdin()
tokenList = createTokens(inpBucket)
lexStack = performLexical(tokenList)
result = generateJsonArrayOP(lexStack)

print(result)

