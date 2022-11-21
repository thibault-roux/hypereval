
import argparse
parser = argparse.ArgumentParser(description="Transform Kaldi output file to a ref hyp file")
parser.add_argument("namef", type=str, help="Path to a Kaldi test file output")
args = parser.parse_args()


def deal_with_spaces_and_asterix(sentence): #peut-être que je devrais supprimer les eps et réutiliser le code de Speechbrain
    sentence = sentence.lower().split(" ")
    newstence = []
    for word in sentence:
        if word != "":
            """if word[0] == "*":
                newstence.append("<eps>")
            else:"""
            if word[0] != "*":
                newstence.append(word)
    return newstence






# #---------associer les fichiers avec la bonne ID/miniID

def addInDic(dico, id, id2, value):
    if id in dico:
        if id2 in dico[id]:
            dico[id][id2] = value
        else:
            dico[id][id2] = value
    else:
        dico[id] = dict()
        dico[id][id2] = value

id2min = dict()
id2ref = dict() # TO DELETE
with open("stmall.txt", "r", encoding="utf8") as file:
    for ligne in file:
        line = ligne[:-1].split(",")
        minid = line[0].split("_")[-1]
        id = line[0][:-1-len(minid)] 
        timestamp = str(float(line[1])) + "," + str(float(line[2]))
        ref = line[3]
        addInDic(id2min, id, timestamp, minid) # id2min[id][timestamp] = minid
        addInDic(id2ref, id, timestamp, ref) # id2ref[id][timestamp] = ref


def realID(id, t1, t2):
    timestamp = str(float(t1)) + "," + str(float(t2))
    try:
        return id + "_" + id2min[id][timestamp]
    except KeyError:
        print("Error occured.")
        for k, v in id2min[id].items():
            if float(k.split(",")[0]) == float(t1) or float(k.split(",")[1]) == float(t2):
                print(k)
                return id + "_" + v
        raise



#with open(args.namef + "/repere_3g.9.ci.pra", "r", encoding="utf8") as file:
with open(args.namef + "/repere_rnnlm.9.ci.pra", "r", encoding="utf8") as file:
    next(file)
    next(file)
    ligne = next(file)
    id = ligne[:-1].split(" ")[1]
    txt = ""

    n_ligne = 0
    for ligne in file:
        n_ligne += 1
        if ligne[:12] == "Start-time: ":
            t1 = ligne[:-1].split(" ")[1]
        elif ligne[:10] == "End-time: ":
            t2 = ligne[:-1].split(" ")[1]
        elif ligne[:6] == "REF:  ":
            temp = deal_with_spaces_and_asterix(ligne[6:-1])
            ref = " ".join(temp)
        elif ligne[:9] == ">> REF:  ":
            temp = deal_with_spaces_and_asterix(ligne[9:-1])
            ref += " " + " ".join(temp)
        elif ligne[:6] == "HYP:  ":
            temp = deal_with_spaces_and_asterix(ligne[6:-1])
            hyp = " ".join(temp)
        elif ligne[:9] == ">> HYP:  ":
            temp = deal_with_spaces_and_asterix(ligne[9:-1])
            hyp += " " + " ".join(temp)
        elif ligne[:5] == "File:":
            fullid = realID(id, t1, t2)
            #print(fullid)
            #if id2ref[id][t1 + "," + t2]
            txt += fullid + "\t" + ref + "\t" + hyp + "\t_\n"

            id = ligne[:-1].split(" ")[1]
    fullid = realID(id, t1, t2)
    txt += fullid + "\t" + ref + "\t" + hyp + "\n"

with open(args.namef + "/refhyp.txt", "w", encoding="utf8") as file:
    file.write(txt)
