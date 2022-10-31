from math import gcd

def getRatio (x, y):
    g = gcd(x,y)
    return x//g, y//g