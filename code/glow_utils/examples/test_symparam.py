
from glow_utils.symparam import Symparam

values = {  'x' : 'a+b',
            'y' : 'c',
            'a' : 1,
            'b' : 2,
            'c' : 3}

params = Symparam(values, {})
expression = 'x * y'
print('Dictionary')
print(values)
print('Expression')
print(expression)
print('Expression after substitution')
print(params.substitute( expression ))
print('Expression numeric value')
print(params.evaluate( expression ))
