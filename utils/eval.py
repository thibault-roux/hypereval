import numpy as np
from scipy import spatial

"""
Compute metrics at the local level

 - Word Error Rate (WER)
 - Character Error Rate (CER)
 - Universal Part-of-Speech Error Rate (uPOSER) & Detailed Part-of-Speech Error Rate (dPOSER)
 - Lemme Error Rate (LER)
 - Embedding Error Rate (EmbER)
 - Semantic Distance variant (SemDist)
 - BERTScore (BERTScore)
 
"""


def removeEPS(ligne):
    retour = ""
    ligne = ligne.split(" ")
    for i in range(len(ligne)):
        if ligne[i] != "<eps>":
            retour += ligne[i] + " "
    return retour[:-1]




"""-------------Automatic choice of POS---------------"""
def prepare_POS(argsid):
    temp_pos = set()
    with open("data/" + argsid + "/" + argsid + "4.txt", "r", encoding="utf8") as file:
        for ligne in file:
            ligne = ligne.split("\t")
            for pos in ligne[1].split(" "):
                temp_pos.add(pos)
    POS_possible1 =['ADJ', 'ADJFP', 'ADJFS', 'ADJMP', 'ADJMS', 'ADV', 'AUX', 'CHIF', 'COCO', 'COSUB', 'DET', 'DETFS', 'DETMS', 'DINTFS', 'DINTMS', 'INTJ', 'MOTINC', 'NFP', 'NFS', 'NMP', 'NMS', 'NOUN', 'NUM', 'PART', 'PDEMFP', 'PDEMFS', 'PDEMMP', 'PDEMMS', 'PINDFP', 'PINDFS', 'PINDMP', 'PINDMS', 'PPER1S', 'PPER2S', 'PPER3FP', 'PPER3FS', 'PPER3MP', 'PPER3MS', 'PPOBJFP', 'PPOBJFS', 'PPOBJMP', 'PPOBJMS', 'PREF', 'PREFP', 'PREFS', 'PREL', 'PRELFP', 'PRELFS', 'PRELMP', 'PRELMS', 'PREP', 'PRON', 'PROPN', 'PUNCT', 'SYM', 'VERB', 'VPPFP', 'VPPFS', 'VPPMP', 'VPPMS', 'X', 'XFAMIL', 'YPFOR', '<eps>']
    POS_possible1.sort()
    POS_possible2 = ["<eps>", "ADJ","ADP","ADV","AUX","CCONJ","DET","INTJ","NOUN","NUM","PART","PRON","PROPN","PUNCT","SCONJ","SYM","VERB","X"] #à adapter selon besoin
    POS_possible = []
    for e in temp_pos:
        POS_possible.append(e)
    POS_possible.sort()
    if POS_possible != POS_possible1 and POS_possible != POS_possible2:
        print("POS automatically detecty are not as usual. We only kept the following POS:")
        if (len(POS_possible)-len(POS_possible2))**2 < (len(POS_possible)-len(POS_possible2))**2:
            POS_possible = POS_possible2
        else:
            POS_possible = POS_possible1
        print(POS_possible)
        """answer = input("Continue ? (o/n) : ")
        if answer == "n":
            print("This program ended as requested.")
            exit(0)
        elif answer != "o":
            print("Unexpected answer. End of program.")
            exit(0)"""

    """-------------Mapper-POS---------------"""
    #Detailed Part-Of-Speech are too many. We used a mapping from dPOS to uPOS to reduce the number of classes
    mapper = dict()
    mapper["<eps>"] = "<eps>"
    mapper[''] = ''
    with open("utils/mapping.txt", "r", encoding="utf8") as file:
        for ligne in file:
            ligne = ligne[:-1].split("\t")
            mapper[ligne[0]] = ligne[1]
    return mapper




def totxt(metric_list, id_list, name): # metric_list is the list containing the local score for each transcription
    if len(metric_list) != len(id_list):
        raise DifferentLength("metric_list and id_list do not have the same length.")
    with open("results/correlation/" + name + ".txt", "w", encoding="utf8") as file:
        for i in range(len(metric_list)):
            file.write( id_list[i] + "\t" + str(metric_list[i]) + "\n")




