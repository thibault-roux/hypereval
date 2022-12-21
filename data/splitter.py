

systems = ["KD_woR", "KD_wR", "SB_bpe1000", "SB_bpe750", "SB_s2s", "SB_w2v_1k", "SB_w2v_3k", "SB_w2v_7k", "SB_xlsr_fr", "SB_xlsr"]


# dico[ref][hyp"] = [KD_wR, SB_w2v, SB_xlsr]

def add(dico, ref, hyp, system):
    if ref in dico:
        if hyp in dico[ref]:
            dico[ref][hyp].append(system)
        else:
            dico[ref][hyp] = [system]
    else:
        dico[ref] = dict()


def removeEPS(sentence):
    new_sentence_list = []
    sentence_list = sentence.split(" ")
    for word in sentence_list:
        if word != '<eps>':
            new_sentence_list.append(word)
    return ' '.join(new_sentence_list)


dico = dict()
for system in systems:
    with open(system+"/"+system+"1.txt", "r", encoding="utf8") as file:
        for ligne in file:
            line = ligne.lower().split("\t")
            ref = removeEPS(line[1])
            hyp = removeEPS(line[2])
            add(dico, ref, hyp, system)

subsets = dict()
for system in systems:
    subsets[system] = ""

with open("autoselect.txt", "r", encoding="utf8") as file:
    for ligne in file:
        line = ligne.split("\t")
        ref = line[1]
        hyp1 = line[2]
        hyp2 = line[3]
        
        if ref in dico:
            if hyp1 in dico[ref]:
                systs = dico[ref][hyp]
                for sys in systs:

# mettre autoselect dans hypereval et lancer l'expé