from konlpy.tag import Okt
okt = Okt()
with open('text/1.txt','r', encoding='utf-8') as f:
    text = f.read()
phrases = okt.phrases(text)

with open('output.txt', 'w', encoding='utf-8') as f:
    for phrase in phrases:
        f.write(phrase + '\n')