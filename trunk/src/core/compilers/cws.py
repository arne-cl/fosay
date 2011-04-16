# -----------------------------------------------------------------------------
# CWS - Cascading Word Sheets (v0.1)
# -----------------------------------------------------------------------------
__author__="Z-CORE"
__date__ ="$5 бер 2011 11:36:40$"

from core.models.ling_units import Token
import core.ply.lex as lex
import core.ply.yacc as yacc
from core.constants import concept
from copy import deepcopy
import core.constants as const

PRINT_TO_CONSOLE = True

ERROR_MULT_VALUE = "attribute '%s' can't have multiple values"
ERROR_INVALID_ATTR_PAR = "'%s' is an invalid attribute value"
ERROR_INVALID_ATTR = "'%s' is an invalid attribute"

# Compute column.
#     input is the input text string
#     token is a token instance
def find_column(lexpos):
    global text
    last_cr = text.rfind('\n',0,lexpos)
    if last_cr < 0:
        last_cr = 0
    column = (lexpos - last_cr)
    return column

def print_error(line, col, errmsg):
    global path
    print("-"*80)
    print("File '%s', line %d, column %d" % (path, line, col))
    print(" "*5, "CWS ERROR:", errmsg)
    print("-"*80)

class CWSSyntaxError(SyntaxError):
    def __init__(self, errmsg, p, n, s):
        global PRINT_TO_CONSOLE
        if PRINT_TO_CONSOLE:
            print_error(p.lineno(n), find_column(p.lexpos(n)), errmsg % s)
        SyntaxError.__init__(self)


tokens = [
    'IDENTIFIER',
    'DCOLON',
    "STRING",
    "NUMBER",
    "NEWLINE",
    "TRANSCR",
    "FLOAT",

    #"ERROR_STRING",
    "ERROR_IDENTIFIER_NUM",
    "ERROR_IDENTIFIER_HYPH",
    "ERROR_IDENTIFIER_NUM_HYPH",
]

# Tokens

literals = ['{', '}', ':', ';', ',', '[', ']']

t_ignore = " \t"
t_TRANSCR = r"\[[^\[\]]+\]"
t_IDENTIFIER = r"[a-zA-Z_][-a-zA-Z_0-9]*"
t_DCOLON = r"::"
t_STRING = r'\"([^\\\n]|(\\.))*?\"'

ident_hyph_suff = '''[a-zA-Z0-9]*
        ((-[a-zA-Z0-9]+)|(-{2,}[a-zA-Z0-9]+))*
        (-{2,}[a-zA-Z0-9]+)+
        (-[a-zA-Z0-9]+)*'''
t_ERROR_IDENTIFIER_NUM = r"[-0-9]+[a-zA-Z0-9]*([a-zA-Z]+|(-[a-zA-Z0-9]+)+)"
t_ERROR_IDENTIFIER_HYPH = r'[a-zA-Z]' + ident_hyph_suff
t_ERROR_IDENTIFIER_NUM_HYPH = r"[-0-9]+" + ident_hyph_suff
#t_ERROR_STRING = r'\"([^\\\n\"]|(\\.))+'

def t_FLOAT(t):
    '''(0\.[0-9]{1,4}|1\.0)'''
    t.value = float(t.value)
    return t

def t_NEWLINE(t):
    r'(\#.*)?\n'
    t.lexer.lineno += 1
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Error handling rule
def t_error(t):
    #t.lexer.skip(1)
    if PRINT_TO_CONSOLE:
        try:
            print_error(-1, -1, "Illegal character '%s'" % t.value[0])
        except UnicodeEncodeError:
            print_error(-1, -1, "Illegal character")
    raise Exception()



precedence = (
    ('left', 'NEWLINE'),
    ('right',
        'IDENTIFIER',
        'FLOAT',
        "ERROR_IDENTIFIER_NUM",
        "ERROR_IDENTIFIER_HYPH",
        "ERROR_IDENTIFIER_NUM_HYPH",),
        #"ERROR_STRING"),
    ('right', '{'),
    ('right', '}'),
)

