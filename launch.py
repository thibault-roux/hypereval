
import argparse
import utils.make_datasets as mk
import utils.eval as eval


if __name__ == '__main__':
    # This code generated the necessary datasets to compute the evaluation metrics

    parser = argparse.ArgumentParser(description="Evaluation of a system using references and hypothesis produced.")
    parser.add_argument("namef", type=str, help="Path to a test file output")
    parser.add_argument("-w", "--wer", help="Word Error Rate", action="store_true")
    parser.add_argument("-c", "--cer", help="Character Error Rate", action="store_true")
    parser.add_argument("-l", "--ler", help="Lemma Character Error Rate", action="store_true")
    parser.add_argument("-d", "--dposer", help="Detailed Part-Of-Speech Error Rate", action="store_true")
    parser.add_argument("-u", "--uposer", help="Universal Part-Of-Speech Error Rate", action="store_true")
    parser.add_argument("-e", "--ember", help="Embedding Error Rate", action="store_true")
    parser.add_argument("-s", "--semdist", help="SemDist", action="store_true")
    # parser.add_argument("-b", "--bertscore", help="BERTScore", action="store_true")
    # parser.add_argument("-l", "--lcer", help="Lemma Character Error Rate", action="store_true") # As it is proven that this metric is useless, we could delete it
    args = parser.parse_args()

    print("Starting datasets' generation...")
    if args.cer or args.ember or args.semdist:
        mk.dataset1(args.namef) # useful for CER, EmbER and SemDist
    if args.wer:
        mk.dataset2(args.namef) # useful for WER
    if args.uposer or args.dposer:
        mk.dataset3(args.namef) # useful for uPOSER and dPOSER
    if args.ler: # or args.lcer:
        mk.dataset4(args.namef) # useful for LER and LCER
    print("Datasets' generation done.")


    print("Starting evaluation...")
    argsid = args.namef.split("/")[1]
    fresults = open("results/"+argsid+".txt","w", encoding="utf8") # File containing the results.
    if args.cer:
        eval.cer(argsid, fresults)
    if args.ember:
        import numpy as np
        from scipy import spatial
        #eval.ember(argsid, fresults, threshold=0.4)
        eval.ember(argsid, fresults, threshold=1)
    if args.semdist:
        eval.semdist(argsid, fresults)
    if args.wer:
        eval.wer(argsid, fresults)
    if args.uposer or args.dposer:
        mapper = eval.prepare_POS(argsid) # Checking POS and loading of mapping 
        if args.uposer:
            eval.uposer(argsid, fresults, mapper)
        if args.dposer:
            eval.dposer(argsid, fresults)
    if args.ler: # or args.lcer:
        eval.ler(argsid, fresults)
    fresults.close()
    print("Evaluation completed!")