# -*- coding: utf-8 -*-
SECOND_MS = 1000
MINUTE_MS = 60*SECOND_MS
HOUR_MS = 60*MINUTE_MS
DAY_MS = 24*HOUR_MS
WEEK_MS = 7*DAY_MS
YEAR_MS = 365*DAY_MS

MINUTE_S = 60
HOUR_S = 60*MINUTE_S
DAY_S = 24*HOUR_S
WEEK_S = 7*DAY_S
YEAR_S = 365*DAY_S

# DayMaxEstimator
#TODO: Redundant? Warum nicht in portable_daymaxestimator.py?
TIME_CALC_FTEMPO_SETPOINT_MS = 6 * MINUTE_MS
TIME_INTERVAL_FTEMPO_SETPOINT_MS = 3 * HOUR_MS

listReplacements = (
    ('_', '-UNDERSCORE-'),
    ('/', '-SLASH-'),
    (';', '-SEMICOLON-'),
    (':', '-COLON-'),
    ("'", '-APR-'),
    ('"', '-APR-'),
    ('*', '-STR-'),
)
