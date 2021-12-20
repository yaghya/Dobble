"""
Dobble SVG generator.
By Thibault Nocchi.
https://github.com/Tiwenty

Run this script from a folder where it has a child folder named "img" with PNG symbols named as 1.png, 2.png, etc.
It'll create a "svg" folder with all generated cards as SVG.

The script will notify you when it has finished, although it is the only alert it'll give you. If you want to watch what it is doing, go into the "svg" folder and watch what is generated.
"""
import svgwrite,os

from math import pi, sqrt
from random import randint
from spot_it.utils.doble_utils import get_image_size, collisionBetweenTwoSurfaces, generateCards, distanceBetweenTwoPoints
class dobble_pipeline:	
    def __init__(self,order,image_path_file,output_dir,expt_no) -> None:
        """ Number of symbols on each card. """
        self.order = order
        self.image_path_file = image_path_file
        self.output_dir = output_dir
        self.expt_no = expt_no


    def create_cards(self):
        
        print("start","order = ",self.order)
        numberofSymb = self.order + 1

        """ Size of a Dobble card in mm. """
        docX = 200
        docY = docX
        """ Ratio to reduce symbols size. """
        surfaceReduction = 4

        circleRadius = round(docX / 2) - 1
        circleArea = round(pi * circleRadius * circleRadius)
        circleCenter = (docX/2, docY/2)

        """ Area allocated to a symbol. """
        imgArea = round(circleArea / (numberofSymb*surfaceReduction))

        """ Retrieves symbols needed on each card. """
        cardsList = generateCards(numberofSymb,self.expt_no)

        """ symbol list"""
        # image_file = "../../data/image_names.txt"
        file1 = open(self.image_path_file,"r")
        symbols = [line.replace('\n','') for line in file1]

        cardNbr = 0

        #create svg file storage dir
        svg_dir_path = os.path.join(str(self.output_dir),str(self.expt_no))
        if not os.path.isdir(svg_dir_path):
            os.makedirs(svg_dir_path)

        while cardNbr < len(cardsList):

            """ Retrieves list of symbols to put on current image. """
            imagesToAdd = cardsList[cardNbr]

            """ Prepares the SVG file. """
            cardSVG = svgwrite.drawing.Drawing("{}/{}.svg".format(svg_dir_path,cardNbr), size=("{}mm".format(docX), "{}mm".format(docY)), viewBox="0 0 {} {}".format(docX, docY))

            """ Draws a circle on the SVG. """
            circleBorder = svgwrite.shapes.Circle(center = (circleCenter[0], circleCenter[1]), r = circleRadius, fill = "white", stroke = "black", stroke_width = 1)
            cardSVG.add(circleBorder)

            """ List which will store tuples of each symbol upper left and lower right corner. Each of these corners are also tuples with X and Y coordinates. """
            imgList = []

            for i in imagesToAdd:
                # print(imagesToAdd)
                """ For each symbol on the current card. """

                """ Number of tries for placing the current symbol. """
                triesNumber = 0

                imgPath = "{}".format(symbols[i-1])
                imgSize = get_image_size(imgPath)

                aspectRatio = imgSize[0] / imgSize[1]
                y = sqrt(imgArea/aspectRatio)
                x = aspectRatio * y

                """ Getting a random upscaling (or downscaling) ratio to be applied to the current symbol, from 80% to 120%. """
                upscale = randint(90, 120) / 100

                """ Sizes of the symbol on the SVG. """
                x = round(x*upscale)
                y = round(y*upscale)

                """ Defining default corners and a collision boolean to True to enter the checking loop once. """
                corner_ul = (-1,-1)
                corner_ur = corner_ul
                corner_ll = corner_ul
                corner_lr = corner_ul

                collision = True

                while distanceBetweenTwoPoints(corner_ul, circleCenter) >= circleRadius or distanceBetweenTwoPoints(corner_ur, circleCenter) >= circleRadius or distanceBetweenTwoPoints(corner_ll, circleCenter) >= circleRadius or distanceBetweenTwoPoints(corner_lr, circleCenter) >= circleRadius or collision == True:
                    """
                    This loop tries to put the current symbol on the card, and checks for whether there is a collision with a symbol already in place or if the symbol is out of bounds.
                    If the symbol isn't well placed, it loops again.
                    distanceBetweenTwoPoints(corner_ul, circleCenter) >= circleRadius: if the symbol is in the lower right part of the SVG and outside the circle.
                    distanceBetweenTwoPoints(corner_ur, circleCenter) >= circleRadius: if the symbol is in the lower left part of the SVG and outside the circle.
                    distanceBetweenTwoPoints(corner_ll, circleCenter) >= circleRadius: if the symbol is in the upper right part of the SVG and outside the circle.
                    distanceBetweenTwoPoints(corner_lr, circleCenter) >= circleRadius: if the symbol is in the upper left part of the SVG and outside the circle.
                    collision == True: if the symbol collides with another one.
                    """
                    
                    """ Thoses are the maximum coordinates for the upper left corner (with SVG Y = 0 is at the top) of the symbol based on its size.
                    It assures the symbol will be entirely in the SVG. """
                    maxX = docX - x
                    maxY = docY - y
                    
                    """ We find a random position on the SVG for upper left corner of the symbol, and extrapolates the other 3 coordinates from it. """
                    corner_ul = (randint(0, maxX), randint(0, maxY))
                    corner_ur = (corner_ul[0]+x, corner_ul[1])
                    corner_ll = (corner_ul[0], corner_ul[1]+y)
                    corner_lr = (corner_ul[0]+x, corner_ul[1]+y)

                    """ We reset the collision boolean. """
                    collision = False


                    for val in imgList:
                        """ Checking each already placed symbol. """
                        if collisionBetweenTwoSurfaces(corner_ul, corner_lr, val[0], val[1]):
                            """ If there is a collision, we break the current for, sets the collision flag to True so it'll retry for the current symbol. """
                            collision = True
                            break
                    
                    """ We increase the tries counter and if it exceeds a certain constant we stop trying to put the symbol. """
                    triesNumber += 1
                    if triesNumber > numberofSymb**2:
                        break

                """ If we stopped trying the current symbol, we just stop trying other symbols, and decrease the card counter so we will retry it next round. """
                if triesNumber > numberofSymb**2:
                    cardNbr -= 1
                    break

                """ Whether the symbol was successfully put or not, we find its center coordinate and rotate it randomly. Collsion may occur now but it'll be subtle. """
                imgCenter = (corner_ul[0] + x/2, corner_ul[1] + y/2)
                imgRotation = randint(-90, 90)

                """ We add the new symbol to the list of approved symbols. """
                imgList.append((corner_ul, corner_lr))

                """ We add the symbol to the SVG. """
                image = svgwrite.image.Image("../../{}".format(imgPath), insert = (corner_ul[0], corner_ul[1]), size = (x, y))
                image.rotate(imgRotation, imgCenter)
                cardSVG.add(image)

            """ We save the SVG even if it was a failure.
                Also, the card counter is always increased as if the card was a success, we will try the next card, and if it was a failure we will retry the same card because we previously decreased it. """
            cardSVG.save()
            cardNbr += 1

        print("Success!")
