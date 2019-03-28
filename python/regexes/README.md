## grep
This script searches through a file and prints lines containing the searchword.
If argument "--highlight" is given, the word is highlighted.

Example:
``` bash
>>> python3 grep.py grep_demo.txt "AB" --highlight
ABAB  a AB aaj
ofiejojAB
oiejjABoijoAB
oijABoijABoj
```

(with highlighting)

## highlighter
This script looks through a ".syntax" file of regexes matching programming language specific
keywords and highlights them in the terminal printout using matching highlight 
codes found in a ".theme" file.

usage:
``` bash
>>> python3 highlighter.py syntaxfile themefile sourcefile_to_color
```

example:
``` bash
>>> python3 highlighter.py python.syntax python.theme highlighter.py
```
