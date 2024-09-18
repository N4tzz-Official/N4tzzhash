#!/usr/bin/env python3

import argparse
import sys
import itertools

# Colors
MAIN = '\033[38;5;50m'
LOGO = '\033[38;5;41m'
LOGO2 = '\033[38;5;42m'
GREEN = '\033[38;5;82m'
ORANGE = '\033[0;38;5;214m'
PRPL = '\033[0;38;5;26m'
PRPL2 = '\033[0;38;5;25m'
RED = '\033[1;31m'
END = '\033[0m'
BOLD = '\033[1m'

def banner():
    print("\033[1;32m")  # Set text color to green
    print("███╗   ██╗██╗  ██╗████████╗███████╗███████╗    ██████╗ ██████╗  ██████╗ ███████╗         █████╗ ████████╗████████╗ █████╗  ██████╗██╗  ██╗")
    print("████╗  ██║██║  ██║╚══██╔══╝╚══███╔╝╚══███╔╝    ██╔══██╗██╔══██╗██╔═══██╗██╔════╝        ██╔══██╗╚══██╔══╝╚══██╔══╝██╔══██╗██╔════╝██║ ██╔╝")
    print("██╔██╗ ██║███████║   ██║     ███╔╝   ███╔╝     ██║  ██║██║  ██║██║   ██║███████╗        ███████║   ██║      ██║   ███████║██║     █████╔╝ ")
    print("██║╚██╗██║╚════██║   ██║    ███╔╝   ███╔╝      ██║  ██║██║  ██║██║   ██║╚════██║        ██╔══██║   ██║      ██║   ██╔══██║██║     ██╔═██╗ ")
    print("██║ ╚████║     ██║   ██║   ███████╗███████╗    ██████╔╝██████╔╝╚██████╔╝███████║███████╗██║  ██║   ██║      ██║   ██║  ██║╚██████╗██║  ██╗")
    print("╚═╝  ╚═══╝     ╚═╝   ╚═╝   ╚══════╝╚══════╝    ╚═════╝ ╚═════╝  ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚═╝  ╚═╝ ╚═════╝╚        ")                                                                                                   
    print("                                                                                                                                            ")
    print("\033[0m")  # Reset text color

def exit_with_msg(msg):
    parser.print_help()
    print(f'\n[{RED}Error{END}] {msg}\n')
    sys.exit(1)

def unique(lst):
    return list(set(lst))

# Arguments & Usage
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    epilog='''
Usage examples:

  Basic:
      python3 psudohash.py -w <keywords> -cpa

  Thorough:
      python3 psudohash.py -w <keywords> -cpa -an 3 -y 1990-2022
'''
)

parser.add_argument("-w", "--words", action="store", help="Comma separated keywords to mutate", required=True)
parser.add_argument("-an", "--append-numbering", action="store", help="Append numbering range at the end of each word mutation.", type=int, metavar='LEVEL')
parser.add_argument("-nl", "--numbering-limit", action="store", help="Change max numbering limit value of option -an.", type=int, metavar='LIMIT')
parser.add_argument("-y", "--years", action="store", help="Single OR comma separated OR range of years to be appended.")
parser.add_argument("-ap", "--append-padding", action="store", help="Add comma separated values to common paddings", metavar='VALUES')
parser.add_argument("-cpb", "--common-paddings-before", action="store_true", help="Append common paddings before each mutated word")
parser.add_argument("-cpa", "--common-paddings-after", action="store_true", help="Append common paddings after each mutated word")
parser.add_argument("-cpo", "--custom-paddings-only", action="store_true", help="Use only user provided paddings for word mutations.")
parser.add_argument("-o", "--output", action="store", help="Output filename (default: output.txt)", metavar='FILENAME')
parser.add_argument("-q", "--quiet", action="store_true", help="Do not print the banner on startup")

args = parser.parse_args()

def banner_output():
    padding = '  '
    N = [[' ', '┌', '─', '┐'], [' ', '│', '─', '│'], [' ', '└', '─', '┘']]
    H = [[' ', '┬', ' ', '┬'], [' ', '├', '─', '┤'], [' ', '┴', ' ', '┴']]
    A = [[' ', '┌', '─', '┐'], [' ', '├', '─', '┤'], [' ', '└', '─', '┘']]
    S = [[' ', '┬', ' ', '┬'], [' ', '├', '─', '┤'], [' ', '└', '─', '┘']]
    banner = [N, H, A, S, H]
    final = []
    print('\r')
    init_color = 37
    txt_color = init_color
    cl = 0

    for charset in range(0, 3):
        for pos in range(0, len(banner)):
            for i in range(0, len(banner[pos][charset])):
                clr = f'\033[38;5;{txt_color}m'
                char = f'{clr}{banner[pos][charset][i]}'
                final.append(char)
                cl += 1
                txt_color = txt_color + 36 if cl <= 3 else txt_color

            cl = 0
            txt_color = init_color
        init_color += 31

        if charset < 2:
            final.append('\n   ')

    print(f"   {''.join(final)}")
    print(f'{END}{padding}                        by N4tzz\n')

def unique(lst):
    return list(set(lst))

# ----------------( Base Settings )---------------- #
mutations_cage = []
basic_mutations = []
outfile = args.output if args.output else 'output.txt'
trans_keys = []

