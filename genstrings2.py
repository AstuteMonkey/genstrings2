#!/usr/bin/python

# Genstrings2
# (c) Astute Monkey Studio
# (c) Angelo Geels (a.geels@locuz.nl)

import fnmatch
import sys
import os

opt_append = False
opt_target = "Base.lproj"
opt_files = []
opt_routine = "NSLocalizedString"

i = 1
while i < len(sys.argv):
	if(sys.argv[i] == "-a"):
		opt_append = True
	elif(sys.argv[i] == "-o"):
		opt_target = sys.argv[i + 1]
		i += 1
	elif(sys.argv[i] == "-s"):
		opt_routine = sys.argv[i + 1]
		i += 1
	else:
		opt_files.append(sys.argv[i])
	i += 1

def readString(f, inside):
	readingString = inside
	ret = ""
	while True:
		c = f.read(1)
		if(readingString):
			if(c == ""):
				break
			if(c == "\\"):
				cc = f.read(1)
				ret += c + cc
				continue
			if(c == "\""):
				break
			ret += c
		else:
			if(c == ""):
				break
			if(c == "\""):
				readingString = True
	return ret

def skipToEndOfComment(f, block):
	while True:
		c = f.read(1)
		if(c == ""):
			break
		if(block):
			#FIXME: This breaks when comment block ends with "**/"
			if(c == "*" and f.read(1) == "/"):
				break
		else:
			if(c == "\n"):
				break

def readNSString(f):
	readingString = False
	ret = ""
	while True:
		c = f.read(1)
		if(readingString):
			if(c == ""):
				break
			if(c == "\\"):
				cc = f.read(1)
				ret += c + cc
				continue
			if(c == "\""):
				break
			ret += c
		else:
			if(c == ""):
				break
			if(c == "@"):
				if(f.read(1) == "\""):
					readingString = True
	return ret

# Strings file path
pathStrings = opt_target + "/Localizable.strings"

# If a strings file already exists, parse it so we can use the old values for the new file
oldStrings = {}
if(opt_append):
	with open(pathStrings) as f:
		while True:
			c = f.read(1)
			if(c == ""):
				break
			if(c == "/"):
				cc = f.read(1)
				if(cc == "/"):
					skipToEndOfComment(f, False)
				elif(cc == "*"):
					skipToEndOfComment(f, True)
			if(c == "\""):
				key = readString(f, True)
				value = readString(f, False)
				oldStrings[key] = value

# We look for stuff like: NSLocalizedString(@"LEAF", @"blad")
lookfor = opt_routine + "("

print(str(len(opt_files)) + " file(s):")

stringsContent = ""
stringsHit = 0
dupesHit = 0
preservesHit = 0
conflicts = []

keysFound = {}

for match in opt_files:
	wroteHeader = False
	fileStringsWritten = 0

	with open(match) as f:
		matchCount = 0

		while True:
			c = f.read(1)

			if(c == ""):
				break

			if(c == lookfor[matchCount]):
				matchCount += 1
				if(matchCount == len(lookfor)):
					matchCount = 0

					key = readNSString(f)
					value = readNSString(f)

					if(key in keysFound):
						if(keysFound[key] != value):
							if(not key in conflicts):
								conflicts.append(key)
							continue
						dupesHit += 1
						continue
					keysFound[key] = value

					if(not wroteHeader):
						stringsContent += "/* " + match + " */\n"
						wroteHeader = True

					sourceValue = value
					if(opt_append):
						if key in oldStrings:
							if(value != oldStrings[key]):
								value = oldStrings[key]
								preservesHit += 1

					stringsContent += "// " + sourceValue + "\n"
					stringsContent += "\"" + key + "\" = \"" + value + "\";\n\n"
					stringsHit += 1
					fileStringsWritten += 1
			else:
				matchCount = 0

	if(fileStringsWritten > 0):
		stringsContent += "\n\n"

statsContent = "/**\n"
statsContent += " * Total strings: " + str(stringsHit) + "\n"
statsContent += " * Total duplicates: " + str(dupesHit) + "\n"
if(opt_append):
	statsContent += " * Total preserves: " + str(preservesHit) + "\n"
statsContent += " * Total conflicts: " + str(len(conflicts)) + "\n"
if(len(conflicts) > 0):
	statsContent += " *  (Check these keys!)\n"
for conflict in conflicts:
	statsContent += " *   \"" + conflict + "\"\n"
statsContent += " */\n"

stringsContent += statsContent

try:
	os.remove(pathStrings)
except OSError:
	pass
with open(pathStrings, "w") as f:
	f.write(stringsContent)

print(statsContent)
