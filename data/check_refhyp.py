

"""
Regarder les refhyp de KD_woR et KD_wR et vérifier s'ils contiennent la même chose
(dans un ordre différent peut-être ?)

Juste utile pour moi pour faire des vérifications pour certains bugs
"""

class EZdico:
    def __init__(self):
        self.dico = dict()

    def add(self, val):
        if val in self.dico:
            self.dico[val] += 1
        else:
            self.dico[val] = 1

    def getDict(self):
        return self.dico


def getdict(id):
    refs = EZdico()
    with open(id + "/refhyp.txt", "r", encoding="utf8") as file:
        for ligne in file:
            refs.add(ligne.split("\t")[0])
    return refs.getDict()

woR = getdict("KD_woR")
wR  = getdict("KD_wR")


print(len(woR.keys()))
print(len(wR.keys()))

lwor = []
for k, v in woR.items():
    if k not in wR:
        lwor.append(k)

lwr = []
for k, v in wR.items():
    if k not in woR:
        lwr.append(k)

from Levenshtein import distance as lv

k = 0
scores = []
bests = []
print(len(lwor), len(lwr))
for i in range(len(lwor)):
    scoremin = 99999
    for j in range(len(lwr)):
        score = lv(lwor[i], lwr[j])
        if scoremin > score:
            scoremin = score
            best = lwr[j]
    scores.append(score)
    bests.append(best)

print(scores)

ref = dict()
hyp = dict()
for i in range(len(bests)):
    print(scores[i])
    print(lwor[i], len(lwor[i]))
    print(bests[i], len(bests[i]))
    print()

    ref[i] = lwor[i].split(" ")
    hyp[i] = bests[i].split(" ")


from speechbrain.utils.edit_distance import wer_details_by_utterance as wer_details
from speechbrain.dataio.wer import print_alignments



d = wer_details(ref, hyp, compute_alignments=True)
print_alignments(d, open("temp.txt", "w", encoding="utf8"))
