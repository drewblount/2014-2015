quine = 'quine = %squine = quine %% repr(quine)\nprint(quine)'
quine = quine % repr(quine)
print(quine)