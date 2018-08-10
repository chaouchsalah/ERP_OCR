output_file = 'fra.cube.word-freq'
file = open(output_file, "r", encoding="utf8")
words = open('big.txt','w', encoding="utf8")
for line in file:
    word = line.split('\t')[0]
    occ = line.split('\t')[1]
    words.write(word+' '+occ)
words.close()