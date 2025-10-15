import random

random_hex_chars = ''.join(random.choices('0123456789abcdef', k=4))

print(random_hex_chars)