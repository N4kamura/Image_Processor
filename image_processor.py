import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtGui import QImage, QPixmap

class ImageProcessor(QMainWindow):
    def __init__(self):
        super(ImageProcessor, self).__init__() 
        loadUi("interface.ui",self)
        self.slider_red.valueChanged.connect(self.update_image)
        self.slider_green.valueChanged.connect(self.update_image)
        self.slider_blue.valueChanged.connect(self.update_image)
        self.slider_threshold.valueChanged.connect(self.update_image)
        self.slider_erosion.valueChanged.connect(self.update_image)
        self.slider_dilatacion.valueChanged.connect(self.update_image)
        self.slider_erosion2.valueChanged.connect(self.update_image)
        self.slider_dilatacion2.valueChanged.connect(self.update_image)
        self.update_image()

    def update_image(self):
        red_value = self.slider_red.value()
        green_value = self.slider_green.value()
        blue_value = self.slider_blue.value()
        threshold = self.slider_threshold.value()

        specific_color = np.array([blue_value, green_value, red_value])
        image = cv2.imread('TEST_ZOOM2-15.png')

        lower_bound = specific_color - threshold
        upper_bound = specific_color + threshold
        mask = cv2.inRange(image, lower_bound, upper_bound)

        inverse_mask = cv2.bitwise_not(mask)
        result = cv2.bitwise_and(image, image, mask= inverse_mask)

        result_gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

        #Aplicación de umlbral para obtener imagen binaria
        umbral_fijo = 0
        _, binary_image = cv2.threshold(result_gray, umbral_fijo, 255, cv2.THRESH_BINARY)

        iteraciones_erosion = self.slider_erosion.value()
        iteraciones_dilatacion = self.slider_dilatacion.value()
        iteraciones_erosion2 = self.slider_erosion2.value()
        iteraciones_dilatacion2 = self.slider_dilatacion2.value()

        kernel = np.ones((5,5),np.uint8)

        dilatacion = cv2.dilate(binary_image, kernel, iterations=iteraciones_dilatacion)
        erosion = cv2.erode(dilatacion, kernel, iterations=iteraciones_erosion)
        dilatacion2 = cv2.dilate(erosion, kernel, iterations=iteraciones_dilatacion2)
        erosion2 = cv2.erode(dilatacion2, kernel, iterations=iteraciones_erosion2)
        
        height, width = erosion2.shape
        bytes_per_line = 1 * width
        q_image = QImage(erosion2.data, width, height, bytes_per_line, QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(q_image)
        self.label_red.setText(str(red_value))
        self.label_green.setText(str(green_value))
        self.label_blue.setText(str(blue_value))
        self.label_threshold.setText(str(threshold))
        self.label_erosion.setText(str(iteraciones_erosion))
        self.label_dilatacion.setText(str(iteraciones_dilatacion))
        self.label_erosion2.setText(str(iteraciones_erosion2))
        self.label_dilatacion2.setText(str(iteraciones_dilatacion2))
        self.label.setPixmap(pixmap)
        #255, 255, 123, 99
        #255, 141, 123, 99, 0 <---
        #255, 141, 123, 99, 1, 1, 5, 1

def main():
    app = QApplication([])
    window = ImageProcessor()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()