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
    for line in file:
        line = line.split("\t")
        r = removeEmpty(line[1].split(" "))
        if len(r) <= 0:
            print("Empty reference, skipped.")
            continue
        id = line[0]
        ref[id] = r
        hyp[id] = removeEmpty(line[2].split(" "))

d = wer_details(ref, hyp, compute_alignments=True)
print_alignments(d, open(args.namef + "/wer_test.txt", "w", encoding="utf8"))
