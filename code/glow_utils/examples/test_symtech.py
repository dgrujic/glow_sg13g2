
from symtech import SymTech
from pathlib import Path

def printTech():
    for key in SymTech.technology.keys():
        print(key, ":", SymTech.technology[key])

print("*"*40)
print("Default technology parameters")
printTech()
print("*"*40)
SymTech.loadTech(str(Path(__file__).resolve().parent) + "/demotech.json")
print("Loaded technology parameters")
printTech()
print("*"*40)