lexer = lex.lex()


# Parsing rules

def p_whole(p):
    '''whole : one_whole
             | nl_whole'''
    p[0] = p[1]

def p_one_whole(p):
    '''one_whole : records'''
    p[0] = p[1]

def p_nl_whole(p):
    '''nl_whole : newlines records'''
    p[0] = p[2]

def p_records(p):
    '''records : one_record
               | few_records'''
    p[0] = p[1]

def fill_dm(dictionary, meanings, tokens):
    for token in tokens:
        if token.text[0] in dictionary:
            dictionary[token.text[0]] += [token]
        else:
            dictionary[token.text[0]] = [token]
        if token.meaning != None:
            if token.meaning in meanings: #maybe do it in the end of the method
                meanings[token.meaning] += [token]
            else:
                meanings[token.meaning] = [token]
    return (dictionary, meanings)

def p_one_record(p):
    '''one_record : record'''
    dictionary = {}
    meanings = {}
    p[0] = fill_dm(dictionary, meanings, p[1])

def p_few_records(p):
    '''few_records : records record'''
    p[0] = fill_dm(p[1][0], p[1][1], p[2])

def y(n, props):
    w = deepcopy(n)
    #w.text = w.text[:-1] + [w.text[-1][:-2]]
    #w.transcription = to_ipa(tr, w.text)
    b = False
    #print(props)
    for p, v in props:
        if p == concept["text"]:
            b = True
            w.text[-1] = modif_text(v, w.text[-1])
        elif p == concept["transcription"]:
            b = False
            #print(w.transcription)
            w.transcription[-1] = modif_text(v, w.transcription[-1])
        elif p == concept["lemma"]:
            b = False
            w.meaning = modif_text(v, w.meaning)
        else:
            w.attr(p, v)
    global to_ipa
    if b: w.transcription = to_ipa(w.text)
    return [w]

funcs = {}

def modify_token(function_name, word):
    global funcs
    words = []
    #if not function_name in funcs:
    #   print(funcs.keys())
    for ff in funcs[function_name]:
        words += y(word, ff)
    return words

def modif_text(pattern, text):
    if pattern.find("|") != -1:
        left, right = pattern.split("|")
        text = modif_text(left, text)
        text = modif_text(right, text)
        return text

    if pattern.find(">") != -1:
        n, wo = pattern.split(">")
        #print(pattern, text)
        temp = text if n == "0" else text[:-int(n)]
        if len(wo) > 1 and wo[0] == ":":
            if temp[-1] == "y":
                temp = temp[:-1] + temp[-2] + temp[-1]
            else:
                temp += temp[-1]
            wo = wo[1:]
        return temp + wo
    if pattern.find("<") != -1:
        wo, n = pattern.split("<")
        temp = text[int(n):]
        return wo + temp
    return pattern

def modify_base(name, tomod, base):
    global funcs
    for pr in funcs[base]:
        n = deepcopy(tomod)
        pattern = None
        for p in pr:
            if p[0] != concept["text"]:
                for j in range(len(n)):
                    if n[j][0] == p[0]:
                        del n[j]
                        break
                n += [p]
            else:
                pattern = p[1]
        if not pattern is None:
            for j in range(len(n)):
                if n[j][0] == concept["text"]:
                    text = n[j][1]
                    if text.find(">") != -1 and pattern.find("<") != -1:
                        n[j] = (n[j][0], pattern + "|" + text)
                    elif text.find("<") != -1 and pattern.find(">") != -1:
                        n[j] = (n[j][0], text + "|" + pattern)
                    else:
                        n[j] = (n[j][0], modif_text(pattern, text))
                    break
            else:
                n += [(concept["text"], pattern)]
        if name in funcs.keys():
            funcs[name] += [n]
        else:
            funcs[name] = [n]

