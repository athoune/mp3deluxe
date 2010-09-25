#!/usr/bin/env python
# -*- coding: utf8 -*-

__author__ = "mathieu@garambrogne.net"

import subprocess
import re

def cdda():
	cd = re.compile(r'(/dev/disk[0-9]+) on (/Volumes/.*?) \(.*?\)')
	c = subprocess.Popen('mount | grep cddafs', stdout=subprocess.PIPE, shell=True)
	c.wait()
	for line in c.stdout.read().split("\n")[:-1]:
		m = cd.match(line)
		if m != None:
			yield m.group(1),m.group(2)

if __name__ == '__main__':
	print list(cdda())