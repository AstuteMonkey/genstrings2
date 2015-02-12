# Genstrings 2

Generates strings for NSLocalizedString properly. Apple's `genstrings` has some bugs where it skips some strings that are on the same line of code, plus it's append flag is broken.

Usage:

	shopt -s globstar
	genstrings2.py [options] [files]

Options:

	-a
	    Instead of overwriting every string, this will preserve existing strings in the strings file.
	-o <path>
	    Output target. This could be "en.lproj" or "Base.lproj". By default, it is "Base.lproj".

Example:

	genstrings2.py -a -o en.lproj **/*.m
