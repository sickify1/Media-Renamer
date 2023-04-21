"""
Script for detecting and renaming media folders and files
Created because I wish to rename large amounts of my media library
Renames: Title - Year to Title (Year)
Author: Sickify
License: MIT license

Usage: python MediaRename.py path
Ex: python MediaRename.py /home/username/Movies/
"""

import os
import sys
import fnmatch
import re

top = sys.argv[1]

# Scans the specified directory recursively for folders or files that contain a 4 digit year in them
# If the match is a file it replaces the ' - ' in the filename with '%#%' to prevent the full path from having more than one ' - '
def Scanner(type):
	list = []
	scans = 0
	for root, dirs, files in os.walk(top, topdown=True):
		if(type == 'folders'):
			var = dirs
		else:
			var = files
		for name in var:
			scans += 1
			year_match = re.match(r'.*([1-3][0-9]{3})', name)
			if year_match is not None:
				if(type == 'files'):
					name = name.replace(" - ", "%#%")	
				fullname = os.path.join(root, name)
				list.append(fullname)
	return list, scans

# Checks if the items returned by the scanner function have a ' - ' in the path for folders
# Or if they have a '%#%' for files
# If a match is found it generates a new name and prompts if you want to rename the source 
def Filter(items, type):
	matched = 0
	renamed = 0
	extra = ""
	if(type =='folders'):
		matchstring = " - "
	else:
		matchstring = "%#%"
	filtered = fnmatch.filter(items, "*" + matchstring + "*")
	for fname in filtered:
		matched += 1
		if(type == "files"):
			original_name = fname.replace(matchstring, " - ")
		else:
			original_name = fname
		basename, postname = fname.split(matchstring)
		if(type == "files"):
			postname, ext = postname.split(".")
			extra = "." + ext
		newname = basename + " (" + postname + ")" + extra
		print("Match Found!\nOld Name: " + original_name + "\nNew Name: " + newname)
		rename = input("Enter y to rename: ")
		if(rename == 'y'):
			os.rename(original_name, newname)
			renamed += 1
	return matched, renamed

# Run the scan and filter functions for folders   		
print("\nChecking for folders to rename")
dirlist, dirscanned = Scanner("folders")            
dirmatched, dirrenamed = Filter(dirlist, "folders")

# Run the scan and filter functions for files
print("\nChecking for files to rename")
flist, fscanned = Scanner("files")            
fmatched, frenamed = Filter(flist, "files")

# Print out some fun statistics
print("\nTotal Folders Scanned: " + str(dirscanned))
print("Total Folders Matched: " + str(dirmatched))
print("Total Folders Renamed: " + str(dirrenamed))
print("Total Files Scanned: " + str(fscanned))
print("Total Files Matched: " + str(fmatched))
print("Total Files Renamed: " + str(frenamed))