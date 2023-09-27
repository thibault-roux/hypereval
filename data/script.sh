

# changer la liste
# changer le nom du dossier source de la copie

# list in bash

# liste from 1 to 49
liste=$(seq 1 49)
for i in $liste
do
    mkdir SB_7k_epoch_${i}
    cp /users/troux/these/expe/end-to-end/Mickael/results_lia_asr/wav2vec2_ctc_fr_7k_50epochs/1234/wer_test_${i}.txt SB_7k_epoch_${i}/wer_test.txt
done
