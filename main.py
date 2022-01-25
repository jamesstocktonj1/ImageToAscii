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

spaceThreshold = 1750

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


    print("Grid Sum: {}".format(gridSum))


    return grid


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


#itterate through grid
for n in range(0, len(subGrid)):

    corValues = []

    for i in range(0, len(charValues)):

        corValues.append(correlationFunction(subGrid[n], symbolSquares[i]))

    if(max(corValues) > spaceThreshold):
        bestChar = corValues.index(max(corValues))
        f.write(charSymbol[bestChar])
        bigString += charSymbol[bestChar]
    else:
        f.write(" ")
        bigString += " "


    if(((n + 1) % int(len(grid[0]) / 8)) == 0):
        f.write("\n")
        bigString += "\n"

f.close()

print("Length: {}, {}".format(len(subGrid), len(bigString)))

plt.imshow(subGrid[50])
plt.show()

#createSubSquares(grid, 25)