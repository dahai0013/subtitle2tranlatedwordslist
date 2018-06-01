# Subtitle 2 Translated List of words

The End goal of this project is to help people learning ( spanish) words from TV series subtitles using Quizlet (or other flash card project ;-)



## Getting Started

    Phase 1- python script  ( create a word list and translate ) [  + Create an dictionary per language / per season = summary of all word list    — for future application / statistics
    Phase 2- website: subtitle search, check if already exist and create a Quizlet
    Phase 3- script apply to many subtitle languages / TV series with many episode
    Phase 4- graph on the website ( statistics of words usage per single subtitle files and multiple subtitle files )  
    Phase 5- Integrate learning progress from Quizlet ( or other ) to create new list of words/ per subtitle files
    Phase 6- Improve the learning, AI looking at all the data collected/statistics to find the best way/time/style to learn  [ will be different project ]

### Prerequisites

  The script is using python 3



### Phase 1a

    1- srt substitute file >>> remove the time stamps create 2 files : list of text subtitle + list of "description information" example

    2- from the "subtitles words only 
        1- count all the words  ( summary )
        2- count only the unique words ( provide stat of words / subtitle text + unique words summary )
        3- More advance: count only the same word for: masculin/feminim, also "la + noums" /"el + noums" = 1 words ,  various tense verbs = 1 words

    3- create a list + translation
        1- translate the words, order based on the count per subtitle



### Phase 1b

1- usage a mix of dictionary and API
2- use of database to save the list of words and meta information like: noums, verb, various statistics
3- cover all features

## Phase 1: python script manual information:

subtitle2tranlatedwordslist.py --help

    usage:  subtitle2tranlatedwordslist.py   <TV_serie_S0xE0x.srt>

    Options:
    TV_serie_S0xE0x.srt      Mandatory.

    -o          Output file <TV_serie_S0xE0x.srt.csv>. Default.
    -d          description file <description_file.csv>.
    -e          translate expression as one word:  "Qué tal"  and not "Qué" "tal".
    -c          composed words: "dímelo or dile or diles" should be made as one_multiword
    --dbo       other output format, database format, to be defile in the future.
    --aato      add article to nouns to origin language: + el, la.
    --aivto     add infinite verb form to origin language, format "<SINGLE SPACE> INFINITE_VERB_FORM".
    --gsv       group same verb.
    --dwi       display word's information: N for Nouns and V for Verb.
    --oon       output only the nouns.
    --oov       output only the verbs.
    --ootr      output only the rest.

    --ol        original_language: esp , en , ...
    --tl        target_language: eng , fr.  
    --st        second language: romanization or transliteration : PinYin , ....
    --ra        remove article: el, la, una, ...

    --bstat     Basic statistics : only summary of count of words.  Default.
    --fstat     Full statistics report: with everything from below.
    --swstat    Single words statistics.
    --swnastat  Single words no articles statistic ???? is it needed ????.
    --swonstat  Single words  only nouns statistic.
    --swovstat  Single words  only verbs statistic.
    --swotrstat Single words  only the rest statistic.
    --swiestat  Single words including expression ( like "Qué tal" ) statistics.

    --mfl       Multi-file option:  list of file.
    --mfd       Multi-file directory.
    --mfso      Multi-file single output file .csv.
    --mfmo      Multi-file multiple output file .csv.
    --mstat     Multi-file stats.




## Contributing

Everyone is welcome ;-)


## Versioning

Beta version

## Authors

* Me, Myself and I ( https://www.youtube.com/watch?v=CGk962QLIzk )


## License

Free Code Forever and Wakanda.

## Acknowledgments

* Python Team and Linus Torvalds
* Youtuber, Blogger and contributor of all type
* and You
