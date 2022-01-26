#takes an image file and converts it into an ascii string of your chosen size
#James Stockton
#23/01/2022


from PIL import Image, ImageColor
import matplotlib.pyplot as plt
import math


Image.MAX_IMAGE_PIXELS = None


imageFile = "bojo.jpg"


#character correlation constants
charSymbol = ["/", "\\", "#"]
charValues = [[-1, 1, -1, 1],
              [1, 0, 1, 0],
              [0, 0.5, 0, 0.5]]

spaceThreshold = 150
intensityThreshold = 100

def loadFromFile(file_name):

    image_grid = []

    #load image
    img = Image.open(file_name)

    #temporary buffer (black and white)
    buf = list(img.getdata(0))
    print(len(buf))

    print(buf[-1])

    
    #convert from 1D to 2D array
    for y in range(0, img.size[1]):      

        image_grid.append(buf[(y * img.size[0]) : ((y + 1) * img.size[0])])


    print("X: {}, Y: {}".format(len(image_grid[0]), len(image_grid)))
    print("X: {}, Y: {}".format(img.size[0], img.size[1]))

    return image_grid




def createSubSquares(image_grid, asciiHeight):

    aspectRatio = len(image_grid[0]) / len(image_grid)

    heightDivide = asciiHeight
    widthDivide = int(asciiHeight * aspectRatio)

    subSizeHeight = int(len(image_grid) / heightDivide)
    subSizeWidth = int(len(image_grid[0]) / widthDivide)
 
    print("Aspect: {}, Height: {}, Width: {}".format(aspectRatio, heightDivide, widthDivide))

    subGrid = []

    for y in range(0, subSizeHeight):

        

        for x in range(0, subSizeWidth):
            
            tempGrid = []

            #itterates through the rows
            for i in range(0, heightDivide):
                tempGrid.append(image_grid[(y * heightDivide) + i][(x * widthDivide) : (x + 1) * widthDivide])
            
            subGrid.append(tempGrid)

    print(subGrid[0])

    return subGrid
            

        



    
#creates a 2D square with gaussian distrubution with means ux, uy
def generateCorrelationSquare(xSize, ySize, uxm, uxc, uym, uyc):

    #ux = (xSize - 1) * 0.5
    #uy = (ySize - 1) * 0.5

    #grid to return
    grid = []

    #used in grid normalisation
    gridSum = 0

    for y in range(0, ySize):

        buf = []
        for x in range(0, xSize):

            ux = (uxm * y) + (uxc * xSize) 
            uy = (uym * x) + (uyc * ySize)

            n = math.exp((-1 * ((x - ux) ** 2)) / xSize) * math.exp((-1 * ((y - uy) ** 2)) / ySize)

            buf.append(n)

        gridSum += sum(buf)
        grid.append(buf)


    for y in range(0, ySize):

        for x in range(0, xSize):

            grid[y][x] = grid[y][x] / gridSum


    print("Grid Sum: {}".format(gridSum))

    return grid




def squareIntensity(imageSquare):

    xSize = len(imageSquare[0])
    ySize = len(imageSquare)

    intensityValue = 0

    for y in range(0, ySize):

        intensityValue += sum(imageSquare[i])

    return intensityValue




def correlationFunction(correlationSquare, imageSquare):

    xSize = len(imageSquare[0])
    ySize = len(imageSquare)

    correlationValue = 0

    for y in range(0, ySize):

        for x in range(0, xSize):

            correlationValue += (correlationSquare[y][x] * imageSquare[y][x])

    return correlationValue


#generateCorrelationSquare(20, 20, 0, 0.5, 0, 0.5)





# / (-1, 1 -1, 1)
# \ (1, 0, 1, 0)
# # (0, 0.5, 0, 0.5)

grid = loadFromFile(imageFile)
#plt.imshow(grid)
#plt.show()

subGrid = createSubSquares(grid, 10)


pixelSize = [8, 10]

f = open("image.txt", "w")

bigString = ""

symbolSquares = []

for i in range(0, len(charValues)):
    symbolSquares.append(generateCorrelationSquare(8, 10, charValues[i][0], charValues[i][1], charValues[i][2], charValues[i][3]))


intensitySquare = []
temp = []

#itterate through grid
for n in range(0, len(subGrid)):

    corValues = []
    curChar = ""

    #itterate through symbols and calculate correlation
    for i in range(0, len(charValues)):

        corValues.append(correlationFunction(subGrid[n], symbolSquares[i]))


    #select best character (highest correlation)
    bestChar = corValues.index(max(corValues))
    curChar = charSymbol[bestChar]

    #calculate square intensity
    sqIntensity = squareIntensity(subGrid[n])
    

    #add blank if less than space threshold
    if(max(corValues) < spaceThreshold):
        curChar = " "
        print(sqIntensity)

    #if larger than certain value
    if(sqIntensity > intensityThreshold):
        curChar = "@"


    #append to array and file
    f.write(curChar)
    bigString += curChar


    #add \n if end of row
    if(((n + 1) % int(len(grid[0]) / 8)) == 0):
        f.write("\n")
        bigString += "\n"


f.close()

print("Length: {}, {}".format(len(subGrid), len(bigString)))

#intensitySquare[50]
print("Intensity Max: {}, Min: {}".format(max(temp), min(temp)))

#plt.imshow(intensitySquare)
#plt.show()

#createSubSquares(grid, 25)