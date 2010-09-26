#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name="MP3 de luxe",
      version="0.1",
      description="Make ultimate MP3 on a Mac",
      license="GPL-3",
      author="Mathieu Lecarme",
      url="http://github.com/athoune/mp3deluxe",
      #packages=['mp3deluxe'],
      package_dir={'': 'src/'},
      keywords= "mp3, osx",
      zip_safe = True,
      install_requires=["mutagen"],
      scripts=['bin/cd2mp3'])