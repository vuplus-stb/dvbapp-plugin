# -*- coding: utf-8 -*-
from re import sub

# Entities to be converted
entities = (
	# ISO-8895-1 (most common)
	("&#228;", "ä"),
	("&auml;", "ä"),
	("&#252;", "ü"),
	("&uuml;", "ü"),
	("&#246;", "ö"),
	("&ouml;", "ö"),
	("&#196;", "Ä"),
	("&Auml;", "Ä"),
	("&#220;", "Ü"),
	("&Uuml;", "Ü"),
	("&#214;", "Ö"),
	("&Ouml;", "Ö"),
	("&#223;", "ß"),
	("&szlig;", "ß"),

	# Rarely used entities
	("&#8230;", "..."),
	("&#8211;", "-"),
	("&#160;", " "),
	("&#34;", "\""),
	("&#38;", "&"),
	("&#39;", "'"),
	("&#60;", "<"),
	("&#62;", ">"),

	# Common entities
	("&lt;", "<"),
	("&gt;", ">"),
	("&nbsp;", " "),
	("&amp;", "&"),
	("&quot;", "\""),
	("&apos;", "'"),
)

def strip_readable(html):
	# Newlines are rendered as whitespace in html
	html = html.replace('\n', ' ')

	# Multiple whitespaces are rendered as a single one
	html = sub('\s\s+', ' ', html)

	# Replace <br> by newlines
	html = sub('<br(\s+/)?>', '\n', html)

	# Replace <p>, <ul>, <ol> and end of these tags by newline
	html = sub('</?(p|ul|ol)(\s+.*?)?>', '\n', html)

	# Replace <li> by - and </li> by newline
	html = sub('<li(\s+.*?)?>', '-', html)
	html = html.replace('</li>', '\n')

	# And 'normal' stripping
	return strip(html)

def strip(html):
	# Strip enclosed tags
	html = sub('<(.*?)>', '', html)

	# Convert html entities
	for escaped, unescaped in entities:
		html = html.replace(escaped, unescaped)

	# Return result with leading/trailing whitespaces removed
	return html.strip()

