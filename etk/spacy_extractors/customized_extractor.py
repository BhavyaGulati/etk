import spacy
import copy
import itertools
import random
import math

FLAG_DICT = {
    "18": spacy.attrs.FLAG18,
    "19": spacy.attrs.FLAG19,
    "20": spacy.attrs.FLAG20,
    "21": spacy.attrs.FLAG21,
    "22": spacy.attrs.FLAG22,
    "23": spacy.attrs.FLAG23,
    "24": spacy.attrs.FLAG24,
    "25": spacy.attrs.FLAG25,
    "26": spacy.attrs.FLAG26,
    "27": spacy.attrs.FLAG27,
    "28": spacy.attrs.FLAG28,
    "29": spacy.attrs.FLAG29,
    "30": spacy.attrs.FLAG30,
    "31": spacy.attrs.FLAG31,
    "32": spacy.attrs.FLAG32,
    "33": spacy.attrs.FLAG33,
    "34": spacy.attrs.FLAG34,
    "35": spacy.attrs.FLAG35,
    "36": spacy.attrs.FLAG36,
    "37": spacy.attrs.FLAG37,
    "38": spacy.attrs.FLAG38,
    "39": spacy.attrs.FLAG39,
    "40": spacy.attrs.FLAG40,
    "41": spacy.attrs.FLAG41,
    "42": spacy.attrs.FLAG42,
    "43": spacy.attrs.FLAG43,
    "44": spacy.attrs.FLAG44,
    "45": spacy.attrs.FLAG45,
    "46": spacy.attrs.FLAG46,
    "47": spacy.attrs.FLAG47,
    "48": spacy.attrs.FLAG48,
    "49": spacy.attrs.FLAG49,
    "50": spacy.attrs.FLAG50,
    "51": spacy.attrs.FLAG51,
    "52": spacy.attrs.FLAG52,
    "53": spacy.attrs.FLAG53,
    "54": spacy.attrs.FLAG54,
    "55": spacy.attrs.FLAG55,
    "56": spacy.attrs.FLAG56,
    "57": spacy.attrs.FLAG57,
    "58": spacy.attrs.FLAG58,
    "59": spacy.attrs.FLAG59,
    "60": spacy.attrs.FLAG60,
    "61": spacy.attrs.FLAG61,
    "62": spacy.attrs.FLAG62,
    "63": spacy.attrs.FLAG63
}

TOP_N = 5

POS_MAP = {
    "noun": "NOUN",
    "pronoun": "PROPN",
    "proper noun": "PROPN",
    "determiner": "DET",
    "symbol": "SYM",
    "adjective": "ADJ",
    "conjunction": "CONJ",
    "verb": "VERB",
    "pre/post-position": "ADP",
    "adverb": "ADV",
    "particle": "PART",
    "interjection": "INTJ",
    "X": "X",
    "NUM": "NUM",
    "SPACE": "SPACE",
    "PRON": "PRON"
}

INV_POS_MAP = {
    "NOUN": "noun",
    "PROPN": "pronoun",
    "DET": "determiner",
    "SYM": "symbol",
    "ADJ": "adjective",
    "CONJ": "conjunction",
    "VERB": "verb",
    "ADP": "pre/post-position",
    "ADV": "adverb",
    "PART": "particle",
    "INTJ": "interjection",
    "X": "X",
    "NUM": "NUM",
    "SPACE": "SPACE",
    "PRON": "PRON"
}

name_dict = {
    1: u'IS_ALPHA',
    2: u'IS_ASCII',
    3: u'IS_DIGIT',
    4: u'IS_LOWER',
    5: u'IS_PUNCT',
    6: u'IS_SPACE',
    7: u'IS_TITLE',
    8: u'IS_UPPER',
    9: u'LIKE_URL',
    10: u'LIKE_NUM',
    11: u'LIKE_EMAIL',
    12: u'IS_STOP',
    13: u'IS_OOV',
    14: u'FLAG14',
    15: u'FLAG15',
    16: u'FLAG16',
    17: u'FLAG17',
    18: u'FLAG18',
    19: u'FLAG19',
    20: u'FLAG20',
    21: u'FLAG21',
    22: u'FLAG22',
    23: u'FLAG23',
    24: u'FLAG24',
    25: u'FLAG25',
    26: u'FLAG26',
    27: u'FLAG27',
    28: u'FLAG28',
    29: u'FLAG29',
    30: u'FLAG30',
    31: u'FLAG31',
    32: u'FLAG32',
    33: u'FLAG33',
    34: u'FLAG34',
    35: u'FLAG35',
    36: u'FLAG36',
    37: u'FLAG37',
    38: u'FLAG38',
    39: u'FLAG39',
    40: u'FLAG40',
    41: u'FLAG41',
    42: u'FLAG42',
    43: u'FLAG43',
    44: u'FLAG44',
    45: u'FLAG45',
    46: u'FLAG46',
    47: u'FLAG47',
    48: u'FLAG48',
    49: u'FLAG49',
    50: u'FLAG50',
    51: u'FLAG51',
    52: u'FLAG52',
    53: u'FLAG53',
    54: u'FLAG54',
    55: u'FLAG55',
    56: u'FLAG56',
    57: u'FLAG57',
    58: u'FLAG58',
    59: u'FLAG59',
    60: u'FLAG60',
    61: u'FLAG61',
    62: u'FLAG62',
    63: u'FLAG63',
    64: u'ID',
    65: u'ORTH',
    66: u'LOWER',
    67: u'NORM',
    68: u'SHAPE',
    69: u'PREFIX',
    70: u'SUFFIX',
    71: u'LENGTH',
    72: u'CLUSTER',
    73: u'LEMMA',
    74: u'POS',
    75: u'TAG',
    76: u'DEP',
    77: u'ENT_IOB',
    78: u'ENT_TYPE',
    79: u'HEAD',
    80: u'SPACY',
    81: u'PROB'
}

