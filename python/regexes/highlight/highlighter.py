import sys, re, argparse

"""
This script looks through a ".syntax" file of regexes matching programming language specific
keywords and highlights them in the terminal printout using matching highlight 
codes found in a ".theme" file.

usage:
    >>> python3 highlighter.py syntaxfile themefile sourcefile_to_color

example:
    >>> python3 highlighter.py python.syntax python.theme highlighter.py
"""

def make_dict_from_file(filename):
    with open(filename, 'r') as infile:
        r_dict = {} # dict to be returned
        for line in infile:
            if line.strip(): # not empty
                words = re.split(':\s+', line)
                words = list(map(lambda s: s.strip().strip('"'), words)) # strip whitespace og '"'
                r_dict[r"" + words[0]] = words[1]
        return r_dict

def color_syntax(regex, name, theme_dict, text):
    color_num = theme_dict[name]

    # Test om gr.1 er tom
    empty_group_one = re.compile(r"^\(\)\(.+")
    if (re.search(empty_group_one, regex)):
        replacement = r"\1\5\6\033[{}m\7\1\8".format(color_num)
    else:
        replacement = r"\1\5\6\033[{}m\7\6\8".format(color_num)

    fargekode = "\\033\[\d+;?\d*m"
    # regex = (en fargekode)(ikke etterfulgt av en ny fargekode før regex)(noe)(regex)
    regex = f"({fargekode})?(?!.*(?:{fargekode}).*{regex})(.*){regex}"
    regex = re.compile(regex, flags=re.MULTILINE)
    text = re.sub(regex,
                        replacement,
                        text)
    return text


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Color inputfiles.')
    parser.add_argument('syntaxfile' , type=str)
    parser.add_argument('themefile' , type=str)
    parser.add_argument('sourcefile' , type=str)

    args = parser.parse_args() 
    syntax_dict = make_dict_from_file(args.syntaxfile)
    theme_dict = make_dict_from_file(args.themefile)

    with open(args.sourcefile, 'r') as infile:
        text = infile.read()

    text = re.sub(r"(^.)", r"\033[0m\1", text, flags=re.MULTILINE)

    # Fargelegg comments først (jeg hadde ikke trengt dette hvis vi kunne hatt navn som key)
    for regex, name in syntax_dict.items():
        if (name == 'comment'):
            text = color_syntax(regex, name, theme_dict, text)

    for regex, name in syntax_dict.items():
        if (name == "comment"):
            continue
        else:
            text = color_syntax(regex, name, theme_dict, text)
    print(text)
