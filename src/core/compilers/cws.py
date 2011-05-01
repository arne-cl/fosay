# -----------------------------------------------------------------------------
# CWS - Cascading Word Sheets (v0.1)
# -----------------------------------------------------------------------------
__author__="Z-CORE"
__date__ ="$5 бер 2011 11:36:40$"

from core.models.ling_units import Token
import core.ply.lex as lex
import core.ply.yacc as yacc
from core.constants import concept, concept_type
from copy import deepcopy
import core.constants as const

PRINT_TO_CONSOLE = True

ERROR_MULT_VALUE = "attribute '%s' can't have multiple values"
ERROR_INVALID_ATTR_PAR = "'%s' is an invalid attribute value"
ERROR_INVALID_ATTR_PAR_TYPE = "'%s' has bad type"
ERROR_INVALID_ATTR = "'%s' is an invalid attribute"
ERROR_IMP_INHERIT_NAME = "it's impossible to inherit any name here"
ERROR_INVALID_BASE_NAME = "base '%s' doesn't exist."

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
    def __init__(self, errmsg, p, n, s=None):
        global PRINT_TO_CONSOLE
        if PRINT_TO_CONSOLE:
            if s is None:
                print_error(p.lineno(n), find_column(p.lexpos(n)), errmsg)
            else:
                print_error(p.lineno(n), find_column(p.lexpos(n)), errmsg % s)
        SyntaxError.__init__(self)


tokens = [
    'IDENTIFIER',
    'DOT_IDENTIFIER',
    'DCOLON',
    "STRING",
    "DOT_STRING",
    "NUMBER",
    "TRANSCR",
    "FLOAT",

    #"ERROR_STRING",
    "ERROR_IDENTIFIER_NUM",
    "ERROR_IDENTIFIER_HYPH",
    "ERROR_IDENTIFIER_NUM_HYPH",
]

# Tokens

literals = ['{', '}', ':', ';', ',', '[', ']', '(', ')']

t_ignore = " \t"
t_TRANSCR = r"\[[^\[\]]+\]"
t_IDENTIFIER = r"[a-zA-Z_][-a-zA-Z_0-9]*"
t_DOT_IDENTIFIER = r"\.[a-zA-Z_][-a-zA-Z_0-9]*"
t_DCOLON = r"::"
t_STRING = r'\"([^\\\n]|(\\.))*?\"'
t_DOT_STRING = r'\.\"([^\\\n]|(\\.))*?\"'

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

# Comment
def t_COMMENT(t):
    r'(/\*(.|\n)*?\*/)|(//.*?\n)'
    t.lexer.lineno += t.value.count("\n")
    pass

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

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
    '''whole : records'''
    p[0] = p[1]

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
    if w.meaning is None and not w.attr(concept['stem']) is None:
        w.meaning = w.attr(concept['stem']).rsplit('.', 1)[0]
    if not w.attr(concept['number']) is None \
        and w.attr(concept['real-number']) is None:
        w.attr(concept['real-number'], w.attr(concept['number']))
    return [w]

funcs = {}

def modify_token(base, word):
    global funcs
    words = []
    #if not function_name in funcs:
    #   print(funcs.keys())
    for ff in get_base(base):
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

def modify(obj, base):
    res = []
    global funcs
    for pr in funcs[base]:
        if pr is None: raise Exception()
        for bj in funcs[obj]:
            n = deepcopy(bj)
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
            res += [n]
    return res

def get_base(base):
    if base[1] is None: return funcs[base[0]]
    else: return modify(base[0], base[1])

