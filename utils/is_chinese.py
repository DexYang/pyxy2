中文符号 = {
    u'\u3002': 1,
    u'\uff1b': 1,
    u'\uff0c': 1,
    u'\uff1a': 1,
    u'\u2018': 1,
    u'\u2019': 1,
    u'\u201c': 1,
    u'\u201d': 1,
    u'\uff08': 1,
    u'\uff09': 1,
    u'\u3001': 1,
    u'\uff1f': 1,
    u'\u300a': 1,
    u'\u300b': 1,
    u'\uff01': 1,
    u'\u2014': 1,
    u'\u2026': 1,
    u'\u2013': 1,
    u'\uff0e': 1
}


def is_chinese(uchar):
    if len(uchar) != 1:
        raise TypeError('expected a character, but a string found!')
    if u'\u4e00' <= uchar <= u'\u9fff':
        return True
    elif uchar in 中文符号:
        return True
    else:
        return False