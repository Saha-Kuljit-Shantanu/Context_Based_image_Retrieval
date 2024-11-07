from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

img = Image.open(dir_path + "\\CBT.png")
img.show()
img = img.convert("L")
img.show()
img = np.asarray(img)
print(img.shape[0], img.shape[1])
h = [0]*256
for x in range(img.shape[0]) :

    for y in range(img.shape[1]) :

        i = img[x,y]
        h[i] = h[i] + 1


i = np.arange(0,256,1)

plt.plot(i,h)
plt.show()
