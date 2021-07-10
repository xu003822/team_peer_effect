from os import environ

STATIC_URL = '/static/'

SESSION_CONFIGS = [
    dict(
        name='public_goods_team',
        display_name='A public goods experiment',
        num_demo_participants=4,
        app_sequence=['public_goods_individual_treatment'],
    ),
    dict(
        name='public_goods_team',
        display_name='A public goods experiment',
        num_demo_participants=12,
        app_sequence=['public_goods_majority_treatment'],
    ),
    dict(
        name='public_goods_team',
        display_name='A public goods experiment',
        num_demo_participants=12,
        app_sequence=['public_goods_random_ballot'],
    )
    ,
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0.1, participation_fee=5.00, doc=""
)

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
#REAL_WORLD_CURRENCY_CODE = 'CNY'
USE_POINTS = True
#POINTS_CUSTOM_NAME = '分'

ROOMS = [
    dict(
        name='Xian_Jiaotong',
        display_name='Xian_Jiaotong_experiment',
        participant_label_file='_rooms/econ101.txt',
        use_secure_urls=True
    ),
    dict(name='live_demo', display_name='Room for live demo (no participant labels)'),
]

#if environ.get('OTREE_PRODUCTION') not in {None, '', '0'}:
   # DEBUG = False
#else:
    #DEBUG = True

ADMIN_USERNAME = 'admin'

ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""
#environ['OTREE_PRODUCTION'] = '1'

# don't share this with anybody.
SECRET_KEY = '-04aty%acnfw&pa*c7f2-hb+2fv57zcy4(pajjfs-t@n4jeqin'

INSTALLED_APPS = ['otree']

# inactive session configs
# dict(name='trust', display_name="Trust Game", num_demo_participants=2, app_sequence=['trust', 'payment_info']),
# dict(name='prisoner', display_name="Prisoner's Dilemma", num_demo_participants=2,
#      app_sequence=['prisoner', 'payment_info']),
# dict(name='volunteer_dilemma', display_name="Volunteer's Dilemma", num_demo_participants=3,
#      app_sequence=['volunteer_dilemma', 'payment_info']),
# dict(name='cournot', display_name="Cournot Competition", num_demo_participants=2, app_sequence=[
#     'cournot', 'payment_info'
# ]),
# dict(name='dictator', display_name="Dictator Game", num_demo_participants=2,
#      app_sequence=['dictator', 'payment_info']),
# dict(name='matching_pennies', display_name="Matching Pennies", num_demo_participants=2, app_sequence=[
#     'matching_pennies',
# ]),
# dict(name='traveler_dilemma', display_name="Traveler's Dilemma", num_demo_participants=2,
#      app_sequence=['traveler_dilemma', 'payment_info']),
# dict(name='bargaining', display_name="Bargaining Game", num_demo_participants=2,
#      app_sequence=['bargaining', 'payment_info']),
# dict(name='common_value_auction', display_name="Common Value Auction", num_demo_participants=3,
#      app_sequence=['common_value_auction', 'payment_info']),
# dict(name='bertrand', display_name="Bertrand Competition", num_demo_participants=2, app_sequence=[
#     'bertrand', 'payment_info'
# ]),
# dict(name='public_goods_simple', display_name="Public Goods (simple version from tutorial)",
#      num_demo_participants=3, app_sequence=['public_goods_simple', 'payment_info']),
# dict(name='trust_simple', display_name="Trust Game (simple version from tutorial)", num_demo_participants=2,
#      app_sequence=['trust_simple']),
