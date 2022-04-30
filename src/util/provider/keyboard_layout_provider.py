# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import GObject
from gi.repository.GnomeDesktop import XkbInfo


# generated via language_codes_to_x_generator.py
language_to_default_keyboard = {
    'ab': 'ru', 'aa': 'us', 'af': 'us(intl)', 'ak': 'us(altgr-intl)', 'sq': 'al', 'am': 'et', 'ar': 'ara', 'an': 'es',
    'hy': 'am', 'as': 'in(eng)', 'av': 'ru', 'ae_AE': 'ara', 'ay': 'latam', 'az': 'az', 'bm': 'us', 'ba': 'ru(bak)',
    'eu': 'es', 'be': 'by', 'bn': 'in(eng)', 'bh_BH': 'ara', 'bi': 'us(euro)', 'bs': 'ba', 'br': 'fr(bre)', 'bg': 'bg',
    'my': 'mm', 'ca': 'es(cat)', 'ch': 'us', 'ce': 'ru', 'ny': 'us', 'zh': 'cn', 'cv': 'ru(cv)', 'kw': 'gb',
    'co': 'fr(oss)', 'cr_CR': 'latam', 'hr': 'hr', 'cs': 'cz', 'da': 'dk', 'dv': 'mv', 'nl': 'us(euro)', 'dz': 'bt',
    'en': 'us', 'en_GB': 'gb', 'eo': 'us(altgr-intl)', 'et': 'ee', 'ee': 'us', 'fo': 'fo', 'fj': 'us', 'fi': 'fi',
    'fr': 'fr(oss)', 'ff': 'fr(oss)', 'gl': 'es', 'ka': 'ge', 'de': 'de(nodeadkeys)', 'el': 'gr', 'gn': 'us',
    'gu': 'in(eng)', 'ht': 'latam', 'ha': 'ng(hausa)', 'he': 'il', 'hz': 'us', 'hi': 'in(eng)', 'ho': 'us',
    'hu': 'hu', 'ia': 'us(euro)', 'id': 'us', 'ie': 'us', 'ga': 'ie(CloGaelach)', 'ig': 'ng(igbo)', 'ik': 'ca(eng)',
    'io': 'us', 'is': 'is', 'it': 'it', 'iu': 'ca(ike)', 'ja': 'jp', 'jv': 'us', 'kl': 'us', 'kn': 'in(eng)',
    'kr': 'us', 'ks': 'in(eng)', 'kk': 'kz', 'km': 'kh', 'ki': 'us', 'rw': 'us', 'ky': 'kg', 'kv': 'ru(kom)',
    'kg': 'fr(oss)', 'ko': 'kr', 'ku': 'tr(ku)', 'kj': 'us', 'la': 'it', 'lb': 'fr(oss)', 'lg': 'us', 'li': 'us(euro)',
    'lo': 'la', 'lt': 'lt', 'lu': 'us', 'lv': 'lv', 'gv': 'gb', 'mk': 'mk', 'mg': 'us', 'ms': 'us', 'ml': 'in(eng)',
    'mt': 'mt', 'mi': 'us', 'mr': 'in(eng)', 'mh': 'us', 'mn': 'mn', 'na': 'us', 'nv': 'us', 'nd': 'us', 'ne': 'np',
    'ng': 'us', 'nb': 'no', 'nn': 'no', 'no': 'no', 'ii': 'us', 'nr': 'us', 'oc': 'fr(oss)', 'cu': 'bg', 'om': 'us',
    'or': 'in(eng)', 'os': 'ru(os_winkeys)', 'pa': 'in(eng)', 'fa': 'ir', 'pl': 'pl', 'ps': 'af(ps)', 'pt': 'br',
    'qu': 'latam', 'rm': 'ch', 'rn': 'us', 'ro': 'ro', 'ru': 'ru', 'sa': 'in(eng)', 'sc': 'it', 'sd': 'in(eng)',
    'se': 'no', 'sm': 'us(euro)', 'sg': 'us', 'sr': 'rs', 'gd': 'gb', 'sn': 'us', 'si': 'us', 'sk': 'sk', 'sl': 'si',
    'so': 'us', 'st': 'us', 'es': 'es', 'su': 'us', 'sw': 'ke', 'ss': 'us', 'sv': 'se', 'ta': 'in(eng)', 'te': 'in(eng)',
    'tg': 'tj', 'th': 'th', 'ti': 'et', 'bo': 'us', 'tk': 'tm', 'tl': 'ph', 'tn': 'za', 'to': 'us', 'tr': 'tr',
    'ts': 'us', 'tt': 'ru(tt)', 'tw': 'us', 'ty': 'fr(oss)', 'ug': 'cn(ug)', 'uk': 'ua', 'ur': 'pk', 'uz': 'uz',
    've': 'za', 'vi': 'vn', 'vo': 'de(nodeadkeys)', 'wa': 'be(oss)', 'cy': 'gb', 'wo': 'sn', 'fy': 'us(euro)',
    'xh': 'us', 'yi': 'us', 'yo': 'ng(yoruba)', 'za': 'us', 'zu': 'us'}


class KeyboardInfo(GObject.GObject):
    __gtype_name__ = __qualname__
    name: str
    layout: str

    def __init__(self, name, layout):
        super().__init__()

        self.name = name
        self.layout = layout


def get_default_layout(language_code):
    if language_code in language_to_default_keyboard:
        return language_to_default_keyboard[language_code]
    else:
        return 'us'


def get_layouts_for(language_short_hand, language):
    xkb_info = XkbInfo()
    layouts = xkb_info.get_layouts_for_language(language_short_hand)

    named_layouts = []
    for layout in layouts:
        name = xkb_info.get_layout_info(layout).display_name
        named_layouts.append(KeyboardInfo(name, layout))

    # Sort the layouts, prefer those starting with language name or matching language short hand. Then by name.
    return sorted(named_layouts, key=lambda o:
                  (not o.name.startswith(language),
                   not o.layout.startswith(language_short_hand),
                   o.name))
