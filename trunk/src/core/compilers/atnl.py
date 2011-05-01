#-------------------------------------------------------------------------------
# ATNL - an Augmented Transition Network Language (v0.1)
#-------------------------------------------------------------------------------
__author__="zoltan kochan"
__date__ ="$6 бер 2011 1:32:14$"
#quenya Quenya (qenya)
import core.ply.lex as lex
import core.ply.yacc as yacc
from core.constants import concept
import core.constants as const
from core.compilers.gener_tools import add_to_lorr, add_to_blocks, return_parent
from core.compilers.gener_tools import any_sequence, unite, straight_sequences, with_conj, finish_atn

PRINT_TO_CONSOLE = True

# Constants
ATN_LABEL = 0
ATN_FUNCTION = 1
ATN_COEFF = 2
ATN_NEXT = 3

MAXOP = 3

# Error messages
ERROR_INVALID_ATTACH = "'%s' is an invalid attachment attribute"
ERROR_INVALID_ATTR = "'%s' is an invalid attribute"
ERROR_INVALID_ATTR_PAR = "'%s' is an invalid attribute value"
ERROR_INVALID_RULE_NAME = "'%s' is an invalid rule name"
ERROR_INVALID_TYPE = "'%s' is an invalid type"
ERROR_INVALID_IDENT_NUM = "'%s' is an invalid identifier. An identifier should start with a letter of the latin alphabet"
ERROR_INVALID_IDENT_HYPH = "'%s' is an invalid identifier. An identifier can't contain hyphen sequences"
ERROR_INVALID_IDENT_NUM_HYPH = "'%s' is an invalid identifier. An identifier should start with a letter of the latin alphabet and can't contain hyphen sequences"
ERROR_INVALID_STRING = "'%s' is an invalid string. String should have a closing \""
ERROR_CONJ = "'%s' already is a conjunction structure"
ERROR_CONJ_SUB = "a conjunction structure rule should consist of one element which is '%s'"

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
    print(" "*5, "ATNL ERROR:", errmsg)
    print("-"*80)

class AtnlSyntaxError(SyntaxError):
    def __init__(self, errmsg, p, n, s):
        global PRINT_TO_CONSOLE
        if PRINT_TO_CONSOLE:
            #if not path is None:
            print_error(p.lineno(n), find_column(p.lexpos(n)), errmsg % s)
            #else:
            #    errmsg = "line %d, col %d: " + errmsg
            #    print(errmsg % (p.lineno(n), find_column(p.lexpos(n)), s))
        SyntaxError.__init__(self)

tokens = [
    'CONJ_IDENTIFIER',
    'DOLLAR_IDENTIFIER',
    'DOLLAR_DOT_IDENTIFIER',
    'DOT_IDENTIFIER',
    'IDENTIFIER',
    'ARROW',
    "STRING",
    "ASSIGN_RULE",
    "ASSIGN_CONST",
    "LANY",
    "RANY",
    "FLOAT",
    "ASSIGN_PRIOR",

    "ERROR_STRING",
    "ERROR_IDENTIFIER_NUM",
    "ERROR_IDENTIFIER_HYPH",
    "ERROR_IDENTIFIER_NUM_HYPH",
]

# Tokens

literals = [',', '(', ')', ':', '{', '}', '|', ';', '<', '>', '[', ']', '&']

LANY = "("
RANY = ")"

ident = "[a-zA-Z][a-zA-Z0-9]*(-[a-zA-Z0-9]+)*"
t_ignore = " \t"
t_CONJ_IDENTIFIER       = r"&" + ident
t_DOLLAR_IDENTIFIER     = r"\$" + ident
t_DOT_IDENTIFIER        = r"\." + ident
t_DOLLAR_DOT_IDENTIFIER = r"\$\." + ident
t_IDENTIFIER            = r"" + ident
t_STRING = r'\"([^\\\n]|(\\.))*?\"'
t_ARROW = r"->"
t_ASSIGN_RULE = r":-"
t_ASSIGN_CONST = r":="
t_ASSIGN_PRIOR = r"::="
t_LANY = r"\("
t_RANY = r"\)"

