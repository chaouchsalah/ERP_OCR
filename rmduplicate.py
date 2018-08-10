

file = open('big2.txt',encoding='utf-8')
lines = file.readlines()
new_file = ''
new_lines = []
i=0
for line in lines:
    print(i)
    i += 1
    try:
        new_lines.append(line.lower())
        lines.remove(line)
    except ValueError:
        print('passed')
        pass
print(new_lines)
file = open('new_big.txt','w+',encoding='utf-8')
file.writelines(new_lines)