DEP_MAP = {
      "adjectival complement": "acomp",
      "adverbial clause modifier": "advcl",
      "adverbial modifier": "advmod",
      "agent": "agent",
      "adjectival modifier": "amod",
      "appositional modifier": "appos",
      "attribute": "attr",
      "auxiliary": "aux",
      "auxiliary passive": "auxpass",
      "coordinating conjunction": "cc",
      "clausal complement": "ccomp",
      "complementizer": "complm",
      "conjunct": "conj",
      "copula": "cop",
      "clausal subject": "csubj",
      "clausal subject passive": "csubjpass",
      "unclassified dependent": "dep",
      "determiner": "det",
      "direct object": "dobj",
      "expletive": "expl",
      "modifier in hyphenation": "hmod",
      "hyphen": "hyph",
      "infinitival modifier": "infmod",
      "interjection": "intj",
      "indirect object": "iobj",
      "marker": "mark",
      "meta modifier": "meta",
      "negation modifier": "neg",
      "modifier of nominal": "nmod",
      "noun compound modifier": "nn",
      "noun phrase as adverbial modifier": "npadvmod",
      "nominal subject": "nsubj",
      "nominal subject passive": "nsubjpass",
      "number modifier": "num",
      "number compound modifier": "number",
      "object predicate": "oprd",
      "object": "obj",
      "oblique nominal": "obl",
      "parataxis": "parataxis",
      "participal modifier": "partmod",
      "complement of preposition": "pcomp",
      "object of preposition": "pobj",
      "possession modifier": "poss",
      "possessive modifier": "possessive",
      "pre-correlative conjunction": "preconj",
      "prepositional modifier": "prep",
      "particle": "prt",
      "punctuation": "punct",
      "modifier of quantifier": "quantmod",
      "relative clause modifier": "rcmod",
      "root": "ROOT",
      "open clausal complement": "xcomp",
      "nummod": "nummod",
      "": "",
      "relcl": "relcl",
      "acl": "acl"
}

INV_DEP_MAP = {v: k for k, v in DEP_MAP.iteritems()}
INV_DEP_MAP["nummod"] = "nummod"
INV_DEP_MAP[""] = ""
INV_DEP_MAP["relcl"] = "relcl"
INV_DEP_MAP["acl"] = "acl"

DEFAULT_TOKEN = {
          "capitalization": [],
          "match_all_forms": "true",
          "contain_digit": "true",
          "is_in_output": "true",
          "is_in_vocabulary": "",
          "is_out_of_vocabulary": "",
          "is_required": "true",
          "length": [],
          "maximum": "",
          "minimum": "",
          "numbers": [],
          "part_of_speech": [],
          "prefix": "",
          "shapes": [],
          "suffix": "",
          "token": [],
          "type": ""
}

DEFAULT_DEPENDENCY = {
    "from": "",
    "to": "",
    "dependency": []
}

'''
Class Rule
'''


class Rule(object):
    # initial and load english vocab
    def __init__(self, nlp):
        self.nlp = nlp
        self.flag_reset_lst = dict()

    # initial macher
    def init_matcher(self):
        self.matcher = spacy.matcher.Matcher(self.nlp.vocab)

    # initial flag for each user specified pattern
    def init_flag(self):
        if self.flag_reset_lst:
            for flag in self.flag_reset_lst:
                for lexeme in self.flag_reset_lst[flag]:
                    self.nlp.vocab[lexeme].set_flag(FLAG_DICT[str(flag)], False)
        self.flag_reset_lst = dict()

    # set a flag, add all cases of a word to vocab and set flag to true
    def set_flag(self, token_l, flagnum):
        self.flag_reset_lst[flagnum] = []
        for t in token_l:
            elst = map(''.join, itertools.product(*((c.upper(), c.lower()) for c in t)))
            for lexeme in elst:
                self.nlp.vocab[lexeme.decode('utf8')].set_flag(FLAG_DICT[str(flagnum)], True)
                self.flag_reset_lst[flagnum].append(lexeme.decode('utf8'))

    def set_num_flag(self, num_l, flagnum):
        self.flag_reset_lst[flagnum] = []
        for lexeme in num_l:
            slexeme = str(lexeme)
            self.nlp.vocab[slexeme.decode('utf8')].set_flag(FLAG_DICT[str(flagnum)], True)
            self.flag_reset_lst[flagnum].append(slexeme.decode('utf8'))


'''
Class Pattern
'''


class Pattern(object):
    # initial a Pattern
    def __init__(self):
        # First list contains pattern to be matched. Second dict contains information about prefix, suffix, shape
        self.token_lst = [[], {}]

    # add a word token
    def add_word_token(self, d, flag, nlp):
        token_to_rule = []

        for this_token in create_word_token(d["token"], d["capitalization"], d["length"], flag,
                                            d["contain_digit"], d["is_out_of_vocabulary"],
                                            d["is_in_vocabulary"], d["match_all_forms"], nlp):
            token_to_rule = add_pos_totoken(d["part_of_speech"],
                                            this_token, token_to_rule)
        # add prefix and suffix information to token information for filter
        token_inf = create_inf(d["prefix"], d["suffix"],
                               not d["token"], d["is_in_output"])
        self.token_lst = add_token_tolist(self.token_lst, token_to_rule,
                                          d["is_required"], token_inf)

    # add a shape token
    def add_shape_token(self, d):
        token_to_rule = []
        for this_token in create_shape_token(d["shapes"]):
            token_to_rule = add_pos_totoken(d["part_of_speech"],
                                            this_token, token_to_rule)
        token_inf = create_inf(d["prefix"], d["suffix"],
                               True, d["is_in_output"])
        # add shape information to token inf for future filter
        if d["shapes"]:
            token_inf["shapes"] = d["shapes"]
        self.token_lst = add_token_tolist(self.token_lst, token_to_rule,
                                          d["is_required"], token_inf)

    # add a number token
    def add_number_token(self, token_d, flag):
        token_to_rule = []
        token_inf = create_inf("", "",
                               False, token_d["is_in_output"])
        if not token_d["numbers"]:
            this_token = {spacy.attrs.IS_DIGIT: True}
            if token_d["length"]:
                for length in token_d["length"]:
                    this_token[spacy.attrs.LENGTH] = int(length)
                    token_to_rule.append(copy.deepcopy(this_token))
            else:
                token_to_rule = [this_token]
            token_inf["minimum"] = token_d["minimum"]
            token_inf["maximum"] = token_d["maximum"]
        elif len(token_d["numbers"]) == 1:
            token_to_rule = [{spacy.attrs.ORTH: str(token_d["numbers"][0])}]
        else:
            token_to_rule = [{FLAG_DICT[str(flag)]: True}]
        self.token_lst = add_token_tolist(self.token_lst, token_to_rule,
                                          token_d["is_required"], token_inf)

    # add a punctuation token
    def add_punctuation_token(self, token_d, flag):
        if not token_d["token"]:
            this_token = {spacy.attrs.IS_PUNCT: True}
        elif len(token_d["token"]) == 1:
            this_token = {spacy.attrs.ORTH: token_d["token"][0]}
        else:
            this_token = {FLAG_DICT[str(flag)]: True}
        token_inf = create_inf("", "",
                               False, token_d["is_in_output"])
        self.token_lst = add_token_tolist(self.token_lst, [this_token],
                                          token_d["is_required"], token_inf)

    def add_linebreak_token(self, token_d):
        num_break = int(token_d["length"][0]) if token_d["length"] else 1
        if num_break:
            s = ''
            for i in range(num_break):
                s += '\n'
            token_to_rule = [{spacy.attrs.LOWER: s.decode('utf-8')}]
            token_inf = create_inf("", "", False, token_d["is_in_output"])
            self.token_lst = add_token_tolist(self.token_lst, token_to_rule,
                                              token_d["is_required"], token_inf)


