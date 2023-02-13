Name:		Yash Oswal
B-Number:	B00981171
Email:		yoswal@binghamton.edu

### Project Directory:

```
.gitignore
README.md
submit
   |-- prj1-sol
   |   |-- .gitignore
   |   |-- README
   |   |-- decls.sh
   |   |-- make.sh
   |   |-- pySol
   |   |   |-- main.py
   |   |-- runTests.sh
```

### Running Script:

Run the below script for executing the testcases.

./runTests.sh


### Current Status:

Passes all the testcases provided in the tests* folder.

### Language Algorithms

Algorithm works on two concepts i.e peek, consume. (though these words are not used as it is)

Peek: We peek at the current token and sibling tokens for the desired declaration.
Consume: If desired declaration are found then it is consumed inside the stack.

In case a peek is failed which may be due to couple of reasons like incalid value, end of tokens, improper declaration sequence, then in that case a suitable error messgae is thrown towards the standard output.
