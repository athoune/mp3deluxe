#!/usr/bin/env python
# -*- coding: utf8 -*-

__author__ = "mathieu@garambrogne.net"

import subprocess
import re
import os
import os.path
import time

from mutagen.mp3 import EasyMP3 as MP3

class MultiProcess(object):
	def __init__(self, processors = 2):
		self.processors = processors
		self.cmds = []
		self.actions = []
	def cmd(self, cmd):
		self.cmds.append(cmd)
	def wait(self):
		while len(self.cmds):
			if len(self.actions) < self.processors:
				cmd = self.cmds.pop()
				print cmd
				self.actions.append(subprocess.Popen(cmd))
			for action in self.actions:
				if action.poll() != None:
					self.actions.remove(action)
			time.sleep(1)

class Tracks(object):
	def __init__(self, cdda, wav):
		self.wav = wav
		self.path = os.path.join(cdda.path, wav)
		self.cdda = cdda
		root, ext = os.path.splitext(wav)
		s = root.split(' ')
		self.root = root
		self.number = int(s[0])
		self.title = ' '.join(s[1:])
	def __repr__(self):
		return '<Track #%i "%s">' % (self.number, self.title)
	def to_mp3(self, folder='.'):
		mp3 = os.path.join(folder, '%s.mp3' % self.root)
		print "Converting %s to mp3" % self.title
		c = subprocess.Popen(['lame', '-b320', '-q0', '-m', 's', '--nohist', '--disptime', '2', self.path, mp3 + ".tmp"])
		c.wait()
		os.rename(mp3 + ".tmp", mp3)
		audio = MP3(mp3)
		audio['title'] = self.title
		audio['tracknumber'] = str(self.number)
		audio['album'] = self.cdda.title
		audio.save()

class FlacFolder(object):
	"A folder full of flac files"

class CDDA(object):
	def __init__(self, path):
		self.path = path
		self.title = path.split('/')[-1]
	def __len__(self):
		return len([p for p in os.listdir(self.path) if p[0] != '.'])
	def __iter__(self):
		for wav in os.listdir(self.path):
			if wav[0] != '.':
				yield Tracks(self, wav)
	def __repr__(self):
		return '<CDDA "%s">' % self.title

def cddas():
	"find all audio cd available"
	cd = re.compile(r'(/dev/disk[0-9]+) on (/Volumes/.*?) \(.*?\)')
	c = subprocess.Popen('mount | grep cddafs', stdout=subprocess.PIPE, shell=True)
	c.wait()
	for line in c.stdout.read().split("\n")[:-1]:
		m = cd.match(line)
		if m != None:
			yield CDDA(m.group(2))

if __name__ == '__main__':
	for cd in cddas():
		print cd, len(cd)
		for track in cd:
			print track
			track.to_mp3()