# Check if prefix matches
def check_prefix(s, prefix):
    if len(s) < len(prefix):
        return False
    elif s[:len(prefix)].lower() == prefix.lower():
        return True
    else:
        return False


# Check if suffix matches
def check_suffix(s, suffix):
    if suffix:
        if len(s) < len(suffix):
            return False
        elif s[-len(suffix):].lower() == suffix.lower():
            return True
        else:
            return False
    else:
        return True


def create_inf(p, s, a, is_in_output=False):
    label = {}
    if a:
        if p:
            label["prefix"] = p
        if s:
            label["suffix"] = s
    if is_in_output == "true":
        label["is_in_output"] = True
    else:
        label["is_in_output"] = False

    return label


# Add each token to list to be processed by matcher
def add_token_tolist(t_lst, token_l, flag, inf):
    result = []
    result_lst = []
    result_dict = t_lst[1]
    lst = t_lst[0]
    # If this token is not optional
    if flag == "true":
        if lst:
            c = -1
            for s_id, token in enumerate(token_l):
                new_inf = copy.deepcopy(inf)
                # add shape information
                if "shapes" in inf:
                    new_inf["shape"] = inf["shapes"][s_id]
                    del new_inf["shapes"]
                for idx, each_lst in enumerate(lst):
                    t_id = len(each_lst)
                    c += 1
                    each_copy = copy.deepcopy(each_lst)
                    each_copy.append(token)
                    result.append(each_copy)
                    if c not in result_dict:
                        result_dict[c] = copy.deepcopy(result_dict[idx])
                    result_dict[c].update({len(each_copy) - 1: new_inf})
                    if t_id not in result_dict[c]["output_idx"]:
                        result_dict[c]["output_idx"].append(t_id)
        else:
            c = -1
            for s_id, token in enumerate(token_l):
                new_inf = copy.deepcopy(inf)
                if "shapes" in inf:
                    new_inf["shape"] = inf["shapes"][s_id]
                    del new_inf["shapes"]
                c += 1
                result.append([token])
                if c not in result_dict:
                    result_dict[c] = {0: new_inf, "output_idx": [0]}
                else:
                    result_dict[c].update({0: new_inf, "output_idx": [0]})

    # If this token is optional
    else:
        if lst:
            c = -1
            for each_lst in lst:
                result.append(copy.deepcopy(each_lst))
                c += 1
            for idx, each_lst in enumerate(lst):
                t_id = len(each_lst)
                for s_id, token in enumerate(token_l):
                    new_inf = copy.deepcopy(inf)
                    if "shapes" in inf:
                        new_inf["shape"] = inf["shapes"][s_id]
                        del new_inf["shapes"]
                    c += 1
                    if c not in result_dict:
                        result_dict[c] = copy.deepcopy(result_dict[idx])
                    each_copy = copy.deepcopy(each_lst)
                    each_copy.append(token)
                    result.append(each_copy)
                    result_dict[c].update({len(each_copy) - 1: new_inf})
                    if t_id not in result_dict[c]["output_idx"]:
                        result_dict[c]["output_idx"].append(t_id)
        else:
            result.append([])
            c = 0
            result_dict[c] = {"output_idx": []}
            for s_id, token in enumerate(token_l):
                new_inf = copy.deepcopy(inf)
                if "shapes" in inf:
                    new_inf["shape"] = inf["shapes"][s_id]
                    del new_inf["shapes"]
                c += 1
                result.append([token])
                if c not in result_dict:
                    result_dict[c] = {0: new_inf, "output_idx": [0]}
                else:
                    result_dict[c].update({0: new_inf, "output_idx": [0]})

    result_lst.append(result)
    result_lst.append(copy.deepcopy(result_dict))
    return result_lst


# add pos to each dict of token to be matched
def add_pos_totoken(pos_l, this_token, token_to_rule):
    # user check some POS
    if pos_l:
        for pos in pos_l:
            this_token[spacy.attrs.POS] = POS_MAP[pos]
            token_to_rule.append(copy.deepcopy(this_token))
    # if user does not specify any specific POS
    else:
        token_to_rule.append(copy.deepcopy(this_token))

    return token_to_rule


# create word token according to user input
def create_word_token(word_l, capi_l, length_l, flag, contain_num, out_vocab, in_vocab, all_forms, nlp):
    # if user enter one word
    if len(word_l) == 1:
        if all_forms == "true":
            if any(x.isupper() for x in nlp([word_l[0]])[0].lemma_):
                token = {spacy.attrs.LOWER: word_l[0].lower()}
            else:
                token = {spacy.attrs.LEMMA: find_lexeme_base(word_l[0], nlp)}
        else:
            token = {spacy.attrs.LOWER: word_l[0].lower()}
        token_l = speci_capi(token, capi_l, word_l)
    # if user does not enter any word
    elif not word_l:
        if contain_num == "true":
            token = {spacy.attrs.IS_ASCII: True, spacy.attrs.IS_PUNCT: False}
        else:
            token = {spacy.attrs.IS_ALPHA: True}
        if out_vocab == "true" and in_vocab != "true":
            token[spacy.attrs.IS_OOV] = True
        elif out_vocab != "true" and in_vocab == "true":
            token[spacy.attrs.IS_OOV] = False

        token_l = speci_capi(token, capi_l, word_l)
        if length_l:
            while spacy.attrs.LENGTH not in token_l[0]:
                token = token_l.pop(0)
                for length in length_l:
                    token[spacy.attrs.LENGTH] = int(length)
                    token_l.append(copy.deepcopy(token))
    # if user enter multiple words, use flag set before
    else:
        if all_forms == "false":
            token = {FLAG_DICT[str(flag)]: True}
            token_l = speci_capi(token, capi_l, word_l)
        else:
            token_l = list()
            for word_token in word_l:
                if any(x.isupper() for x in nlp([word_token])[0].lemma_):
                    token = {spacy.attrs.LOWER: word_token.lower()}
                else:
                    token = {spacy.attrs.LEMMA: find_lexeme_base(word_token, nlp)}
                token_l += speci_capi(token, capi_l, word_l)

    return token_l


