quine = 'quine = %s\nquine = quine %% repr(quine)\nprint(quine)'
quine = quine % repr(quine)
print(quine)