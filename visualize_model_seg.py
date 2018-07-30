import wiki_loader
import gensim
import evaluate
import utils
from pathlib2 import Path
from argparse import ArgumentParser
import torch
import choiloader
import numpy as np
import glob
from choiloader import clean_paragraph

section_delimiter = "-----"

def segment(path, model, word2vec, output_folder, wiki = False):
    
    for filename in glob.glob(path+ '*.txt'):
        with open(files,  "r+") as f:
            paragraph = f.read()
            sentences = [clean_paragraph(paragraph)]

            cutoffs = evaluate.predict_cutoffs(sentences, model, word2vec)
            total = []
            segment = []
            for i, (sentence, cutoff) in enumerate(zip(sentences, cutoffs)):
                segment.append(sentence)
                if cutoff:
                    full_segment ='.'.join(segment) + '.'
                    full_segment = full_segment + '\n' + section_delimiter + '\n'
                    total.append(full_segment)
                    segment = []

        file_id = str(filename).split('/')[-1:][0]

        # Model does not return prediction for last sentence
        segment.append(sentences[-1:][0])
        total.append('.'.join(segment))

        output_file_content = "".join(total)
        output_file_full_path = Path(output_folder).joinpath(Path(file_id))
        with output_file_full_path.open('w') as f:
            f.write(output_file_content)

def main(args):
    utils.read_config_file(args.config)
    utils.config.update(args.__dict__)


    if not args.test:
        word2vec = gensim.models.KeyedVectors.load_word2vec_format(utils.config['word2vecfile'], binary=True)
    else:
        word2vec = None

    with open(args.model, 'rb') as f:
        model = torch.load(f)
        model.eval()

    segment(args.path, model, word2vec, args.output, wiki=args.wiki)



if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--test', help='Test mode? (e.g fake word2vec)', action='store_true')
    parser.add_argument('--model', help='Model to run - will import and run', required=True)
    parser.add_argument('--config', help='Path to config.json', default='./config.json')
    parser.add_argument('--path', help='Path to files to segment by model', default='./data/Dataset/test-data/')
    parser.add_argument('--output', help='output folder', required=True)
    parser.add_argument('--wiki', help='use wikipedia files', action='store_true')


    main(parser.parse_args())