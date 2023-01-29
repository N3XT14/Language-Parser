import sys

result = []
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

inpBucket = getInputFromStdin()
result = createTokens(inpBucket)

print(result)
#print(inpBucket)
