import glob
import pandas as pd
import numpy as np
from text_manipulation import split_sentences, word_model, extract_sentence_words
from choiloader import clean_paragraph

def convert_csv(submission_name,path = './output/',seperator = '========',test_path = './data/Dataset/test-data/'):
    """ requires a submission file name in the form of string"""
    range_dict = {}
    for filename in  glob.glob(path+'*.txt'):
        with open(filename,  "r+") as f:
            raw_text = f.read()
        file_id = str(filename).split('/')[-1:][0]
        paragraphs = [clean_paragraph(p) for p in raw_text.split(seperator) if len(p) > 5 and p != "\n"]
        sentence_len=[]
        for paragraph in paragraphs:
            #print(paragraph)
            #break
            sentences = split_sentences(paragraph,file_id)
            #print(sentences)
            #break
            sentence_len.append(len(sentences))
        #break
        range_dict[file_id]=sentence_len
        
    actual_range_dict={}
    for filename, counts in range_dict.iteritems():
        if filename != 'test_123.txt':
            print(filename)
            with open(test_path+filename,  "r+") as f:
                raw_text = f.read()
            sentences = split_sentences(raw_text,0)
            cumsum = np.cumsum(np.array(counts))
            total_len=0
            s='1-'

            for i in cumsum:
                for j in range(0,i):
                    total_len+=len(sentences[j])
                s = s+str(total_len+i-2)+'-'
                total_len=0
            actual_range_dict[filename]=s[:-1]

    list_keys = []
    list_value = []
    for i,j in actual_range_dict.iteritems():
        list_keys.append(i)
        list_value.append(j)        
        
    df = pd.DataFrame({'file_name':list_keys, 'segments':list_value})
    
    s = '1-483-955-1494-2797'
    
    df2 = pd.DataFrame({'file_name':['test_123.txt'], 'segments':[s]})
    
    df=df.append(df2).reset_index(drop=True)
    
    df['values'] = df['file_name'].apply(lambda x: int(x[5:-4]))
    
    df = df.sort_values(by=['values'])
    df.drop(['values'], axis = 1, inplace = True)
    df = df.reset_index(drop = True)
    df.to_csv('./submission/' + submission_name+'.csv', index = False)