"""---------------Word Error Rate---------------"""
def wer(argsid, fresults):
    with open("data/" + argsid + "/" + argsid + "2.txt", "r", encoding="utf8") as file:
        total = 0
        errors = 0
        wer_list = [] 
        id_list = [] 
        for ligne in file:
            errors_local = 0 
            total_local = 0 
            for err in ligne.split("\t")[2].split(" "): # for each error (S I =)
                if err != "=":
                    errors += 1
                    errors_local += 1 
                if err != "I": # Insertions are not counted comptabilisés in the total of words
                    total += 1
                    total_local += 1 
            wer_list.append(errors_local/total_local*100) 
            id_list.append(ligne.split("\t")[0]) 
    fresults.write("WER: ")
    a = "{:.2f}".format(float(errors/total)*100)
    fresults.write(a)
    fresults.write("\n")

    totxt(wer_list, id_list, "wer_" + argsid)
    print("WER done")


"""---------------detailed POS Error Rate---------------"""
def dposer(argsid, fresults):
    from jiwer import wer as jiwer
    with open("data/" + argsid + "/" + argsid + "3.txt", "r", encoding="utf8") as file:
        gt = []
        hp = []
        per_list = []
        id_list = []
        for ligne in file:
            ligne = ligne.split("\t")
            ref = removeEPS(ligne[1])
            hyp = removeEPS(ligne[2])
            gt.append(ref)
            hp.append(hyp)
            per_list.append(jiwer(ref, hyp)*100)
            id_list.append(ligne[0])
    fresults.write("dPOSER: " + str(jiwer(gt, hp)*100) + "\n")
    totxt(per_list, id_list, "per_" + argsid)
    print("POS ER done")

"""---------------universal POS Error Rate---------------"""
def uposer(argsid, fresults, mapper):
    from jiwer import wer as jiwer
    with open("data/" + argsid + "/" + argsid + "3.txt", "r", encoding="utf8") as file:
        gt = []
        hp = []
        per_list = []
        id_list = []
        for ligne in file:
            ligne = ligne.split("\t")
            ref = removeEPS(ligne[1]).split(" ")
            hyp = removeEPS(ligne[2]).split(" ")
            for i in range(len(ref)):
                ref[i] = mapper[ref[i]]
            for i in range(len(hyp)):
                hyp[i] = mapper[hyp[i]]
            ref = " ".join(ref)
            hyp = " ".join(hyp)
            gt.append(ref)
            hp.append(hyp)
            per_list.append(jiwer(ref, hyp)*100)
            id_list.append(ligne[0])
    fresults.write("uPOSER: " + str(jiwer(gt, hp)*100) + "\n")
    totxt(per_list, id_list, "uper_" + argsid)
    print("uPOS ER done")



"""---------------Embedding Error Rate----------------"""
def similarite(syn1, syn2):
    try:
        return 1 - spatial.distance.cosine(syn1, syn2)
    except KeyError:
        return 0

def EmbER(id, threshold, argsid): # called by ember()
    verytemp = 0
    #embeddings:
    namefile = "utils/embeddings/cc.fr.300.vec"
    ember_list = []
    id_list = []
    ref = []
    hyp = []
    refhyp = set()
    # Loading dataset
    with open("data/" + id + "/" + id + "1.txt", "r", encoding="utf8") as file:
        pre_id_list = []
        for ligne in file:
            ligne = ligne.split("\t")
            r = ligne[1].lower()
            h = ligne[2].lower()
            ref.append(r)
            hyp.append(h)
            pre_id_list.append(ligne[0])
            for e in r.split(" "):
                refhyp.add(e)
            for e in h.split(" "):
                refhyp.add(e)
    print("Embeddings loading...")
    tok2emb = {}
    try:
        file = open(namefile, "r", encoding="utf8")
    except FileNotFoundError:
        print("ERROR: embeddings file " + str(namefile) + " is not found. Please download text embeddings from https://fasttext.cc/docs/en/crawl-vectors.html in utils/embeddings. If you already downloaded the file, make sure your filename matches the one in utils/eval.Ember().namefile")
        raise
    next(file)
    for ligne in file:
        ligne = ligne[:-1].split(" ")
        if ligne[0] in refhyp:
            emb = np.array(ligne[1:]).astype(float)
            if emb.shape != (300,):
                print("Erreur à " + ligne[0])
            else:
                tok2emb[ligne[0]] = emb
    print("Embeddings loaded.")
    voc = tok2emb.keys()
    # Embedding Error Rate computation
    print("Embedding Error Rate computation...")
    errors = []
    d = 0
    c = 0
    for i in range(len(ref)):
        """if i %100 == 0:
            print(i)"""
        error = []
        r = ref[i].split(" ")
        h = hyp[i].split(" ")
        if len(r) != len(h): # if ref and hypothesis are different -> error
            d += 1
            continue
        else:
            c += 1
        for j in range(len(r)):
            if r[j] != h[j]:
                if r[j] == "<eps>" or h[j] == "<eps>":
                    error.append(1)
                else:
                    if r[j] in voc and h[j] in voc:
                        sim = similarite(tok2emb[r[j]], tok2emb[h[j]])
                        if sim > threshold: # Threshold
                            print("localsim:", sim)
                            exit(-1)
                            error.append(0.1)
                        else:
                            error.append(1)
                    else:
                        error.append(1)
            else:
                error.append(0)
        errors.append(error)
        ember_list.append(sum(error)/len(error)*100)
        id_list.append(pre_id_list[i])
    totxt(ember_list, id_list, "ember_" + argsid)
    print("EmbER done")

    print("Number of time the ref and hyp had a different length: ", d)
    print("Percentage of incorrect length: ", str((d/c)*100))
    s = 0
    length = 0
    for i in range(len(errors)):
        s += sum(errors[i])
        length += len(errors[i])
    return s/length