def attr_to_dict(l):
    d = {}
    for key, value in l:
        d[key] = value
    return d

def p_record(p):
    '''record : header newlines "{" newlines attributes "}" newlines
              | header newlines "{" newlines "}" newlines'''
    global funcs
    p[0] = []
    header = p[1]
    attributes = p[5] if len(p) == 8 else [[]]
    #print(p[1])
    for name, base in header:
        #print(len(name[0]), name[0][0])
        is_word, nme, ipa = name
        if is_word:
            for attr in attributes:
                if not base is None:
                    tok = Token(None, 0, 0)
                    tok._attrs = attr_to_dict(attr)
                    if not ipa is None:
                        tok.attr(concept['transcription'], ipa)
                    if not tok.attr(concept['transcription']) is None:
                        tok.attr(concept['transcription'], [tok.attr(concept['transcription'])])
                    tok.text = [nme]
                    p[0] += modify_token(base, tok)
                else:
                    tok = Token(None, 0, 0)
                    tok._attrs = attr_to_dict(attr)
                    if not ipa is None:
                        tok.attr(concept['transcription'], ipa)
                    if not tok.attr(concept['transcription']) is None:
                        tok.attr(concept['transcription'], [tok.attr(concept['transcription'])])
                    tok.text = [nme]
                    p[0] += [tok]
        else:
            #print(nme)
            if not ipa is None:
                raise Exception()
            for attr in attributes:
                if not base is None:
                    modify_base(nme, attr, base)
                elif attr != []:
                    if nme in funcs.keys():
                        funcs[nme] += [attr]
                    else:
                        funcs[nme] = [attr]

#-------------------------------------------------------------------------------
# Identifiers
#-------------------------------------------------------------------------------

def p_identifier(p):
    '''identifier : prop_identifier
                  | error_ident'''
    p[0] = p[1]
    
def p_prop_identifier(p):
    '''prop_identifier : IDENTIFIER'''
    p[0] = p[1]

def p_error_ident(p):
    '''error_ident : error_ident_num
                   | error_ident_hyph
                   | error_ident_num_hyph'''

def p_error_ident_num(p):
    '''error_ident_num : ERROR_IDENTIFIER_NUM'''
    raise AtnlSyntaxError(ERROR_INVALID_IDENT_NUM, p, 1, p[1])

def p_error_ident_hyph(p):
    '''error_ident_hyph : ERROR_IDENTIFIER_HYPH'''
    raise AtnlSyntaxError(ERROR_INVALID_IDENT_HYPH, p, 1, p[1])

def p_error_ident_num_hyph(p):
    '''error_ident_num_hyph : ERROR_IDENTIFIER_NUM_HYPH'''
    raise AtnlSyntaxError(ERROR_INVALID_IDENT_NUM_HYPH, p, 1, p[1])

#-------------------------------------------------------------------------------

#reqion header
def p_header(p):
    '''header : simple_header
              | full_header'''
    p[0] = p[1]

def p_simple_header(p):
    '''simple_header : words'''
    p[0] = [(w, None) for w in p[1]]

def p_full_header(p):
    '''full_header : words DCOLON base_tokens'''
    p[0] = [(w, bt) for bt in [None] + p[3] for w in p[1]]
#endregion

def p_words(p):
    '''words : word
             | few_words'''
    p[0] = p[1]

def p_few_words(p):
    '''few_words : words ";" word'''
    p[0] = p[1] + p[3]

def p_word(p):
    '''word : word_txt
            | word_txtipa
            | identifier_head'''
    p[0] = [p[1]]

def p_identifier_head(p):
    '''identifier_head : identifier'''
    p[0] = (False, p[1], None)

def p_word_txt(p):
    '''word_txt : STRING'''
    p[0] = (True, p[1][1:-1], None)

