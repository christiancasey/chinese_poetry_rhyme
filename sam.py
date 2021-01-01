import sys


# Main Program
if __name__ == '__main__':

	# Enable command-line argument with input text filename
	if len(sys.argv) > 1:
		vInputs = sys.argv[1:]
		print(vInputs)
	else:
		vInputs = ["text.txt"]

	# Load all required data files
	file = open("Data/punct.dat", "r")
	strPunct = file.read()

	file = open("Data/chinese.dat", "r")
	strChinese = file.read()

	file = open("Data/penult.dat", "r")
	strPenult = file.read()

	file = open("Data/ipa.dat", "r")
	vIPA = file.read().splitlines()

	# Loop through input files and process
	for strInput in vInputs:

		# Load all of the required files
		# First file contains the text, rest are data
		file = open(strInput, "r")
		vText = file.read().splitlines()

		# Loop through lines in text
		n = len(vText)
		for i in range(n):
			strI = vText[i]
			if(len(strI) < 1):
				continue

			# Starting at end of line, look for first non-punctuation character
			iLast = len(strI)-1
			if iLast <= 1:
				continue
			while strPunct.find(strI[iLast]) != -1:
				iLast -= 1
				if iLast <= 1:
					break

			# Get last non-punctuation character
			strSign = strI[iLast]
			# Determine whether the sign is one of the "penult" signs,
			# 	which require that the sign before be transcribed
			iMatch = strPenult.find(strSign)
			if iMatch > 0 and iLast > 0:
				strSign = strI[iLast-1]

			iMatch = strChinese.find(strSign)

			# Find match in list of chinese characters and select IPA match
			# If character is not found, output NA
			strIPA = " {NA} "
			if iMatch >= 0:
				strIPA = "{" + vIPA[iMatch] + "}"

			vText[i] = strI[:iLast+1] + " " + strIPA + " " + strI[iLast+1:]
			vText[i] = strI + " " + strIPA

			print(vText[i])

		# Save annotated text to new file
		strOutput = strInput[0:-4] + "_annotated.txt"
		file = open(strOutput, "w")
		for strLine in vText:
			file.write("%s\n" % strLine)
		file.close()