ident_hyph_suff = '''[a-zA-Z0-9]*
        ((-[a-zA-Z0-9]+)|(-{2,}[a-zA-Z0-9]+))*
        (-{2,}[a-zA-Z0-9]+)+
        (-[a-zA-Z0-9]+)*'''
t_ERROR_IDENTIFIER_NUM = r"[-0-9]+[a-zA-Z0-9]*([a-zA-Z]+|(-[a-zA-Z0-9]+)+)"
t_ERROR_IDENTIFIER_HYPH = r'[a-zA-Z]' + ident_hyph_suff
t_ERROR_IDENTIFIER_NUM_HYPH = r"[-0-9]+" + ident_hyph_suff
t_ERROR_STRING = r'\"([^\\\n\"]|(\\.))+'

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

# Error handling rule
def t_error(t):
    t.lexer.skip(1)
    if not PRINT_TO_CONSOLE: return
    try:
        print_error(-1, -1, "Illegal character '%s'" % t.value[0])
    except UnicodeEncodeError:
        print_error(-1, -1, "Illegal character")

precedence = (
    ('right',
        'CONJ_IDENTIFIER',
        'DOLLAR_IDENTIFIER',
        'DOLLAR_DOT_IDENTIFIER',
        'DOT_IDENTIFIER',
        'IDENTIFIER',
        "ERROR_IDENTIFIER_NUM",
        "ERROR_IDENTIFIER_HYPH",
        "ERROR_IDENTIFIER_NUM_HYPH",
        "ERROR_STRING"),
    ('right', '<'),
    ('right', '{'),
    ('left', ','),
    ('left', 'ARROW'),
    ('left', ':'),
)

lexer = lex.lex()

# Parsing rules
atn = {}
prior = {}
d = {}
label = ""
consts = {}
label_types = {}

def p_rules(p):
    '''rules : rule
             | assignment
             | priority
             | is_type
             | rules rule
             | rules assignment
             | rules priority
             | rules is_type'''

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
# String
#-------------------------------------------------------------------------------

def p_string(p):
    '''string : proper_string
              | invalid_string'''
    p[0] = p[1]

def p_proper_string(p):
    '''proper_string : STRING'''
    p[0] = p[1][1:-1]

def p_invalid_string(p):
    '''invalid_string : ERROR_STRING'''
    raise AtnlSyntaxError(ERROR_INVALID_STRING, p, 1, p[1])

#-------------------------------------------------------------------------------
# is_type rules
#-------------------------------------------------------------------------------
def p_is_type(p):
    '''is_type : identifier identifier rule_name_simple ";"
               | identifier identifier rule_name_complex ";"'''
    if p[2] != 'is':
        AtnlSyntaxError("'%s' is an invalid keyword", p, 2, p[2])
    global label_types, standard_attr
    label_types[p[1]], standard_attr[p[1]] = p[3]

def p_rule_name_simple(p):
    '''rule_name_simple : identifier'''
    if not p[1] in const.type:
        AtnlSyntaxError(ERROR_INVALID_TYPE, p, 1, p[1])
    p[0] = (const.type[p[1]], [])

def p_rule_name_complex(p):
    '''rule_name_complex : identifier "{" attributes "}"'''
    if not p[1] in const.type:
        AtnlSyntaxError(ERROR_INVALID_TYPE, p, 1, p[1])
    p[0] = (const.type[p[1]], p[3])

#-------------------------------------------------------------------------------
# Priority rules
#-------------------------------------------------------------------------------
def p_priority(p):
    '''priority : priority_header priority_expressions ";"'''
    global prior
    prior = update_dict(prior, {p[1]: p[2]})

def p_priority_header(p):
    '''priority_header : identifier ASSIGN_PRIOR'''
    p[0] = p[1]

def p_priority_expressions(p):
    '''priority_expressions : priority_expression_single
                            | priority_expression_few'''
    p[0] = p[1]

def p_priority_expression_single(p):
    '''priority_expression_single : priority_expression'''
    p[0] = [p[1]]

def p_priority_expression_few(p):
    '''priority_expression_few : priority_expressions priority_expression_single'''
    p[0] = p[1] + p[2]

