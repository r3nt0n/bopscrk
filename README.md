<div id="top"></div>
<!-- 
This documentation was written using Best-README-Template by othneildrew
https://github.com/othneildrew/
https://github.com/othneildrew/Best-README-Template/edit/master/README.md 
Thanks dude :)
-->



<!-- PROJECT SHIELDS -->
[![BlackArch package](https://repology.org/badge/version-for-repo/blackarch/bopscrk.svg)](https://repology.org/project/bopscrk/versions)
[![Rawsec's CyberSecurity Inventory](https://inventory.raw.pm/img/badges/Rawsec-inventoried-FF5050_flat.svg)](https://inventory.raw.pm/)
[![Packaging status](https://repology.org/badge/tiny-repos/bopscrk.svg)](https://repology.org/project/bopscrk/versions)
![[GPL-3.0 License](https://github.com/r3nt0n)](https://img.shields.io/badge/license-GPL%203.0-brightgreen.svg)
![[Python 3](https://github.com/r3nt0n)](http://img.shields.io/badge/python-3-blue.svg)
![[Version 2.4.5](https://github.com/r3nt0n)](http://img.shields.io/badge/version-2.4.5-orange.svg)



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/r3nt0n/bopscrk">
    <img src="https://github.com/r3nt0n/bopscrk/blob/master/img/logo_raster.svg" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">bopscrk</h3>

  <p align="center">
    A tool to generate smart and powerful wordlists for targeted attacks
    <br />
    <a href="#usage"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="#about-the-project">View Demo</a>
    ·
    <a href="https://github.com/r3nt0n/bopscrk">Report Bug</a>
    ·
    <a href="https://github.com/r3nt0n/bopscrk">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About the Project</a>
      <ul>
        <li><a href="#whats-new">What's new</a></li>
        <li><a href="#built-with">Built with</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#run-interactive-mode">Run interactive mode</a></li>
      </ul>
    </li>
    <li>
      <a href="#usage">Usage</a>
      <ul>
        <li><a href="#how-it-works">How it works</a></li>
        <li><a href="#tips">Tips</a></li>
        <li><a href="#lyricpass">Lyricpass</a></li>
        <li><a href="#advanced-usage">Advanced usage</a></li>
      </ul>
    </li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li>
      <a href="#contributing">Contributing</a>
      <ul>
        <li><a href="#contributors">Contributors</a></li>
      </ul>
    </li>
    <li><a href="#changelist">Changelist</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
    <li><a href="#legal-disclaimer">Legal disclaimer</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About the Project

<p align="center"><img src="https://github.com/r3nt0n/bopscrk/blob/master/img/bopscrk-2.4.5.gif" /></p>  



+ **Targeted-attack wordlist creator**: introduce personal info related to target, combines every word and transforms results into possible passwords. The *lyricpass* module allows to **search lyrics related to artists** and include them to the wordlists.
+ **Customizable case** and **leet transforms**: create **custom charsets** and **transforms patterns** trough a simple **config file**.
+ **Interactive mode** and **one-line command interface** supported. 
+ Included in **<a href="https://blackarch.org/">BlackArch Linux</a>** pentesting distribution and **<a href="https://inventory.raw.pm/">Rawsec's Cybersecurity Inventory</a>** since August 2019.


### Built with

+ **Python 3** (secondary branch keeps Python 2.7 legacy support)
  + **requests**
  + **alive-progress**

### What's new

**2.4.5 RELEASED**: Progress bar with ETA implemented!

[//]: # (<p align="center"><img src="https://github.com/r3nt0n/bopscrk/blob/master/img/progressbar_example1.gif" /></p>)

[//]: # (<p align="center"><img src="https://github.com/r3nt0n/bopscrk/blob/master/img/progressbar_example2.gif" /></p>)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting started

### Installation

```
pip install bopscrk
```

<!-- Download from Github and install requirements -->
<!-- COMMENTED FOR NOW -->
[//]: # (#### Option 2: Download last version published on Github &#40;more updated&#41;)

[//]: # (```)

[//]: # (git clone --recurse-submodules https://github.com/r3nt0n/bopscrk)

[//]: # (cd bopscrk)

[//]: # (pip install -r requirements.txt)

[//]: # (```)
<!-- END COMMENT -->

### Run interactive mode
```
bopscrk -i
```

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- USAGE EXAMPLES -->
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
  -o , --output      output file to save the wordlist (default: tmp.txt)
  -C , --config      specify config file to use (default: ./bopscrk.cfg)
  --version          print version and exit

```

_For more information, please refer to the [Advanced usage](#advanced-usage) section._

<p align="right">(<a href="#top">back to top</a>)</p>

### How it works
+ You have to **provide** some **words** which will act as a base.      
+ The **lyricpass feature** allows to introduce **artists**. The tool will download all his **songs' lyrics** and each line will be added as a new word. By default, artist names and a word formed by the initial of word on each phrase, will be added too.
+ The tool will generate **all possible combinations** between them.  
+ To generate more combinations, it will add some **common separators** (e.g. "-", "_", "."), **numbers** and **special chars** frequently used in passwords.
+ You can use **leet** and **case transforms** to increase your chances.  

[//]: # (+ You can provide **wordlists** that you have already tested against the target in order **to exclude** all this words from the resultant wordlist &#40;`-x`&#41;.)
  
### Tips  
+ Fields can be left **empty**.
+ You **can use accentuation** in your words.
+ In the others field you can write **several words comma-separated**. *Example*: 2C,Flipper.
+ If you want to produce **all possible leet transformations**, enable the **recursive_leet option** in configuration file.
+ You can **select which transforms to apply on lyrics phrases** found through the **cfg file**.
+ Using the **non-interactive mode**, you should provide years in the long and short way (1970,70) to get the same result than the interactive mode.
+ You have to be careful with **-n** argument. If you set a big value, it could result in **too huge wordlists**. I recommend values between 2 and 5.
+ To provide **several artist names** through command line you should provides it **comma-separated**. *Example*: `-a johndoe,johnsmith`
+ To provide **artist names with spaces** through command line you should provides it **quotes-enclosed**. *Example*: `-a "john doe,john smith"`

### Lyricpass 
<p align="center"><img src="https://github.com/R3nt0n/bopscrk/blob/master/img/lyricpass_demo.png" /></p>  

This feature is based in a modified version of a [tool](https://github.com/initstring/lyricpass) developed originally by [initstring](https://github.com/initstring/). The changes are made to integrate input and output's tool with bopscrk.  

It will retrieve all lyrics from all songs which belongs to artists that you provide. **By default it will store each artist, each phrase found with space substitution, each phrase found reduced to its initials** (which will be transformed later if you have activated leet and case transforms).

### Advanced usage

#### Customizing behaviour using .cfg file
+ In `bopscrk.cfg` file you can specify your own charsets and enable/disable options:
  + **threads**: number of threads to use in multithreaded operations
  + **extra_combinations** (like `(john, doe) => 123john, john123, 123doe, doe123, john123doe doe123john`) are *enabled by default*. You can disable it in the configuration file in order to get more focused wordlists.  
  + **separators_chars**: characters to use in extra-combinations. *Can be a single char or a string of chars, e.g.: `!?-/&(`*  
  + **separators_strings**: strings  to use in extra-combinations. *Can be a single string or a list of strings space-separated, e.g.: `123` `34!@`*
  + **leet_charset**: characters to replace and correspondent substitute in leet transforms, *e.g.: `e:3 b:8 t:7 a:4`* 
  + **recursive_leet**: enables a recursive call to leet_transforms() function to get all possible leet transforms (*disabled by default*). *WARNING*: enabled with huge --max parameters (e.g.: greater than 18) could take even days. *Can be true or false.* 
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

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] Improve **memory management**
    - [ ] Write wordlists into filesystem during execution and use it as cache (<a href="https://github.com/r3nt0n/bopscrk/issues">#12</a>)
- [ ] Improve **performance**
    - [ ] Refactor and improve threads and transforms logic
- [ ] Extra features
    - [x] Implement **progress bar** to keep user informed of the execution state
    - [ ] Implement **session file** to keep track of the execution point and **be able to stop and resume sessions** (<a href="https://github.com/r3nt0n/bopscrk/issues">#12</a>)
    - [ ] Create **config options** for customized **case transforms** (e.g.: disable pair/odd transforms)

See the [open issues](https://github.com/r3nt0n/bopscrk/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


### Contributors
* [noraj](https://github.com/noraj) contributed opening several issues and pull requests that have allow to fix some important bugs. He also managed by his own the tool's addition in BlackArch and RawSec repositories, which has increase its popularity and use
* [nylocx](https://github.com/nylocx) and [agoertz-fls](https://github.com/agoertz-fls) contributed adding Python3 support
* [glozanoa](https://github.com/glozanoa) and [fabaff](https://github.com/fabaff) contributed adding bopscrk command (improvements on setup.py)

Thank you all!

<p align="right">(<a href="#top">back to top</a>)</p>



## Changelist
[//]: # (+ `last development version &#40;available on Github&#41;`)
+ `2.4.5 version notes (02/08/2022)`
  + **progress bar** implemented and working
  + `version` argument included
  + Docs improved

+ `2.4.4 version notes (31/07/2022)`
  + **Relative imports bug fixed**
  + Starting to refactor general structure to allow **progressbar feature inclusion**

+ `2.4.3 version notes (28/07/2022)`
  + Fixing project structure to allow properly install via pip:
    + Add MANIFEST to exclude compiled and tests files when building dist
    + Improving structure to properly copy all structure into python packages dir inside a parent dir
    + Fixing relative path to config file
  + Catch exception when a wrong config file was provided (notice and exit)

+ `2.4 version notes (26/07/2022)`
  + Make the installation process easier enabling `pip install` method
  + Starting to implement better memory management (cached wordlists writing and reading i/o files), not working yet
  + Updating and fixing minor bugs related to dependencies
  + **REMOVED FEATURE**: 'exclude from other wordlists', doesn't seem useful, there is other tools to do this specific work 

+ `2.3.1 version notes`
  + Fixing namespace bug (related to aux.py module, renamed to auxiliars.py) when running on windows systems
  + **unittest** (and simple unitary tests for transforms, excluders and combinators functions) **implemented**.

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

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the GNU General Public License v3.0. See `LICENSE` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

r3nt0n: [Github](https://github.com/r3nt0n) - [email](r3nt0n@protonmail.com)  
bopscrk: [Github](https://github.com/r3nt0n/bopscrk) - [Pypi](https://pypi.org/project/bopscrk)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* lyricpass module is based on a [project](https://github.com/initstring/lyricpass) created by [initstring](https://github.com/initstring).
* [Pixel Gothic font](https://dafonttop.com/pixel-gothic-font.font) by [Kajetan Andrzejak](https://dafonttop.com/tags.php?key=Kajetan%20Andrzejak).

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LEGAL DISCLAIMER -->
## Legal disclaimer
This tool is created for the sole purpose of security awareness and education, it should not be used against systems that you do not have permission to test/attack. The author is not responsible for misuse or for any damage that you may cause. You agree that you use this software at your own risk.

<p align="right">(<a href="#top">back to top</a>)</p>


