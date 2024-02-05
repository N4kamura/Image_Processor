import cv2
import numpy as np

def image_contours(image_path):

    path = image_path

    threshold = 9
    specific_color = np.array([238,255,255])

    image = cv2.imread(path)

    lower_bound = specific_color - threshold
    upper_bound = specific_color + threshold

    mask = cv2.inRange(image, lower_bound, upper_bound)

    inverse_mask = cv2.bitwise_not(mask)

    result = cv2.bitwise_and(image, image, mask=inverse_mask)
    #result = cv2.bitwise_and(image, image, mask=mask)

    gray_image = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

    _, threshold_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)

    kernel = np.ones((5,5),np.uint8)
    eroded_image = cv2.erode(threshold_image, kernel, iterations=3) #Yo deducí que eran 3
    dilated_image = cv2.dilate(eroded_image, kernel, iterations=3) #Yo deducí que eran 3

    inverted_image = cv2.bitwise_not(dilated_image)

    contours, _ = cv2.findContours(inverted_image,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #Dibujar contornos en la imagen original
    image_with_contours = image.copy()
    cv2.drawContours(image_with_contours, contours, -1, (0,255,0), 2)

    cv2.imshow("Original image", inverted_image)
    cv2.imshow("Image with contours", image_with_contours)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return contours

def main():
    contornos = image_contours("TEST_ZOOM-15.png")
    print(contornos)

if __name__ == '__main__':
    main()