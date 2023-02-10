import sys, re, json

#Global Language Reserved Words.
reservedWords = ["var", "number", "string", "record"]
reservedTypeWordList = ["number", "string", "record"]


#Helper Function: Checks whether the identifier passed is Valid.
def isValidIdentifier(id):
    if id.endswith(':'): id = id[:-1]
    return id.isidentifier() and id not in reservedWords


#Helper Function: Checks whether the declaration passed is Valid.
def isValidType(id):
    return id in reservedTypeWordList


#Function for substitution of string using regex.
#Creates pairs of regex passed as an list.
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


#Function to modify output such that it represents JSON Structure.
def generateJsonArrayOP(inpList):
    inpList = multiRegSub([("'\[*[\[]'*,", '['),(", '\]'", ']'), (", '\]", ']'), ("\]'", ']'), ("\'","\"")], str(inpList))
    return inpList


#Function to collect from standard input.
def getInputFromStdin():
    inputBucket = [line for line in sys.stdin]
    return inputBucket


#Generates a list of tokens for lexical analysis.
def createTokens(*args):
    tokens = []
    
    for id,tok in enumerate(args[0]):
        tok = tok.strip() #Remove whitespace

        if len(tok) == 0: #Remove empty tokens
            continue
        elif tok.startswith("#"): #Remove Comments
            continue
        tokens.append(tok)

    if len(tokens) == 0:
        return []

    return tokens


#Performs Lexical Analysis to return a valid string or an appropriate error.
#Uses lookahead/peeks before consuming the current into the stack.
def performLexical(l):
    isVarFound = False
    isIDFound = False
    isColonFound = False
    isTypeFound = False
    isSemiColonFound = False
    recCnt, endCnt = 0,0
    lexStack, tmp = [], []
    try :

        #Following Loop creates a list containing tokens withtout comments, empty strings.
        for i in l:
            if len(i) == 0: continue #Avoid empty string
            stmp = i.split()
            
            if len(stmp) == 0: continue #Avoid emtpy string tokens.

            for ele in stmp:
                if ele.startswith('#'): #Ignore the list of tokens when comments found.
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

                #If "var" not encountered then check for "var".
                if val != "var": raise KeyError("Syntax Error Found expected var")
                
                if i >= len(tmp) - 1:
                    raise ValueError("Identifier Missing")
                
                isVarFound = True
                i += 1
            elif isVarFound and not isIDFound:
                
                if val.startswith(':'): raise ValueError("Identifier Missing") #Handle: ID starting with ":"
                
                #Handle: Peek if ID ends with ":" and if yes then consume it.
                if val.endswith(':'): 
                    val = val[:-1]
                    isColonFound = True
                
                #Handle: Check if identifier is a valid one or not.
                if not isValidIdentifier(val): raise AttributeError("Identifier used is incorrect. It cannot be from a reserverd word")
                
                lexStack.append('[')
                lexStack.append(val)
                isIDFound = True
                i += 1
            elif isVarFound and isIDFound and not isColonFound:
                
                #Checks whether colon is present or not.
                if not val.startswith(':'): raise SyntaxError("Colon Needed")
                if val == ":":
                    i += 1
                isColonFound = True
            elif isVarFound and isIDFound and isColonFound and not isTypeFound:

                if val.startswith(':'): #Handle: if Type starts with ":" then transform.
                    val = val[1:]

                if val.endswith(';'): #Handle: if Type ends with ";".
                    val = val[:-1]
                    isSemiColonFound = True

                #Handle: Check if the Type is valid or not.
                if not isValidType(val): raise TypeError("Invalid value of the Type field")
                
                #Handle: Check for Semicolon
                #Case1: if tokens exhausted then throw error.
                #Case2: if Type is not "record" check for semicolon.
                if not isSemiColonFound:
                    if i >= len(tmp) - 1: 
                        raise SyntaxError("Semicolon Missing")
                    if not tmp[i+1].startswith(';') and val != 'record':
                        raise SyntaxError("Semicolon Missing")
                
                #Handle: Check for "record" declaration and perform peek on next token for Valid Identifier.
                if val == 'record':
                    if not isValidIdentifier(tmp[i+1]):
                        raise SyntaxError('Identifier expected after record')
                    recCnt += 1
                    lexStack.append('[')
                
                #Set All Found Flags as False if record declaration is present in grammar to rerun the above checks.
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

                #Handle: Perform Check for Semicolon.
                if val == ";":
                    isSemiColonFound = True
                else:
                    raise SyntaxError("Semicolon Missing")
                i += 1

            #Reset Flags to Re Run.
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

inpBucket = getInputFromStdin() #Gets Input
tokenList = createTokens(inpBucket) #Creates Token
lexStack = performLexical(tokenList) #Perform Lexical Analysis
result = generateJsonArrayOP(lexStack) #If valid output then generate JSON Output structure.

print(result) #Print to standard output.
