"""Константы."""

ROLES = (
    ('anonymous', 'anon',),
    ('user', 'user'),
    ('admin', 'admin'),
    ('superuser', 'superuser'),
)

BLACK_LIST_OF_USERNAMES = ('me', 'ME', 'Me',
                           'user', 'USER', 'User',
                           'admin', 'ADMIN', 'Admin',
                           'admins', 'ADMINS', 'Admins',
                           'adm1n', 'ADM1N', 'adm1n',
                           'Adm1n', 'ADM1N', '4dm1n',
                           '4Dm1n', '4DM1N'
                           'moderator', 'Moderator', 'MODERATOR',
                           'm0d3r4t0r', 'M0d3r4t0r', 'm0d3rator',
                           'M0d3rator'
                           )

MAX_LENGTH_USERNAME = 150
MAX_LENGTH_EMAIL = 254
MAX_LENGTH_ROLE = 20
MAX_LENGTH_FIRSTNAME = 50
MAX_LENGTH_LASTNAME = 50
FOLLOWINGS_ON_PAGE = 10
