
import argparse
parser = argparse.ArgumentParser(description="Check if transcriptions in refhyp are contained in test.csv and have the same ID.")
parser.add_argument("namef", type=str, help="Path to a Kaldi test file output")
args = parser.parse_args()

def removeEPS(sentence):
    sentencelist = sentence.split(" ")
    newsent = []
    for word in sentencelist:
        if word != "<eps>":
            newsent.append(word)
    return " ".join(newsent)

dico = dict()
with open(args.namef + "/refhyp.txt", "r", encoding="utf8") as file:
    for ligne in file:
        line = ligne.split("\t")
        ref = removeEPS(line[1])
        id = line[0]
        dico[id] = ref

dico_test = dict()
with open("test.csv", "r", encoding="utf8") as file:
    next(file)
    for ligne in file:
        line = ligne[:-1].split(",")
        ref = line[3].lower()
        id = line[0]
        dico_test[id] = ref

# checker que chaque id de dico correspond à la réf de dico_test
counter = 0
different = 0
for k, v in dico.items(): # pour chaque élément de refhyp
    if k not in dico_test: # si l'élément de réfhyp n'est pas dans test.csv
        counter += 1
    else:
        if v != dico_test[k]:
            """print(v)
            print(dico_test[k])
            exit(-1)"""
            different += 1
print(str(counter) + " segments de " + args.namef + "/refhyp.txt ne sont pas dans test.csv. (" + str(counter/len(dico)*100) + "%)")
print(str(different) + " segments de " + args.namef + "/refhyp.txt ne correspondent pas à test.csv. (" + str(different/len(dico)*100) + "%)")

input()

# checker que chaque id de dico_test correspond à la réf de dico
counter = 0
different = 0
for k, v in dico_test.items():
    if k not in dico:
        counter += 1
    else:
        if v != dico[k]:
            different += 1
print(str(counter) + " segments de test.csv ne sont pas dans " + args.namef + "/refhyp.txt. (" + str(counter/len(dico_test)*100) + "%)")
print(str(different) + " segments de " + args.namef + "/refhyp.txt ne correspondent pas à test.csv. (" + str(different/len(dico_test)*100) + "%)")


# LES FICHIERS NE CORRESPONDENT PAS DU TOUT (moins de 4%)
# Regarder comment est généré le test.csv de REPERE

# Sinon, directement pendant la génération des IDs, checker dans test.csv la phrase égale issu du même
# fichier (BFMTV_BFMStory_2012-07-24_175800 comporte plusieurs audio)