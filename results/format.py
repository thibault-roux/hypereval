


with open("systems.txt", "r", encoding="utf8") as file:
    systems = []
    for ligne in file:
        systems.append(ligne.split(".txt")[0])

metrics = ['WER', 'CER', 'uPOSER', 'dPOSER', 'LER', 'EmbER', 'SemDist', 'BERTScore']

scores = dict()
for system in systems:
    scores[system] = dict()
    with open("subset_" + system + ".txt", "r", encoding="utf8") as file:
        for ligne in file:
            line = ligne[:-1].split(": ")
            metric = line[0]
            score = int(1000*float(line[1]))/1000
            scores[system][metric] = score


txt = ","
for metric in metrics:
    txt += metric + ","
txt = txt[:-1] + "\n"
for system, scores_sys in scores.items():
    txt += system + ","
    for metric in metrics:
        txt += str(scores_sys[metric]) + ","
    txt = txt[:-1] + "\n"

with open("results_subset.txt", "w", encoding="utf8") as file:
    file.write(txt)
