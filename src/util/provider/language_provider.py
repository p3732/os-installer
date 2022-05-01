# SPDX-License-Identifier: GPL-3.0-or-later

from threading import Lock
import os

from gi.repository import GObject, GnomeDesktop

from .global_state import global_state


# generated via language_codes_to_x_generator.py
language_to_default_locale = {
    'ab': 'ab_GE.UTF-8', 'aa': 'aa_DJ.UTF-8', 'af': 'af_ZA.UTF-8', 'ak': 'ak_GH.UTF-8', 'sq': 'sq_AL.UTF-8',
    'am': 'am_ET.UTF-8', 'ar': 'ar_EG.UTF-8', 'an': 'an_ES.UTF-8', 'hy': 'hy_AM.UTF-8', 'as': 'as_IN.UTF-8',
    'ae_AE': 'ar_AE.UTF-8', 'az': 'az_AZ.UTF-8', 'ba_BA': 'bs_BA.UTF-8', 'eu': 'eu_ES.UTF-8', 'be': 'be_BY.UTF-8',
    'bn': 'bn_BD.UTF-8', 'bh_BH': 'ar_BH.UTF-8', 'bi': 'bi_VU.UTF-8', 'bs': 'bs_BA.UTF-8', 'br': 'br_FR.UTF-8',
    'bg': 'bg_BG.UTF-8', 'my': 'my_MM.UTF-8', 'ca': 'ca_ES.UTF-8', 'ch_CH': 'de_CH.UTF-8', 'ce': 'ce_RU.UTF-8',
    'zh': 'zh_CN.UTF-8', 'cv': 'cv_RU.UTF-8', 'kw': 'kw_GB.UTF-8', 'co_CO': 'es_CO.UTF-8', 'cr_CR': 'es_CR.UTF-8',
    'hr': 'hr_HR.UTF-8', 'cs': 'cs_CZ.UTF-8', 'da': 'da_DK.UTF-8', 'dv': 'dv_MV.UTF-8', 'nl': 'nl_NL.UTF-8', 'dz':
    'dz_BT.UTF-8', 'en': 'en_US.UTF-8', 'en_GB': 'en_GB.UTF-8', 'eo': 'eo.UTF-8', 'et': 'et_EE.UTF-8',
    'ee_EE': 'et_EE.UTF-8', 'fo': 'fo_FO.UTF-8', 'fj_FJ': 'hif_FJ.UTF-8', 'fi': 'fi_FI.UTF-8', 'fr': 'fr_FR.UTF-8',
    'ff': 'ff_SN.UTF-8', 'gl': 'gl_ES.UTF-8', 'ka': 'ka_GE.UTF-8', 'de': 'de_DE.UTF-8', 'el': 'el_GR.UTF-8',
    'gu': 'gu_IN.UTF-8', 'ht': 'ht_HT.UTF-8', 'ha': 'ha_NG.UTF-8', 'he': 'he_IL.UTF-8', 'hi': 'hi_IN.UTF-8',
    'hu': 'hu_HU.UTF-8', 'ia': 'ia_FR.UTF-8', 'id': 'id_ID.UTF-8', 'ie_IE': 'en_IE.UTF-8', 'ga': 'ga_IE.UTF-8',
    'ig': 'ig_NG.UTF-8', 'ik': 'ik_CA.UTF-8', 'is': 'is_IS.UTF-8', 'it': 'it_IT.UTF-8', 'iu': 'iu_CA.UTF-8',
    'ja': 'ja_JP.UTF-8', 'kl': 'kl_GL.UTF-8', 'kn': 'kn_IN.UTF-8', 'kr_KR': 'ko_KR.UTF-8', 'ks': 'ks_IN.UTF-8@devanagari',
    'kk': 'kk_KZ.UTF-8', 'km': 'km_KH.UTF-8', 'rw': 'rw_RW.UTF-8', 'ky': 'ky_KG.UTF-8', 'kg_KG': 'ky_KG.UTF-8',
    'ko': 'ko_KR.UTF-8', 'ku': 'ku_TR.UTF-8', 'la_LA': 'lo_LA.UTF-8', 'lb': 'lb_LU.UTF-8', 'lg': 'lg_UG.UTF-8',
    'li': 'li_NL.UTF-8', 'ln': 'ln_CD.UTF-8', 'lo': 'lo_LA.UTF-8', 'lt': 'lt_LT.UTF-8', 'lu_LU': 'fr_LU.UTF-8',
    'lv': 'lv_LV.UTF-8', 'gv': 'gv_GB.UTF-8', 'mk': 'mk_MK.UTF-8', 'mg': 'mg_MG.UTF-8', 'ms': 'ms_MY.UTF-8',
    'ml': 'ml_IN.UTF-8', 'mt': 'mt_MT.UTF-8', 'mi': 'mi_NZ.UTF-8', 'mr': 'mr_IN.UTF-8', 'mn': 'mn_MN.UTF-8',
    'ne': 'ne_NP.UTF-8', 'ng_NG': 'en_NG.UTF-8', 'nb': 'nb_NO.UTF-8', 'nn': 'nn_NO.UTF-8', 'no': 'no_NO.UTF-8',
    'nr': 'nr_ZA.UTF-8', 'oc': 'oc_FR.UTF-8', 'cu_CU': 'es_CU.UTF-8', 'om': 'om_ET.UTF-8', 'or': 'or_IN.UTF-8',
    'os': 'os_RU.UTF-8', 'pa': 'pa_IN.UTF-8', 'fa': 'fa_IR.UTF-8', 'pl': 'pl_PL.UTF-8', 'ps': 'ps_AF.UTF-8',
    'pt': 'pt_BR.UTF-8', 'ro': 'ro_RO.UTF-8', 'ru': 'ru_RU.UTF-8', 'sa': 'sa_IN.UTF-8', 'sc': 'sc_IT.UTF-8',
    'sd': 'sd_IN.UTF-8', 'se': 'se_NO.UTF-8', 'sm': 'sm_WS.UTF-8', 'sg_SG': 'en_SG.UTF-8', 'sr': 'sr_RS.UTF-8',
    'gd': 'gd_GB.UTF-8', 'sn_SN': 'wo_SN.UTF-8', 'si': 'si_LK.UTF-8', 'sk': 'sk_SK.UTF-8', 'sl': 'sl_SI.UTF-8',
    'so': 'so_SO.UTF-8', 'st': 'st_ZA.UTF-8', 'es': 'es_ES.UTF-8', 'sw': 'sw_KE.UTF-8', 'ss': 'ss_ZA.UTF-8',
    'sv': 'sv_SE.UTF-8', 'ta': 'ta_IN.UTF-8', 'te': 'te_IN.UTF-8', 'tg': 'tg_TJ.UTF-8', 'th': 'th_TH.UTF-8',
    'ti': 'ti_ER.UTF-8', 'bo': 'bo_CN.UTF-8', 'tk': 'tk_TM.UTF-8', 'tl': 'tl_PH.UTF-8', 'tn': 'tn_ZA.UTF-8',
    'to': 'to_TO.UTF-8', 'tr': 'tr_TR.UTF-8', 'ts': 'ts_ZA.UTF-8', 'tt': 'tt_RU.UTF-8', 'tw_TW': 'zh_TW.UTF-8',
    'ug': 'ug_CN.UTF-8', 'uk': 'uk_UA.UTF-8', 'ur': 'ur_PK.UTF-8', 'uz': 'uz_UZ.UTF-8@cyrillic', 've': 've_ZA.UTF-8',
    'vi': 'vi_VN.UTF-8', 'wa': 'wa_BE.UTF-8', 'cy': 'cy_GB.UTF-8', 'wo': 'wo_SN.UTF-8', 'fy': 'fy_NL.UTF-8',
    'xh': 'xh_ZA.UTF-8', 'yi': 'yi_US.UTF-8', 'yo': 'yo_NG.UTF-8', 'za_ZA': 'zu_ZA.UTF-8', 'zu': 'zu_ZA.UTF-8'}


