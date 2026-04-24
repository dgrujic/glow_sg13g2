
from glow_utils.symdict import Symdict

print("Symdict example")
print("")
# Symdict implements hierarchical dictionary
# Suppose we have a top level dictionary
topDict = Symdict( {}, localDict = { 'x':1, 'y':2})
# and a local dictionary defining new variables and possibly 
# redefining some variables of top level dictionary
level1Dict = Symdict( topDict, localDict={'x':5, 'z':7 } )
# Print dictionaries
print("Top level dictionary hierarchy")
print(topDict, "\n")
print("Local dictionary hierarchy")
print(level1Dict, "\n")
# Variable 'x' is redefined in local dictionary,
# so x evaluates to 5 instead of 2.
print("Top level dictionary x =", topDict['x'])
print("Local dictionary     x =", level1Dict['x'], "\n")
# Changing the value in top level dictionary 
# reflects on local dictionary
topDict.update({'y' : 10})
print("Changed y value to 10 in top level dictionary\n")
# Print dictionaries
print("Top level dictionary hierarchy")
print(topDict, "\n")
print("Local dictionary hierarchy")
print(level1Dict, "\n")

