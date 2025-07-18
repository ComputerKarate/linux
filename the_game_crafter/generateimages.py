#!/usr/bin/python3
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
inputFilePattern = '*.txt'          # Handy if you have other files mingled into the directory
imageOutputDirectory = "./images/"  # This directory will be created if missing
outputFilenamePrefix = ""

# Text related variables
textFontSize = 52
textFontStyle = "Lato-Medium"
textOffsetFromTop = 120
textOffsetFromLeft = 100
imageWidth = 1125           # Jumbo card width
imageHeight = 1725          # Jumbo card height

# Card dimensions depending on font size and type
textNumberOfLines = 35
textNumberOfColumns = 34

# If you choose a font that has a variable pitch, 
# your title may need some help appearing centered over the list below it
textTitleBias = 10 + int(textNumberOfColumns / 2)

# Set the text color with the RGB values
cardTextColor = (0, 0, 0)
cardBackgroundColor = 'white'

def createFileList():
    inputFileList = ""
    global outputFilenamePrefix

    inputFileList = glob.glob(inputFilePattern, recursive=False)
    for entry in inputFileList:
        # Break out the filename prefix and extension
        outputFilenamePrefix, file_extension = os.path.splitext(entry)
        getFileContents(entry)

def getFileContents(filename):
    linecount = 0
    formattedFileContents = []
    formattedTitle = ""

    filehandle = open(filename, "r")

    for value in filehandle:
        if 1 > linecount:
            formattedTitle = f"{' ' * textTitleBias}{value.strip()}"
            formattedFileContents.append(formattedTitle)
            titleLine = False
        else:
            if '\n' == value:
                # We removed the trailing crlf from value so we add two here
                formattedFileContents.append('\r\n\r\n')
            else:
                formattedFileContents.append(value)
        linecount += 1
    createImageFile(formattedFileContents)


def createImageFile(fileContents):
    outputFilename = imageOutputDirectory + outputFilenamePrefix + ".png"
    print("Creating image file: %s" % outputFilename)
    image = Image.new("RGB", (imageWidth, imageHeight), cardBackgroundColor)
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
    if not os.path.isdir(imageOutputDirectory):
        print("%s does not exist, creating..." % imageOutputDirectory)
        os.makedirs(imageOutputDirectory)
    createFileList()


