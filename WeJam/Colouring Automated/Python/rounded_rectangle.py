import cv2
import random
import sys

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

def rounded_rectangle(src, top_left, bottom_right, radius=1, color=255, thickness=1, line_type=cv2.LINE_AA):

    #  corners:
    #  p1 - p2
    #  |     |
    #  p4 - p3

    p1 = top_left
    p2 = (bottom_right[0], top_left[1])
    p3 = (bottom_right[0], bottom_right[1])
    p4 = (top_left[0], bottom_right[1])

    height = abs(bottom_right[1] - top_left[1])

    if radius > 1:
        radius = 1

    corner_radius = int(radius * (height/2))

    if thickness < 0:

        #big rect
        top_left_main_rect = (int(p1[0] + corner_radius), int(p1[1]))
        bottom_right_main_rect = (int(p3[0] - corner_radius), int(p3[1]))

        top_left_rect_left = (p1[0], p1[1] + corner_radius)
        bottom_right_rect_left = (p4[0] + corner_radius, p4[1] - corner_radius)

        top_left_rect_right = (p2[0] - corner_radius, p2[1] + corner_radius)
        bottom_right_rect_right = (p3[0], p3[1] - corner_radius)

        all_rects = [
        [top_left_main_rect, bottom_right_main_rect], 
        [top_left_rect_left, bottom_right_rect_left], 
        [top_left_rect_right, bottom_right_rect_right]]

        [cv2.rectangle(src, rect[0], rect[1], color, thickness) for rect in all_rects]

    # draw straight lines
    cv2.line(src, (p1[0] + corner_radius, p1[1]), (p2[0] - corner_radius, p2[1]), color, abs(thickness), line_type)
    cv2.line(src, (p2[0], p2[1] + corner_radius), (p3[0], p3[1] - corner_radius), color, abs(thickness), line_type)
    cv2.line(src, (p3[0] - corner_radius, p4[1]), (p4[0] + corner_radius, p3[1]), color, abs(thickness), line_type)
    cv2.line(src, (p4[0], p4[1] - corner_radius), (p1[0], p1[1] + corner_radius), color, abs(thickness), line_type)

    # draw arcs
    cv2.ellipse(src, (p1[0] + corner_radius, p1[1] + corner_radius), (corner_radius, corner_radius), 180.0, 0, 90, color ,thickness, line_type)
    cv2.ellipse(src, (p2[0] - corner_radius, p2[1] + corner_radius), (corner_radius, corner_radius), 270.0, 0, 90, color , thickness, line_type)
    cv2.ellipse(src, (p3[0] - corner_radius, p3[1] - corner_radius), (corner_radius, corner_radius), 0.0, 0, 90,   color , thickness, line_type)
    cv2.ellipse(src, (p4[0] + corner_radius, p4[1] - corner_radius), (corner_radius, corner_radius), 90.0, 0, 90,  color , thickness, line_type)

    return src


    

def addRoundedRectangleBorder(img):
    height, width, channels = img.shape

    border_radius = int(width * random.randint(1, 10)/100.0)
    line_thickness = int(max(width, height) * random.randint(1, 3)/100.0)
    edge_shift = int(line_thickness/2.0)

    red = random.randint(230,255)
    green = random.randint(230,255)
    blue = random.randint(230,255)
    color = (blue, green, red)

    #draw lines
    #top
    cv2.line(img, (border_radius, edge_shift), 
    (width - border_radius, edge_shift), (blue, green, red), line_thickness)
    #bottom
    cv2.line(img, (border_radius, height-line_thickness), 
    (width - border_radius, height-line_thickness), (blue, green, red), line_thickness)
    #left
    cv2.line(img, (edge_shift, border_radius), 
    (edge_shift, height  - border_radius), (blue, green, red), line_thickness)
    #right
    cv2.line(img, (width - line_thickness, border_radius), 
    (width - line_thickness, height  - border_radius), (blue, green, red), line_thickness)

    #corners
    cv2.ellipse(img, (border_radius+ edge_shift, border_radius+edge_shift), 
    (border_radius, border_radius), 180, 0, 90, color, line_thickness)
    cv2.ellipse(img, (width-(border_radius+line_thickness), border_radius), 
    (border_radius, border_radius), 270, 0, 90, color, line_thickness)
    cv2.ellipse(img, (width-(border_radius+line_thickness), height-(border_radius + line_thickness)), 
    (border_radius, border_radius), 10, 0, 90, color, line_thickness)
    cv2.ellipse(img, (border_radius+edge_shift, height-(border_radius + line_thickness)), 
    (border_radius, border_radius), 90, 0, 90, color, line_thickness)

    return img

##############################################################################################################

