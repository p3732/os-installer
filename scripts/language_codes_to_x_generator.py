import gi
gi.require_version('GnomeDesktop', '3.0')  # noqa: E402
from gi.repository import GnomeDesktop
import langtable


# from https://en.wikipedia.org/wiki/ISO_639
language_codes = [
    'ab', 'aa', 'af', 'ak', 'sq', 'am', 'ar', 'an', 'hy', 'as', 'av', 'ae', 'ay', 'az', 'bm', 'ba', 'eu', 'be', 'bn',
    'bh', 'bi', 'bs', 'br', 'bg', 'my', 'ca', 'ch', 'ce', 'ny', 'zh', 'cv', 'kw', 'co', 'cr', 'hr', 'cs', 'da', 'dv',
    'nl', 'dz', 'en', 'en_GB', 'eo', 'et', 'ee', 'fo', 'fj', 'fi', 'fr', 'ff', 'gl', 'ka', 'de', 'el', 'gn', 'gu', 'ht',
    'ha', 'he', 'hz', 'hi', 'ho', 'hu', 'ia', 'id', 'ie', 'ga', 'ig', 'ik', 'io', 'is', 'it', 'iu', 'ja', 'jv', 'kl',
    'kn', 'kr', 'ks', 'kk', 'km', 'ki', 'rw', 'ky', 'kv', 'kg', 'ko', 'ku', 'kj', 'la', 'lb', 'lg', 'li', 'ln', 'lo',
    'lt', 'lu', 'lv', 'gv', 'mk', 'mg', 'ms', 'ml', 'mt', 'mi', 'mr', 'mh', 'mn', 'na', 'nv', 'nd', 'ne', 'ng', 'nb',
    'nn', 'no', 'ii', 'nr', 'oc', 'oj', 'cu', 'om', 'or', 'os', 'pa', 'pi', 'fa', 'pl', 'ps', 'pt', 'qu', 'rm', 'rn',
    'ro', 'ru', 'sa', 'sc', 'sd', 'se', 'sm', 'sg', 'sr', 'gd', 'sn', 'si', 'sk', 'sl', 'so', 'st', 'es', 'su', 'sw',
    'ss', 'sv', 'ta', 'te', 'tg', 'th', 'ti', 'bo', 'tk', 'tl', 'tn', 'to', 'tr', 'ts', 'tt', 'tw', 'ty', 'ug', 'uk',
    'ur', 'uz', 've', 'vi', 'vo', 'wa', 'cy', 'wo', 'fy', 'xh', 'yi', 'yo', 'za', 'zu']


def handle_results(func, language_code, storage, duplicates):
    results = func(languageId=language_code)
    if len(results) > 0:
        storage[language_code] = results[0]
        for result in results[1:]:
            duplicates.add((language_code, result))
        return True
    return False


def language_2_x(func):
    duplicates_set = set()
    results = {}
    for language_code in language_codes:
        if not handle_results(func, language_code, results, duplicates_set):
            long_language_code = language_code + '_' + language_code.upper()
            if not handle_results(func, long_language_code, results, duplicates_set):
                print(f"Can't convert country code '{language_code}' nor"
                      f"'{long_language_code}' to locale")
                if not GnomeDesktop.language_has_translations(language_code) \
                   and not GnomeDesktop.language_has_translations(language_code):
                    print('No translations exist.')
    return results, duplicates_set


def normalize_keyboards(keyboards):
    normalized = {}
    for code in keyboards:
        normalized[code] = keyboards[code].replace('(', '+').replace(')', '')
    return normalized


code_to_locale, locale_dups = language_2_x(langtable.list_locales)
code_to_keyboard, keyboard_dups = language_2_x(langtable.list_common_keyboards)
code_to_keyboard = normalize_keyboards(code_to_keyboard)

print('-------------')
print('---Results---')
print('-------------')
print('language code -> locale')
print('-------------')
print(code_to_locale)
print('----------')
print('language code -> default keyboard')
print('----------')
print(code_to_keyboard)
print('----------')
print('locale duplicates')
print('----------')
print(locale_dups)
print('----------')
print('keyboard duplicates')
print('----------')
print(keyboard_dups)