def p_word_txtipa(p):
    '''word_txtipa : STRING TRANSCR'''
    p[0] = (True, p[1][1:-1], p[2][1:-1])

# string sequences region
def p_strings(p):
    '''strings : one_string
               | few_strings'''
    p[0] = p[1]

def p_one_string(p):
    '''one_string : STRING'''
    p[0] = [p[1][1:-1]]

def p_few_strings(p):
    '''few_strings : strings ";" STRING'''
    p[0] = p[1] + [p[3][1:-1]]
# string sequences endregion

#region base tokens
def p_base_tokens(p):
    '''base_tokens : base_token
                   | few_base_tokens'''
    p[0] = p[1]

def p_base_token(p):
    '''base_token : identifier'''
    p[0] = [p[1]]

def p_few_base_tokens(p):
    '''few_base_tokens : base_tokens ";" identifier'''
    p[0] = p[1] + [p[3]]
#endregion

def p_sem_identifiers(p):
    '''sem_identifiers : one_sem_identifier
                       | few_sem_identifiers'''
    p[0] = p[1]

def p_one_sem_identifier(p):
    '''one_sem_identifier : com_identifiers'''
    p[0] = [p[1]]

def p_few_sem_identifiers(p):
    '''few_sem_identifiers : sem_identifiers ";" com_identifiers'''
    p[0] = p[1] + [p[3]]

def p_com_identifiers(p):
    '''com_identifiers : one_com_ident
                       | few_com_ident'''
    p[0] = p[1]

def p_one_com_ident(p):
    '''one_com_ident : identifier'''
    p[0] = [p[1]]

def p_few_com_ident(p):
    '''few_com_ident : com_identifiers "," identifier'''
    p[0] = p[1] + [p[3]]

#region attributes
def p_attributes(p):
    '''attributes : one_attribute
                  | few_attributes'''
    p[0] = p[1]

def p_one_attribute(p):
    '''one_attribute : attribute'''
    p[0] = [p[1]]
    
def p_few_attributes(p):
    '''few_attributes : attributes attribute'''
    #p[0] = p[1] + [p[2]]
    p[0] = []
    for head in p[1]:
        for end in p[2]:
            p[0] += [head + [end]]
#endregion attributes

def p_attribute(p):
    '''attribute : attr_ident
                 | attr_str
                 | attr_numb
                 | attr_float'''
    p[0] = p[1]

def p_attr_ident(p):
    '''attr_ident : identifier ":" sem_identifiers newlines'''
    if not p[1] in concept:
        error_text = ERROR_INVALID_ATTR + ".\nValid attributes are: " + ', '.join(concept.keys()) + "."
        raise CWSSyntaxError(error_text, p, 1, p[1])
    p[0] = []
    for item in p[3]:
        if len(item) > 1 and concept[p[1]] != concept['tags']:
            raise CWSSyntaxError(ERROR_MULT_VALUE, p, 1, p[1])
        else:
            val = item[0]
        if val == 'true':
            p[0] += [(concept[p[1]], True)]
        elif val == 'false':
            p[0] += [(concept[p[1]], False)]
        else:
            pd = const.__dict__[p[1].replace("-", "_")]
            if not val in pd:
                error_text = ERROR_INVALID_ATTR_PAR + ".\nValid values are: " + ', '.join(pd.keys()) + "."
                raise CWSSyntaxError(error_text, p, 3, val)
            p[0] += [(concept[p[1]], pd[val])]

def p_attr_str(p):
    '''attr_str : identifier ":" strings newlines'''
    if not p[1] in concept:
        raise CWSSyntaxError(ERROR_INVALID_ATTR, p, 1, p[1])
    if len(p[3]) > 1:
        raise CWSSyntaxError(ERROR_MULT_VALUE, p, 1, p[1])
    else:
        val = p[3][0]
    p[0] = [(concept[p[1]], val)]

