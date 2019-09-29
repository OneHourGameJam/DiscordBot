from datetime import datetime as dt
from collections import namedtuple

Jam = namedtuple('Jam', 'number, theme, start_datetime, timediff')


def __get_jams(jams, api):
    return [Jam(**k) for k in api[jams]]


def ongoing(api):
    r"""Is there an ongoing jam?
    :return: bool
    """
    if len(api['current_jams']) == 0:
        return False
    else:
        return True


def get_time(api):
    r"""Gets the server time from the One Hour Game Jam API
    :return: datetime
    """
    return dt.strptime(api['now'], "%Y-%m-%d %H:%M:%S")


def get_theme(api):
    r"""Gets the theme of the ongoing jam.
    Returns None if there is no ongoing jam.
    """
    if not ongoing(api):
        return None

    return __get_jams('current_jams', api)[0].theme


def get_last_theme(api):
    r""" Gets the theme of the previous jam
    :return: str
    """
    return __get_jams('previous_jams', api)[-1].theme


def get_time_diff(api):
    r"""Gets the time remaining to either the end of the ongoing jam or the next jam
    :return: time
    """
    if ongoing(api):
        return __get_jams('current_jams', api)[0].timediff
    else:
        return __get_jams('upcoming_jams', api)[0].timediff


def get_next_jam_date(api):
    r"""Gets the date of the upcoming jam
    :return: datetime
    """
    return dt.strptime(__get_jams('upcoming_jams', api)[0].start_datetime, "%Y-%m-%d %H:%M:%S")


def get_jam_number(api):

    if ongoing(api):
        return __get_jams('current_jams', api)[0].number
    else:
        return __get_jams('upcoming_jams', api)[0].number
