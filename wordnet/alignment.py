# coding:utf-8
import re, argparse, collections, random
random.seed(0)

def read(file_path):
  res = {}
  cnt = collections.defaultdict(int)
  for i, l in enumerate(open(file_path)):
    if i == 0:
      continue
    cnt[len(l.split('\t'))] += 1
    if len(l.split('\t')) != 3:
      continue
    _id, _type, word = l.split('\t')
    if len(word.split()) == 1 and not re.search('\+', word): 
      word = word.replace('\n', '').lower()
      res[_id] = word
  return res

def main(args):
  lang1 = read(args.src_lang_file)
  lang2 = read(args.trg_lang_file)
  shared_ids = set(lang1.keys()).intersection(lang2.keys())

  all_pairs = [ (lang1[_id], lang2[_id]) for _id in shared_ids]
  train_pairs = [i for i in range(len(all_pairs))]
  test_rate = 0.1
  test_pairs = sorted(random.sample(train_pairs, int(len(train_pairs)* test_rate)))
  train_pairs = list(set(train_pairs) - set(test_pairs))
  train_pairs = [all_pairs[i] for i in train_pairs]
  test_pairs = [all_pairs[i] for i in test_pairs]

  with open(args.output_prefix + '.train.txt', 'w') as f:
    for s,t in train_pairs:
      f.write('%s %s\n' % (s, t))

  with open(args.output_prefix + '.test.txt', 'w') as f:
    for s,t in test_pairs:
      f.write('%s %s\n' % (s, t))

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--src_lang_file", default='jpn/wn-data-jpn.tab', type=str)
  parser.add_argument("--trg_lang_file", default='eng/wn-data-eng.tab', type=str)
  parser.add_argument("--output_prefix", default='ja-en', type=str)
  args  = parser.parse_args()
  main(args)
