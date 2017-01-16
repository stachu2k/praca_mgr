import datetime


def roman_to_arabic(value):
    choices = {'I': '1', 'II': '2', 'III': '3', 'IV': '4', 'V': '5', 'VI': '6'}
    return choices.get(value, '1')


def is_stationary(value):
    if value == 'stacjonarne':
        return True
    elif value == 'niestacjonarne':
        return False
    else:
        return True


def get_sem_type(value):
    choices = {'letni': 'l', 'zimowy': 'z'}
    return choices.get(value, 'z')


def get_classes_type(value):
    choices = {
        'WYKŁAD': 'WYK',
        'ĆWICZENIA': 'CW',
        'LABORATORIUM': 'LAB',
        'PROJEKT': 'PR',
        'SEMINARIUM': 'SEM'
    }
    return choices.get(value, 'WYK')


def str_to_date(value):
    return datetime.datetime.strptime(value, "%Y-%m-%d")


def str_to_time(value):
    return datetime.datetime.strptime(value, "%H:%M")


def get_short_name(specialization, studies_type, grade, year_of_study, sem_nr):
    spec_list = {
        'Inżynieria biomedyczna': 'IBM',
        'Automatyka i Robotyka': 'AiR',
        'Elektronika i Telekomunikacja': 'EiT',
        'Elektronika Przemysłowa': 'EP',
        'Elektrotechnika': 'ELE',
        'Informatyka': 'INF',
        'Technologie energetyki odnawialnej': 'TEO'
    }

    stac_or_ns = {True: 'stac.', False: 'ns.'}

    return "{0} {1} {2} {3}-go st. (sem. {4})".format(year_of_study, spec_list.get(specialization, specialization),
                                                      stac_or_ns.get(studies_type, 'stac.'), grade, sem_nr)
