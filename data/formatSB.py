from speechbrain.utils.edit_distance import wer_details_by_utterance as wer_details
from speechbrain.dataio.wer import print_alignments

import argparse
parser = argparse.ArgumentParser(description="Transform ref-hyp to Speechbrain output")
parser.add_argument("namef", type=str, help="Path to a refhyp file")
args = parser.parse_args()

def removeEmpty(sentence):
    corrected = []
    for j in range(len(sentence)):
        if sentence[j] != "":
            corrected.append(sentence[j])
    return corrected


ref = dict()
hyp = dict()
with open(args.namef + "/refhyp.txt", "r", encoding="utf8") as file:
    i = 0
    for line in file:
        line = line.split("\t")
        r = removeEmpty(line[0].split(" "))
        if len(r) <= 0:
            print("Empty reference, skipped.")
            continue
        ref[i] = r
        hyp[i] = removeEmpty(line[1].split(" "))
        i += 1

d = wer_details(ref, hyp, compute_alignments=True)
print_alignments(d, open(args.namef + "/wer_file.txt", "w", encoding="utf8"))