def ember(argsid, fresults, threshold):
    fresults.write("EmbER: " + str(EmbER(argsid, threshold, argsid)*100) + "\n")


"""---------------Semantic Distance---------------"""
def semdist(argsid, fresults):
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
    model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
    sim_list = []
    id_list = []
    ind = 0
    with open("data/" + argsid + "/" + argsid + "1.txt", "r", encoding="utf8") as file:
        print("Computing Semdist...")
        for ligne in file:
            if ind%100 == 0:
                print(ind)
            ind += 1
            ligne = ligne.split("\t")
            ligne[1] = removeEPS(ligne[1])
            ligne[2] = removeEPS(ligne[2])
            ligne0 = [ligne[1].lower()]
            ligne1 = [ligne[2].lower()]
            if ligne0 != ligne1:
                ligne0 = model.encode(ligne0)
                ligne1 = model.encode(ligne1)
                sim_list.append(cosine_similarity(ligne0, ligne1)[0][0])
            else: #cosine_similarity(model.encode(["le temps est bon"]), model.encode(["le temps est beau"]))
                sim_list.append(1)
            id_list.append(ligne[0])


    for i in range(len(sim_list)):
        sim_list[i] = (1 - sim_list[i])*100
    totxt(sim_list, id_list, "semdist_" + argsid)
    semdist_score = sum(sim_list)/len(sim_list)
    fresults.write("SemDist: " + str(semdist_score) + "\n")
    print("SemDist done")


"""---------------Lemma Error Rate---------------"""
def ler(argsid, fresults):
    from jiwer import wer as jiwer
    with open("data/" + argsid + "/" + argsid + "4.txt", "r", encoding="utf8") as file:
        gt = []
        hp = []
        ler_list = []
        id_list = []
        for ligne in file:
            ligne = ligne.split("\t")
            ref = ligne[1]
            hyp = ligne[2]
            if len(ref) > 0 and len(hyp) > 0:
                gt.append(ref)
                hp.append(hyp)

                ler_list.append(jiwer(ref, hyp)*100)
                id_list.append(ligne[0])
    fresults.write("LER: " + str(jiwer(gt, hp)*100) + "\n")
    totxt(ler_list, id_list, "ler_" + argsid)
    print("LER done")



"""--------------Character Error Rate---------------------"""
def cer(argsid, fresults):
    from jiwer import cer
    refs = []
    hyps = []
    cer_list = []
    id_list = []
    with open("data/" + argsid + "/" + argsid + "1.txt", "r", encoding="utf8") as file:
        inc = 0
        for ligne in file:
            ligne = ligne.split("\t")
            ref = removeEPS(ligne[1])
            hyp = removeEPS(ligne[2])
            if len(ref) > 0 and len(hyp) > 0:
                refs.append(ref)
                hyps.append(hyp)
                try:
                    temp = cer(ref, hyp)
                    cer_list.append(temp * 100)
                    id_list.append(ligne[0])
                except ValueError:
                    inc += 1
    error = cer(refs, hyps)*100
    fresults.write("CER: " + str(error) + "\n")
    totxt(cer_list, id_list, "cer_" + argsid)
    print("CER done")


"""--------------BERTScore----------------"""
def bertscore(argsid, fresults):
    from bert_score import score
    
    refs = []
    hyps = []
    ids = []
    with open("data/" + argsid + "/" + argsid + "1.txt", "r", encoding="utf8") as file:
        for ligne in file:
            line = ligne.split("\t")
            ids.append(line[0])
            refs.append(removeEPS(line[1]))
            hyps.append(removeEPS(line[2]))

    P, R, F1 = score(hyps, refs, lang="fr", verbose=True)
        
    fresults.write("BERTScore: " + str(100 - F1.mean().item()*100) + "\n")
    totxt(F1, ids, "bertscore_" + argsid)
    print("BERTScore done")