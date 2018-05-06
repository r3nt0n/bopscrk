# Bopscrk
Bopscrk (**Before Outset PaSsword CRacKing**) is a tool to **assist** in all the **previous process of password cracking**. By now, it's able to generate smart and powerful wordlists.
  
  
  
<p align="center"><img src="https://github.com/R3nt0n/bopscrk/blob/master/img/example.gif" /></p>
  
  
  

The first idea was inspired by **Cupp** and **Crunch**. We could say that bopscrk is a wordlist generator **situated between them**, taking the best of each one. The challenge was try to apply the Cupp's idea to more generic-situations and amplify the shoot-range of the resultant wordlist, without loosing this custom-wordlist-profiler feature.


## How it works
* You have to **provide** some **words** which will act as a **base**.
* The tool will generate **all possible combinations** between them.
* To generate more combinations, it will add some **common separators** (e.g. "-", "_", "."), **random numbers** and **special chars**.
* You can enable **leet** and **case transforms** to increase your chances.
<<<<<<< HEAD
* If you enable **lyricpass mode**, the tool will ask you about **artists** and it will download all his **songs' lyrics**. Each line will be added as a new word. Then it will be **transform in several ways** (leet, case, only first letters, with and without spaces...). Artist names will be added too. 
=======
If you enable **lyricpass mode**, the tool will ask you about **artists** and it will download all his **songs' lyrics**. Each line will be added as a new word. Then it will be **transform in several ways** (leet, case, only first letters, with and without spaces...). Artist names will be added too. 
>>>>>>> origin/master
 

## Requirements
* Python 2.7
* requests (*optional*, only if you want to use lyricpass)
* beautifulsoup4 (*optional*, only if you want to use lyricpass)

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
  -x wordlist        exclude all the words included in other wordlists  
                     (several wordlists should be comma-separated)  
  -o , --output      output file to save the wordlist (default: tmp.txt)  

```
 

## Tips
* Fields can be left **empty**.
* Words have to be written **without accents**, just normal characters.
* In the others field you can write **several words comma-separated**. *Example*: 2C,Flipper.
* Using the **non-interactive mode**, you should provide years in the long and short way (1970,70) to get the same result than the interactive mode.
* You have to be careful with **-n** argument. If you set a big value, it could be result in **too huge wordlists**. I recommend values between 2 and 5.


## Experimental features
* Lyricpass integration is cooming soon.
* Excluded wordlists needs some improvements, with huge wordlists could be too slow (I would appreaciate any help).


### Lyricpass 
This feature is based in a modified version of a [tool](https://github.com/initstring/lyricpass) developed originally by [initstring](https://github.com/initstring/).

Still under development.