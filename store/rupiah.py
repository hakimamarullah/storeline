import locale

def rupiah_format(angka, with_prefix=False, desimal=2):
    # locale.setlocale(locale.LC_NUMERIC, 'IND')
    locale.setlocale(locale.LC_ALL, 'de_DE.utf8')
    rupiah = locale.format("%.*f", (desimal, angka), True)
    if with_prefix:
        return "Rp.{}".format(rupiah)
    return rupiah