def p_priority_expression(p):
    '''priority_expression : FLOAT ":" identifiers'''
    p[0] = (p[1], p[3])

def p_identifiers(p):
    '''identifiers : idents_all
                   | ident_clue'''
    p[0] = p[1]

def p_ident_all(p):
    '''idents_all : ident
              | dot_ident'''
    p[0] = p[1]

def p_ident(p):
    '''ident : identifier'''
    p[0] = [p[1]]

def p_dot_ident(p):
    '''dot_ident : DOT_IDENTIFIER'''
    p[0] = [p[1][1:]+":empty"]
    
def p_ident_clue(p):
    '''ident_clue : identifiers idents_all'''
    p[0] = p[1] + p[2]

#-------------------------------------------------------------------------------
# Constant rules
#-------------------------------------------------------------------------------
def p_assignment(p):
    '''assignment : identifier ASSIGN_CONST attaches ";"'''
    global consts
    consts[p[1]] = p[3]

#-------------------------------------------------------------------------------
#Grammar rules
#-------------------------------------------------------------------------------
def add_up_attributes(rp, terms):
    if not rp[1] is None:
        new = []
        for item in terms[const.STATE_START]:
            if item[1] is None:
                new += [(item[0], dict(f = return_parent, up = rp[1]), item[2], item[3])]
            else:
                new += [(item[0], dict(f = item[1], up = rp[1]), item[2], item[3])]
        terms[const.STATE_START] = new
    return terms

def p_rule(p):
    '''rule : full_rule ";"
            | conj_rule ";"'''
    p[0] = p[1]

def p_conj_rule(p):
    '''conj_rule : CONJ_IDENTIFIER ASSIGN_RULE conj_sub'''
    label = p[1][1:]
    global atn
    if const.STATE_CONJ_A1 in atn[label]:
        raise AtnlSyntaxError(ERROR_CONJ, p, 1, label)
    if p[3][0] != label:
        raise AtnlSyntaxError(ERROR_CONJ_SUB, p, 1, label)
    atn[label] = with_conj(label, p[3][1], atn[label])

def p_conj_sub(p):
    '''conj_sub : DOLLAR_IDENTIFIER "<" attaches ">"'''
    p[0] = (p[1][1:], p[3])

def p_full_rule(p):
    '''full_rule : rule_params ASSIGN_RULE terms'''
    global atn
    pars = p[1]
    terms = add_up_attributes(pars, p[3])
    label = pars[0]
    if label in atn:
        atn[label] = unite(atn[label], terms)
    else:
        atn[label] = terms

def p_rule_params(p):
    '''rule_params : rule_params_empty
                   | rule_params_simple
                   | rule_params_complex_empty
                   | rule_params_complex'''
    p[0] = p[1]

def p_rule_params_empty(p):
    '''rule_params_empty : DOT_IDENTIFIER'''
    global label_types
    if not p[1][1:] in label_types:
        raise AtnlSyntaxError(ERROR_INVALID_RULE_NAME, p, 1, p[1][1:])
    p[0] = (p[1][1:]+":empty", None)

def p_rule_params_simple(p):
    '''rule_params_simple : identifier'''
    global label_types
    if not p[1] in label_types:
        raise AtnlSyntaxError(ERROR_INVALID_RULE_NAME, p, 1, p[1])
    p[0] = (p[1], None)

def p_rule_params_complex_empty(p):
    '''rule_params_complex_empty : DOT_IDENTIFIER "{" attributes "}"'''
    global label_types
    if not p[1][1:] in label_types:
        raise AtnlSyntaxError(ERROR_INVALID_RULE_NAME, p, 1, p[1][1:])
    p[0] = (p[1][1:]+":empty", p[3])

def p_rule_params_complex(p):
    '''rule_params_complex : identifier "{" attributes "}"'''
    global label_types
    if not p[1] in label_types:
        raise AtnlSyntaxError(ERROR_INVALID_RULE_NAME, p, 1, p[1])
    p[0] = (p[1], p[3])