# create shape token according to user input
def create_shape_token(shape_l):
    # if user does not enter a shape, it can be a number, punct
    if not shape_l:
        token = {spacy.attrs.IS_ASCII: True}
        token_l = [token]
    # if user enter some shape
    else:
        token_l = []
        for shape in shape_l:
            this_shape = generate_shape(shape, counting_stars(shape))
            token = {spacy.attrs.SHAPE: this_shape}
            token_l.append(copy.deepcopy(token))

    return token_l


# add capitalization to token
def speci_capi(t, capi_lst, word_l):
    result = []
    if not capi_lst:
        result.append(copy.deepcopy(t))
    else:
        if "exact" in capi_lst and word_l != []:
            for word in word_l:
                token = copy.deepcopy(t)
                token[spacy.attrs.ORTH] = word
                result.append(token)
        if "lower" in capi_lst:
            token = copy.deepcopy(t)
            token[spacy.attrs.IS_LOWER] = True
            result.append(token)
        if "upper" in capi_lst:
            token = copy.deepcopy(t)
            token[spacy.attrs.IS_UPPER] = True
            result.append(token)
        if "title" in capi_lst:
            token = copy.deepcopy(t)
            token[spacy.attrs.IS_TITLE] = True
            result.append(token)
        if "mixed" in capi_lst:
            token = copy.deepcopy(t)
            token[spacy.attrs.IS_UPPER] = False
            token[spacy.attrs.IS_LOWER] = False
            token[spacy.attrs.IS_TITLE] = False
            result.append(token)

    return result


# Filter function is to process the output to match shape and prefix, suffix
def filter(doc, matches, inf_inf):
    result = []
    for match in matches:
        flag = True
        (ent_id, label, start, end) = match
        pattern = doc[start:end]
        for i in range(len(pattern)):
            inf = inf_inf[i]
            if "shape" in inf:
                if compare_shape(pattern[i], inf["shape"]):
                    flag = False
                    break
            if "prefix" in inf:
                prefix = inf["prefix"]
            else:
                prefix = ""
            if "suffix" in inf:
                suffix = inf["suffix"]
            else:
                suffix = ""
            if not check_prefix(str(pattern[i]), prefix) or not check_suffix(str(pattern[i]), suffix):
                flag = False
                break
            if "minimum" in inf or "maximum" in inf:
                if inf["minimum"] != "":
                    minimum = float(inf["minimum"])
                else:
                    minimum = -float("inf")
                if inf["maximum"] != "":
                    maximum = float(inf["maximum"])
                else:
                    maximum = float("inf")
                if minimum or maximum:
                    match_number = float(str(pattern[i]))
                    if match_number < minimum:
                        flag = False
                        break
                    if match_number > maximum:
                        flag = False
                        break
        if flag:
            result.append(match)

    return result


# create output
def create_print(lst):
    result = []
    for each_d in lst:
        new_d = {}
        for e in each_d:
            new_d[name_dict[e].encode('utf-8')] = each_d[e]
        result.append(new_d)

    return result


def counting_stars(word):
    count = [1]
    for i in range(1, len(word)):
        if word[i - 1] == word[i]:
            count[-1] += 1
        else:
            count.append(1)

    return count


def generate_shape(word, count):
    shape = ""
    p = 0
    for c in count:
        if c > 4:
            shape += word[p:p + 4]
        else:
            shape += word[p:p + c]
        p = p + c

    return shape


def get_value(doc, start, end, output_inf, label):
    result_str = ""
    #    s = list(output_format.encode("utf-8"))
    for i in range(len(output_inf)):
        if output_inf[i]:
            result_str += str(doc[start + i])
            result_str += " "
    return (start, end, result_str.strip(), label)


def filter_value(value, output_format):
    if not output_format:
        return value
    else:
        result_str = ""
        s = list(output_format.encode("utf-8"))
        (start, end, v, label) = value
        v = v.split()
        t1 = s.pop(0)
        t2 = s.pop(0)
        while 1:
            t3 = s.pop(0)
            if t1 == '{' and t2.isdigit() and t3 == '}':
                if int(t2) > len(v):
                    result_str = value[2]
                    break
                result_str += v[int(t2) - 1]
                if not s:
                    break
                t1 = s.pop(0)
                if not s:
                    result_str += t1
                    break
                t2 = s.pop(0)
                if not s:
                    result_str += t2
                    break
            else:
                result_str += t1
                t1 = t2
                t2 = t3
                if not s:
                    result_str += t1
                    result_str += t2
                    break
        return (start, end, result_str, label)


def get_longest(value_lst):
    value_lst.sort()
    result = []
    start = value_lst[0][0]
    end = value_lst[0][1]
    pivot = value_lst[0]
    pivot_e = end
    pivot_s = start
    for idx, (s, e, v, l, identi) in enumerate(value_lst):
        if s == pivot_s and pivot_e < e:
            pivot_e = e
            pivot = value_lst[idx]
        elif s != pivot_s and pivot_e < e:
            result.append(pivot)
            pivot = value_lst[idx]
            pivot_e = e
            pivot_s = s
    result.append(pivot)
    return result


# reject negative matches based on overlapping
def reject(pos_lst, neg_lst):
    pos_lst.sort()
    neg_lst.sort()
    result = []
    pivot_pos = pos_lst[0]
    pivot_neg = neg_lst[0]
    while pos_lst:
        if pivot_pos[1] <= pivot_neg[0]:
            result.append(pivot_pos)
            pos_lst.pop(0)
            if pos_lst:
                pivot_pos = pos_lst[0]
        elif pivot_pos[0] >= pivot_neg[1]:
            neg_lst.pop(0)
            if not neg_lst:
                result += pos_lst
                break
            else:
                pivot_neg = neg_lst[0]
        else:
            pos_lst.pop(0)
            if pos_lst:
                pivot_pos = pos_lst[0]
    return result


def add_dep(m_lst, def_inf, output_lst):
    if not def_inf:
        return m_lst
    else:
        for element in def_inf:
            if int(element["from"]) in output_lst and int(element["to"]) in output_lst and element["dependency"]:
                to_idx = output_lst.index(int(element["to"]))
                m_lst[to_idx][spacy.attrs.DEP] = DEP_MAP[element["dependency"]]
        return m_lst


def check_head(m_lst, output_lst, def_inf, doc):
    if not def_inf:
        return m_lst
    else:
        return_lst = list()
        for element in def_inf:
            if int(element["from"]) in output_lst and int(element["to"]) in output_lst:
                from_idx = output_lst.index(int(element["from"]))
                to_idx = output_lst.index(int(element["to"]))
                for a_match in m_lst:
                    (ent_id, label, start, end) = a_match
                    if doc[start+to_idx].head == doc[start+from_idx]:
                        return_lst.append(a_match)
        return return_lst


