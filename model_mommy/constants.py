import string

# ref: http://docs.python.org/howto/unicode.html
UNICODE_RANGE = (0, 1114111)
LATIN1_RANGE = (0, 255)
ASCII_RANGE = (0, 127)

LATIN1_TABLE = u''.join([unichr(i) for i in range(256)])
ASCII_TABLE = LATIN1_TABLE[:128]
SLUG_TABLE = string.ascii_lowercase + string.digits + "-_"

LEAVE_TO_CHANCE = (True, False, False, False)  # +- 25% chance
TEXT_MAX_LENGTH = 500
MIN_INT, MAX_INT = -2147483648, 2147483647
MIN_BIG_INT, MAX_BIG_INT = -9223372036854775808l, 9223372036854775807l
MIN_SMALL_INT, MAX_SMALL_INT = -32768, 32767
