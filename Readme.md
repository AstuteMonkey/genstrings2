# Genstrings 2

Generates strings for NSLocalizedString properly. Apple's `genstrings` has some bugs where it skips some strings that are on the same line of code, plus it's append flag is broken.

Things to do:

* Generate positional formatting parameters (`%d and %0.4f` becomes `%1$d and %2$0.4f`)
* There should be support for `CF`-prefixed localization macros (for compatibility)
* Support tables that go into `Table.strings` instead of `Localizable.strings` (`NSLocalizedStringFromTable`, `NSLocalizedStringFromTableInBundle`)
* Support `NSLocalizedStringWithDefaultValue`

Usage:

	shopt -s globstar
	genstrings2.py [options] [files]

Options:

	* -a
	  Instead of overwriting every string, this will preserve existing strings in
	  the strings file.
	* -o <path>
	  Output target. This could be "en.lproj", "Base.lproj", etc. By default, it
	  is "Base.lproj".
	* -s <routine>
	  Search for the given routine instead of `NSLocalizedString`.

Example:

	genstrings2.py -a -o en.lproj **/*.m
