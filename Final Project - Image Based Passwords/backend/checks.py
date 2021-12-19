from PIL import Image
import numpy as np
import os

PROJECT_DIR = os.path.dirname(os.path.realpath(__file__))
IMAGES_DIR = "images"


def check_existence(image_file):
    image_path = os.path.join(PROJECT_DIR, IMAGES_DIR, image_file)
    if os.path.exists(image_path):
        return image_path
    else:
        raise OSError("Request Image Does Not Exist")


def check_bounds(image_path, x, y):
    if x < 0 or y < 0:
        raise IndexError("Image Coordinated Out of Bounds")

    image = np.asarray(Image.open(image_path))
    x_max, y_max, _ = image.shape
    if x >= x_max or y >= y_max:
        raise IndexError("Image Coordinated Out of Bounds")


def get_radial_distance(password_point, provided_point):
    password_x, password_y = password_point
    provided_x, provided_y = provided_point
    return abs(password_x - provided_x) + abs(password_y - provided_y)


def get_midpoint(point1, point2):
    p1_x, p1_y = point1
    p2_x, p2_y = point2

    mid_x = round((p1_x + p2_x) / 2)
    mid_y = round((p1_y + p2_y) / 2)
    return mid_x, mid_y
