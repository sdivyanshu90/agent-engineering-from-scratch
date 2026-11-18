import math
def wilson(successes,n,z=1.96):
    if type(n) is not int or n<=0 or type(successes) is not int or not 0<=successes<=n or z<=0:raise ValueError('invalid binomial sample')
    p=successes/n;d=1+z*z/n;center=(p+z*z/(2*n))/d;half=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return max(0.0,center-half),min(1.0,center+half)
