# from address_segmentation.utils import *
import re
from db.store import *
import string

curfolder = 'address_segmentation'

folders = {
    'data-source': 'db/data-src',
    'model-source': 'db/model-src',
    'log': 'db/log',
    'image': 'db/image-src'
}

files = {
    'data-source': { 'dictionary': 'dictionary.json' },
    'model-source': {'name': 'model_name.pkl', 'address': 'model_address.pkl', 'phone': 'model_phone.pkl'},
    'log': {'log': 'log.xlsx', 'wlog': 'wlog.xlsx'},
    'image': {}
}

# tmp = loadJson(curfolder + '/' + folders['data-source'] + '/' + files['data-source']['dictionary'])
tmp = loadJson(folders['data-source'] + '/' + files['data-source']['dictionary'])
nameTermSet = tmp['name-term-set']
addressTermSet = tmp['address-term-set']
phoneTermSet = tmp['phone-term-set']

addressBeginningTermSet = tmp['address-beginning-term-set']

streetTermSet = tmp['street-term-set']
wardDistrictTermSet = tmp['ward-district-term-set']
cityTermSet = tmp['city-term-set']

asi = tmp['ascii']
unic = tmp['unicode']
upchars = tmp['upper-characters']

_f = lambda x: {'layer_' + str(i): {'w': x[0], 'b': x[1]} for i, x in enumerate(x.weights)}

models = {
    'name': _f(loadPKL(folders['model-source'] + '/' + files['model-source']['name'])),
    'address': _f(loadPKL(folders['model-source'] + '/' + files['model-source']['address'])),
    'phone': _f(loadPKL(folders['model-source'] + '/' + files['model-source']['phone'])),
}

skip_punctuation = ' .'
rm_preprocessed_punctuation = string.punctuation + string.whitespace # """ ,"""


# _punc = {"!": 1, "\"": 0.5, "#": 1, "$": 1, "%": 1, "&": 1, "'": 1, "(": 0.5, ")": 1, "*": 1, "+": 0.5, ",": 1,
#          "-": 0.8, ".": 0.8, "/": 0.5, ":": 1, ";": 1, "<": 1, "=": 1, ">": 1, "?": 1, "@": 0.8, "[": 0.5, "\\": 0.5,
#          "]": 1, "^": 1, "_": 1, "`": 1, "{": 0.5, "|": 1, "}": 1, "~": 1}
# _whitespace = {" ": 0.1, "\t": 1, "\n": 1, "\r": 1, "\v": 1, "\f": 1}

_punc = {"!": 1, "\"": 0.5, "#": 1, "$": 1, "%": 1, "&": 1, "'": 1, "(": 0.5, ")": 1, "*": 1, "+": 0.5, ",": 1,
         "-": 0.8, ".": 0.8, "/": 0.5, ":": 0.1, ";": 1, "<": 1, "=": 1, ">": 1, "?": 1, "@": 0.8, "[": 0.5, "\\": 0.5,
         "]": 1, "^": 1, "_": 1, "`": 1, "{": 0.5, "|": 1, "}": 1, "~": 1, " ": 0.2, "\t": 1, "\n": 1, "\r": 1, "\v": 1, "\f": 1}

# split_characters = _punc.copy()
# split_characters.update(_whitespace)
split_characters = _punc
viableCharacters = string.printable + unic

