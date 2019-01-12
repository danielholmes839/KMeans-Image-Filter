# Daniel Holmes
# 2018/1/6
# Functions
# These are the functions used for the KMeans colour filter

import math
from PIL import Image
from sklearn.cluster import KMeans
from urllib.request import Request, urlopen


def open_image_path(image_path):
    """ open image from file path """
    img = Image.open(image_path, 'r')
    width, height = img.size

    return img, width, height


def open_image_url(url):
    """ open image from a url """
    request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    img = Image.open(urlopen(request))
    width, height = img.size

    return img, width, height


def get_pixels(img, width, height):
    # get data / read pixels
    pixels = []
    for y in range(height):
        for x in range(width):
            pixel_tuple = img.getpixel((x, y))

            pixels.append([pixel_tuple[0], pixel_tuple[1], pixel_tuple[2]])

    return pixels


def get_training_pixels(pixels, skip, width, height):
    """ get the pixels that will be used to train the classifier """

    if skip == 1:  # if skip equals 1 then all pixels will be kept so just return all the pixels
        return pixels

    training_pixels = []
    for y in range(0, height, skip):
        for x in range(0, width, skip):
            training_pixels.append(pixels[x + (y * width)])

    return training_pixels


def create_classifier(training_pixels, num_clusters):
    """ takes a list of pixels (training_pixels) and trains and returns a classifier """
    cls = KMeans(num_clusters)
    cls.fit(training_pixels)  # cluster the pixels from the image

    return cls


def make_predictions(cls, pixels):
    """ Decides which cluster each pixel belongs to """
    predictions = cls.predict(pixels)  # returns a list of which cluster each pixel belongs to

    return predictions


def get_sorted_pixels(pixels, predictions, num_clusters):
    """ Sorts the pixels into separate lists based on which cluster they belong to """
    sorted_pixels = []  # sorted_pixels will have multiple lists representing each cluster of pixels
    for i in range(num_clusters):
        sorted_pixels.append([])

    num_pixels = len(pixels)
    for i in range(num_pixels):
        sorted_pixels[predictions[i]].append(pixels[i])  # add each pixel to the array that represents the cluster it was put into

    return sorted_pixels  # return multiple lists of different pixels


def get_avg_pixels(sorted_pixels, num_clusters):
    """ Gets the avg colour for each cluster of pixels """
    avg_pixels = []

    for cluster in range(num_clusters):  # each cluster of pixels
        length = len(sorted_pixels[cluster])  # the number of pixels in that cluster

        for pixel_num in range(length):  # for every pixel
            for rgb_value in range(3):  # for every rgb value of each pixel
                sorted_pixels[cluster][pixel_num][rgb_value] *= sorted_pixels[cluster][pixel_num][rgb_value]  # average rgb by squaring all values, then divide by the amount of values and take the square root

        rgb = []  # avg rgb value for current cluster
        for rgb_value in range(3):  # for each rgb value
            sum = 0

            for pixel_num in range(length):  # for every pixel
                sum += sorted_pixels[cluster][pixel_num][rgb_value]  # add together all values of all r, g or b

            rgb.append(int(math.sqrt(sum / pixel_num)))  # take the square root of the sum divided by the number of pixels

        avg_pixels.append(rgb)

    return avg_pixels


def create_image(predictions, avg_pixels, width, height):
    """ creates the image """
    img = Image.new('RGB', (width, height))
    pixel_counter = 0

    for y in range(height):
        for x in range(width):
            img.putpixel((x, y), (avg_pixels[predictions[pixel_counter]][0], avg_pixels[predictions[pixel_counter]][1], avg_pixels[predictions[pixel_counter]][2]))
            pixel_counter += 1

    return img


def kmeans_filter_from_file_path(image_path, num_clusters, skip):
    """ all steps combined using a file path return a PIL Image that can be saved """
    img, width, height = open_image_path(image_path)

    pixels = get_pixels(img, width, height)
    training_pixels = get_training_pixels(pixels, skip, width, height)

    cls = create_classifier(training_pixels, num_clusters)
    predictions = make_predictions(cls, pixels)

    sorted_pixels = get_sorted_pixels(pixels, predictions, num_clusters)
    avg_pixels = get_avg_pixels(sorted_pixels, num_clusters)

    compressed_img = create_image(predictions, avg_pixels, width, height)

    return compressed_img


def kmeans_filter_from_url(image_url, num_clusters, skip):
    """ all steps combined using a url return a PIL Image that can be saved """
    img, width, height = open_image_url(image_url)

    pixels = get_pixels(img, width, height)
    training_pixels = get_training_pixels(pixels, skip, width, height)

    cls = create_classifier(training_pixels, num_clusters)
    predictions = make_predictions(cls, pixels)

    sorted_pixels = get_sorted_pixels(pixels, predictions, num_clusters)
    avg_pixels = get_avg_pixels(sorted_pixels, num_clusters)

    compressed_img = create_image(predictions, avg_pixels, width, height)

    return compressed_img
