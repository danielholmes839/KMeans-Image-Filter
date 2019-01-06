import os
from functions import kmeans_filter_from_file_path, kmeans_filter_from_url


def file_input():
    """ Takes a file name to get the image """
    image_name = str(input('file name: '))                              # image name
    folder_name = image_name.split('.')[0]                              # folder name will be the image name excluding the file type

    if not os.path.exists(folder_name):                                 # if there is no folder
        os.makedirs(folder_name)                                        # create a folder

    num_colours = int(input('number of colours: '))                     # number of colours / clusters

    filtered_img = kmeans_filter_from_file_path(image_name, num_colours, skip)                                  # get the filtered image
    filtered_img.save(folder_name + os.sep + 's' + str(skip) + '-' + str(num_colours) + 'clusters.png', 'png')  # save the image as a png


def url_input():
    """ Takes a url to get the image """
    image_url = str(input('image url: '))
    folder_name = str(input('output folder (will be created if it does not exist): '))

    if not os.path.exists(folder_name):                             # if there is no folder
        os.makedirs(folder_name)                                    # create a folder

    num_colours = int(input('number of colours: '))                 # number of colours / clusters

    filtered_img = kmeans_filter_from_url(image_url, num_colours, skip)     # get the filtered image
    filtered_img.save(folder_name + os.sep + 's' + str(skip) + '-' + str(num_colours) + 'clusters.png', 'png')  # save the image as a png


while True:
    skip = 1                                                        # 1/skip^2 pixels will be used to train the classifier. can be increased to reduce the time the program takes to run
    file_or_url = str(input('image from file or url: '))            # choose to get an image from a url or a file

    if file_or_url.lower() == 'file':
        filtered_img = file_input()

    elif file_or_url.lower() == 'url':
        filtered_img = url_input()

    else:
        print('Sorry you did not enter a valid option.')
        continue                                                    # new loop

    yes_or_no = str(input('would you like to process more images? [y/n]: ')).lower()
    if yes_or_no != 'y':
        break
