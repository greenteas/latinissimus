infile = open('latinwords.csv','r')
rows = list(infile)
dict = {}
latin = []
english = []
for i in rows[:21]:
	line = i
	line = line.split("|")
	latin_word = line[0]
	english_word = line[1]
	n = len(english_word)
	english_word = english_word[:n-1]
	latin.append(latin_word)
	english.append(english_word)
	dict[latin_word] = english_word

infile.close()