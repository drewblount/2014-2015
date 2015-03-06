#time-saving script-writer for uploading all the htmls to reed.edu

def s(i):
    print('''
cd html/hypertext
mkdir net_%d
put node*
    ''' % i)