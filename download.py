#!/usr/bin/python

import os
import commands

for path in commands.getoutput("find . -name changelog | grep -v mate-desktop-environment").split("\n"):
	(current, project, debian, changelog) = path.split("/")
	header = commands.getoutput("cat %s/debian/changelog | grep urgency | head -1" % project)
	version = header.split("(")[1]	
	version = version.split(")")[0]	
	if ("-" in version):
		version = version.split("-")[0]	
	version_components = version.split(".")
	major = "%s.%s" % (version_components[0], version_components[1])
	if project == "mate-themes":
		url = "https://pub.mate-desktop.org/releases/themes/%s/%s-%s.tar.xz" % (major, project, version)
	else:
		url = "https://pub.mate-desktop.org/releases/%s/%s-%s.tar.xz" % (major, project, version)
	dest = "%s_%s.orig.tar.xz" % (project, version)
	command = "wget -c %s -O %s" % (url, dest)
	print "Running %s" % command
	os.system(command)
