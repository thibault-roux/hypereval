
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


with open(args.namef + "/repere_3g.9.ci.pra", "r", encoding="utf8") as file:
#with open(args.namef + "/repere_rnnlm.9.ci.pra", "r", encoding="utf8") as file:
    next(file)
    next(file)
    next(file)
    txt = ""
    for ligne in file:
        if ligne[:6] == "REF:  ":
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
            txt += ref + "\t" + hyp + "\t_\n"
    txt += ref + "\t" + hyp + "\n" #"\t_\n"

with open(args.namef + "/refhyp.txt", "w", encoding="utf8") as file:
    file.write(txt)
