[![BlackArch package](https://repology.org/badge/version-for-repo/blackarch/bopscrk.svg)](https://repology.org/project/bopscrk/versions)
[![Rawsec's CyberSecurity Inventory](https://inventory.raw.pm/img/badges/Rawsec-inventoried-FF5050_flat.svg)](https://inventory.raw.pm/)
[![Packaging status](https://repology.org/badge/tiny-repos/bopscrk.svg)](https://repology.org/project/bopscrk/versions)
![[Version 2.3](https://github.com/r3nt0n)](http://img.shields.io/badge/version-v2.3-orange.svg)
![[Python 3.8](https://github.com/r3nt0n)](http://img.shields.io/badge/python-3.8-blue.svg)
![[GPL-3.0 License](https://github.com/r3nt0n)](https://img.shields.io/badge/license-GPL%203.0-brightgreen.svg)



# bopscrk
**bopscrk** (**B**efore **O**utset **P**a**S**sword **CR**ac**K**ing) is a tool to generate smart and powerful wordlists for targeted attacks.

Included in **<a href="https://blackarch.org/">BlackArch Linux</a>** pentesting distribution and **<a href="https://inventory.raw.pm/">Rawsec's Cybersecurity Inventory</a>** since August 2019.  
  
<p align="center"><img src="https://github.com/R3nt0n/bopscrk/blob/master/img/bopscrk-2.3.gif" /></p>  

+ **Targeted-attack wordlist creator**: introduce personal info related to target, combines every word and transforms results into possible passwords. The *lyricpass* module allows to **search lyrics related to artists** and include them to the wordlists.

+ **Customizable case** and **leet transforms**: create **custom charsets** and **transforms patterns** trough a simple **config file**.

+ **Wordlists exclusion**: Exclude words from another wordlist (to avoid passwords that you have already tested).

+ **Interactive mode** and **one-line command interface** supported. 

## Requirements
+ **Python 3** (secondary branch keeps Python 2.7 legacy support)
+ *optional* - to use `lyricpass` module:   
    `pip install lib/lyricpass/requirements.txt`

## Usage
```

  -h, --help         show this help message and exit
  -i, --interactive  interactive mode, the script will ask you about target
  -w                 words to combine comma-separated (non-interactive mode)
  --min              min length for the words to generate (default: 4)
  --max              max length for the words to generate (default: 32)
  -c, --case         enable case transformations
  -l, --leet         enable leet transformations
  -n                 max amount of words to combine each time (default: 2)
  -a , --artists     artists to search song lyrics (comma-separated)
  -x , --exclude     exclude all the words included in other wordlists
                     (several wordlists should be comma-separated)
  -o , --output      output file to save the wordlist (default: tmp.txt)


```
 
## How it works
+ You have to **provide** some **words** which will act as a base.      
+ The **lyricpass feature** allows to introduce **artists**. The tool will download all his **songs' lyrics** and each line will be added as a new word. By default, artist names and a word formed by the initial of word on each phrase, will be added too.
+ The tool will generate **all possible combinations** between them.  
+ To generate more combinations, it will add some **common separators** (e.g. "-", "_", "."), **numbers** and **special chars** frequently used in passwords.
+ You can use **leet** and **case transforms** to increase your chances.  
+ You can provide **wordlists** that you have already tested against the target in order **to exclude** all this words from the resultant wordlist (`-x`).
  
### Tips  
+ Fields can be left **empty**.
+ You **can use accentuation** in your words.
+ In the others field you can write **several words comma-separated**. *Example*: 2C,Flipper.
+ If you want to produce **all possible leet transformations**, enable the **recursive_leet option** in configuration file.
+ You can **select which transforms to apply on lyrics phrases** found trough the cfg file.
+ Using the **non-interactive mode**, you should provide years in the long and short way (1970,70) to get the same result than the interactive mode.
+ You have to be careful with **-n** argument. If you set a big value, it could result in **too huge wordlists**. I recommend values between 2 and 5.
+ To provide **several artist names** through command line you should provides it **comma-separated**. *Example*: `-a johndoe,johnsmith`
+ To provide **artist names with spaces** through command line you should provides it **quotes-enclosed**. *Example*: `-a "john doe,john smith"`

### Lyricpass 
This feature is based in a modified version of a [tool](https://github.com/initstring/lyricpass) developed originally by [initstring](https://github.com/initstring/). The changes are made to integrate input and output's tool with bopscrk.

It will retrieve all lyrics from all songs which belongs to artists that you provide. **By default it will store each artist, each phrase found with space substitution, each phrase found reduced to its initials** (which will be transformed later if you have activated leet and case transforms).



### Advanced usage

#### Customizing behaviour using .cfg file
+ In `bopscrk.cfg` file you can specify your own charsets and enable/disable options:
  + **extra_combinations** (like `(john, doe) => 123john, john123, 123doe, doe123, john123doe doe123john`) are *enabled by default*. You can disable it in the configuration file in order to get more focused wordlists.  
  + **separators_chars**: characters to use in extra-combinations. *Can be a single char or a string of chars, e.g.: `!?-/&(`*  
  + **separators_strings**: strings  to use in extra-combinations. *Can be a single string or a list of strings space-separated, e.g.: `123` `34!@`*
  + **leet_charset**: characters to replace and correspondent substitute in leet transforms, *e.g.: `e:3 b:8 t:7 a:4`* 
  + **recursive_leet**: enables a recursive call to leet_transforms() function to get all possible leet transforms (*disabled by default*). *WARNING*: enabled with huge --max parameters (e.g.: greater than 18) could take several minutes. *Can be true or false.* 
  + **remove_parenthesis**: remove all parenthesis in lyrics found before any transform  
  + **take_initials**: produce words based on initial of each word in lyric phrases found (if enabled with remove_parenthesis disabled, it can produce useless words)
  + **artist_split_by_word**: split artist names and add each word as a new one 
  + **lyric_split_by_word**: same with lyrics found
  + **artist_space_replacement**: replace spaces in artist names with chars/strings defined in charset
  + **lyric_space_replacement**: same with lyrics found
  + **space_replacement_chars**: characters to insert instead of spaces inside an artist name or a lyric phrase.  *Can be a single char or a string of chars, e.g.: `!?-/&(`*
  + **space_replacement_strings**: strings to insert instead of spaces inside an artist name or a lyric phrase.  *Can be a single string or a list of strings space-separated, e.g.: `123` `34!@`*
+ Some transforms have extensive charsets preincluded. To use it instead of the basic, just uncomment the corresponding line.

+ **Parameters configuration examples**
  + Combine all the words using dots as separator, and same using commas  
    `separators_chars=.,` 
  + Convert all "a/A" occurrences into "4" and all "e/E" occurrences into "3"  
    `leet_charset=a:4 e:3`      


#### Weighted-words system
[...] Coming soon [...]

## Changelist
+ `2.3 version notes (15/10/2020)`
  + **Customizable** configuration for **artists and lyrics transforms** using the cfg file 
  + Requirements at **setup.py updated**
  + **Multithreads logic improved**
  + **Leet and case order reversed** to improve operations efficiency
  + **BUG FIXED** in lyrics space replacement
  + **BUG FIXED** when remove duplicates (*Type Error: unhashable type: 'list'*)
  + **Memory management and efficiency improved**
  + **SPLIT INTO MODULES** to improve project structure
  + **BUG FIXED** in wordlists-exclusion feature
+ `2.2 version notes (11/10/2020`
  + **Configuration file** implemented
  + **NEW FEATURE**: Allow to create **custom charsets** and **transforms patterns** trough the **config file**
  + **NEW FEATURE**: **Recursive leet transforms** implemented (*disabled by default*, can be enabled in cfg file)
+ `2.2~beta version notes (10/10/2020)`
  + The **lyricpass** integration have been **updated to run with last version released by initstring**
  + `--lyrics-all` option removed (feature integrated in other options)        
+ `2.1 version notes (11/07/2020)`  
  + Fixing **min and max length bug**  
+ `2.0/1.5 version notes (17/06/2020)`  
  + **PYTHON 3 NOW IS SUPPORTED**: master branch moves to Python 3. Secondary branch keeps Python 2.7 legacy support    
+ `0-1.2(beta) version notes`  
  + **EXCLUDE WORDLISTS**: speed improvement using multithreaded exclusions  
  + **NEW FEATURE**: lyrics searching related to artists increase the wordlist chances


## TO-DO list
+ Implement **unittests**.
+ Implement **weighted-words system**.
+ Create options to **custom case transforms** (e.g.: disable pair/odd transforms).
+ **Lyricpass** integration was upgraded to last version released by initstring, but still needs some tweaks to speed up the search process (I would appreciate any help).


## Legal disclaimer
This tool is created for the sole purpose of security awareness and education, it should not be used against systems that you do not have permission to test/attack. The author is not responsible for misuse or for any damage that you may cause. You agree that you use this software at your own risk.