def find_lexeme_base(word, nlp):
    return nlp([word])[0].lemma_


def compare_shape(token, shape):
    token_shape = ""
    for i in str(token):
        if i.isalpha():
            if i.islower():
                token_shape += "x"
            elif i.isupper():
                token_shape += "X"
        elif i.isdigit():
            token_shape += "d"
    return counting_stars(str(token_shape)) != counting_stars(shape)


def extract(field_rules, nlp_doc, nlp):
    pattern_description = field_rules
    rule = Rule(nlp)
    extracted_lst = []
    value_lst_pos = []
    value_lst_neg = []
    for index, line in enumerate(pattern_description["rules"]):
        if line["is_active"] == "true":

            if "polarity" not in line:
                line["polarity"] = "true"
            if "dependencies" not in line:
                line["dependencies"] = []
            rule.init_matcher()
            rule.init_flag()
            new_pattern = Pattern()
            flagnum = 17

            for current_token_idx in range(len(line["pattern"])):
                token_d = line["pattern"][current_token_idx]
                if "match_all_forms" not in token_d:
                    token_d["match_all_forms"] = "false"
                if token_d["type"] == "word":
                    if len(token_d["token"]) >= 2 and token_d["match_all_forms"] == "false":
                        # set flag for multiply words
                        flagnum += 1
                        rule.set_flag(token_d["token"], flagnum)
                    new_pattern.add_word_token(token_d, flagnum, nlp)

                if token_d["type"] == "shape":
                    new_pattern.add_shape_token(token_d)

                if token_d["type"] == "number":
                    if len(token_d["numbers"]) >= 2:
                        flagnum += 1
                        rule.set_num_flag(token_d["numbers"], flagnum)
                    new_pattern.add_number_token(token_d, flagnum)

                if token_d["type"] == "punctuation":
                    if len(token_d["token"]) >= 2:
                        # set flag for multiply punctuations
                        flagnum += 1
                        rule.set_flag(token_d["token"], flagnum)
                    new_pattern.add_punctuation_token(token_d, flagnum)

                if token_d["type"] == "linebreak":
                    new_pattern.add_linebreak_token(token_d)

            tl = new_pattern.token_lst[0]
            ps_inf = new_pattern.token_lst[1]

            for i in range(len(tl)):
                # rule_num += 1
                if tl[i]:
                    tl_add_dep = add_dep(copy.deepcopy(tl[i]), line["dependencies"],
                                         ps_inf[i]["output_idx"])
                    rule_to_print = create_print(tl_add_dep)
                    rule.matcher.add_pattern(str(rule_to_print), tl_add_dep, label=index)
                    m = check_head(rule.matcher(nlp_doc), ps_inf[i]["output_idx"], line["dependencies"],
                                   nlp_doc)
                    matches = filter(nlp_doc, m, ps_inf[i])
                    output_infs = []
                    for e in ps_inf[i]:
                        if e != "output_idx":
                            output_infs.append((e, ps_inf[i][e]["is_in_output"]))
                    output_infs.sort()
                    output_inf = [p[1] for p in output_infs]

                    for (ent_id, label, start, end) in matches:
                        value = get_value(nlp_doc, start, end, output_inf, label)
                        filtered_value = filter_value(value, line["output_format"])
                        filtered_value = filtered_value + (line["identifier"],)
                        if line["polarity"] != "false":
                            value_lst_pos.append(filtered_value)
                        else:
                            value_lst_neg.append(filtered_value)
                    rule.init_matcher()
            rule.init_flag()

    if value_lst_pos:
        longest_lst_pos = get_longest(value_lst_pos)
        if value_lst_neg:
            longest_lst_neg = get_longest(value_lst_neg)
            return_lst = reject(longest_lst_pos, longest_lst_neg)
        else:
            return_lst = longest_lst_pos
        for (start, end, value, label, identifier) in return_lst:
            result = {
                "value": value,
                "context": {
                    "start": start,
                    "end": end,
                    "rule_id": label,
                    "identifier": identifier
                }
            }
            extracted_lst.append(result)

    return extracted_lst


def init_rules():
    result = {
        "field": "",
        "rules": [
            {
                "description": "",
                "identifier": "infer_rule",
                "is_active": "true",
                "output_format": "",
                "dependencies": [],
                "pattern": [],
                "polarity": "true"
            }
        ]
    }
    return result


def create_rule_lst(l):
    df = []
    for i in range(len(l[0])):
        digit_flag = [j[i].is_digit for j in l]
        df.append(digit_flag)

    result = list()
    for match in l:
        rr = list()
        rr.append(init_rules())
        for token_id, token in enumerate(match):
            this_token = copy.deepcopy(DEFAULT_TOKEN)

            if token.is_punct:
                this_token["type"] = "punctuation"
                temp_element = list()
                for element in rr:
                    temp_element.append(copy.deepcopy(element))
                    element["rules"][0]["pattern"].append(copy.deepcopy(this_token))

            elif True in df[token_id] and False not in df[token_id] :
                this_token["type"] = "number"
                temp_element = list()
                for element in rr:
                    temp_element.append(copy.deepcopy(element))
                    element["rules"][0]["pattern"].append(copy.deepcopy(this_token))
                temp_token = copy.deepcopy(DEFAULT_TOKEN)
                temp_token["type"] = "word"
                for element in temp_element:
                    element["rules"][0]["pattern"].append(copy.deepcopy(temp_token))
                    rr.append(element)

            elif False in df[token_id]:
                if token.is_alpha:
                    this_token["type"] = "word"
                    this_token["contain_digit"] = "false"
                    for element in rr:
                        element["rules"][0]["pattern"].append(copy.deepcopy(this_token))

                elif '\n' in str(token):
                    this_token["type"] = "linebreak"
                    this_token["length"] = [str(token).count("\n")]
                    for element in rr:
                        element["rules"][0]["pattern"].append(copy.deepcopy(this_token))

                else:
                    this_token["type"] = "word"
                    for element in rr:
                        element["rules"][0]["pattern"].append(copy.deepcopy(this_token))
        result += copy.deepcopy(rr)

    return result


def calc_ratio(extracts, pos_lst, neg_lst, tokenizer, nlp):
    extracted_lst = [[k["value"].decode("utf-8") for k in tokenizer.extract(i["value"], lowercase=False)] for i in
                     extracts]
    extracted_docs = [nlp(i).text for i in extracted_lst]

    positive_intersection = [x.text for x in pos_lst if x.text in extracted_docs]
    negative_intersection = [x.text for x in neg_lst if x.text in extracted_docs]

    num_extracts = len(extracted_lst)
    r = ((len(positive_intersection) - len(negative_intersection)) / float(num_extracts)
                                                                          ) if extracted_lst else 0

    return tuple((len(positive_intersection), r, num_extracts))


