# bopscrk
Bopscrk (**Before Outset PaSsword CRacKing**) is a tool to **assist** in all the **previous process of password cracking**. By now, it's able to generate smart and powerful wordlists.
  
  
  
<p align="center"><img src="https://github.com/R3nt0n/bopscrk/blob/master/img/example.gif" /></p>
  
  
  

The first idea was inspired in **Cupp** and **Crunch**. We could say that bopscrk is a wordlist generator **situated between them**, taking the best of each one. The challenge was try to apply the Cupp's idea to more generic-situations and amplify the shoot-range of the resultant wordlist, without loosing this custom-wordlist-profiler feature.


## How it works
* You have to **provide** some **words** which will act as a **base**.
* The tool will generate **all possible combinations** between them.
* To generate more combinations, it will add some **common separators** (e.g. "-", "_", "."), random numbers and special chars.
* You can enable **leet** and **case transforms** to increase your chances.
 


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
  -o , --output      output file to save the wordlist (default: tmp.txt)  
```

 

## Tips
* Names have to be written **without accents**, just normal characters.
* In the others field you can write **several words comma-separated**. *Example*: 2C,Flipper.
* Fields can be left **empty**.
* If you enable case transforms, doesn't matter the lower/uppercases in your inputs (because all case posibilities will be created).
