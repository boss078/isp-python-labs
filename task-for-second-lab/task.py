import re
from statistics import median

CONST_EXAMPLE = '''Surprisingly Abraham really did nothing important in his life. He was not a great writer, king, inventor or military leader. He did nothing except camp out where he was told to go and father a few children. His name is great only because the children became nation(s) that kept the record of his life – and then individuals and nations that came from him became great. This is exactly how it was promised in Genesis 12 ("I will make you into a great nation … I will make your name great"). No one else in all history is so well-known only because of descendants rather than from great achievements in his own life.'''

def main():
  k = 10
  n = 4

  accepting_text = input('Do you want to input text? (y/n)')
  if accepting_text == r'Y|y':
    text = input('Enter text: ')

  accepting_k_n = input('Do you want to input k and n? (y/n)')
  if accepting_k_n == r'Y|y':
    k = input('Input k: ')
    n = input('Input n: ')

  text = CONST_EXAMPLE
  # print(f'Input text: {text}')

  text_arr = re.split(r'[(),.;:-]|\s', text)
  formatted_text_arr = []
  excluded_values = [ '…', '...', '' ]
  for elem in text_arr:
    formatted_elem = elem.strip(r'["\'\s–-]')
    if formatted_elem not in excluded_values:
      formatted_text_arr.append(formatted_elem.lower())


  # print(formatted_text_arr)

  amount_dict = {}
  for elem in formatted_text_arr:
    if elem not in amount_dict.keys():
      amount_dict[elem] = 1
    else:
      amount_dict[elem] += 1

  print(f'All words count: {amount_dict}')

  sentencies = re.split(r'[.!?…]', CONST_EXAMPLE)
  sentencies_count = len(sentencies)
  word_count = len(formatted_text_arr)
  middle_value = word_count / sentencies_count

  # print(sentencies)

  median_value = median([len(sentence.split()) for sentence in sentencies])
  print(f'Middle value of words in sentence: {middle_value}')
  print(f'Median value of words in sentence: {median_value}')

  filtered_dict = {}
  for key in amount_dict.keys():
    if len(key) == n:
      filtered_dict[key] = amount_dict[key]

  top_dict = dict(sorted(filtered_dict.items(), key=lambda item: item[1], reverse=True))
  top_of_k = {}
  if k >= len(top_dict):
    top_of_k = top_dict
  else:
    i = 0
    for key in top_dict.keys():
      if i >= k:
        break
      top_of_k[key] = top_dict[key]
      i += 1

  print(f'Top {k} of count of words of {n} length: {top_of_k}')  

if __name__ == '__main__':
  main()