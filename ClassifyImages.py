import glob

# CONSTANTS
THRESH_HASH_DISTANCE_STRICT = 0.05
THRESH_OCR_DISTANCE_STRICT = 0.03

THRESH_HASH_DISTANCE_STRICT_IMAGE_DOMINANT = 0.01
THRESH_HASH_DISTANCE_REMOVE_IMAGE_DOMINANT = 0.35
THRESH_OCR_DISTANCE_REMOVE_IMAGE_DOMINANT = 1.999

THRESH_HASH_DISTANCE_REMOVE = 0.1
THRESH_OCR_DISTANCE_REMOVE = 0.16

THRESH_HASH_DISTANCE_GRAPH = 0.009


# returns true if an imageName contains a C
# a C indicates that the questions should be skipped
# imageName is a string in the format L123123123_C12.jpg
def containsC( imageName ):

  underScoreIndex = imageName.rfind("_")
  slicedName = imageName[ underScoreIndex : ]
  cIndex = slicedName.rfind("C")

  return cIndex != -1

def hasSamePrefix( imageNameOne, imageNameTwo):
	underScoreIndexOne = imageNameOne.rfind("_")
	underScoreIndexTwo = imageNameTwo.rfind("_")

	if imageNameOne[: underScoreIndexOne] == imageNameTwo[:underScoreIndexTwo]:
		return True

	return False

def getOrderedImageNames( folderName )
	orderedImageNames = []
	for imagePath in glob.glob( folderName +"/*.jpg"):

    	slashPosition = imagePath.rfind("/")
		orderedImageNames.append( imagePath[slashPosition+1:])

	return orderedImageNames


def isPotentialMatch( imageTable, imageNameOne, imageNameTwo ):

	diffOCRdistance = commonMethods.percentageEditDistance( imageTable[imageNameOne]["ocr_text"],\
                                                              imageTable[imageNameTwo]["ocr_text"] )
      diffHashDistance = commonMethods.percentHashDifference( imageTable[imageNameOne]["hash_value"],\
                                                              imageTable[imageNameTwo]["hash_value"] )
      # print(matchKey, " " , diffOCRdistance, diffHashDistance)

      # a picture is a strict match if the ocr is within 3 percent and
      # image structure is within a 5 percent difference
      if diffHashDistance <= THRESH_HASH_DISTANCE_STRICT and diffOCRdistance <= THRESH_OCR_DISTANCE_STRICT:
        return True
      
      # if image is imageDominant
      elif imageTable[imageNameOne]["imageDominant"] or imageTable[imageNameTwo]["imageDominant"]:
        if diffHashDistance < THRESH_HASH_DISTANCE_STRICT_IMAGE_DOMINANT:
          return True
        elif diffHashDistance > THRESH_HASH_DISTANCE_REMOVE_IMAGE_DOMINANT or diffOCRdistance > THRESH_OCR_DISTANCE_REMOVE_IMAGE_DOMINANT:
          return False

      # if the picture is both not similar in image structure and writing
      elif diffHashDistance > THRESH_HASH_DISTANCE_REMOVE and diffOCRdistance > THRESH_OCR_DISTANCE_REMOVE: 
        return False

      # if not a strict match or needing to be removed checked it against
      # other elements that also do not need to be removed
      # CAN BE DONE WITH removed elements also but for the time being
      # have not checked the feasibility with all elements
      else:
        return True


def printClassification( orderedNames, imageTable ):
	for image in orderedNames:
		print(imageTable[image]["classification"])


def addClassification( folderName, imageTable ):

	# for continuation tomorrow: just give the two pictures to the image matching thing and see which one is better
	

	# check if the name's prefix is the same; takes care of different classes
	# then check if match
	# then add the next value in the cycle

	cycle = [ "single", "group", "iso"]
	lastCycleVal = None

	orderedImageNames = getOrderedImageNames(folderName)

	for i in range(len(orderedImageNames) - 1):
		
		prevImageName = orderedImageNames[i]
		curImageName = orderedImageNames[i+1]


		if containsC(imageName):
			continue
		if lastCycleVal == None or !hasSamePrefix(prevImageName, curImageName):
			# set the imageTable value to single
			lastCycleVal = 0
			# imageTable[curImageName] = cycle[lastCycleVal]

		elif isPotentialMatch(imageTable, prevImageName, curImageName):
			# set to last cycle val incremented by one
			lastCycleVal = (lastCycleVal+1)%3
			# imageTable[curImageName] = cycle[lastCycleVal]

		else:
			# means that ispotentialmatch returned false
			lastCycleVal = 0
			# imageTable[curImageName] = cycle[lastCycleVal]
			# set the current value 


