from address_segmentation.utils import *

curfolder = 'address_segmentation'

folders = {
    'data-source': 'data-src',
    'model-source': 'model-src'
}

files = {
    'data-source': { 'dictionary': 'dictionary.json' },
    'model-source': {'name': 'model_name.pkl', 'address': 'model_address.pkl', 'phone': 'model_phone.pkl'}
}

tmp = loadJson(curfolder + '/' + folders['data-source'] + '/' + files['data-source']['dictionary'])
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

models = {
    'name': loadPKL(curfolder + '/' + folders['model-source'] + '/' + files['model-source']['name']),
    'address': loadPKL(curfolder + '/' + folders['model-source'] + '/' + files['model-source']['address']),
    'phone': loadPKL(curfolder + '/' + folders['model-source'] + '/' + files['model-source']['phone']),
}

skip_punctuation = ' .'
rm_preprocessed_punctuation = """ ,"""


_punc = {"!": 1, "\"": 0.5, "#": 1, "$": 1, "%": 1, "&": 1, "'": 1, "(": 0.5, ")": 1, "*": 1, "+": 0.5, ",": 1,
         "-": 0.8, ".": 0.8, "/": 0.5, ":": 1, ";": 1, "<": 1, "=": 1, ">": 1, "?": 1, "@": 0.8, "[": 0.5, "\\": 0.5,
         "]": 1, "^": 1, "_": 1, "`": 1, "{": 0.5, "|": 1, "}": 1, "~": 1}
_whitespace = {" ": 0.1, "\t": 1, "\n": 1, "\r": 1, "\v": 1, "\f": 1}

split_characters = _punc.copy()
split_characters.update(_whitespace)

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

        ('b#ascii >= 7', True),
        ('b#digit >= 8', False),

        ('b,', True),
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

        ('bStreet-Term', True),
        ('bWardDistrict-Term', True),
        ('bCity-Term', True),

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