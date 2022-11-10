# Hypereval

## Context
Framework to automatically evaluate transcriptions from an Automatic Speech Recognition system with different metrics.

This code allows to evaluate Automatic Speech Recognition Systems with different metrics:
- Word Error Rate (WER)
- Character Error Rate (CER)
- Universal Part-of-Speech Error Rate (uPOSER) & Detailed Part-of-Speech Error Rate (dPOSER)
- Lemme Error Rate (LER)
- Embedding Error Rate (EmbER)
- Semantic Distance variant (SemDist)
- ~~BERTScore (BERTScore)~~ (soon to be released)
- *Feel free to add any news metrics*
    
For more informations on metrics, read the papers:
 - Qualitative Evaluation of Language Model Rescoring in Automatic Speech Recognition

In order to evaluate the system, it is needed to have the references and associated hypothesis.

## QuickStart

### Installation
```
pip install numpy
pip install matplotlib
pip install jiwer
pip install spacy
pip install sklearn
pip install speechbrain
pip install sentence-transformers
git clone https://github.com/thibault-roux/hypereval.git
```

### Run an evaluation

Steps:
* [IF YOU DO NOT USE SPEECHBRAIN] Adapt results to a Speechbrain format.
* Produce data related to the reference and hypothesis for each metric (part-of-speech tagging, lemmas tagging, WER alignment).
* Evaluate with metrics.

#### If your system was trained with Speechbrain
```
> mkdir data/{folder} # to store data related to metrics
> mv {wer_file} data/{folder}/{wer_file}
> python launch.py data/{folder}/{wer_file} [-w --wer] [-c --cer] [-l --ler] [-d --dposer] [-u --uposer] [-e --ember] [-s --semdist]
```

#### If your system was not trained with Speechbrain
```
> mkdir data/{folder} # to store data related to metrics
> # produce refhyp.txt with a easy to process format (cf FORMAT) and put it in data/{folder}
> cd data
> python formatSB.py {folder} # Speechbrain format
> cd ..
> python launch.py data/{folder}/wer_test.txt [-w --wer] [-c --cer] [-l --ler] [-d --dposer] [-u --uposer] [-e --ember] [-s --semdist]
```

## Format

This code need to transform your reference and hypothesis in a Speechbrain format.
To do this, a code was developped to produce a Speechbrain format given an easy to produce format called refhyp.

The refhyp format is a table of two columns separated by a tabulation.
For example:
```
I DO NOT KNOW I NOT NOW HIM
HELLO WORLD  HELLO WORD
MY FRIEND IS GREAT  MY BRAND IS GREAT
I CAN'T BELIEVE THAT    I CANNOT BELIEVE THAT
...
```

The Speechbrain format produced is like following:
```
================================================================================
my_dataset_179624, %WER 60.00 [ 3 / 5, 1 ins, 1 del, 1 sub ]
I  ;   DO  ; NOT ; KNOW ; <eps>
=  ;   D   ;  =  ;  S   ;   I
I  ; <eps> ; NOT ; NOW  ;  HIM
================================================================================
my_dataset_179625, %WER 50.00 [ 1 / 2, 0 ins, 0 del, 1 sub ]
HELLO  ;  WORLD
  =    ;   S
HELLO  ;  WORD
...
```

## Language-dependend metrics

Some of these metrics such as Part-of-Speech Error Rate (POSER), Lemma Error Rate (LER) and embedding-based metrics (EmbER, SemDist, BERTScore), need linguistics information provided by diverses tools. **If you do not plan to use these metrics on French**, feel free to modify source code to adapt your evaluation to your problem.

### Part-of-Speech Error Rate (dPOSER & uPOSER)
As these metrics use part-of-speech specifically designed for French, this metric is not expected to work on any other languages. If you would like to use this metric, you have to:
- generate the POS tagged dataset (like dataset3.txt) with a new function in utils/make_dataset.py (called in launch.py) using your part-of-speech tagger.
- Adapt the dposer() function in eval.py by linking it to your new dataset name.

### Lemma Error Rate
For this metric to work in your language, you just need to modify the lemmatizer (dataset4() in utils/make_dataset.py).

### Embedding Error Rate
For this metric to work in your language, you have to download text embeddings from https://fasttext.cc/docs/en/crawl-vectors.html and put them in utils/embeddings/. Do not forget to rename the namefile in utils/eval.EmbER().

### SemDist
This metric is expected to be multilingual as it use a Sentence Transformer. Feel free to change the transformer in eval.py.semdist().
```
model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
```

## Cite

Please, cite the related paper if you use this framework.

```
@inproceedings{roux2022qualitative,
  title={Qualitative Evaluation of Language Model Rescoring in Automatic Speech Recognition},
  author={Ba{\~n}eras-Roux, Thibault and Rouvier, Mickael and Wottawa, Jane and Dufour, Richard},
  booktitle={Interspeech},
  year={2022}
}
```
