import os
import fnmatch
import re
import time
import json
import ast

from collections import defaultdict
from os.path import isfile, join
from google.cloud import translate

# Returns a list of all .srt files paths (strings) in a directory (Relative to the directory where the script is being executed)
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

# Writes all lines into a file
# Arguments:
#   line_list: List of subtitle lines, text only
#      Example: ["My name is John and", "I come from New York"]
def write_subtitle_to_file(path, suffix, line_list, _encoding):

    with open(path[0:-4] + suffix + ".txt", 'w', encoding=_encoding) as fp:

        for line in line_list:
            fp.write(line+"\n")

# Counts all the words in a given line list and all unique ocurrences
# Arguments:
#   line_list: List of subtitle lines, text only
#       Example: ["My name is John and", "I come from New York"]
# Returns:
#   count_dict: Dictionary, each key value pair represents a unique word and its number of ocurrences Note: All words are converted to lowercase before checking
#   count_total_words: Int, total amount of words in the list.
def count_words(line_list):

    count_dict = defaultdict(int)
    count_total_words = 0

    for line in line_list:
        # Regular Expression to separate a sentence into words ignoring punctuation
        words =  re.findall(r'[^-\s!,.¿?♪":;0-9\]\[]+', line)

        for word in words:
            count_dict[word.strip().lower()] += 1
            count_total_words += 1

    return (count_dict, count_total_words)


# Separates a list of lines of words into a list of words. Order is preserved.
# Arguments:
#   line_list: List of subtitle lines, text only.
#       Example: ["My name is John and", "I come from New York"]
# Returns:
#   return_list: List of words - Ex: ["My", "name", "is", "John", "and" "I", "come", "from", "New", "York"]
def get_words(line_list):
    
    return_list = []

    for line in line_list:
        # Regular Expression to separate a sentence into words ignoring punctuation
        words =  re.findall(r'[^-\s!,.¿?":;0-9\]\[]+', line)

        for word in words:
            return_list.append(word)

    return return_list



# Aux function. Takes a list and splits it into n equally sized sublists, preserving the ordering
def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))


def translate_subtitle_file(word_list, target="en"):
    # Instantiates a client
    translate_client = translate.Client()

    # Calls the Google Translation API to translate the text. The API supports sending a list of strings however it must no be very long.
    # Sending a list of 100 words in each request works well.

    translated_text = []

    # The number of 100 words segments
    num_segments = len(word_list) // 100

    # Splits the word list into a list of lists of 100 elements each
    segments = list(split(word_list, num_segments))

    for i in range(len(segments)):

        #print("SEGMENT")
        #print(segments[i])
        translation = translate_client.translate(
            segments[i],
            target_language=target,
            source_language="es")

        for d in translation:
            translated_text.append(d["translatedText"])

        print("request {}".format(i + 1))
        time.sleep(0.1)

    return translated_text


def main():
    # CONFIG PARAMETERS
    source_folder_path = "./narcos-spanish/"
    _encoding = "utf-8-sig"
    output_folder_path = "output/"

    # Begin
    files_paths = load_srt_files(source_folder_path)

    for path in files_paths:
        print("Processing file: {}".format(path))
        # Remove timestamps to generate the text only subtitle file
        textonly_list = process_srt_file(source_folder_path + path, _encoding)

        count_dict, count_total_words = count_words(textonly_list)

        sorted_keys = sorted(count_dict, key=count_dict.get, reverse=True)

        translated_text = translate_subtitle_file(sorted_keys, "en")

        # Write the first file: List of text subtitle
        write_subtitle_to_file(output_folder_path + path, "_subtitleText", textonly_list, _encoding)

        # Build the list of lines to be written
        
        lines = [str(count_total_words)]

        i = 0

        for k in sorted_keys:
            lines.append("{},{},{}".format(count_dict[k], k, translated_text[i]))
            i += 1

        # Write the second file: Stats + translation. Format: count, spanish_word, english_word
        write_subtitle_to_file(output_folder_path + path, "_stats_translation", lines, _encoding)

main()