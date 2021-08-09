import cv2
import logging
import numpy as np
import os
import random
import requests
from typing import Dict, List

from shutil import copy2
from bs4 import BeautifulSoup

LOG = logging.getLogger(__name__)

def check_path(path: str) -> str:
    """
    Check if the path exists and unify its format.

    Args:
        path: Folder path used to access the images to be sorted.

    Returns:
        Corrected folder path.
    """
    if path:
        path = path.rstrip('/') + '/'
        if not os.path.isdir(path):
            LOG.warning('Given path is incorrect. Default directory will be '
                        'used instead.')
            path = 'sample/'
    else:
        path = 'sample/'

    return path


def collect_images(path: str) -> Dict:
    """
    Collect all images located in a given folder.

    Args:
        path: Folder path where the images are located.

    Returns:
        Dictionary with file names as keys and BGR maps as values.
    """
    files = os.listdir(path)

    images = {}
    for file_name in files:
        img = cv2.imread(path + file_name)
        if img is None:
            LOG.warning(
                f'File {file_name} is probably not a valid image type.')
        else:
            images[file_name] = img

    LOG.info(f'There are {len(images.keys())} image(s) chosen.')
    if len(images) == 0:
        LOG.warning('The directory does not contain any images.')

    return images


def generate_images(path: str, count: int, filename: str) -> Dict:
    path = 'sample/' if not path else path
    filename = '04-nature_721703848.jpg' if not filename else filename
    img = cv2.imread(path + filename)
    images = {}
    for i in range(count):
        images['copy' + str(i)] = modify_color(img)
    return images

def modify_color(bgr):
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    h_shift = random.randint(0, 179)
    s_shift = random.random()
    v_shift = random.random()**0.5
    h_new = h + h_shift - 179*(h + h_shift > 179)
    h_new = h_new.astype('uint8')
    s_new = s*s_shift
    s_new = s_new.astype('uint8')
    v_new = v*v_shift
    v_new = v_new.astype('uint8')
    hsv_new = cv2.merge([h_new, s_new, v_new])
    bgr_new = cv2.cvtColor(hsv_new, cv2.COLOR_HSV2BGR)
    return bgr_new
    """cv2.imshow('Original image', bgr)
    cv2.imshow('HSV image', bgr_new)
    cv2.waitKey(0)
    cv2.destroyAllWindows()"""

#modify_color(cv2.imread('sample/04-nature_721703848.jpg'))

def get_average_color(image: np.array) -> List:
    """
    Count the average color value for image.

    Args:
        image: Instance of cv2 image.

    Returns:
        List of average BGR values.
    """
    return list(np.mean(np.mean(image, axis=0), axis=0))


def create_color_dict() -> Dict:
    """
    Parse Web colors table and extract the RGB values for basic colors.

    Returns:
        Basic color names with their BGR values.
    """
    color_dict = {}
    url = 'https://en.wikipedia.org/wiki/Web_colors'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    table = soup.find_all('tbody')[1]
    rows = table.find_all('tr')[1:]
    for row in rows:
        color_name = row.th.a.text
        columns = row.find_all('td')
        get_rgb_values = lambda x : int(columns[x].text.strip('%\n'))*2.56
        red = get_rgb_values(1)
        green = get_rgb_values(2)
        blue = get_rgb_values(3)
        color_dict[color_name] = [blue, green, red]
    return color_dict


def find_best_color(value: List, color_dict: Dict) -> str:
    """
    Compare the given color with basic colors and find the closest one.

    Args:
        value: BGR color representation.
        color_dict: Basic color names with their BGR values.

    Returns:
        Name of the closest basic color to given value.
    """
    metric = lambda a, b : abs(b[0] - a[0]) + abs(b[1] - a[1]) + \
                           abs(b[2] - a[2])
    best_color = ''
    lowest_difference = 1000
    for color in color_dict.keys():
        difference = metric(value, color_dict[color])
        if difference < lowest_difference:
            best_color = color
            lowest_difference = difference
    return best_color


def create_folders(images: Dict, color_dict: Dict, source: str) -> None:
    """
    Create color folders and populate them with sorted images.

    Args:
        images: Dictionary with file names as keys and BGR maps as values.
        color_dict: Basic color names with their BGR values.
        source: Folder path where the images are located.
    """
    os.mkdir('colors')
    for file_name, values in images.items():
        average_color = get_average_color(values)
        best_color = find_best_color(average_color, color_dict)
        destination = 'colors/' + best_color + '/'
        if not os.path.exists(destination):
            os.mkdir(destination)
            LOG.info(f'Creating \'{destination}\' folder')
        cv2.imwrite(source + file_name, values)