def contains_jump(lst, curr, is_last):
    for item in lst:
        if item[ATN_LABEL] != "JMP": continue
        if item[ATN_NEXT] != curr + 1 and \
            (not is_last or item[ATN_NEXT] != const.STATE_END):
            raise Exception('In ANY only single elements could be optional')
        return True
    return False

def div_to_op(seq):
    a, b = [], []
    i = 0
    for item in seq:
        i += 1
        if contains_jump(seq[item], item, i == len(seq)):
            b += [seq[item]]
        else:
            a += [seq[item]]
    return a, b



def concat(a, b):
    '''Adds a way to the end.'''
    last = max(a.keys())
    next = last + 1
    new = []
    for item in a[last]:
        if item[ATN_NEXT] != const.STATE_END:
            raise Exception()
        else:
            new += [(item[0], item[1], item[2], next)]
    a[last] = new
    if type(b) == dict:
        for key in b:
            nont = []
            for item in b[key]:
                if item[3] == const.STATE_END:
                    nont += [item]
                else:
                    nont += [(item[0], item[1], item[2], item[3] + last)]
            a[key + last] = nont
    else:
        if type(b) == tuple:
            b = [b]
        a[next] = [(item[0], item[1], 0.0, const.STATE_END) for item in b]
    return a

def addjump(dc):
    dc[min(dc.keys())] += [('JMP', None, 0.0, const.STATE_END)]

def p_terms(p):
    '''terms : term_1
             | terms_clue'''
    p[0] = p[1]

def p_term_1(p):
    '''term_1 : term_str
              | terms_not_required
              | terms_any'''
    p[0] = p[1]

def p_terms_clue(p):
    '''terms_clue : terms term_1'''
    p[0] = concat(p[1], p[2])

def p_terms_not_required(p):
    '''terms_not_required : "[" terms "]"'''
    addjump(p[2])
    p[0] = p[2]

def p_terms_any(p):
    '''terms_any : LANY terms RANY'''
    ob, op = div_to_op(p[2])
    p[0] = any_sequence(ob, op, MAXOP)

def p_term_str(p):
    '''term_str : term'''
    p[0] = straight_sequences([[[p[1]]]])

def p_term(p):
    '''term : ling_unit
            | ling_unit_attaches
            | ling_unit_attr
            | ling_unit_comlex'''
    p[0] = p[1]

def p_ling_unit(p):
    '''ling_unit : term_name'''
    global standard_attr
    p[0] = (p[1][0], dict(f = p[1][1], down = standard_attr[root_label(p[1][0])]))

def p_ling_unit_attaches(p):
    '''ling_unit_attaches : term_name "<" attaches ">"'''
    global standard_attr
    func = dict(f = p[1][1], attach = p[3].get('attach', []), fixed = p[3].get('fixed', []), down = standard_attr[root_label(p[1][0])])
    p[0] = (p[1][0], func)

def p_ling_unit_attr(p):
    '''ling_unit_attr : term_name "{" attributes "}"'''
    global standard_attr
    p[0] = (p[1][0], dict(f = p[1][1], down = p[3] + standard_attr[root_label(p[1][0])]))
    
def p_ling_unit_comlex(p):
    '''ling_unit_comlex : term_name "<" attaches ">" "{" attributes "}"'''
    global standard_attr
    func = dict(f = p[1][1], attach = p[3].get('attach', []), fixed = p[3].get('fixed', []), down = p[6] + standard_attr[root_label(p[1][0])])
    p[0] = (p[1][0], func)

def p_term_name(p):
    '''term_name : term_name_main
                 | term_name_child
                 | term_name_empty
                 | term_name_empty_main'''
    p[0] = p[1]

def p_term_name_main(p):
    '''term_name_main : DOLLAR_IDENTIFIER'''
    global label_types
    if not p[1][1:] in label_types:
        raise AtnlSyntaxError(ERROR_INVALID_RULE_NAME, p, 1, p[1][1:])
    p[0] = (p[1][1:], add_to_blocks)

def p_term_name_child(p):
    '''term_name_child : identifier'''
    global label_types
    if not p[1] in label_types:
        raise AtnlSyntaxError(ERROR_INVALID_RULE_NAME, p, 1, p[1])
    p[0] = (p[1], add_to_lorr)

