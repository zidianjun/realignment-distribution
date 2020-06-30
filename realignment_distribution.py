
import numpy as np
from scipy.special import comb, perm

def prob(n, k):
	if type(n) is not int or type(k) is not int:
		return TypeError
	if n < 0:
		return ValueError

	if n == 0:
		if k >= 0:
			return (6 - min(k, 6)) * (7 - min(k, 6)) / 2 / 36.
		else:
			return 15 / 36. + (12 + max(k, -6)) * (1 - max(k, -6)) / 2 / 36.
	else:
		if k >= n:
			return (6+n - min(k, 6+n)) / 36.
		else:
			return (6-n + max(k, -6+n)) / 36.

def realignment_f(infl, adv):
	if type(infl) is not int or type(adv) is not int:
		return TypeError
	if infl not in [1, 2, 3, 4]:
		return ValueError

	f = []
	cumulative = 0
	for i in range(infl+1):
		if i != infl:
			p = prob(i, adv)
			if p == 0.:
				p += 1e-9
			f.append(p)
			cumulative += p
		else:
			f.append(1 - cumulative)

	return f

def realignment_distribution(infl, adv):
	f = realignment_f(infl, adv)

	exp = 0
	cum_p = 0
	for n in range(1, 100):
		if infl == 1: # Zaire, geometric distribution
			p = f[0]**(n-1) * f[1]
		if infl == 2: # Mexico
			p = f[0]**(n-1) * f[2] + (n-1)*f[0]**(n-2)*f[1] * (f[1]+f[2])
		if infl == 3: # Cuba
			p = f[0]**(n-1) * f[3] + comb(n-1, 1)*f[0]**(n-2)*f[1] * (f[2]+f[3]) + \
			    (comb(n-1, 1)*f[0]**(n-2)*f[2] + comb(n-1, 2)*f[0]**(n-3)*f[1]**2) * (f[1]+f[2]+f[3])
		if infl == 4: # West Germany
			p = f[0]**(n-1) * f[4] + comb(n-1, 1)*f[0]**(n-2)*f[1] * (f[3]+f[4]) + \
			    (comb(n-1, 1)*f[0]**(n-2)*f[2] + comb(n-1, 2)*f[0]**(n-3)*f[1]**2) * (f[2]+f[3]+f[4]) + \
			    (comb(n-1, 1)*f[0]**(n-2)*f[3] + perm(n-1, 2)*f[0]**(n-3)*f[1]*f[2] + comb(n-1, 3)*f[0]**(n-4)*f[1]**3) * (f[1] + f[2]+f[3]+f[4])
		exp += n * p
		if n < 5:
			cum_p += p
			print "[%+d advantage] %d-infl %.1f%% succuess with %d-point card" %(
			       adv, infl, cum_p * 100, n)

	return exp

for infl in range(1, 5):
	for adv in range(-2, 5):
		print "[%+d advantage] %d-infl needs %.3f times (expectation)" %(
			  adv, infl, realignment_distribution(infl, adv))
		print "--------------------------------------------"
	print "============================================"


