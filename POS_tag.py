from flair.data import Sentence
from flair.models import SequenceTagger

extended_POS = True

print("Loading Flair tagger...")
if extended_POS:
    tagger = SequenceTagger.load("qanastek/pos-french")
else:
    #tagger = SequenceTagger.load("flair/upos-multi") #-fast")
    tagger = SequenceTagger.load("flair/upos-multi-fast")
print("Flair tagger loaded.")

"""
Il va falloir que je retire les apostrophes du corpus pour le tagging de POS.
"""

# iterate over entities and print
def getPosTxt(sentence):
    """
    Input :
        sentence = #Format Sentence with associated POS
    Output :
        pos = "PRON VERB ADJ"
    """
    pos = ""
    temp = sentence.get_spans()
    for i in range(len(temp)):
        pos += temp[i].tag + " "
    pos = pos[:-1]
    return pos

def get_list_index(elem, l):
    return [i for i,d in enumerate(l) if d==elem]

def POS(sentence):
    """
    Input :
        sentence = "BONJOUR JE VAIS BIEN <eps> <eps>"
    Output :
        pos = #part-of-speech of sentence with <eps> symbol instead of pos
    """
    #The next part is useful to delete <eps> from the sentence but to keep it in memory
    sentence = sentence.split(" ")
    eps_index = get_list_index("<eps>", sentence)
    eps_index.sort(reverse=True)
    for ind in eps_index:
        del sentence[ind]
    sentence = " ".join(str(x) for x in sentence)

    #Prediction of POS
    sentence = Sentence(sentence)
    tagger.predict(sentence)
    pos = getPosTxt(sentence)

    #Adding <eps> in POS sentence
    pos = pos.split(" ")
    eps_index.sort()
    for ind in eps_index:
        pos.insert(ind, "<eps>")
    pos = " ".join(str(x) for x in pos)
    return pos

def correct(txt):
    txt_ = ""

    i = 0
    for c in txt:
        if c == ">":
            if txt[i-4:i+1] == "<eps>":
                txt_ += c
        else:
            if c not in ["'", "(", ")", "=", "/", "\\", ";", ".", "!", "ã", "©", "ª", "¨", "§", "»"]:
                txt_ += c
        i += 1
    #print("txt_ : " + txt_)
    return txt_

def tag(id):
    ref = []
    hyp = []
    j = 0
    i_stock = []
    with open("data/" + id + "/" + id + "1.txt", "r", encoding="utf8") as file:
        for ligne in file:
            j += 1
            l1 = ligne.split("\t")[1]
            l2 = ligne.split("\t")[2]
            if l1 != '':
                l1_ = l1.split(" ")
                for i in range(len(l1_)):
                    if l1_[i] != "<eps>":
                        ref.append(l1)
                        hyp.append(l2)
                        i_stock.append(j)
                        break
    error_count = 0


    #Pour chaque POS de la réf, j'ajoute le POS de la transcription associé dans le dictionnaire ci-dessous
    if extended_POS:
        list_pos = ['ADJ', 'ADJFP', 'ADJFS', 'ADJMP', 'ADJMS', 'ADV', 'AUX', 'CHIF', 'COCO', 'COSUB', 'DET', 'DETFS', 'DETMS', 'DINTFS', 'DINTMS', 'INTJ', 'MOTINC', 'NFP', 'NFS', 'NMP', 'NMS', 'NOUN', 'NUM', 'PART', 'PDEMFP', 'PDEMFS', 'PDEMMP', 'PDEMMS', 'PINDFP', 'PINDFS', 'PINDMP', 'PINDMS', 'PPER1S', 'PPER2S', 'PPER3FP', 'PPER3FS', 'PPER3MP', 'PPER3MS', 'PPOBJFP', 'PPOBJFS', 'PPOBJMP', 'PPOBJMS', 'PREF', 'PREFP', 'PREFS', 'PREL', 'PRELFP', 'PRELFS', 'PRELMP', 'PRELMS', 'PREP', 'PRON', 'PROPN', 'PUNCT', 'SYM', 'VERB', 'VPPFP', 'VPPFS', 'VPPMP', 'VPPMS', 'X', 'XFAMIL', 'YPFOR', '<eps>']
        list_pos.sort()
        POS_matrix = dict()
        for p in list_pos:
            POS_matrix[p] = []
    else:
        POS_matrix = {"ADJ":[],"ADP":[],"ADV":[],"AUX":[],"CCONJ":[],"DET":[],"INTJ":[],"NOUN":[],"NUM":[],"PART":[],"PRON":[],"PROPN":[],"PUNCT":[],"SCONJ":[],"SYM":[],"VERB":[],"X":[], "<eps>":[]}

    POS_to_file = ""


    for i in range(len(ref)):
        """if i < 2200: #39.863
            continue"""
        if i%40 == 0:
            print("POS tagging... " + str(i/len(ref)*100) + "%")
        r = POS(correct(ref[i]))
        h = POS(correct(hyp[i]))
        POS_to_file += str(i_stock[i]) + "\t" + r + "\t" + h + "\t_\n"
        #print(r)
        #print(h)

        r = r.split(" ")
        h = h.split(" ")
        if len(r) != len(h):
            print("Error: Different length between reference and hypothesis !")
            """print(len(ref[i].split(" ")), ref[i], correct(ref[i]))
            print(len(r), r)
            print(len(hyp[i].split(" ")), hyp[i], correct(hyp[i]))
            print(len(h), h)
            exit(-1)"""
            error_count += 1
            continue
        for j in range(len(r)):
            try:
                POS_matrix[r[j]].append(h[j])
            except KeyError:
                print("KeyError: " + str(r[j]))
                print(i)
                print(str(len(ref[i])) + ", ref : '" + str(ref[i]) + "'")
                print(str(len(hyp[i])) + ", hyp : '" + str(hyp[i]) + "'")
                print(r)
                print(h)
                exit(-1)

    #print("Pourcentage d'erreur dans le POS_tagging : " + str(error_count/20*100))
    print("Pourcentage d'erreur dans le POS_tagging : " + str(error_count/len(ref)*100))

    with open("data/" + id + "/" + id + "3.txt", "w", encoding="utf8") as file:
        file.write(POS_to_file)

    print("data/" + id + "/" + id + "3.txt")