def p_term_name_empty(p):
    '''term_name_empty : DOT_IDENTIFIER'''
    global label_types
    if not p[1][1:] in label_types:
        raise AtnlSyntaxError(ERROR_INVALID_RULE_NAME, p, 1, p[1][1:])
    p[0] = (p[1][1:]+':empty', add_to_lorr)

def p_term_name_empty_main(p):
    '''term_name_empty_main : DOLLAR_DOT_IDENTIFIER'''
    global label_types
    if not p[1][2:] in label_types:
        raise AtnlSyntaxError(ERROR_INVALID_RULE_NAME, p, 1, p[1][2:])
    p[0] = (p[1][2:]+':empty', add_to_blocks)



def p_attributes(p):
    '''attributes : attribute
                  | attribute_clue'''
    p[0] = p[1]

def p_attribute_clue(p):
    '''attribute_clue : attributes ";" attribute'''
    p[0] = p[1] + p[3]

def p_attribute(p):
    '''attribute : attr_ident
                 | attr_str
                 | attr_float'''
    p[0] = [p[1]]

def p_attr_ident(p):
    '''attr_ident : identifier ":" identifier'''
    if not p[1] in concept:
        raise AtnlSyntaxError(ERROR_INVALID_ATTR, p, 1, p[1])
    if p[3] == 'true':
        p[0] = (concept[p[1]], True)
    elif p[3] == 'false':
        p[0] = (concept[p[1]], False)
    else:
        pd = const.__dict__[p[1].replace("-", "_")]
        if not p[3] in pd:
            raise AtnlSyntaxError(ERROR_INVALID_ATTR_PAR, p, 3, p[3])
        p[0] = (concept[p[1]], pd[p[3]])

def p_attr_str(p):
    '''attr_str : identifier ":" string'''
    if not p[1] in concept:
        raise AtnlSyntaxError(ERROR_INVALID_ATTR, p, 1, p[1])
    p[0] = (concept[p[1]], p[3])

def p_attr_float(p):
    '''attr_float : identifier ":" FLOAT'''
    if not p[1] in concept:
        raise AtnlSyntaxError(ERROR_INVALID_ATTR, p, 1, p[1])
    p[0] = (concept[p[1]], p[3])

import copy

def update_dict(c, b):
    '''Unites two dictionaries'''
    if c is None: return b
    if b is None: return c
    a = copy.deepcopy(c)
    for key in b:
        if key in a:
            a[key] += b[key] if type(b[key]) == list else [b[key]]
        else:
            a[key] = b[key] if type(b[key]) == list else [b[key]]
    return a

def p_attaches(p):
    '''attaches : pair
                | attaches_clue'''
    p[0] = p[1]

def p_attaches_clue(p):
    '''attaches_clue : attaches "," pair'''
    p[0] = update_dict(p[1], p[3])

def p_pair(p):
    '''pair : pair_complex_attached
            | pair_complex_fixed
            | pair_attached
            | pair_fixed'''
    p[0] = p[1]

def p_pair_attached(p):
    '''pair_attached : identifier'''
    if p[1] in consts:
        p[0] = consts[p[1]]
    else:
        if not p[1] in concept:
            raise AtnlSyntaxError(ERROR_INVALID_ATTACH, p, 1, p[1])
        p[0] = {'attach': [concept[p[1]]]}

def p_pair_fixed(p):
    '''pair_fixed : DOLLAR_IDENTIFIER'''
    if p[1][1:] in consts:
        p[0] = {'fixed': consts[p[1][1:]]['attach']}
    else:
        if not p[1][1:] in concept:
            raise AtnlSyntaxError(ERROR_INVALID_ATTACH, p, 1, p[1][1:])
        p[0] = {'fixed': [concept[p[1][1:]]]}

def p_pair_complex_attached(p):
    '''pair_complex_attached : identifier ARROW identifier'''
    if not p[1] in concept:
        raise AtnlSyntaxError(ERROR_INVALID_ATTACH, p, 1, p[1])
    if not p[3] in concept:
        raise AtnlSyntaxError(ERROR_INVALID_ATTACH, p, 3, p[3])
    p[0] = {'attach': [(concept[p[1]], concept[p[3]])]}

