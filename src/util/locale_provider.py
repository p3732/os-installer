from gi.repository import GnomeDesktop
import locale as Locale

locales = {
    'as_IN.UTF-8', 'pt_BR.UTF-8', 'am_ET.UTF-8', 'os_RU.UTF-8', 'ta_LK.UTF-8', 'ka_GE.UTF-8', 'ar_DZ.UTF-8',
    'nan_TW.UTF-8', 'el_GR.UTF-8', 'ta_IN.UTF-8', 'bo_CN.UTF-8', 'so_ET.UTF-8', 'sr_ME.UTF-8', 'hi_IN.UTF-8',
    'ru_RU.UTF-8', 'sk_SK.UTF-8', 'en_PH.UTF-8', 'en_BW.UTF-8', 'ur_PK.UTF-8', 'sm_WS.UTF-8', 'ik_CA.UTF-8',
    'sr_RS.UTF-8@latin', 'th_TH.UTF-8', 'en_US.UTF-8', 'tn_ZA.UTF-8', 'es_EC.UTF-8', 'zu_ZA.UTF-8',
    'nan_TW.UTF-8@latin', 'ar_SD.UTF-8', 'sw_KE.UTF-8', 'aa_ET.UTF-8', 'ar_TN.UTF-8', 'en_AG.UTF-8', 'es_ES.UTF-8',
    'aa_ER.UTF-8', 'gu_IN.UTF-8', 'pt_PT.UTF-8', 'he_IL.UTF-8', 'ar_AE.UTF-8', 'bg_BG.UTF-8', 'es_PE.UTF-8',
    'dv_MV.UTF-8', 'es_CR.UTF-8', 'kk_KZ.UTF-8', 'fi_FI.UTF-8', 'lg_UG.UTF-8', 'el_CY.UTF-8', 'fr_FR.UTF-8',
    'ar_EG.UTF-8', 'ak_GH.UTF-8', 'yo_NG.UTF-8', 'sr_RS.UTF-8', 'en_HK.UTF-8', 'es_MX.UTF-8', 'wae_CH.UTF-8',
    'lt_LT.UTF-8', 'fr_LU.UTF-8', 'kn_IN.UTF-8', 'te_IN.UTF-8', 'hak_TW.UTF-8', 've_ZA.UTF-8', 'dz_BT.UTF-8',
    'wa_BE.UTF-8', 'az_AZ.UTF-8', 'es_AR.UTF-8', 'gv_GB.UTF-8', 'hu_HU.UTF-8', 'ca_ES.UTF-8', 'mk_MK.UTF-8',
    'aa_ER.UTF-8@saaho', 'ar_SA.UTF-8', 'hy_AM.UTF-8', 'de_IT.UTF-8', 'lb_LU.UTF-8', 'mt_MT.UTF-8', 'en_IN.UTF-8',
    'sd_IN.UTF-8', 'ar_OM.UTF-8', 'bi_VU.UTF-8', 'kw_GB.UTF-8', 'en_NZ.UTF-8', 'sc_IT.UTF-8', 'li_NL.UTF-8',
    'tr_TR.UTF-8', 'af_ZA.UTF-8', 'uz_UZ.UTF-8@cyrillic', 'ts_ZA.UTF-8', 'so_DJ.UTF-8', 'en_IE.UTF-8', 'my_MM.UTF-8',
    'de_AT.UTF-8', 'ig_NG.UTF-8', 'ko_KR.UTF-8', 'de_BE.UTF-8', 'ms_MY.UTF-8', 'es_VE.UTF-8', 'sv_FI.UTF-8',
    'cy_GB.UTF-8', 'ar_IN.UTF-8', 'ha_NG.UTF-8', 'eu_ES.UTF-8', 'en_DK.UTF-8', 'yi_US.UTF-8', 'es_US.UTF-8',
    'mg_MG.UTF-8', 'ar_MA.UTF-8', 'cs_CZ.UTF-8', 'xh_ZA.UTF-8', 'nl_NL.UTF-8', 'es_DO.UTF-8', 'uk_UA.UTF-8',
    'mi_NZ.UTF-8', 'hr_HR.UTF-8', 'om_KE.UTF-8', 'eo.UTF-8', 'ja_JP.UTF-8', 'to_TO.UTF-8', 'be_BY.UTF-8@latin',
    'tt_RU.UTF-8@iqtelif', 'ar_IQ.UTF-8', 'it_IT.UTF-8', 'mn_MN.UTF-8', 'ug_CN.UTF-8', 'es_BO.UTF-8', 'rw_RW.UTF-8',
    'oc_FR.UTF-8', 'ss_ZA.UTF-8', 'ff_SN.UTF-8', 'ti_ER.UTF-8', 'sa_IN.UTF-8', 'es_CO.UTF-8', 'it_CH.UTF-8',
    'es_SV.UTF-8', 'vi_VN.UTF-8', 'fr_CA.UTF-8', 'de_LU.UTF-8', 'zh_CN.UTF-8', 'ro_RO.UTF-8', 'tk_TM.UTF-8',
    'ne_NP.UTF-8', 'nl_BE.UTF-8', 'ar_BH.UTF-8', 'es_CL.UTF-8', 'de_CH.UTF-8', 'ar_YE.UTF-8', 'sq_AL.UTF-8',
    'be_BY.UTF-8', 'is_IS.UTF-8', 'ar_QA.UTF-8', 'ky_KG.UTF-8', 'ca_ES.UTF-8@valencia', 'sv_SE.UTF-8', 'en_ZW.UTF-8',
    'lzh_TW.UTF-8', 'pa_PK.UTF-8', 'ar_JO.UTF-8', 'id_ID.UTF-8', 'ia_FR.UTF-8', 'de_LI.UTF-8', 'bn_BD.UTF-8',
    'es_HN.UTF-8', 'cv_RU.UTF-8', 'fy_NL.UTF-8', 'pa_IN.UTF-8', 'ks_IN.UTF-8@devanagari', 'ga_IE.UTF-8', 'nso_ZA.UTF-8',
    'sw_TZ.UTF-8', 'bo_IN.UTF-8', 'en_AU.UTF-8', 'wo_SN.UTF-8', 'lo_LA.UTF-8', 'az_IR.UTF-8', 'gl_ES.UTF-8',
    'ps_AF.UTF-8', 'gd_GB.UTF-8', 'sq_MK.UTF-8', 'no_NO.UTF-8', 'en_ZA.UTF-8', 'ar_SY.UTF-8', 'en_NG.UTF-8',
    'ru_UA.UTF-8', 'tg_TJ.UTF-8', 'da_DK.UTF-8', 'mr_IN.UTF-8', 'ln_CD.UTF-8', 'ti_ET.UTF-8', 'se_NO.UTF-8',
    'ce_RU.UTF-8', 'es_CU.UTF-8', 'li_BE.UTF-8', 'om_ET.UTF-8', 'an_ES.UTF-8', 'km_KH.UTF-8', 'nr_ZA.UTF-8',
    'nn_NO.UTF-8', 'ca_AD.UTF-8', 'zh_HK.UTF-8', 'lv_LV.UTF-8', 'es_PR.UTF-8', 'or_IN.UTF-8', 'fo_FO.UTF-8',
    'ca_IT.UTF-8', 'pl_PL.UTF-8', 'sd_IN.UTF-8@devanagari', 'en_IL.UTF-8', 'fr_CH.UTF-8', 'cmn_TW.UTF-8',
    'hif_FJ.UTF-8', 'ca_FR.UTF-8', 'en_GB.UTF-8', 'bn_IN.UTF-8', 'en_SG.UTF-8', 'nb_NO.UTF-8', 'es_PA.UTF-8',
    'tl_PH.UTF-8', 'ks_IN.UTF-8', 'fa_IR.UTF-8', 'tt_RU.UTF-8', 'si_LK.UTF-8', 'kl_GL.UTF-8', 'st_ZA.UTF-8',
    'bs_BA.UTF-8', 'zh_SG.UTF-8', 'br_FR.UTF-8', 'ur_IN.UTF-8', 'ar_SS.UTF-8', 'fr_BE.UTF-8', 'fy_DE.UTF-8',
    'es_UY.UTF-8', 'es_GT.UTF-8', 'es_NI.UTF-8', 'es_PY.UTF-8', 'et_EE.UTF-8', 'so_KE.UTF-8', 'en_ZM.UTF-8',
    'nl_AW.UTF-8', 'zh_TW.UTF-8', 'ht_HT.UTF-8', 'ar_LY.UTF-8', 'de_DE.UTF-8', 'ml_IN.UTF-8', 'sl_SI.UTF-8',
    'tr_CY.UTF-8', 'ar_KW.UTF-8', 'uz_UZ.UTF-8', 'ku_TR.UTF-8', 'en_CA.UTF-8', 'ar_LB.UTF-8', 'iu_CA.UTF-8',
    'aa_DJ.UTF-8', 'so_SO.UTF-8'}


class LocaleProvider:
    def __init__(self, global_state):
        self.global_state = global_state

    ### public methods ###

    def get_timezone(self):
        timezone = GnomeDesktop.WallClock().get_timezone()
        return timezone.get_identifier()

    def get_current_formats(self):
        formats = self.global_state.get_config('formats')
        if not formats:
            formats = self.global_state.get_config('locale')
            self.global_state.set_config('formats', formats)
        name = GnomeDesktop.get_country_from_locale(formats)
        if not name:
            # solely to prevent crashes, e.g. for Esperanto
            # TODO add to translatation
            name = 'Undefined'
        return (name, formats)

    def get_formats(self):
        formats = []
        # separate name set to prevent duplicates in list
        # see gnome-desktop issue https://gitlab.gnome.org/GNOME/gnome-shell/-/issues/3610
        names = set()
        translation_locale = self.global_state.get_config('locale')

        for locale in locales:
            name = GnomeDesktop.get_country_from_locale(locale, translation_locale)
            if name and not name in names:
                names.add(name)
                formats.append((name, locale))

        # return sorted (considers umlauts and such)
        return sorted(
            formats,
            key=lambda t: Locale.strxfrm(t[0])
        )
