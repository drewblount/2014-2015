import numpy as np
import nltk
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import rc
from nltk.corpus import reuters
import re

matplotlib.rc('font', family='serif') 
matplotlib.rc('font', serif='Times') 
matplotlib.rc('text', usetex='false') 
matplotlib.rcParams.update({'font.size': 14})



def get_words_from_string(s):
    return re.findall(re.compile('\w+'), s.lower())

def get_words_from_file(fname):
    with open(fname, 'rb') as inf:
        return get_words_from_string(inf.read())


kant_words = get_words_from_file('kant_markov.txt')
wCounts = {}
for w in kant_words:
    if w in wCounts:
        wCounts[w]+=1
    else:
        wCounts[w]=1


## filter out all words that appear les than 5 times
minCount = 5
# This is pure sorted log word counts, no words (in reverse order)
logcounts = np.log(np.sort(np.array([wCounts[elem] for elem in wCounts])))

len(kant_words)
len(logcounts)

# ranks of each count (reverse order maintained)
logranks = np.log([len(logcounts)-i for i in range(len(logcounts))])

# fit with np.polyfit
m, b = np.polyfit(logranks, logcounts, 1)



plt.scatter(logranks, logcounts)

line = plt.plot(logranks, m*logranks + b, '-', label='slope = %.2f'%m)
plt.xlabel('log(frequency rank)')
plt.legend()
plt.ylabel('log(frequency)')
plt.title('Zipf plot of Carroll\'s Alice\'s...Wonderland')
plt.show()


#reuters_words = [w.lower() for w in reuters.words()]
