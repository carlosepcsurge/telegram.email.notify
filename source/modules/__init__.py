"""
modules for transform
"""
from html2text import convert
from models import SavedSource

MARKUP = '###text_mode markdown'
BUTTONS = '###buttons'
NBSP = chr(0xC2) + chr(0xA0)


def store(label, subj, body):
    """
    default handler for store incoming messages
    """
    SavedSource(label=label, subject=subj, body=body).put()
    return subj + '\n' + convert(body, extract_link=True).replace(NBSP, ' ')


def is_present(marks, text):
    """
    return True, if all marks present in given text
    """
    return all([mark in text for mark in marks])


def by_subj(subj, body, text, label, prefix, handlers):  # pylint: disable=too-many-arguments
    """
    process message by subject
    """
    for marks, func in handlers:
        if is_present(marks, subj):
            return prefix + '\n'.join(func(subj, text))

    # unknown subject, save to db for analizing and return default answer
    SavedSource(label=label, subject=subj, body=body).put()

    return prefix + subj + '\n' + text
