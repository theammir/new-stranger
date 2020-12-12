# Common config

# StarCog Config
TRUE_PHOENIX_ROLE_NAME = 'True Phoenix'
TROPHY = '🏆'
STAR = '🌟'
PROPERTIES = {
	'@Trophy': TROPHY,
	'@AllianceScore': STAR
}
UPDATE_INTERVALS = { # Minutes
	'@Trophy': 30,
	'@AllianceScore': 5,
	'PROPERTY': 15
}
DIVISIONS = 'DCBA'
BREAKTIME = 3
BRACKET_PATTERN = r'\(([^]]+)\)'
INFO_PATTERN = r'\[[' + r'A-D🇦🇧🇨🇩]?[\d' + f'{TROPHY}{STAR}' + r']+]'
CTX_CHANNEL = 747865777276715150
CTX_MESSAGE = 787291012262395905