def p_attr_float(p):
    '''attr_float : identifier ":" FLOAT newlines'''
    if not p[1] in concept:
        raise AtnlSyntaxError(ERROR_INVALID_ATTR, p, 1, p[1])
    p[0] = [(concept[p[1]], p[3])]

#region attr_number
def p_attr_numb(p):
    '''attr_numb : identifier ":" numbers newlines'''
    if not p[1] in concept:
        raise CWSSyntaxError(ERROR_INVALID_ATTR, p, 1, p[1])
    if len(p[3]) > 1:
        raise CWSSyntaxError(ERROR_MULT_VALUE, p, 1, p[1])
    else:
        val = p[3][0]
    p[0] = [(concept[p[1]], val)]

def p_numbers(p):
    '''numbers : one_number
               | few_numbers'''
    p[0] = p[1]

def p_one_number(p):
    '''one_number : NUMBER'''
    p[0] = [p[1]]

def p_few_numbers(p):
    '''few_numbers : numbers ";" NUMBER'''
    p[0] = p[1] + [p[2]]
#endregion

def p_error(p):
    global PRINT_TO_CONSOLE
    if PRINT_TO_CONSOLE:
        try:
            if not p is None:
                print_error(p.lineno, find_column(p.lexpos), "Syntax error at '%s'" % p.value)
                global text
                print(text)
            else:
                print_error(-1, -1, "Syntax error")
        except UnicodeEncodeError:
            print_error(p.lineno, find_column(p.lexpos), "Syntax error")
    raise Exception()

def p_newlines(p):
    '''newlines : NEWLINE
                | newlines NEWLINE'''

yaccer = yacc.yacc()

path = None

def _parse_text(s, print_to_console):
    global PRINT_TO_CONSOLE
    PRINT_TO_CONSOLE = print_to_console

    global text
    text = s
    lexer.lineno = 1
    res = None
    try:
        res = yaccer.parse(s, lexer=lexer, tracking=PRINT_TO_CONSOLE)
    except Exception:
        if PRINT_TO_CONSOLE:
            print("WARNING: internal CWS compiler error")
        return None
    return res

def parse(s, print_to_console):
    global path
    path = None
    return _parse_text(s, print_to_console)

def _read_file(file_path):
    try:
        f = open(file_path, encoding = 'utf-8')
        s = [x.split('#')[0].strip() for x in f.readlines()]
        i = 0
        while i < len(s):
            if len(s[i]) == 0:
                del s[i]
            elif s[i][-1] != '\\':
                i += 1
            else:
                s[i] = s[i][:-1] + ' ' + s[i + 1]
                del s[i + 1]
    except IOError:
        print("can't open file '" + os.path.join(self.path, file_path) + "'")
    finally:
        f.close()
    return s

def _parse_file(_path, print_to_console=True):
    global path
    path = _path
    f = _read_file(path)
    #print(f)
    lines = []
    for line in f:
        lines += [line] if line.find(':-') == -1 else ["\n" + line]
    s = "\n".join(lines) + "\n" ##
    #print(s)
    return _parse_text(s, print_to_console)

to_ipa = None

def parse_file(_path, _to_ipa, print_to_console=True):
    global funcs, to_ipa
    funcs = {}
    to_ipa = _to_ipa
    return _parse_file(_path, print_to_console)

def update_dict(c, b):
    a = deepcopy(c)
    for key in b:
        if key in a:
            a[key] += b[key] if type(b[key]) == list else [b[key]]
        else:
            a[key] = b[key] if type(b[key]) == list else [b[key]]
    return a

def parse_files(pathes, _to_ipa, print_to_console=True):
    global funcs, to_ipa
    funcs = {}
    to_ipa = _to_ipa
    vocabulary, meanings = {}, {}
    for path in pathes:
        #print(path)
        tmp = _parse_file(path, print_to_console)
        vocabulary = update_dict(vocabulary, tmp[0])
        meanings = update_dict(meanings, tmp[1])
    return vocabulary, meanings