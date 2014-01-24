#!/usr/bin/env python

import sys
import os
import codecs

package = sys.argv[1]
packages = [
            "atril",
            "caja",
            "caja-extensions",
            "engrampa",
            "eom",
            "libmatekbd",
            "libmateweather",
            "marco",
            "mate-applets",
            "mate-backgrounds",
            "mate-common",
            "mate-control-center",
            "mate-desktop",
            "mate-icon-theme",
            "mate-icon-theme-faenza",
            "mate-media",
            "mate-menus",
            "mate-notification-daemon",
            "mate-panel",
            "mate-power-manager",
            "mate-screensaver",
            "mate-session-manager",
            "mate-settings-daemon",
            "mate-terminal",
            "mate-themes",
            "mozo",
            "pluma"
            ]

if not package in packages:
    print "E: package '%s' not valid" % package
    sys.exit(1)

os.system("rm -rf /tmp/%s/ " % package)
os.system("cp " + package + " /tmp/" + package + "/ -R") 

os.chdir("/tmp/%s" % package)
os.system("rm -rf debian/")
os.system("cp -R ~/mate/debian-packages/%s/debian/ ." % package)
os.system("echo '3.0 (native)' > debian/source/format")

orig_rules_file = codecs.open("debian/rules", encoding="utf-8", mode="r")
orig_rules = orig_rules_file.read()
orig_rules_file.close()
new_rules = orig_rules.replace("dh_auto_configure --", "NOCONFIGURE=1 ./autogen.sh --with-gtk=3.0\n\tdh_auto_configure --")
new_rules = new_rules.replace("#DEB_CONFIGURE_SCRIPT := ./autogen.sh", "DEB_CONFIGURE_SCRIPT := ./autogen.sh")
new_rules_file = codecs.open("debian/rules", encoding="utf-8", mode="w")
new_rules_file.write(new_rules)
new_rules_file.close()

os.system("dpkg-buildpackage -b -Zxz -uc -tc 2>&1 | tee build.log")
os.system("mv -v build.log ~/mate/build.log")
os.system("rm -v ../*.changes")
os.system("mv -v ../*.deb ~/mate/")
os.chdir("/home/stefano/mate")
os.system("rm -rf /tmp/%s/ " % package)
os.system("ls -1 *.deb")
