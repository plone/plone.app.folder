#!/usr/bin/env python

from fileinput import input
from re import compile
from sys import argv

test = compile(r'^\s*test(.*)(Regular|Unordered|Ordered) \(')
time = compile(r'([\d.]*) seconds$')

bench = {}
keys = set()
for line in input(argv[1:]):
    match = test.search(line)
    if match:
        name, folder = match.groups()
        keys.add(folder)
    match = time.search(line)
    if match:
        seconds, = map(float, match.groups())
        results = bench.setdefault(name, {})
        results[folder] = seconds

out = [''] + sorted(keys)
print '\t'.join(map(str, out))

for folder in sorted(bench):
    out = [folder]
    for key in sorted(keys):
        out.append(bench[folder][key])
    print '\t'.join(map(str, out))