def get_score(a_rule):
    score = 0
    consider_fields = {
        "length": 3,
        "capitalization": 1,
        "part_of_speech": 2,
        "shapes": 2,
        "prefix": 3,
        "numbers": 2,
        "token": 2,
        "suffix": 3
    }
    for pattern in a_rule["rules"][0]["pattern"]:
        this_score = 1
        for field in consider_fields:
            if pattern[field]:
                this_score += 2
                if field == "capitalization":
                    if len(pattern[field]) >= 4:
                        this_score += 20
                    else:
                        this_score += (consider_fields[field] * (len(pattern[field]) - 1))
                elif field == "token" or field == "number" or field == "shapes":
                    if len(pattern[field]) >= 1:
                        this_score += math.pow(len(pattern[field])+1, consider_fields[field])
                elif field == "prefix" or field == "suffix":
                    this_score += math.pow(len(pattern[field]), consider_fields[field])
                elif isinstance(pattern[field], list):
                    if len(pattern[field]) >= 1:
                        this_score += math.pow(len(pattern[field])+1, consider_fields[field])
                    else:
                        this_score += consider_fields[field]
                else:
                    this_score += consider_fields[field]
        score += this_score
    return score


def check_capitalization(word_token):
    if word_token.is_lower:
        return "lower"
    elif word_token.is_title:
        return "title"
    elif str(word_token).isupper():
        return "upper"
    else:
        return "mixed"


def get_shape(word):
    result = ""
    for i in word:
        if i.isdigit():
            result += "d"
        elif i.islower():
            result += "x"
        else:
            result += "X"

    return result


def allsame(x):
    return len(set(x)) == 1


def get_prefix(lst):
    r = [i[0] for i in itertools.takewhile(allsame, itertools.izip(*lst))]
    return "".join(r)


def get_suffix(lst):
    r_lst = [x[::-1] for x in lst]
    r = [i[0] for i in itertools.takewhile(allsame, itertools.izip(*r_lst))]
    return "".join(r)[::-1]


def add_punct_constrain(rule, p_id, docs):
    result = list()
    this_rule = copy.deepcopy(rule)
    for doc in docs:
        if doc[p_id].lemma_ not in this_rule["rules"][0]["pattern"][p_id]["token"]:
            this_rule["rules"][0]["pattern"][p_id]["token"].append(doc[p_id].lemma_)
    result.append(copy.deepcopy(this_rule))
    this_rule["rules"][0]["pattern"][p_id]["is_required"] = "false"
    result.append(copy.deepcopy(this_rule))
    return result


def add_number_constrain(rule, p_id, docs):
    result = list()

    # add length constrains
    this_rule = copy.deepcopy(rule)
    for doc in docs:
        if len(doc[p_id]) not in this_rule["rules"][0]["pattern"][p_id]["length"]:
            this_rule["rules"][0]["pattern"][p_id]["length"].append(len(doc[p_id]))
    result.append(copy.deepcopy(this_rule))
    this_rule["rules"][0]["pattern"][p_id]["is_required"] = "false"
    result.append(copy.deepcopy(this_rule))
    temp_lst = copy.deepcopy(result)

    # add numbers constrains
    this_rule = copy.deepcopy(rule)
    number_lst = []
    for doc in docs:
        if doc[p_id].lemma_ not in number_lst:
            number_lst.append(doc[p_id].lemma_)
    this_rule["rules"][0]["pattern"][p_id]["numbers"] = number_lst
    result.append(copy.deepcopy(this_rule))
    this_rule["rules"][0]["pattern"][p_id]["is_required"] = "false"
    result.append(copy.deepcopy(this_rule))

    for a_rule in temp_lst:
        this_rule = copy.deepcopy(a_rule)
        this_rule["rules"][0]["pattern"][p_id]["numbers"] = number_lst
        result.append(copy.deepcopy(this_rule))

    return result


