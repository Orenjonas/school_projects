import sys, os


if (len(sys.argv) < 2):
    print("Usage:\n>python3 [filename]")

def count_and_print_stats_about(filename: str):
    """
    Counts and prints the number of lines, words and characters in a file,
    or several files.

    Args:
        filename (string): Name of the file

    Returns:
        None

    Examples:
        >>> python3 wc.py wc.py

        file:  wc.py
        -----------
        lines: 53
        words: 123
        chars: 1152

        >>> python3 wc.py wc.py wc.py

        file:  wc.py
        -----------
        lines: 53
        words: 123
        chars: 1152


        file:  wc.py
        -----------
        lines: 53
        words: 123
        chars: 1152

    """
    try:
        infile = open(filename, "r")
        lines = 0
        words = 0
        chars = 0

        for line in infile:
            lines += 1
            words += len(line.split())
            chars += len(line)

        print("\nfile:  %s" % (filename))
        print("-----------")
        print("lines: %d" % (lines))
        print("words: %d" % (words))
        print("chars: %d\n" % (chars))
        infile.close()
    except:
        print("Could not open " + filename)
    finally:
        infile.close()

if (len(sys.argv) == 2):        # Only one file
    filename = sys.argv[1]
    count_and_print_stats_about(filename)

else:
    files = sys.argv[1:]
    for f in files:
        count_and_print_stats_about(f)

