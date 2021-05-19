#!/usr/bin/env python3
from scipy import stats
import sys

Q = float(sys.argv[1])
V = float(sys.argv[2])

print(stats.chi2.ppf(q=Q, df=V))