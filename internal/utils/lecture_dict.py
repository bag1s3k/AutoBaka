import logging
from internal.utils.logging_setup import setup_logging

logger = logging.getLogger(__name__)
setup_logging()

subject_dict = {
    "Cesky jazyk a literatura": "CJL",
    "Anglicky jazyk": "AJ",
    "Konverzace v anglickem jazyce": "KAJ",
    "Technicka anglictina": "TAJ",
    "Nemecky jazyk": "NJ",
    "Obcanska nauka": "ON",
    "Matematika": "M",
    "Telesna vychova": "TV",
    "Programovani": "Prog",
    "Operacni systemy": "OSy",
    "Operacni systemy - cviceni": "Osyc",
    "Informacni site": "IS",
    "Informacni site - cviceni": "ISc",
    "Ekonomika a pravo": "EaP",
    "Programovani II": "Prg2"
}

def short(to_find):
    """Translate name of subject to shorter version (like in timetable)
    :param to_find: value to find
    :return: if value is not found return it"""
    if to_find not in subject_dict:
        logger.error(f"The value: {to_find} wasn't translated")
    return subject_dict.get(to_find, to_find)