featureConfig = {
    'name': [
        # ('length', True),
        # (['', '', ''], False)

        ('length', False),

        ('#ascii', False),
        ('#digit', False),
        ('#punctuation', False),

        ('%ascii-adp', True),
        ('%digit-adp', True),
        ('%punctuation-adp', False),

        ('digit-adp/ascii-adp', True),

        ('%ascii', False),
        ('%digit', False),
        ('%punctuation', False),

        ('%keyword-name', True),
        ('%keyword-address', True),
        ('%keyword-phone', True),

        ('#max-digit-skip-all-punctuation', False),
        ('b#max-digit-skip-all-punctuation >= 8', True),
        ('%max-digit-skip-all-punctuation', False),
        ('#max-digit-skip-space-&-dot', False),
        ('%max-digit-skip-space-&-dot', False),

        ('bfirst-character-digit', True),
        ('bfirst-character-ascii', True),
        ('blast-character-digit', True),
        ('blast-character-ascii', True),

        ('b#ascii >= 7', False),
        ('b#digit >= 8', False),

        ('b,', False),
        ('1/length', True)
    ],
    'address': [
        # ('%ascii-adp', True),
        # (['', '', ''], False)

        ('length', False),

        ('#ascii', False),
        ('#digit', False),
        ('#punctuation', False),

        ('%ascii-adp', True),
        ('%digit-adp', True),
        ('%punctuation-adp', False),

        ('digit-adp/ascii-adp', True),

        ('%ascii', False),
        ('%digit', False),
        ('%punctuation', False),

        ('%keyword-name', True),
        ('%keyword-address', True),
        ('%keyword-phone', True),

        ('bkeyword-address-beginning', False),
        ('bStreet-Term', False),
        ('bWardDistrict-Term', False),
        ('bCity-Term', False),

        ('bfirst-term-address', True),

        ('#max-digit-skip-all-punctuation', False),
        ('b#max-digit-skip-all-punctuation >= 8', True),
        ('%max-digit-skip-all-punctuation', False),
        ('#max-digit-skip-space-&-dot', False),
        ('%max-digit-skip-space-&-dot', False),

        ('bfirst-character-digit', True),
        ('bfirst-character-ascii', True),
        ('bsecond-character-digit', True),
        ('bsecond-character-ascii', True),
        ('blast-character-digit', False),
        ('blast-character-ascii', False),

        ('b#ascii >= 7', False),
        ('b#digit >= 8', False),

        ('b/', True)
    ],
    'phone': [
        # ('%digit-adp', True),
        # (['', '', ''], False)

        ('length', False),

        ('#ascii', False),
        ('#digit', False),
        ('#punctuation', False),

        ('%ascii-adp', True),
        ('%digit-adp', True),
        ('%punctuation-adp', False),

        ('digit-adp/ascii-adp', True),

        ('%ascii', False),
        ('%digit', False),
        ('%punctuation', False),

        ('%keyword-name', True),
        ('%keyword-address', True),
        ('%keyword-phone', True),

        ('bStreet-Term', False),
        ('bWardDistrict-Term', False),
        ('bCity-Term', False),

        ('#max-digit-skip-all-punctuation', False),
        ('b#max-digit-skip-all-punctuation >= 8', True),
        ('%max-digit-skip-all-punctuation', False),
        ('#max-digit-skip-space-&-dot', False),
        ('%max-digit-skip-space-&-dot', False),

        ('bfirst-character-digit', True),
        ('bfirst-character-ascii', True),
        ('blast-character-digit', True),
        ('blast-character-ascii', True),

        ('b#ascii >= 7', False),
        ('b#digit >= 8', True),

        ('b+', True),
        ('b()', True)
    ]
}


term_regex = {
    'name': re.compile(r"(?:^|(?<= ))(" + '|'.join(tmp['title']) + ")(?:(?= )|$)"),
    'address': re.compile(r"(?:^|(?<= ))(" + '|'.join(tmp['address']) + ")(?:(?= )|$)"),
    'phone': re.compile(r"(?:^|(?<= ))(" + '|'.join(tmp['phone']) + ")(?:(?= )|$)"),
    'company': re.compile(r"(?:^|(?<= ))(" + '|'.join(tmp['company']) + ")(?:(?= )|$)"),
    'fax': re.compile(r"(?:^|(?<= ))(" + '|'.join(tmp['fax']) + ")(?:(?= )|$)"),

    'email': re.compile(r"(?:^|(?<= ))(" + '|'.join(tmp['email']) + ")(?:(?= )|$)"),
    'url': re.compile(r"(?:^|(?<= ))(" + '|'.join(tmp['url']) + ")(?:(?= )|$)"),

    'unknown': re.compile(r"")
}

email_regex = re.compile(r"(?:^|(?<= ))([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)(?:(?= )|$)")
url_regex = re.compile(r"""(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))""")
