#!/usr/bin/env python3
import json
import os
import re

repo={
    'armv6' : 'deb-rpi-1b',
    'armv7' : 'deb',
    'arm64' : 'deb-arm64'
}

darch={
    'armv6' : 'armhf',
    'armv7' : 'armhf',
    'arm64' : 'arm64'
}

name = os.getenv("TRAVIS_TAG")
component = "main"
if name :
  for c in ('testing','experimental'):
    if re.search(r'-{}$'.format(c),name):
      component = c

def descriptor(arch):
  _package = {
    "name" : "grafana-on-raspberry",
    "repo" : repo[arch],
    "subject" : "fg2it"
  }

  _version = {
    "name": name,
    "vcs_tag": name
  }

  if arch == "arm64":
    comp = 'experimental'
  else:
    comp = component

  _files = [
    {
      "includePattern": "{}/(.*\.deb$)".format(arch),
      "uploadPattern": "{}/g/$1".format(comp),
      "matrixParams": {
        "deb_distribution": "wheezy,jessie,stretch",
        "deb_component": comp,
        "deb_architecture": darch[arch]
      }
    }
  ]

  return {
    "package" : _package,
    "version" : _version,
    "files" : _files,
    "publish" : True
  }

for arch in ('armv6','armv7','arm64'):
  print(json.dumps(descriptor(arch)),file=open(arch+'.d','w'))
