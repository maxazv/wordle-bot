import math
import numpy as np

def numberToBase(n, b):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits[::-1]
def fromBase3(num):
	res = 0
	for i in range(len(num)):
		res += (int(num[i])) * math.pow(3, (len(num)-i-1))
	return int(res)

class wordle_bot:
	def __init__(self, wordlist=None, patterns=None):
		self.total = wordlist
		self.words = None
		self.patterns = np.asarray(patterns)
		self.scannedPatterns = np.zeros(self.patterns.size)
		self.filtered = {}


	''' storing and loading of words '''
	def loadWords(self, path='../res/sgb-words.txt'):
		words = []
		with open(path, 'r') as rf:
			for line in rf:
				words.append(line[:-1])
		self.words = words
		self.total = words

	def loadPatterns(self, length=5):
		# creates all possible patterns for a word of a certain length
		size = int(math.pow(3, length))-1
		res = np.zeros(shape=(size+1, 5))
		pattern = [0, 0, 0, 0, 0]
		res[0] = pattern
		for i in range(size):
			num = fromBase3(pattern)

			pattern = numberToBase(num+1, 3)
			if len(pattern) < 5:
				for j in range(5-len(pattern)):
					pattern.insert(0, 0)

			res[i+1] = pattern
		self.patterns = res

	def loadTop(self, path='../res/top-words.txt'):
		top = {}
		with open(path, 'r') as rf:
			for line in rf:
				pair = line.split(":")
				top[pair[0]] = float(pair[1][0:-1])
		self.filtered = top

	def storeData(data):
		with open('../res/top-words.txt', 'w') as wf:
			for k, v in data.items():
				wf.write(f'{k}:{v}\n')

	def setup(self):
		self.loadWords()
		self.loadPatterns()
		self.loadTop()


	''' bot body '''
	def __match(self, frame, word):
		# check whether word fits a certain frame
		# here a "frame" is defined as tuple(pattern, word)
		for i in range(len(frame[0])):
			if frame[0][i] == 0:
				if frame[1][i] in word:
					return False

			elif frame[0][i] == 1:
				if frame[1][i] not in word or frame[1][i] == word[i]:
					return False

			else:
				if frame[1][i] != word[i]:
					return False	
		return True

	def filter(self, frame):
		# output all words which fit the frame
		return [word for word in self.words if self.__match(frame, word)]

	''' information theory '''
	def chance(self, frame, total):
		return len(self.filter(frame))/len(self.words)

	def entropy(self, word):
		probs = [self.chance((pattern, word), self.words) for pattern in self.patterns]
		entropy = -sum([p*-math.log2(1/p) if p != 0 else 0 for p in probs])
		return entropy

	def calcWordsEntropy(self, sort=True):
		allEnts = {word: self.entropy(word) for word in self.words}
		if sort:
			allEnts = {k: v for k, v in sorted(allEnts.items(), key=lambda item:item[1], reverse=True)}
		return allEnts

	def getTop(self, to=10):
		return [list(self.filtered.items())[:to]]