#
- [Description](#description)
- [Details](#details)
- [Change Default Values](#change-default-values)
- [Execution](#change-default-values)

## Description
I was helping someone create a card game and they were struggling with creating image files to upload to [The Game Crafter](https://www.thegamecrafter.com)  
They wanted to hire the gamecrafter site to print high quality cards  
Since the images must have specific dimensions this lent itself to automation so I created this Python script to convert a text file into an image with the correct dimensions  
Each image will be compatible with the Jumbo card dimensions for [The Game Crafter](https://www.thegamecrafter.com/make/products/JumboDeck) image assets  

## Details
Jumbo cards have the following physical dimensions:  
3.5" x 5.5", 89mm x 140mm  

- The .png files are intended to fit the Jumbo cards with image dimensions of 1125px x 1725px  
- The generated .png has a default top border of 120px and a left border of 100px  
  
This application looks for `inputFilePattern` in `inputDirectory` and converts the contents of each text file into a .png image  
The images will be written to the directory `imageOutputDirectory`  
If `imageOutputDirectory` does not exist, it will be created  
`imageWidth` and `imageHeight` are the desired dimensions of the final image  
`textNumberOfColumns` is used for formatting the title and each line

## Change default values
The following variables have been broken out to make it easy to modify:
```
inputDirectory = "./"  
inputFilePattern = '*.txt'  
imageOutputDirectory = "./images/"  
outputFilenamePrefix = ""
  
textFontSize = 52
textFontStyle = "Lato-Medium"
textOffsetFromTop = 120
textOffsetFromLeft = 100
imageWidth = 1125
imageHeight = 1725
  
textNumberOfColumns = 34  
textTitleBias = 0
```

This is a handy site to get the RGB (Red, Green, Blue) value for any hue:
https://colorspire.com/rgb-color-wheel/

An example would be to set the text to yellow:
```
cardTextColor = (239, 255, 0) # Yellow text
or  
cardTextColor = (0, 0, 0) # Black text
cardBackgroundColor = 'white'  
```

## Execution
Run the application as you would any python script:  
This assumes that `generateimages.py` is saved into `~/Documents/TheGameCrafter/generateimages.py`  
`python3 ~/Documents/TheGameCrafter/generateimages.py`  
