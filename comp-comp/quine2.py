quine = '''quine = %s
quine = quine %% repr(quine)
print(quine)'''
quine = quine % quine
print(quine)