def add_word_constrain(rule, p_id, docs):
    result = list()

    # add only token constrains
    this_rule = copy.deepcopy(rule)
    token_orth_lst = []
    token_lemma_lst = []
    for doc in docs:
        if doc[p_id].orth_ not in token_orth_lst:
            token_orth_lst.append(doc[p_id].orth_)
        if any(x.isupper() for x in doc[p_id].lemma_):
            if doc[p_id].lower_ not in token_lemma_lst:
                token_lemma_lst.append(doc[p_id].lower_)
        else:
            if doc[p_id].lemma_ not in token_lemma_lst:
                token_lemma_lst.append(doc[p_id].lemma_)
    this_rule["rules"][0]["pattern"][p_id]["token"] = token_lemma_lst
    result.append(copy.deepcopy(this_rule))
    this_rule["rules"][0]["pattern"][p_id]["is_required"] = "false"
    result.append(copy.deepcopy(this_rule))
    this_rule["rules"][0]["pattern"][p_id]["match_all_forms"] = "false"
    this_rule["rules"][0]["pattern"][p_id]["token"] = token_orth_lst
    result.append(copy.deepcopy(this_rule))
    this_rule["rules"][0]["pattern"][p_id]["is_required"] = "true"
    result.append(copy.deepcopy(this_rule))

    # add exact capitalization constrains
    this_rule["rules"][0]["pattern"][p_id]["capitalization"].append("exact")
    result.append(copy.deepcopy(this_rule))
    this_rule["rules"][0]["pattern"][p_id]["is_required"] = "false"
    result.append(copy.deepcopy(this_rule))

    # add only capitalization constrains to non token constrain rules
    this_rule = copy.deepcopy(rule)
    capi_lst = []
    for doc in docs:
        capi = check_capitalization(doc[p_id])
        if capi not in capi_lst:
            capi_lst.append(capi)
    if not this_rule["rules"][0]["pattern"][p_id]["capitalization"]:
        this_rule["rules"][0]["pattern"][p_id]["capitalization"] = capi_lst
    else:
        for x in capi_lst:
            if x not in this_rule["rules"][0]["pattern"][p_id]["capitalization"]:
                this_rule["rules"][0]["pattern"][p_id]["capitalization"].append(x)
    result.append(copy.deepcopy(this_rule))
    this_rule["rules"][0]["pattern"][p_id]["is_required"] = "false"
    result.append(copy.deepcopy(this_rule))
    this_rule["rules"][0]["pattern"][p_id]["match_all_forms"] = "false"
    result.append(copy.deepcopy(this_rule))
    this_rule["rules"][0]["pattern"][p_id]["is_required"] = "true"
    result.append(copy.deepcopy(this_rule))

    # add capitalization constrains to non-empty token constrain rules
    temp_lst = copy.deepcopy(result)
    for a_rule in temp_lst:
        if a_rule["rules"][0]["pattern"][p_id]["token"]:
            this_rule = copy.deepcopy(a_rule)
            if not this_rule["rules"][0]["pattern"][p_id]["capitalization"]:
                this_rule["rules"][0]["pattern"][p_id]["capitalization"] = capi_lst
            else:
                for x in capi_lst:
                    if x not in this_rule["rules"][0]["pattern"][p_id]["capitalization"]:
                        this_rule["rules"][0]["pattern"][p_id]["capitalization"].append(x)
            result.append(copy.deepcopy(this_rule))

    # add length constrains
    length_lst = []
    for doc in docs:
        if len(doc[p_id]) not in length_lst:
            length_lst.append(len(doc[p_id]))

    temp_lst = copy.deepcopy(result)
    for a_rule in temp_lst:
        if not a_rule["rules"][0]["pattern"][p_id]["token"]:
            this_rule = copy.deepcopy(a_rule)
            this_rule["rules"][0]["pattern"][p_id]["length"] = length_lst
            result.append(copy.deepcopy(this_rule))

    this_rule = copy.deepcopy(rule)
    this_rule["rules"][0]["pattern"][p_id]["length"] = length_lst
    result.append(copy.deepcopy(this_rule))
    this_rule["rules"][0]["pattern"][p_id]["is_required"] = "false"
    result.append(copy.deepcopy(this_rule))

    # add pos tag constrains
    pos_lst = []
    for doc in docs:
        if INV_POS_MAP[doc[p_id].pos_] not in pos_lst:
            pos_lst.append(INV_POS_MAP[doc[p_id].pos_])

    temp_lst = copy.deepcopy(result)
    for a_rule in temp_lst:
        this_rule = copy.deepcopy(a_rule)
        this_rule["rules"][0]["pattern"][p_id]["part_of_speech"] = pos_lst
        result.append(copy.deepcopy(this_rule))

    this_rule = copy.deepcopy(rule)
    this_rule["rules"][0]["pattern"][p_id]["part_of_speech"] = pos_lst
    result.append(copy.deepcopy(this_rule))
    this_rule["rules"][0]["pattern"][p_id]["is_required"] = "false"
    result.append(copy.deepcopy(this_rule))

    # add in_vocab, out_vocab constrains
    invob = "false"
    outvob = "false"
    for doc in docs:
        if doc[p_id].is_oov:
            invob = "true"
        else:
            outvob = "true"

    temp_lst = copy.deepcopy(result)
    for a_rule in temp_lst:
        if not a_rule["rules"][0]["pattern"][p_id]["token"]:
            this_rule = copy.deepcopy(a_rule)
            this_rule["rules"][0]["pattern"][p_id]["is_out_of_vocabulary"] = invob
            this_rule["rules"][0]["pattern"][p_id]["is_in_vocabulary"] = outvob
            result.append(copy.deepcopy(this_rule))

    this_rule = copy.deepcopy(rule)
    this_rule["rules"][0]["pattern"][p_id]["is_out_of_vocabulary"] = invob
    this_rule["rules"][0]["pattern"][p_id]["is_in_vocabulary"] = outvob
    result.append(copy.deepcopy(this_rule))
    this_rule["rules"][0]["pattern"][p_id]["is_required"] = "false"
    result.append(copy.deepcopy(this_rule))

    # add prefix, suffix constrain
    this_token_lst = [doc[p_id].orth_ for doc in docs]
    this_prefix = get_prefix(this_token_lst)
    this_suffix = get_suffix(this_token_lst)

    temp_lst = copy.deepcopy(result)
    for a_rule in temp_lst:
        if not a_rule["rules"][0]["pattern"][p_id]["token"]:
            this_rule = copy.deepcopy(a_rule)
            this_rule["rules"][0]["pattern"][p_id]["prefix"] = this_prefix
            result.append(copy.deepcopy(this_rule))
            this_rule["rules"][0]["pattern"][p_id]["suffix"] = this_suffix
            result.append(copy.deepcopy(this_rule))
            this_rule["rules"][0]["pattern"][p_id]["prefix"] = ""
            result.append(copy.deepcopy(this_rule))

    this_rule = copy.deepcopy(rule)
    this_rule["rules"][0]["pattern"][p_id]["prefix"] = this_prefix
    result.append(copy.deepcopy(this_rule))
    this_rule["rules"][0]["pattern"][p_id]["is_required"] = "false"
    result.append(copy.deepcopy(this_rule))
    this_rule["rules"][0]["pattern"][p_id]["suffix"] = this_suffix
    result.append(copy.deepcopy(this_rule))
    this_rule["rules"][0]["pattern"][p_id]["is_required"] = "true"
    result.append(copy.deepcopy(this_rule))
    this_rule["rules"][0]["pattern"][p_id]["prefix"] = ""
    result.append(copy.deepcopy(this_rule))
    this_rule["rules"][0]["pattern"][p_id]["is_required"] = "false"
    result.append(copy.deepcopy(this_rule))

    return result


def add_shape_constrain(rule, p_id, docs):
    result = list()

    # add shape constrain
    this_rule = copy.deepcopy(rule)
    this_rule["rules"][0]["pattern"][p_id]["type"] = "shape"
    for doc in docs:
        if get_shape(str(doc[p_id])) not in this_rule["rules"][0]["pattern"][p_id]["shapes"]:
            this_rule["rules"][0]["pattern"][p_id]["shapes"].append(get_shape(str(doc[p_id])))
    result.append(copy.deepcopy(this_rule))
    this_rule["rules"][0]["pattern"][p_id]["is_required"] = "false"
    result.append(copy.deepcopy(this_rule))

    # add pos tag constrain
    temp_lst = copy.deepcopy(result)
    for a_rule in temp_lst:
        this_rule = copy.deepcopy(a_rule)
        for doc in docs:
            if get_shape(str(doc[p_id])) not in this_rule["rules"][0]["pattern"][p_id]["shapes"]:
                this_rule["rules"][0]["pattern"][p_id]["shapes"].append(get_shape(str(doc[p_id])))
        result.append(copy.deepcopy(this_rule))

    # add prefix suffix constrain
    this_token_lst = [doc[p_id].orth_ for doc in docs]
    this_prefix = get_prefix(this_token_lst)
    this_suffix = get_suffix(this_token_lst)

    temp_lst = copy.deepcopy(result)
    for a_rule in temp_lst:
        this_rule = copy.deepcopy(a_rule)
        this_rule["rules"][0]["pattern"][p_id]["prefix"] = this_prefix
        result.append(copy.deepcopy(this_rule))
        this_rule["rules"][0]["pattern"][p_id]["suffix"] = this_suffix
        result.append(copy.deepcopy(this_rule))
        this_rule["rules"][0]["pattern"][p_id]["prefix"] = ""
        result.append(copy.deepcopy(this_rule))

    this_rule = copy.deepcopy(rule)
    this_rule["rules"][0]["pattern"][p_id]["prefix"] = this_prefix
    result.append(copy.deepcopy(this_rule))
    this_rule["rules"][0]["pattern"][p_id]["is_required"] = "false"
    result.append(copy.deepcopy(this_rule))
    this_rule["rules"][0]["pattern"][p_id]["suffix"] = this_suffix
    result.append(copy.deepcopy(this_rule))
    this_rule["rules"][0]["pattern"][p_id]["is_required"] = "true"
    result.append(copy.deepcopy(this_rule))
    this_rule["rules"][0]["pattern"][p_id]["prefix"] = ""
    result.append(copy.deepcopy(this_rule))
    this_rule["rules"][0]["pattern"][p_id]["is_required"] = "false"
    result.append(copy.deepcopy(this_rule))

    return result


