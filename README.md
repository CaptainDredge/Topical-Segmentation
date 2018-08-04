# Topical Segmentation

word2vec:
>  https://drive.google.com/a/audioburst.com/uc?export=download&confirm=zrin&id=0B7XkCwpI5KDYNlNUTTlSS21pQmM



Fill relevant paths in configgenerator.py, and execute the script (git repository includes Choi dataset)

## Creating an environment:

    conda create -n textseg python=2.7 numpy scipy gensim ipython 
    source activate textseg
    pip install http://download.pytorch.org/whl/cu80/torch-0.3.0-cp27-cp27mu-linux_x86_64.whl 
    pip install tqdm pathlib2 segeval tensorboard_logger flask flask_wtf nltk
    pip install pandas xlrd xlsxwriter termcolor

## How to run training process?

    python run.py --help

Example:

    python run.py --cuda --model max_sentence_embedding