class LanguageInfo(GObject.GObject):
    __gtype_name__ = __qualname__
    name: str
    language_code: str
    locale: str

    def __init__(self, name, language_code, locale):
        super().__init__()

        self.name = name
        self.language_code = language_code
        self.locale = locale


class LanguageProvider:
    languages_loaded = False
    languages_loading_lock = Lock()

    def _assert_languages_loaded(self):
        with self.languages_loading_lock:
            if not self.languages_loaded:
                self.suggested_languages, self.all_languages = self.languages.result()
                self.languages = None
                self.languages_loaded = True

    def _get_all_languages(self, locale):
        translated = []
        for info in self.all_languages:
            info.name = GnomeDesktop.get_language_from_code(
                info.language_code, locale)
            translated.append(info)
        return translated

    def _get_default_locale(self, language):
        if language in language_to_default_locale:
            return language_to_default_locale[language]
        else:
            return None

    def _get_existing_translations(self, localedir):
        # English always exists
        existing_translations = {'en'}

        # check what translations exist in the locale folder
        for file in os.scandir(localedir):
            if file.is_dir():
                locale_folder = os.path.join(file.path, 'LC_MESSAGES')
                if os.path.isdir(locale_folder):
                    for locale_file in os.scandir(locale_folder):
                        if locale_file.name == 'os-installer.mo':
                            language = os.path.basename(file.path)
                            existing_translations.add(language)
        return existing_translations

    def _get_language_info(self, language_code, locale=None):
        if not locale:
            locale = self._get_default_locale(language_code)
        name = GnomeDesktop.get_language_from_code(language_code, locale)
        if not name:
            print(f'Distribution developer hint: {name}'
                  'is not available as a locale in current system.')
        else:
            return LanguageInfo(name, language_code, locale)

    def _get_languages(self, localedir):
        translations = self._get_existing_translations(localedir)

        all_languages = []
        for language_code in translations:
            language_info = self._get_language_info(language_code)
            if not language_info:
                continue
            all_languages.append(language_info)
        all_languages.sort(key=lambda k: k.name)

        suggested_languages = []
        suggested_codes = global_state.get_config('suggested_languages')
        if suggested_codes and len(suggested_codes) > 0:
            for language_info in all_languages:
                if language_info.language_code in suggested_codes:
                    suggested_languages.append(language_info)

        return (suggested_languages, all_languages)

    ### public methods ###

    def get_all_languages(self):
        self._assert_languages_loaded()
        return self.all_languages

    def get_all_languages_translated(self):
        self._assert_languages_loaded()
        locale = global_state.get_config('locale')
        return self._get_all_languages(locale)

    def get_suggested_languages(self):
        self._assert_languages_loaded()
        return self.suggested_languages

    def has_additional_languages(self):
        self._assert_languages_loaded()
        return len(self.suggested_languages) < len(self.all_languages)

    def prepare(self):
        # load all languages from existing translations
        localedir = global_state.get_config('localedir')
        self.languages = global_state.thread_pool.submit(
            self._get_languages, localedir=localedir)


language_provider = LanguageProvider()
