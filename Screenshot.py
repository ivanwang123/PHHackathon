import PIL.ImageGrab
import cv2
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
import pyautogui


# 0, 193, 32
template = cv2.imread('plusplus.png',0)
w, h = template.shape[::-1]

# All the 6 methods for comparison in a list
methods = ['cv2.TM_CCORR_NORMED']
# 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF_NORMED']

def detect_upvote(screenshot):

    color_img = screenshot

    img = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    img2 = img.copy()

    for meth in methods:

        img = img2.copy()
        method = eval(meth)

        # Apply template 
        res = cv2.matchTemplate(img,template,method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)

        # cropped image
        # not upvoted color [133 131 128] or [128 131 133]
        # upvoted color [33 180 4] or [4 180 33]
        crop_img = color_img[max_loc[1]:bottom_right[1], max_loc[0]:bottom_right[0]]

        
        #print(np.where((crop_img == [33,180,4]).all(axis = 2)))
        cv2.rectangle(crop_img, (11, 12), (11, 12), 255)
        
        ###cv2.imshow("cropped", crop_img)
        
        #print(crop_img[11, 12])


        cv2.rectangle(img,top_left, bottom_right, 255, 2)

        # click location
        click_x = int((max_loc[0]+bottom_right[0])/2)
        click_y = int((max_loc[1]+bottom_right[1])/2)
        cv2.rectangle(img, (click_x-5, click_y-1), (click_x-5, click_y-1), 255)
        #print(crop_img[int(w/2)-5, int(h/2)-1])
        if np.any(crop_img[int(w/2)-5, int(h/2)-1] == (113, 111, 108)):
        	pyautogui.leftClick(click_x, click_y)

        plt.subplot(121),plt.imshow(res,cmap = 'gray')
        plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
        plt.subplot(122),plt.imshow(img,cmap = 'gray')
        plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
        plt.suptitle(meth)

        #plt.show()

def take_screenshot():
	screen = PIL.ImageGrab.grab()
	cropped = screen.crop((0, 0, screen.width/2, screen.height/2))

	np_image = np.array(cropped.getdata(), dtype = 'uint8').reshape((cropped.size[1], cropped.size[0], 3))
	cv2_image = cv2.cvtColor(np_image, cv2.COLOR_RGB2BGR)

	detect_upvote(cv2_image)

take_screenshot()