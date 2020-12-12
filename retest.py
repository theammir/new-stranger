import re

nickname = 'something (something else)'

match = re.findall(r'something', nickname)

print(match.group())