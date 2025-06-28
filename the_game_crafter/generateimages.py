#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import glob
import os

# With FreeMono,    1125x1725, 42 point font, the document has 40 lines available and 45 columns
# With Lato-Medium, 1125x1725, 52 point font, the document has 35 lines available and 34 columns

# Assumptions
# The first line is the title so it can have leading and trailing spaces removed and be centered
# Any carriage returns in the file will be transferred to the resulting image

# Ideally you will have a directory for your input files instead of the current directory
inputDirectory = "./"
imageDirectory = "./images/"
inputFilePattern = '*.txt'
outputFilenamePrefix = "" # Holds filename minus the extension
                          # Image filename will be <filename>.png

# Text dimensions and X Y
textFontSize = 52
textFontStyle = "Lato-Medium"
textOffsetFromTop = 120
textOffsetFromLeft = 100

# Card dimensions depending on font size and type
textNumberOfColumns = 65
textTitleBias = 5 # Need to push the title over a little further to the right
                  # Do not remove this variable, just set it to 0 if not needed

# Set the text color with the RGB values
# https://colorspire.com/rgb-color-wheel/
# Some common values:
# 255, 255, 255 = White (#FFFFFF)
# 0, 0, 0       = Black (#000000)
# 239, 255, 0   = Yellow (#EFFF00)
# 0, 255, 68    = Green (#00FF44)
cardTextColor = (0, 0, 0)
cardBackgroundColor = 'white'

def createFileList():
    inputFileList = ""
    global outputFilenamePrefix

    inputFileList = glob.glob(inputFilePattern, recursive=False)
    for entry in inputFileList:
        print("Entry: %s" % entry)

        # Break out the filename prefix and extension
        outputFilenamePrefix, file_extension = os.path.splitext(entry)
        print("Filename %s, Extension %s" % (outputFilenamePrefix, file_extension))
        getFileContents(entry)

def getFileContents(filename):
    linecount = 0
    formattedFileContents = []
    firstRun = True

    print("\tReading %s" % filename)
    filehandle = open(filename, "r")

    for value in filehandle:
        if 1 > linecount:
            value = value.strip()
            if True == firstRun:
                value = f"{value:{' '}>{textTitleBias}}"
                firstRun = False
            formattedFileContents.append(value.center(textNumberOfColumns, " "))
        else:
            formattedFileContents.append(value)
        linecount = linecount + 1
    createImageFile(formattedFileContents)


def createImageFile(fileContents):
    outputFilename = imageDirectory + outputFilenamePrefix + ".png"
    print("Creating image file: %s" % outputFilename)
    image = Image.new("RGB", (1125, 1725), cardBackgroundColor)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(textFontStyle, size=textFontSize)

    # .join is to add a list to the output as a string
    draw.text((textOffsetFromLeft, textOffsetFromTop), ''.join(fileContents), font=font, fill=cardTextColor)
    image.save(outputFilename)


if not os.path.isdir(inputDirectory):
    print("ERROR: %s does not exist" % (inputDirectory))
    quit()
else:
    print("%s exists, continuing" % (inputDirectory))
    if not os.path.isdir(imageDirectory):
        print("%s does not exist, creating..." % imageDirectory)
        os.makedirs(imageDirectory)
    createFileList()



