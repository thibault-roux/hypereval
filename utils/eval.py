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
    with open("data/" + argsid + "/" + argsid + "3.txt", "r", encoding="utf8") as file:
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
    F1_number = []
    for f1 in F1:
        F1_number.append(100 - f1.item()*100)
    totxt(F1_number, ids, "bertscore_" + argsid)
    print("BERTScore done")





"""--------------MinWER-----------------"""
def get_next_level(prev_level):
    level = set()
    for errors in prev_level:
        errors = list(errors) # string to list for item assigment
        for i in range(len(errors)):
            error = errors[i]
            if error == '0':
                new_errors = errors.copy()
                new_errors[i] = 1
                level.add(''.join(str(x) for x in new_errors)) # add list (converted to string)
    return level

def correcter(ref, hyp, corrected, errors):
    ref = ref.split(" ")
    hyp = hyp.split(" ")
    INDEX = 0
    new_hyp = ""
    ir = 0
    ih = 0
    for i in range(len(errors)):
        if errors[i] == "e": # already
            new_hyp += ref[ir] + " "
            ih += 1
            ir += 1
        elif errors[i] == "i": # insertion corrected
            if corrected[INDEX] == '0': # if we do not correct the error
                new_hyp += hyp[ih] + " " # the extra word is not deleted
            ih += 1
            INDEX += 1
        elif errors[i] == "d": # deletion
            if corrected[INDEX] == '1': # if we do correct the error
                new_hyp += ref[ir] + " " # we add the missing word
            ir += 1
            INDEX += 1
        elif errors[i] == "s": # substitution
            if corrected[INDEX] == '1':
                new_hyp += ref[ir] + " "
            else:
                new_hyp += hyp[ih] + " " # we do not correct the substitution 
            ih += 1
            ir += 1
            INDEX += 1
        else: 
            print("Error: the newhyp inputs 'errors' and 'new_errors' are expected to be string of e,s,i,d. Received", errors[i])
            exit(-1)
        i += 1
    return new_hyp[:-1]
   
def MinWER(ref, hyp, metric, threshold, save, memory):
    __MAX__ = 10 # maximum distance to avoid too high computational cost
    errors, distance = awer.wer(ref.split(" "), hyp.split(" "))
    base_errors = ''.join(errors)
    level = {''.join(str(x) for x in [0]*distance)}
    if distance <= __MAX__: # to limit the size of graph
        minwer = 0
        while minwer < distance:
            for node in level:
                corrected_hyp = correcter(ref, hyp, node, base_errors)
                try:
                    score = save[ref][corrected_hyp]
                except KeyError:
                    score = metric(ref, corrected_hyp, memory)
                    if ref not in save:
                        save[ref] = dict()
                    save[ref][corrected_hyp] = score
                if score < threshold: # lower-is-better
                    return minwer
            level = get_next_level(level)
            minwer += 1
        return distance
    else:
        return distance

def semdist_minwer(ref, hyp, memory):
    model = memory
    ref_projection = model.encode(ref).reshape(1, -1)
    hyp_projection = model.encode(hyp).reshape(1, -1)
    score = cosine_similarity(ref_projection, hyp_projection)[0][0]
    return (1-score) # lower is better

def minwer(argsid, fresults):
    import pickle

    # recover scores save
    try:
        with open("../interpretable/pickle/SD_sent_camemlarge.pickle", "rb") as handle:
            save = pickle.load(handle)
    except FileNotFoundError:
        save = dict()
    
    refs = []
    hyps = []
    ids = []
    with open("data/" + argsid + "/" + argsid + "1.txt", "r", encoding="utf8") as file:
        for ligne in file:
            line = ligne.split("\t")
            ids.append(line[0])
            refs.append(removeEPS(line[1]))
            hyps.append(removeEPS(line[2]))

    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
    model = SentenceTransformer('dangvantuan/sentence-camembert-large')
    memory = model
    metric = semdist_minwer
    
    scores = []
    number_of_words_in_ref = 0
    for i in range(len(ids)):
        ref = refs[i]
        hyp = hyps[i]
        score = MinWER(ref, hyp, metric, 0.024, save, memory)
        scores.append(score)
        number_of_words_in_ref += len(ref.split(" "))

    # storing scores save
    with open("../interpretable/pickle/SD_sent_camemlarge.pickle", "wb") as handle:
        pickle.dump(save, handle, protocol=pickle.HIGHEST_PROTOCOL)

    score_Minwer = sum(scores)/number_of_words_in_ref*100
    fresults.write("MinWER SemDist CamemBERT-large: " + str(score_Minwer) + "\n")

    converted = []
    for s in scores:
        converted.append(s*100)
    totxt(converted, ids, "minwer_SD_sent_camemlarge" + argsid)
    print("MinWER done")