def modify_base(has_dot, name, tomod, base):
    global funcs
    for pr in get_base(base):
        if pr is None and has_dot: continue
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
    '''record : header "{" attributes "}"
              | header "{" attributes ";" "}"
              | header "{" "}"'''
    global funcs
    p[0] = []
    header = p[1]
    attributes = p[3] if len(p) > 4 else [[]]
    #print(p[1])
    for name, base in header:
        #print(len(name[0]), name[0][0])
        has_dot, is_word, nme, ipa = name
        if is_word:
            for attr in attributes:
                if not base is None:
                    tok = Token(None, 0, 0)
                    tok._attrs = attr_to_dict(attr)
                    if not ipa is None:
                        tok.attr(concept['transcription'], ipa)
                    if not tok.attr(concept['transcription']) is None:
                        tok.attr(concept['transcription'], [tok.attr(concept['transcription'])])
                    if tok.meaning is None and not tok.attr(concept['stem']) is None:
                        tok.meaning = tok.attr(concept['stem']).rsplit('.', 1)[0]
                    if not tok.attr(concept['number']) is None \
                        and tok.attr(concept['real-number']) is None:
                        tok.attr(concept['real-number'], tok.attr(concept['number']))
                    tok.text = [nme]
                    p[0] += modify_token(base, tok)
                else:
                    tok = Token(None, 0, 0)
                    tok._attrs = attr_to_dict(attr)
                    if not ipa is None:
                        tok.attr(concept['transcription'], ipa)
                    if not tok.attr(concept['transcription']) is None:
                        tok.attr(concept['transcription'], [tok.attr(concept['transcription'])])
                    if tok.meaning is None and not tok.attr(concept['stem']) is None:
                        tok.meaning = tok.attr(concept['stem']).rsplit('.', 1)[0]
                    if not tok.attr(concept['number']) is None \
                        and tok.attr(concept['real-number']) is None:
                        tok.attr(concept['real-number'], tok.attr(concept['number']))
                    tok.text = [nme]
                    if not has_dot: p[0] += [tok]
        else:
            #print(nme)
            if not ipa is None:
                raise Exception()
            for attr in attributes:
                if not base is None:
                    modify_base(has_dot, nme, attr, base)
                elif not has_dot and attr != []:
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
              | full_header
              | lil_full_header'''
    p[0] = p[1]

def p_simple_header(p):
    '''simple_header : words'''
    p[0] = [(w, None) for w in p[1]]

def p_full_header(p):
    '''full_header : words DCOLON base_tokens'''
    global prev
    prev = p[1]
    p[0] = [(w, bt) for bt in [None] + p[3] for w in prev]

def p_lil_full_header(p):
    '''lil_full_header : DCOLON base_tokens'''
    global prev
    if prev is None:
        raise CWSSyntaxError(ERROR_IMP_INHERIT_NAME, p, 1)
    p[0] = [(w, bt) for bt in [None] + p[2] for w in prev]
#endregion

def p_words(p):
    '''words : word
             | few_words'''
    p[0] = p[1]

def p_few_words(p):
    '''few_words : words word'''
    p[0] = p[1] + p[2]

def p_word(p):
    '''word : word_txt
            | word_txtipa
            | identifier_head
            | dot_word_txt
            | dot_word_txtipa
            | dot_identifier_head'''
    p[0] = [p[1]]

def p_identifier_head(p):
    '''identifier_head : identifier'''
    p[0] = (False, False, p[1], None)

def p_word_txt(p):
    '''word_txt : STRING'''
    p[0] = (False, True, p[1][1:-1], None)

def p_word_txtipa(p):
    '''word_txtipa : STRING TRANSCR'''
    p[0] = (False, True, p[1][1:-1], p[2][1:-1])

def p_dot_identifier_head(p):
    '''dot_identifier_head : DOT_IDENTIFIER'''
    p[0] = (True, False, p[1][1:], None)

def p_dot_word_txt(p):
    '''dot_word_txt : DOT_STRING'''
    p[0] = (True, True, p[1][2:-1], None)

def p_dot_word_txtipa(p):
    '''dot_word_txtipa : DOT_STRING TRANSCR'''
    p[0] = (True, True, p[1][2:-1], p[2][1:-1])

# string sequences region
def p_strings(p):
    '''strings : one_string
               | few_strings'''
    p[0] = p[1]

def p_one_string(p):
    '''one_string : STRING'''
    p[0] = [p[1][1:-1]]

def p_few_strings(p):
    '''few_strings : strings STRING'''
    p[0] = p[1] + [p[2][1:-1]]
# string sequences endregion

#region base tokens
def p_base_tokens(p):
    '''base_tokens : base_token
                   | complex_base_token
                   | few_base_tokens
                   | few_complex_base_tokens'''
    p[0] = p[1]

def p_base_token(p):
    '''base_token : identifier'''
    global funcs
    if not p[1] in funcs:
        raise CWSSyntaxError(ERROR_INVALID_BASE_NAME, p, 1, p[1])
    p[0] = [(p[1], None)]

def p_complex_base_token(p):
    '''complex_base_token : identifier "(" identifier ")"'''
    global funcs
    if not p[1] in funcs:
        raise CWSSyntaxError(ERROR_INVALID_BASE_NAME, p, 1, p[1])
    if not p[3] in funcs:
        raise CWSSyntaxError(ERROR_INVALID_BASE_NAME, p, 3, p[3])
    p[0] = [(p[1], p[3])]

def p_few_base_tokens(p):
    '''few_base_tokens : base_tokens identifier'''
    global funcs
    if not p[2] in funcs:
        raise CWSSyntaxError(ERROR_INVALID_BASE_NAME, p, 2, p[2])
    p[0] = p[1] + [(p[2], None)]

def p_few_complex_base_tokens(p):
    '''few_complex_base_tokens : base_tokens identifier "(" identifier ")" '''
    global funcs
    if not p[2] in funcs:
        raise CWSSyntaxError(ERROR_INVALID_BASE_NAME, p, 2, p[2])
    if not p[4] in funcs:
        raise CWSSyntaxError(ERROR_INVALID_BASE_NAME, p, 4, p[4])
    p[0] = p[1] + [(p[2], p[4])]

def p_sem_identifiers(p):
    '''sem_identifiers : one_sem_identifier
                       | few_sem_identifiers'''
    p[0] = p[1]

def p_one_sem_identifier(p):
    '''one_sem_identifier : com_identifiers'''
    p[0] = [p[1]]

def p_few_sem_identifiers(p):
    '''few_sem_identifiers : sem_identifiers com_identifiers'''
    p[0] = p[1] + [p[2]]

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
    '''few_attributes : attributes ";" attribute'''
    #p[0] = p[1] + [p[2]]
    p[0] = []
    for head in p[1]:
        for end in p[3]:
            p[0] += [head + [end]]
#endregion attributes

def p_attribute(p):
    '''attribute : attr_ident
                 | attr_str
                 | attr_numb
                 | attr_float'''
    p[0] = p[1]

def p_attr_ident(p):
    '''attr_ident : identifier ":" sem_identifiers'''
    if not p[1] in concept:
        error_text = ERROR_INVALID_ATTR + ".\nValid attributes are: " + ', '.join(concept.keys()) + "."
        raise CWSSyntaxError(error_text, p, 1, p[1])
    p[0] = []
    for item in p[3]:
        if len(item) > 1 and concept[p[1]] != concept['tags']:
            raise CWSSyntaxError(ERROR_MULT_VALUE, p, 1, p[1])
        else:
            val = item[0]
        if val in ['true', 'false']:
            if concept_type[p[1]] != 'bool':
                raise CWSSyntaxError(ERROR_INVALID_ATTR_PAR_TYPE, p, 3, p[3])
            p[0] += [(concept[p[1]], val == 'true')]
        else:
            if concept_type[p[1]] != 'ident':
                raise CWSSyntaxError(ERROR_INVALID_ATTR_PAR_TYPE, p, 3, p[3])
            pd = const.__dict__[p[1].replace("-", "_")]
            if not val in pd:
                error_text = ERROR_INVALID_ATTR_PAR + ".\nValid values are: " + ', '.join(pd.keys()) + "."
                raise CWSSyntaxError(error_text, p, 3, val)
            p[0] += [(concept[p[1]], pd[val])]

def p_attr_str(p):
    '''attr_str : identifier ":" strings'''
    if not p[1] in concept and \
        not p[1] in ['sufix', 'prefix']:
        raise CWSSyntaxError(ERROR_INVALID_ATTR, p, 1, p[1])
    if len(p[3]) > 1:
        raise CWSSyntaxError(ERROR_MULT_VALUE, p, 1, p[1])
    else:
        val = p[3][0]
    if p[1] == 'sufix':
        val = '0>' + val
        attr = concept['text']
    elif p[1] == 'prefix':
        val = val + '<0'
        attr = concept['text']
    else:
        attr = concept[p[1]]
    if concept_type[attr] != 'str':
        raise CWSSyntaxError(ERROR_INVALID_ATTR_PAR_TYPE, p, 3, p[3])
    p[0] = [(attr, val)]

def p_attr_float(p):
    '''attr_float : identifier ":" FLOAT'''
    if not p[1] in concept:
        raise AtnlSyntaxError(ERROR_INVALID_ATTR, p, 1, p[1])
    if concept_type[p[1]] != 'float':
        raise CWSSyntaxError(ERROR_INVALID_ATTR_PAR_TYPE, p, 3, p[3])
    p[0] = [(concept[p[1]], p[3])]

#region attr_number
def p_attr_numb(p):
    '''attr_numb : identifier ":" numbers'''
    if not p[1] in concept:
        raise CWSSyntaxError(ERROR_INVALID_ATTR, p, 1, p[1])
    if len(p[3]) > 1:
        raise CWSSyntaxError(ERROR_MULT_VALUE, p, 1, p[1])
    else:
        val = p[3][0]
    if concept_type[p[1]] != 'int':
        raise CWSSyntaxError(ERROR_INVALID_ATTR_PAR_TYPE, p, 3, p[3])
    p[0] = [(concept[p[1]], val)]

def p_numbers(p):
    '''numbers : one_number
               | few_numbers'''
    p[0] = p[1]

def p_one_number(p):
    '''one_number : NUMBER'''
    p[0] = [p[1]]

def p_few_numbers(p):
    '''few_numbers : numbers NUMBER'''
    p[0] = p[1] + [p[2]]
#endregion

def p_error(p):
    global PRINT_TO_CONSOLE
    if PRINT_TO_CONSOLE:
        try:
            if not p is None:
                print_error(p.lineno, find_column(p.lexpos), "Syntax error at '%s'" % p.value)
                #global text
                #print(text)
            else:
                print_error(-1, -1, "Syntax error")
        except UnicodeEncodeError:
            print_error(p.lineno, find_column(p.lexpos), "Syntax error")
    raise Exception()

#def p_newlines(p):
#    '''newlines : NEWLINE
#                | newlines NEWLINE'''

yaccer = yacc.yacc()

path = None

def _parse_text(s, print_to_console):
    global PRINT_TO_CONSOLE
    PRINT_TO_CONSOLE = print_to_console

    global text, prev
    prev = None
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
        s = f.read()
    except IOError:
        print("can't open file '" + os.path.join(self.path, file_path) + "'")
    finally:
        f.close()
    return s

def _parse_file(_path, print_to_console=True):
    global path
    path = _path
    return _parse_text(_read_file(path), print_to_console)

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