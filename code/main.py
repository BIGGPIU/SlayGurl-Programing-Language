from syntax_tree import SyntaxParser,execute
import os
import sys

TOKEN = {
    "cap": "NEGATE",
    "💅": "PRINT",
    "diva":"INPUT",
    "✨": "VAR_DEC",
    "frfr": "IF",
    "anyways": "ELSE",
    "literally": "WHILE",
    "girl dinner": "FUNCTION",
    "ate": "RETURN",
    "period": "END",
    "💬":"STRING_ID",
    "+":"PLUS",
    "-":"MINUS",
    "*":"TIMES",
    "/":"DIVIDED",
    "%":"MODULO",
    "(":"LPAREN",
    ")":"RPAREN",
    "and":"AND",
    "or":"OR",
    ">":"GRATER",
    ">=":"GRATERE",
    "<":"LESSER",
    "<=":"LESSERE",
    "==":"EQUEL",
    "!=":"NEQUEL",
    "slay":"OPEN_BLOCK",
    "serve":"CLOSE_BLOCK",
    ",":"COMMA",
    "newline":"NEWLINE",
    "no delulu math":"NOGIRLMATH"
}

if len(sys.argv)<2:
    print("Slaaayy guurrl💅💅💅 compiler v1.0")
    sys.exit(0)

file_path = sys.argv[1]

if not os.path.exists(file_path):
    print("File does not exist:", file_path)
    sys.exit(1)

def tokenize(code):
    tokens=[]
    i=0
    n=len(code)
    while i<n:
        if i>=n:
            break
        if code[i].isspace():
            i+=1
            continue
        if code[i:i+len("💬")]=="💬":
                value=""
                i+=len("💬")
                while i<len(code) and code[i:i+len("💬")]!="💬":
                    value+=code[i]
                    i+=1
                i+=len("💬")
                tokens.append(("STRING",value))
                continue
        matched=False
        for key in sorted(TOKEN.keys(),key=len,reverse=True):
            if code[i:i+len(key)]==key:
                tokens.append((TOKEN[key],key))
                i+=len(key)
                matched=True
                break
        if matched:
            continue
        c=code[i]
        
        #numbers
        if c.isdigit():
            value=""
            while i<len(code)and code[i].isdigit():
                value+=code[i]
                i+=1
            tokens.append(("INT",int(value)))
            continue
        
        #variables
        if c.isalpha() or c=="_":
            value=""
            while i<len(code) and (code[i].isalnum() or code[i]=="_"):
                value +=code[i]
                i+=1
            if value in TOKEN:
                tokens.append((TOKEN[value],value))
            else:
                tokens.append(("VARIABLE",value))
            continue
        
        #operators
        if c=="=":
            tokens.append(("ASSIGN","="))
            i+=1
            continue
        
        i+=1
    return tokens


secretTokens=[
    ('WHILE', 'literally'),
    ('INT', 1),
    ('EQUEL', '=='),
    ('INT', 1),
    ('OPEN_BLOCK', 'slay'),
    ('PRINT', '💅'),
    ('STRING', 'peak'),
    ('END', 'period'),
    ('CLOSE_BLOCK', 'serve')
]

code=open(file_path,encoding="utf-8").read()
tokens=tokenize(code)

runPeak=True
if len(tokens)==len(secretTokens):
    for i in range (len(secretTokens)):
        if secretTokens[i][1]!=tokens[i][1]:
            runPeak=False
            break
else:
    runPeak=False
 
if runPeak: 
    match sys.platform:
        case "win32":
            os.startfile("steam://rungameid/105600")
        case "darwin":
            os.system("open steam://rungameid/105600")
        case _:
            os.system("xdg-open steam://rungameid/105600")
    sys.exit(0)

sp=SyntaxParser(tokens)
#for token in tokens:
#   print(token)
nodes=sp.parse_program()

execute(nodes)


