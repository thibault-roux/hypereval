from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay


def pos_matrix(system, ignore_correct=False, ignore_pos=[]):

    # mapper
    with open("utils/mapping.txt", "r", encoding="utf8") as file:
        mapper = dict()
        for ligne in file:
            line = ligne[:-1].split("\t")
            mapper[line[0]] = line[1]
        mapper["<eps>"] = "<eps>"
        
        all_labels = ['ADJ', 'ADV', 'AUX', 'NUM', 'CCONJ', 'SCONJ', 'DET', 'NOUN', 'PRON', 'ADP', 'PROPN', 'VERB', 'INTJ', 'PUNCT', 'SYM', 'X', 'PART', '<eps>']
        labels = []
        for label in all_labels:
            if label not in ignore_pos: # ignore label
                labels.append(label)

    with open("data/" + system + "/" + system + "3.txt", "r", encoding="utf8") as file:
        # With sklearn, we can do things easily
        # >>> y_true = ["cat", "ant", "cat", "cat", "ant", "bird"]
        # >>> y_pred = ["ant", "ant", "cat", "cat", "ant", "cat"]
        # >>> confusion_matrix(y_true, y_pred, labels=["ant", "bird", "cat"])
        # array([[2, 0, 0],
        #     [0, 0, 1],
        #     [1, 0, 2]])

        references_global = []
        hypothesis_global = []
        correct = 0
        problem = 0
        for ligne in file:
            line = ligne.split("\t")
            ref = line[1].split(" ")
            hyp = line[2].split(" ")
            if len(ref) != len(hyp):
                problem += 1
            else:
                correct += 1
                for i in range(len(ref)):
                    flag = True
                    if ignore_correct and ref[i] == hyp[i]: # ignore correct transcriptions
                            flag = False
                    if ref[i] in ignore_pos or hyp[i] in ignore_pos:
                        flag = False
                    if flag:
                        references_global.append(mapper[ref[i]])
                        hypothesis_global.append(mapper[hyp[i]])
        print("correct: ", correct)
        print("problem: ", problem)
        print(labels)
        # print(confusion_matrix(references_global, hypothesis_global, labels=labels))
        ConfusionMatrixDisplay.from_predictions(references_global, hypothesis_global, labels=labels, normalize="true", include_values=False, xticks_rotation='vertical')
        plt.show()
        plt.savefig("results/matrix/pos/" + system + ".png")