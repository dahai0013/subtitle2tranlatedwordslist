import os
import fnmatch
import re
from collections import defaultdict
from os.path import isfile, join
from google.cloud import translate


# Returns a list of all .srt files paths in a directory (Relative to the directory where the script is being executed)
def load_srt_files(path):
    file_paths = [f for f in os.listdir(path) if isfile(join(path, f))]
    file_paths = fnmatch.filter(file_paths, '*.srt')
    return file_paths

# Processes an srt file removing time stamps and blank lines (According to the isubtitles.in format)
# Arguments:
#   path: Path to a single .srt file
#   encoding: Encoding for said file. Example: utf-8
# Returns a list of only the subtitle text line by line
def process_srt_file(path, _encoding):

    text_only_list = []

    with open(path, encoding=_encoding) as fp:
        
        # Get rid of the first two time stamp lines
        line = fp.readline()
        line = fp.readline()

        emptyline_found_flag = 0

        while line:
            line = fp.readline()

            if emptyline_found_flag > 0:
                emptyline_found_flag -= 1
                continue

            if len(line.strip()) == 0:
                emptyline_found_flag = 2
                continue
            else:
                text_only_list.append(line.strip())    

    return text_only_list

def write_subtitle_to_file(path, word_list):

    with open(path[0:-4] + "_out.txt", 'w') as fp:

        for line in word_list:
            fp.write(line+"\n")

# Counts all the words in a given word list and all unique ocurrences
# Arguments:
#   word_list: List of subtitle lines, text only
# Returns:
#   count_dict: Dictionary, each key value pair represents a unique word and its number of ocurrences Note: All words are converted to lowercase before checking
#   count_total_words: Int, total amount of words in the list.
def count_words(word_list):

    count_dict = defaultdict(int)
    count_total_words = 0
    
    for line in word_list:
        # Regular Expression to separate a sentence into words ignoring punctuation
        words =  re.findall(r'[^-\s!,.¿?":;0-9\]\[]+', line)

        for word in words:
            count_dict[word.strip().lower()] += 1
            count_total_words += 1

    return (count_dict, count_total_words)


# Aux function. Takes a list and splits it into n equally sized sublists, preserving the ordering
def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))

def translate_subtitle_file(word_list, target):
    # Instantiates a client
    translate_client = translate.Client()

    # Calls the Google Translation API to translate the text. The API supports sending a list of string however it must no be very long.
    # I tried sending the entire subtitle text but the API rejects it so here I send one line at a time

    translated_text = []

    # segments = list(split(word_list, len(word_list)//100))

    for line in word_list[0:20]:
        translation = translate_client.translate(
            line,
            target_language=target)

        translated_text.append(translation['translatedText'])

    return translated_text


# CONFIG PARAMETERS
source_folder_path = "./narcos-spanish/"
_encoding = "utf-8-sig"

output_folder_path = "output/"

files = load_srt_files(source_folder_path)

textonlylist = process_srt_file(source_folder_path + files[0], _encoding)

write_subtitle_to_file(output_folder_path + files[0], textonlylist)

# for line in textonlylist:
    # print(line)

# translated_text = translate_subtitle_file(textonlylist, "en")

# print(len(translated_text))
# for line in translated_text:
#     print(line)

d, count = count_words(textonlylist)

for w in sorted(d, key=d.get, reverse=True):
  print(w, d[w])