"""--------------MinCER-----------------"""

def correcter_mincer(ref, hyp, corrected, errors):
    # ref, hyp, corrected (100), errors (deesei)

    # ref = ref.split(" ")
    # hyp = hyp.split(" ")
    INDEX = 0

    new_hyp = ""
    ir = 0
    ih = 0
    for i in range(len(errors)):
        if errors[i] == "e": # already
            new_hyp += ref[ir]
            ih += 1
            ir += 1
            # print("e\t", new_hyp)
        elif errors[i] == "i": # insertion corrected
            if corrected[INDEX] == '0': # if we do not correct the error
                new_hyp += hyp[ih] # the extra word is not deleted
            ih += 1
            INDEX += 1
            # print("i\t", new_hyp)
        elif errors[i] == "d": # deletion
            if corrected[INDEX] == '1': # if we do correct the error
                new_hyp += ref[ir] # we add the missing word
            # else  # we do not restaure the missing word
            ir += 1
            INDEX += 1
            # print("d\t", new_hyp)
        elif errors[i] == "s": # substitution
            if corrected[INDEX] == '1':
                new_hyp += ref[ir]
            else:
                new_hyp += hyp[ih] # we do not correct the substitution 
            ih += 1
            ir += 1
            INDEX += 1
            # print("s\t", new_hyp)
        else: 
            print("Error: the newhyp inputs 'errors' and 'new_errors' are expected to be string of e,s,i,d. Received", errors[i])
            exit(-1)
        i += 1
    return new_hyp

def MinCER(ref, hyp, metric, threshold, save, memory):
    __MAX__ = 15 # maximum distance to avoid too high computational cost
    errors, distance = awer.wer(ref, hyp)
    base_errors = ''.join(errors)
    level = {''.join(str(x) for x in [0]*distance)}
    # base_errors = ['esieed']
    # distance = 3
    # level = {000}
    if distance <= __MAX__: # to limit the size of graph
        mincer = 0
        while mincer < distance:
            for node in level:
                corrected_hyp = correcter_mincer(ref, hyp, node, base_errors)
                # optimization to avoid recomputation
                try:
                    score = save[ref][corrected_hyp]
                except KeyError:
                    score = metric(ref, corrected_hyp, memory)
                    if ref not in save:
                        save[ref] = dict()
                    save[ref][corrected_hyp] = score
                if score < threshold: # lower-is-better
                    return mincer
            level = get_next_level(level)
            mincer += 1
        return distance
    else:
        return distance



def mincer(argsid, fresults):
    import pickle

    # recover scores save
    try:
        with open("../interpretable/pickle/SD_sent_camemlarge.pickle", "rb") as handle:
            save = pickle.load(handle)
    except FileNotFoundError:
        save = dict()
    
    refs = []
    hyps = []
    ids = []
    with open("data/" + argsid + "/" + argsid + "1.txt", "r", encoding="utf8") as file:
        for ligne in file:
            line = ligne.split("\t")
            ids.append(line[0])
            refs.append(removeEPS(line[1]))
            hyps.append(removeEPS(line[2]))

    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
    model = SentenceTransformer('dangvantuan/sentence-camembert-large')
    memory = model
    metric = semdist_minwer # use the same function for minwer and for mincer
    
    scores = []
    number_of_words_in_ref = 0
    for i in range(len(ids)):
        ref = refs[i]
        hyp = hyps[i]
        score = MinCER(ref, hyp, metric, 0.0095, save, memory)
        scores.append(score)
        number_of_words_in_ref += len(ref.split(" "))

    # storing scores save
    with open("../interpretable/pickle/SD_sent_camemlarge.pickle", "wb") as handle:
        pickle.dump(save, handle, protocol=pickle.HIGHEST_PROTOCOL)

    score_Mincer = sum(scores)/number_of_words_in_ref*100
    fresults.write("MinCER SemDist CamemBERT-large: " + str(score_Mincer) + "\n")

    converted = []
    for s in scores:
        converted.append(s*100)
    totxt(converted, ids, "mincer_SD_sent_camemlarge" + argsid)
    print("MinCER done")







"""---------------Semantic Distance---------------"""
def sentcamemlarge(argsid, fresults):
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer('dangvantuan/sentence-camembert-large')
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
    fresults.write("SemDist camemlarge: " + str(semdist_score) + "\n")
    print("SemDist done")
