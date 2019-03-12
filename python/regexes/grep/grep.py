import argparse, re

"""
This script searches through a file and prints lines containing the searchword.
If argument "--highlight" is given, the word is highlighted.

Example:
    >>> python3 grep.py grep_demo.txt "AB" --highlight
    ABAB  a AB aaj
    ofiejojAB
    oiejjABoijoAB
    oijABoijABoj

    (med highlighting)
"""

parser = argparse.ArgumentParser(description='Grep utility, find lines in files that matches regex')
parser.add_argument('filename', type=str)
parser.add_argument('regex', type=str)
parser.add_argument('--highlight', action='store_true')
args = parser.parse_args()

with open(args.filename, 'r') as infile:
    """
    Match første treff + alt foran og legg det til i outputline,
    fjern det som er lagt til i outputline fra inputline
    rinse and repeat til det ikke er flere matches.
    """
    regex = args.regex
    color = ''
    defcolor = ''

    if (args.highlight):
        color    = r'\033[101;97m'
        defcolor = r'\033[0m'

    regex2 = re.compile(f'(?P<before>.*?)(?P<match>{regex})(?P<rest>.*$)')
    output_replace   = r'\g<before>'+color+r'\g<match>'+defcolor

    for line in infile:
        matches = re.findall(regex, line)
        inputline  = line
        outputline = ''
        for match in matches:
            # sub legger til newline av en eller annen grunn, slik at jeg må rightstrippe
            outputline += re.sub(regex2, output_replace, inputline).rstrip()
            inputline = re.sub(regex2, r'\g<rest>', inputline).rstrip()
        if (outputline):
            outputline += inputline # legg til siste rest etter match
            print(outputline)
