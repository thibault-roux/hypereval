

# create refhyp file by cleaning the reference and hypothesis from encoding bugs

# remove token <eps> from the sentence string without useless spaces
def remove_eps(sentence):
    sentence = sentence.replace(" <eps> ", " ")
    sentence = sentence.replace(" <eps>", "")
    sentence = sentence.replace("<eps> ", "")
    sentence = sentence.replace("<eps>", "")
    return sentence

def clean_string(string):
    string = string.lower()
    string = string.replace("’", "'")
    string = string.replace("œ", "oe")
    string = string.replace("æ", "ae")
    string = string.replace("«", "")
    string = string.replace("»", "")
    string = string.replace("(", "")
    string = string.replace(")", "")
    string = string.replace("-", " ")
    for c in set(string):
        if c not in " éèêçâàîïôùûabcdefghijklmnopqrstuvwxyz0123456789'":
            string = string.replace(c, "")
    return string


if __name__ == "__main__":
    systems = ["KD_woR", "KD_wR", "SB_bpe1000", "SB_bpe750", "SB_s2s", "SB_w2v", "SB_w2v_1k", "SB_w2v_3k", "SB_w2v_7k", "SB_xlsr", "SB_xlsr_fr"]

    for system in systems:
        ids = []
        refs = []
        hyps = []
        with open("old/" + system + "/" + system + "1.txt", "r", encoding="utf8") as f:
            for line in file:
                line = line.split("\t")
                ids.append(line[0])
                refs.append(remove_eps(line[1]))
                hyps.append(remove_eps(line[2]))
                