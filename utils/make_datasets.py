import os.path

def clean(line):
    line = line.split(";")
    line = " ".join(line)
    """line = line.split("<eps>")
    line = " ".join(line)"""
    line = line.split()
    line = " ".join(line)
    return line


def retirerEPS(ligne): #utile pour le dataset 4
    retour = ""
    ligne = ligne.split(" ")
    for i in range(len(ligne)):
        if ligne[i] != "<eps>":
            retour += ligne[i] + " "
    return retour[:-1]




"""---------------Dataset-1---------------"""
def dataset1(namef): # useful for CER, EmbER and SemDist
    argsid = namef.split("/")[1]
    if os.path.isfile("data/" + argsid + "/" + argsid + "1.txt") != True:
        with open(namef, "r", encoding="utf8") as basefile:
            lines = basefile.readlines()
            i = 0
            splitted = lines[i].split(" ")
            condition = True
            if len(splitted) > 4:
                if splitted[1] == "%WER":
                    idfile = splitted[0].split(",")[0]
                    condition = False
            while condition:
                i += 1
                splitted = lines[i].split(" ")
                condition = True
                if len(splitted) > 4:
                    if splitted[1] == "%WER":
                        idfile = splitted[0].split(",")[0]
                        condition = False
            X = ""
            j = 0
            while True:
                j += 1
                i += 1
                line = clean(lines[i])
                X += idfile + "\t" + line + "\t"
                i += 2
                line = clean(lines[i])
                X += line + "\t_\n"
                i += 2
                if i >= len(lines):
                    break
                idfile = lines[i].split(",")[0]
        with open("data/" + argsid + "/" + argsid + "1.txt", "w", encoding="utf8") as file:
            file.write(X)
        print("Dataset 1 created")
    else:
        print("Dataset 1 already exists")



"""---------------Dataset-2---------------"""
def dataset2(namef): # useful for WER
    argsid = namef.split("/")[1]
    if os.path.isfile("data/" + argsid + "/" + argsid + "2.txt") != True:
        with open(namef, "r", encoding="utf8") as basefile:
            lines = basefile.readlines()
            i = 0
            splitted = lines[i].split(" ")
            condition = True
            if len(splitted) > 4:
                if splitted[1] == "%WER":
                    idfile = splitted[0].split(",")[0]
                    condition = False
            while condition:
                i += 1
                splitted = lines[i].split(" ")
                condition = True
                if len(splitted) > 4:
                    if splitted[1] == "%WER":
                        idfile = splitted[0].split(",")[0]
                        condition = False
            X = ""
            j = 0
            while i < len(lines):
                j += 1
                i += 1
                line = idfile + "\t" + clean(lines[i])
                X += line + "\t"
                i += 1
                line = clean(lines[i])
                X += line + "\t_\n"
                i += 3
                if i >= len(lines):
                    break
                idfile = lines[i].split(",")[0]
        with open("data/" + argsid + "/" + argsid + "2.txt", "w", encoding="utf8") as file:
            file.write(X)
        print("Dataset 2 created")
    else:
        print("Dataset 2 already exists")


"""---------------Dataset-3---------------"""
def dataset3(namef): # useful for uPOSER and dPOSER
    argsid = namef.split("/")[1]
    if os.path.isfile("data/" + argsid + "/" + argsid + "3.txt") != True:
        from utils.POS_tag import tag
        tag(argsid)
        print("Dataset 3 created")
    else:
        print("Dataset 3 already exists")



"""---------------Dataset-4---------------"""
def dataset4(namef): # useful for LER and LCER
    argsid = namef.split("/")[1]
    if os.path.isfile("data/" + argsid + "/" + argsid + "4.txt") != True:
        try:
            import spacy
            nlp = spacy.load('fr_core_news_md')
        except:
            print("An error was detected during dataset 4 production (Lemmatization)")
            print("To avoid the problem :")
            print("pip install spacy")
            print("python -m spacy download fr_core_news_md")

        def getLemme(s):
            doc = nlp(s)
            r = ""
            for token in doc:
                r += token.lemma_ + " "
            return r[:-1]


        txt = ""
        with open("data/" + argsid + "/" + argsid + "1.txt", "r", encoding="utf8") as file:
            for ligne in file:
                ligne = ligne.split("\t")
                i = ligne[0]
                ref = retirerEPS(ligne[1].lower())
                hyp = retirerEPS(ligne[2].lower())
                newref = getLemme(ref)
                newhyp = getLemme(hyp)
                txt += i + "\t" + newref.upper() + "\t" + newhyp.upper() + "\t_\n"

        with open("data/" + argsid + "/" + argsid + "4.txt", "w", encoding="utf8") as file:
            file.write(txt)
        print("Dataset 4 created")
    else:
        print("Dataset 4 already exists")



"""---------------Dataset-5---------------"""
def dataset5(namef): # useful for BERTScore
    argsid = namef.split("/")[1]
    if os.path.isfile("data/" + argsid + "/" + argsid + "5.txt") != True:
        with open("data/" + argsid + "/" + argsid + "1.txt", "r", encoding="utf8") as file:
            newref = ""
            newhyp = ""
            for ligne in file:
                ligne = ligne.split("\t") # id are ignored
                ref = retirerEPS(ligne[1].lower())
                hyp = retirerEPS(ligne[2].lower())
                newref += ref + "\n"
                newhyp += hyp + "\n"
        with open("data/" + argsid + "/" + argsid + "5.txt", "w", encoding="utf8") as file:
            file.write(newref)
            print("Dataset 5 created")
        with open("data/" + argsid + "/" + argsid + "6.txt", "w", encoding="utf8") as file:
            file.write(newhyp)
            print("Dataset 6 created")
    else:
        print("Dataset 5 already exists")
