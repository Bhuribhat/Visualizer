import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


def create_map(image_path):
    rows = image.shape[0] // 32
    cols = image.shape[1] // 32

    image = cv2.imread(image_path)
    gray  = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    resize = cv2.resize(gray, (cols, rows))
    binary = cv2.threshold(resize, 128, 1, cv2.THRESH_BINARY)[1]
    return binary


def create_grid(image_path):
    image = Image.open(image_path)
    image = np.asarray(image)
    image = rgb_2_gray(image)
    image = normalizes(image)
    return image


def rgb_2_gray(image):
    return np.dot(image[..., :3], [0.299, 0.587, 0.144])


def binary_threshold(image):
    image[image >  0.3] = 1
    image[image <= 0.3] = 0
    return image


def normalizes(image):
    normalized_image = np.zeros_like(image.astype(float))

    # number of image, [height, width and depth of the image]
    iteration = image.shape[0]

    # minimum and maximum value of the input image to do the normalization
    maximum_value, minimum_value = image.max(), image.min()

    # Normalize all the pixel values of the image to be from 0 to 1
    for img in range(iteration):
        normalized_image[img, ...] = (image[img, ...] - float(minimum_value)) / \
                                     (float(maximum_value - minimum_value))
    return normalized_image


if __name__ == '__main__':
    image_path = '../assets/map.png'
    grid = create_map(image_path)
    matrix  = create_grid(image_path)

    # print(np.unique(matrix))
    print(f"Min   = {matrix.min():.2f}")
    print(f"Max   = {matrix.max():.2f}")
    print(f"Avg   = {matrix.mean():.2f}")
    print(f"Shape = {matrix.shape}\n")

    # create binary 1 for wall, 0 otherwise
    binary = matrix.copy()

    # binary threshold
    binary[matrix  > 0.3] = 1
    binary[matrix <= 0.3] = 0

    # display gray scale image
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    axes[0].imshow(matrix, cmap='gray')
    axes[1].imshow(binary, cmap='gray')
    axes[2].imshow(grid,   cmap='gray')

    axes[0].set_title("Matrix")
    axes[1].set_title("Binary")
    axes[2].set_title("Grid")

    fig.tight_layout()
    plt.show()