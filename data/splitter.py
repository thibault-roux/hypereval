import os


systems = ["SB_w2v", "KD_woR", "KD_wR", "SB_bpe1000", "SB_bpe750", "SB_s2s", "SB_w2v_1k", "SB_w2v_3k", "SB_w2v_7k", "SB_xlsr_fr", "SB_xlsr"]
# systems = ["KD_woR"]


def add(dico, ref, hyp, system):
    if ref in dico:
        if hyp in dico[ref]:
            dico[ref][hyp].append(system)
        else:
            dico[ref][hyp] = [system]
    else:
        dico[ref] = dict()
        dico[ref][hyp] = [system]


def removeEPS(sentence):
    new_sentence_list = []
    sentence_list = sentence.split(" ")
    for word in sentence_list:
        if word != '<eps>':
            new_sentence_list.append(word)
    return ' '.join(new_sentence_list)


dico = dict() # dico[ref][hyp] = [KD_wR, SB_w2v, SB_xlsr]
for system in systems: # Associer reference, hypothesis to their system
    with open(system+"/"+system+"1.txt", "r", encoding="utf8") as file:
        for ligne in file:
            line = ligne.lower().split("\t")
            ref = removeEPS(line[1])
            hyp = removeEPS(line[2])
            add(dico, ref, hyp, system)


subsets = dict()
for system in systems:
    subsets[system] = set()

# Récupérer les transcriptions de autoselect dans subsets
hyp1error = 0
hyp2error = 0
referror = 0
correct = 0
with open("autoselect.txt", "r", encoding="utf8") as file:
    for ligne in file:
        line = ligne.split("\t")
        id = line[0]
        ref = line[1]
        hyp1 = line[2]
        hyp2 = line[3]
        
        if ref in dico:
            # print(ref)
            # print(hyp1)
            # input()
            if hyp1 in dico[ref]:
                correct += 1
                systs = dico[ref][hyp1]
                for sys in systs:
                    subsets[sys].add(id + "\t" + ref + "\t" + hyp1 + "\t_\n")
            else:
                hyp1error += 1
            if hyp2 in dico[ref]:
                correct += 1
                systs = dico[ref][hyp2]
                for sys in systs:
                    subsets[sys].add(id + "\t" + ref + "\t" + hyp2 + "\t_\n")
            else:
                hyp2error += 1
        else:
            referror += 1

# Write subsets in files

for system in systems:
    txt = ""
    for t in subsets[system]:
        txt += t

    path = os.path.join(os.getcwd(), "subset_" + system)
    if not os.path.exists(path):
        os.makedirs(path)
    print(path)
    with open(path+"/refhyp.txt", "w", encoding="utf8") as file:
        file.write(txt)
    
print("Terminus.")
print("hyp1error:", hyp1error)
print("hyp2error:", hyp2error)
print("referror:", referror)
print("correct:", correct)