transformations = [
    {'a': ['@', '4']},
    {'b': '8'},
    {'e': '3'},
    {'g': ['9', '6']},
    {'i': ['1', '!']},
    {'o': '0'},
    {'s': ['$', '5']},
    {'t': '7'}
]

for t in transformations:
    for key in t.keys():
        trans_keys.append(key)

# Common Padding Values
if (args.custom_paddings_only or args.append_padding) and not (args.common_paddings_before or args.common_paddings_after):
    exit_with_msg('Options -ap and -cpo must be used with -cpa or -cpb.')

elif (args.common_paddings_before or args.common_paddings_after) and not args.custom_paddings_only:
    try:
        with open('common_padding_values.txt', 'r') as f:
            common_paddings = [val.strip() for val in f.readlines()]
    except FileNotFoundError:
        exit_with_msg('File "common_padding_values.txt" not found.')

elif (args.common_paddings_before or args.common_paddings_after) and (args.custom_paddings_only and args.append_padding):
    common_paddings = []

elif not (args.common_paddings_before or args.common_paddings_after):
    common_paddings = []

else:
    exit_with_msg('\nIllegal padding settings.\n')

if args.append_padding:
    for val in args.append_padding.split(','):
        if val.strip() != '' and val not in common_paddings:
            common_paddings.append(val)

if (args.common_paddings_before or args.common_paddings_after):
    common_paddings = list(set(common_paddings))

# ----------------( Functions )---------------- #
def evalTransformations(w):
    trans_chars = []
    total = 1
    c = 0
    w = list(w)

    for char in w:
        for t in transformations:
            if char in t.keys():
                trans_chars.append(c)
                if isinstance(t[char], list):
                    total *= len(t[char])
                else:
                    total *= 2
        c += 1

    return [trans_chars, total]

def mutate(tc, word):
    global trans_keys, mutations_cage

    i = trans_keys.index(word[tc].lower())
    trans = transformations[i][word[tc].lower()]
    limit = len(trans) * len(mutations_cage)
    c = 0

    for m in mutations_cage:
        w = list(m)

        if isinstance(trans, list):
            for tt in trans:
                w[tc] = tt
                transformed = ''.join(w)
                mutations_cage.append(transformed)
                c += 1
        else:
            w[tc] = trans
            transformed = ''.join(w)
            mutations_cage.append(transformed)
            c += 1

        if limit == c:
            break

    return mutations_cage

def mutations_handler(kword, trans_chars, total):
    global mutations_cage, basic_mutations

    container = []

    for word in basic_mutations:
        mutations_cage = [word.strip()]
        for tc in trans_chars:
            results = mutate(tc, kword)
        container.append(results)

    for m_set in container:
        for m in m_set:
            basic_mutations.append(m)

    basic_mutations = list(set(basic_mutations))

    with open(outfile, 'a') as wordlist:
        for m in basic_mutations:
            wordlist.write(m + '\n')

def mutateCase(word):
    trans = list(map(''.join, itertools.product(*zip(word.upper(), word.lower()))))
    return trans

def caseMutationsHandler(word, mutability):
    global basic_mutations
    case_mutations = mutateCase(word)

    for m in case_mutations:
        basic_mutations.append(m)

    if not mutability:
        basic_mutations = list(set(basic_mutations))

# ----------------( Start )---------------- #
if not args.quiet:
    banner()

# Process words
words = args.words.split(',')
words = [w.strip() for w in words]

if args.years:
    years = args.years.split(',')
    years = [y.strip() for y in years]

    if len(years) == 1:
        words = [f"{w}{years[0]}" for w in words]
    elif len(years) > 1:
        years = unique(years)
        for w in words:
            for y in years:
                words.append(f"{w}{y}")

if args.append_numbering:
    if args.numbering_limit:
        limit = args.numbering_limit
    else:
        limit = 999

    words = [f"{w}{n}" for w in words for n in range(1, args.append_numbering + 1) if n <= limit]

if args.append_padding:
    for padding in args.append_padding.split(','):
        for w in words:
            basic_mutations.append(f"{w}{padding.strip()}")
            basic_mutations.append(f"{padding.strip()}{w}")

if args.common_paddings_before or args.common_paddings_after:
    for word in words:
        if args.common_paddings_before:
            for padding in common_paddings:
                basic_mutations.append(f"{padding}{word}")
        if args.common_paddings_after:
            for padding in common_paddings:
                basic_mutations.append(f"{word}{padding}")

if args.custom_paddings_only:
    for word in words:
        for padding in common_paddings:
            basic_mutations.append(f"{word}{padding}")

for word in words:
    transformed_word = mutateCase(word)
    basic_mutations.extend(transformed_word)

if args.append_numbering or args.append_padding:
    mutations_cage = unique(mutations_cage)
    for word in words:
        trans_chars, total = evalTransformations(word)
        mutations_handler(word, trans_chars, total)

basic_mutations = unique(basic_mutations)

with open(outfile, 'a') as wordlist:
    for mutation in basic_mutations:
        wordlist.write(mutation + '\n')

print(f"\n[{GREEN}Success{END}] Processed mutations saved to '{outfile}'")
