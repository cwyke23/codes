from __future__ import print_function

import cv2 as cv
from PIL import Image
import numpy as np
import sys

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

def draw_arrow(img, pos):
    first_image = Image.open(img)
#    first_image = img
    second_image = Image.open("Stock Images/Rounded Arrow.jpg")
    first_image.paste(second_image, pos)
    cv2_im_processed = cv.cvtColor(np.array(first_image), cv.COLOR_RGB2BGR)
    return cv2_im_processed

#    cv.destroyAllWindows()
#    return cv2_im_processed
#img = "C:/Users/arvin/Documents/WeJam/Example Image Set/IDWTMAT Example L3 Triggers/Weird/test_input/Sharp Detects\Tie_same-003sharp_detected.jpg"
#pos = (1820, 200)
#img = draw_arrow(img, pos)
#cv.imshow('dst', img)
#cv.waitKey(0)