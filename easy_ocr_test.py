import easyocr
import time
import numpy as np
import cv2
from pdf2image import convert_from_path
# from PIL import Image

# set False if using a cpu
gpu = True

reader = easyocr.Reader(['en'],gpu = gpu)

#converting to pdf
images = convert_from_path("test.pdf")
#converting the color space
image = cv2.cvtColor(np.array(images[0]), cv2.COLOR_RGB2BGR)



t1 = time.time()
result = reader.readtext(image)
t2 = time.time()

for i in result:
    print(i)

print(f"Time to extract {t2-t1} ; GPU : {gpu}")