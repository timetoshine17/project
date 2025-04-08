from konlpy.tag import Okt
okt = Okt()
with open('output.txt', 'r', encoding = 'utf-8') as f:
    text = f.read()
submit = okt.nouns(text)

with open('output2t.txt', 'w', encoding='utf-8') as f:
    for submits in submit:
        f.write(submits + '\n')

with open('output2t.txt', 'r', encoding='utf-8') as f:
    nouns = f.readlines()

nouns = [noun.strip() for noun in nouns]
unique_nouns = sorted(set(nouns))

with open('output2.txt', 'w', encoding='utf-8') as f:
    for noun in unique_nouns:
        f.write(noun + '\n')