def p_pair_complex_fixed(p):
    '''pair_complex_fixed : DOLLAR_IDENTIFIER ARROW identifier'''
    if not p[1][1:] in concept:
        raise AtnlSyntaxError(ERROR_INVALID_ATTACH, p, 1, p[1][1:])
    if not p[3] in concept:
        raise AtnlSyntaxError(ERROR_INVALID_ATTACH, p, 3, p[3])
    p[0] = {'fixed': [(concept[p[1][1:]], concept[p[3]])]}

#-------------------------------------------------------------------------------
# Common rules
#-------------------------------------------------------------------------------

def p_error(p):
    if not PRINT_TO_CONSOLE: return
    try:
        if not p is None:
            print_error(p.lineno, find_column(p.lexpos), "Syntax error at '%s'" % p.value)
        else:
            print("Syntax error")
    except UnicodeEncodeError:
        print_error(p.lineno, 0, "Syntax error")

def search_way(patn, state, way, prior):
    if len(way) == 0: return False
    i = -1
    b = False
    for item in patn[state]:
        i += 1
        if item[0] != way[0]: continue
        if item[ATN_NEXT] == const.STATE_END:
            if len(way) == 1:
            #if len(way) == 1 and item[2] in [0.0, prior]:
                patn[state][i] = item[0], item[1], max(prior, item[2]), item[3]
                b = True
            continue
        if search_way(patn, item[ATN_NEXT], way[1:], prior):
        #if item[2] in [0.0, prior] and search_way(patn, item[ATN_NEXT], way[1:], prior):
            patn[state][i] = item[0], item[1], max(prior, item[2]), item[3]
            b = True
    return b

def add_priorities(atn, pr):
    for item in pr:
        if not item in atn:
            print(item,)
            raise Exception()
        pa = atn[item]
        for way in pr[item]:
            search_way(pa, const.STATE_START, way[1], way[0])


####################################################################
def print_interlingua(dc, c = 0):
    d = 5
    b = d*c*" "
    b1 = b + d*" "
    if type(dc) in [int, str, tuple]:
        print(b + str(dc))
        return
    print(b + "{")
    for key in dc.keys():
        if dc[key] == None: continue
        if type(dc[key]) == list:
            if key == concept["tags"]:
                print(b1 + str(key) + ":", ', '.join(dc[key]))
            else:
                for item in dc[key]:
                    print(b1 + str(key) + ":")
                    print_interlingua(item, c + 2)
        elif not type(dc[key]) in [int, str, tuple]: #isinstance(dc, dict):!!!!!!!!!!
            print(b1 + str(key) + ":")
            print_interlingua(dc[key], c + 2)
        else:
            print(b1 + str(key) + ":", dc[key])
    print(b + "}")
####################################################################

yaccer = yacc.yacc()
path = None

def root_label(label):
    return label.split(":")[0]

def gen_to_type_code():
    global label_types
    return lambda label: label_types[root_label(label)]

def _parse_text(s, print_to_console):
    global PRINT_TO_CONSOLE
    PRINT_TO_CONSOLE = print_to_console
    #global path

    global atn, text, prior, label_types, standard_attr
    atn = {}
    prior = {}
    label_types = {'JMP': const.type['epsilon'], 'CONJ': const.type['conjunction']}
    standard_attr = {}
    text = s
    lexer.lineno = 1
    try:
        yaccer.parse(s, lexer=lexer, tracking=PRINT_TO_CONSOLE)
        add_priorities(atn, prior)
        ret = finish_atn(atn, gen_to_type_code())
    except Exception:
        if PRINT_TO_CONSOLE:
            print("WARNING: internal ATNL compiler error")
        return None
    atn = ret if ret != {} else None
    if atn is None: return None
    return atn, label_types

def parse(s, print_to_console=True):
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

def parse_file(_path, print_to_console=True):
    global path
    path = _path
    return _parse_text(_read_file(path), print_to_console)