def add_dependency(rule, pos_lst):
    result = list()
    dep_lst = dict()
    for p in pos_lst:
        for t in p:
            if t.i not in dep_lst:
                dep_lst[t.i] = list()
            dep = copy.deepcopy(DEFAULT_DEPENDENCY)
            dep["dependency"] = INV_DEP_MAP[t.dep_]
            dep["from"] = t.head.i
            dep["to"] = t.i
            if dep not in dep_lst[t.i]:
                dep_lst[t.i].append(dep)
    dep_lst = {i:dep_lst[i] for i in dep_lst if len(dep_lst[i]) == 1}
    for key in dep_lst:
        temp_lst = copy.deepcopy(result)
        for a_rule in temp_lst:
            this_rule = copy.deepcopy(a_rule)
            this_rule["rules"][0]["dependencies"].append(copy.deepcopy(dep_lst[key][0]))
            result.append(copy.deepcopy(this_rule))
        this_rule = copy.deepcopy(rule)
        this_rule["rules"][0]["dependencies"].append(copy.deepcopy(dep_lst[key][0]))
        result.append(copy.deepcopy(this_rule))
    return result


def longest_docs(l):
    result = []
    length = len(l[0])
    for ll in l:
        if len(ll) > length:
            result = [ll]
            length = len(ll)
        elif len(ll) == length:
            result.append(ll)
    return result


def infer_rule(nlp_doc, nlp, p, t):
    positive_docs = [nlp(i) for i in p]
    longest_positive_docs = longest_docs(positive_docs)
    pos_strings = [str(i) for i in positive_docs]
    match_length_lst = sorted(list(set([len(x) for x in positive_docs])))

    negative_docs = []
    for i in range(len(nlp_doc) - match_length_lst[0] + 1):
        for match_length in match_length_lst:
            span = nlp_doc[i:i + match_length]
            sub_doc = nlp([k["value"].decode("utf-8") for k in t.extract(str(span), lowercase=False)])
            if str(sub_doc) not in pos_strings:
                negative_docs.append(sub_doc)

    positive_instances = random.sample(longest_positive_docs, 3) if len(
        longest_positive_docs) > 3 else longest_positive_docs
    base_rule_results = list()

    field_rules_lst = create_rule_lst(positive_instances)

    result_lst = []
    for iter_num in range(3):
        for field_rules in field_rules_lst:
            extractions = extract(field_rules, nlp_doc, nlp)

            r = calc_ratio(extractions, positive_docs, negative_docs, t, nlp)

            base_rule_results.append((r, field_rules))

        base_rule_results.sort(key=lambda t: t[0], reverse=True)
        base_rule_r = base_rule_results[0][0]
        base_rule = base_rule_results[0][1]
        best_rule_lst_whole = [(get_score(base_rule), base_rule)]

        rr = base_rule_r
        pattern_lst = copy.deepcopy(base_rule["rules"][0]["pattern"])

        p_id_lst = range(len(pattern_lst))
        random.shuffle(p_id_lst)
        for p_id in p_id_lst:
            pattern = pattern_lst[p_id]
            new_rule_lst = list()
            best_rule_lst_whole = sorted(best_rule_lst_whole, key=lambda x: x[0])[:TOP_N]
            random.shuffle(best_rule_lst_whole)
            best_rule_lst = [d[1] for d in best_rule_lst_whole]
            if pattern["type"] == "punctuation":
                for base_rule in best_rule_lst:
                    new_rule_lst += add_punct_constrain(base_rule, p_id, longest_positive_docs)

            if pattern["type"] == "number":
                for base_rule in best_rule_lst:
                    new_rule_lst += add_number_constrain(base_rule, p_id, longest_positive_docs)

            if pattern["type"] == "word" and pattern["contain_digit"] == "true":
                for base_rule in best_rule_lst:
                    new_rule_lst += add_shape_constrain(base_rule, p_id, longest_positive_docs)
                    new_rule_lst += add_word_constrain(base_rule, p_id, longest_positive_docs)

            if pattern["type"] == "word" and pattern["contain_digit"] != "true":
                for base_rule in best_rule_lst:
                    new_rule_lst += add_word_constrain(base_rule, p_id, longest_positive_docs)

            if new_rule_lst:
                for new_rule in new_rule_lst:
                    extractions = extract(new_rule, nlp_doc, nlp)
                    new_score = get_score(new_rule)
                    new_r = calc_ratio(extractions, positive_docs, negative_docs, t, nlp)
                    if rr[0] < new_r[0]:
                        best_rule_lst_whole = [(new_score, copy.deepcopy(new_rule))]
                        rr = new_r
                    elif rr[0] == new_r[0]:
                        if rr[1] < new_r[1]:
                            best_rule_lst_whole = [(new_score, copy.deepcopy(new_rule))]
                            rr = new_r
                        elif rr[1] == new_r[1]:
                            if rr[2] < new_r[2]:
                                best_rule_lst_whole = [(new_score, copy.deepcopy(new_rule))]
                                rr = new_r
                            elif rr[2] == new_r[2]:
                                best_rule_lst_whole.append((new_score, copy.deepcopy(new_rule)))

        result_lst += best_rule_lst_whole

    best_rule_lst_whole = sorted(result_lst, key=lambda x: x[0])[:TOP_N]
    random.shuffle(best_rule_lst_whole)
    return best_rule_lst_whole[0][1]["rules"][0]
