#coding:utf-8
import argparse
from collections import OrderedDict
import numpy as np
def cosine_similarity(v1, v2):
  '''
   v1, v2: a vector.
  '''
  return np.dot(v1, v2) / np.linalg.norm(v1) / np.linalg.norm(v2)

def read(file_path, max_rows):
  emb_dict = OrderedDict()
  embedding_size = None
  for i, l in enumerate(open(file_path)):
    if max_rows and i+1 >=max_rows:
      break
    if i == 0:
      embedding_size = int(l.split()[1])
    line = l.split()
    if len(line) != embedding_size +1:
      continue
    word = line[0]
    embedding = np.array([float(x) for x in line[1:]])
    emb_dict[word] = embedding
  return emb_dict

def main(args):
  ja_emb_name = args.ja_emb
  en_emb_name = args.en_emb
  ja_emb = read(ja_emb_name, args.max_rows)
  en_emb = read(en_emb_name, args.max_rows)
  #print (len(ja_emb), len(en_emb))
  #exit(1)
  while True:
    word = input('Input word: ')
    lang = input('Input language (jpn or eng): ')
    
    if lang == 'jpn':
      lang1 = ja_emb
      lang2 = en_emb
    elif lang == 'eng':
      lang1 = en_emb
      lang2 = ja_emb
    else: 
      print ("Input jpn or eng as language.")
      continue

    if word in lang1:
      # 1. 
      N = 10
      similarities = [(k, cosine_similarity(lang1[word], lang1[k])) for k in lang1 if k != word]
      similarities = sorted(similarities, key=lambda x:-x[1])
      print ('top-%d similar words in source language' % N)
      for x in similarities[:N]:
        print (x)

      # 2.
      N = 10
      similarities = [(k, cosine_similarity(lang1[word], lang2[k])) for k in lang2 if k != word]
      similarities = sorted(similarities, key=lambda x:-x[1])
      print ('top-%d similar words in target language' % N)
      for x in similarities[:N]:
        print (x)

      # 3. 
      N = 20
      similarities = [('l1_' + k , cosine_similarity(lang1[word], lang1[k])) for k in lang1 if k != word] + [('l2_' + k, cosine_similarity(lang1[word], lang2[k])) for k in lang2 if k != word]
      similarities = sorted(similarities, key=lambda x:-x[1])
      print ('top-%d similar words in multilingual' % N)
      for x in similarities[:N]:
        print (x)
    else:
      print ('%s is not found in vocabulary.' % word)
if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--ja_emb', default='fasttext/wiki.ja.vec.mapped', 
                      type=str, help ='')
  parser.add_argument('--en_emb', default='fasttext/wiki.en.vec.mapped',
                      type=str, help ='')
  parser.add_argument('-mr', '--max_rows', default=100000,
                      type=int, help ='')
  args  = parser.parse_args()
  main(args)


