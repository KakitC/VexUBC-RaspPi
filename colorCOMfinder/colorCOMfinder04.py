# Feb 5, 2014

import numpy as np
from colorsys import *
from collections import deque
from PIL import Image


def pixel_compare(pixel, targ):
    """ Check if a pixel's rgb value is within a target RGB range array

        Args:
            rgb: <3-tuple> RGB pixel value
            targ: <3x2 list> RGB min and max range for matching
        Returns:
            <bool> Whether or not the pixel matched the target range
        """

    return all([pixel[i] <= targ[0][i] for i in range(3)]) \
        and all([pixel[i] >= targ[1][i] for i in range(3)])


def neighbor_px(px, img_data):
    """ Return the list of cardinal neighbors to the px if they exist
        and have not been searched yet, determined by the pixel alpha channel.

        Args:
            px: <2-tuple> Coordinates of current pixel
            img_data: <np.Array> 3D array of image data (MxNxRGBA)
        Returns:
            List of unchecked, valid neighboring px's
        """

    neighbors = []
    m, n = px

    if m > 0 and img_data[m - 1][n][3] > checked_alpha:
        neighbors.append((m - 1, n))
    if n > 0 and img_data[m][n - 1][3] > checked_alpha:
        neighbors.append((m, n - 1))
    if m < img_data.shape[0]-1 and img_data[m + 1][n][3] > checked_alpha:
        neighbors.append((m + 1, n))
    if n < img_data.shape[1]-1 and img_data[m][n + 1][3] > checked_alpha:
        neighbors.append((m, n + 1))

    return neighbors


def gen_px_list(res):
    """ Generate a list of px coordinates to search through.

        Args:
            res - <2-tuple> Size of image array (height, width)
        Returns:
            <List> a list of px coordinates, as a square spiral out from center
    """

    h, w = res
    ctr = [int(h / 2), int(w / 2)]
    # Make a square spiral list
    px_list = [ctr, [ctr[0], ctr[1] + 1]]  # center, right one
    for l in range(2, max(h, w), 2):
        sub_list = [[px_list[-1][0] + 1, px_list[-1][1]]]  # One up of last
        # Up - 1, left, down, right
        sub_list += [[sub_list[-1][0], sub_list[-1][1] - n] for n in range(1, l + 1)]
        sub_list += [[sub_list[-1][0] - m, sub_list[-1][1]] for m in range(1, l + 1)]
        sub_list += [[sub_list[-1][0], sub_list[-1][1] + n] for n in range(1, l + 2)]
        sub_list += [[sub_list[-1][0] + m, sub_list[-1][1]] for m in range(1, l + 1)]

        px_list += sub_list

    return [xy for xy in px_list if (0 <= xy[0] < h) and (0 <= xy[1] < w)
            and (xy[0] % 2 == 0 and xy[1] % 2 == 0)]


def gen_rgb_range(hls_target, hls_thresh):
    """ Transform a target HLS range into less picky RGB range.

        Creates a 3x2 list of min and max RGB pairs. Not a
        perfect transform - this basically takes a cube in RGB
        space encompassing the HLS region we're searching for.

        Args:
            hls_target: <3-tuple> HLS target values
            hls_thresh: <3-tuple> HLS threshold ranges
        Returns:
            <3x2 list> RGB min and max values to match within
        """

    # Compute RGB coordinates for all the ways you can modify the hls_target
    # values by the threshold values (up, down, or all the same), and keep
    # the min and max R,G,B values from that set.

    # Compute all different HLS target ranges
    hls_list = []
    for mod_mult in [(h, l, s) for h in [-1, 0, 1]
                     for l in [-1, 0, 1] for s in [-1, 0, 1]]:
        mod_list = [0 for i in range(3)]
        mod_list[0] = hls_target[0] + hls_thresh[0] * mod_mult[0]
        mod_list[1] = hls_target[1] + hls_thresh[1] * mod_mult[1]
        mod_list[2] = hls_target[2] + hls_thresh[2] * mod_mult[2]

        # Wrap around hue value, clip saturation and luminosity
        mod_list[0] %= 255
        for i in [1, 2]:
            mod_list[i] = 0 if mod_list[i] < 0 else mod_list[i]
            mod_list[i] = 255 if mod_list[i] > 255 else mod_list[i]
        hls_list.append(mod_list)

    # Transform from HLS targets to RGB
    hls_norm = [[i[j] / 255 for j in range(3)] for i in hls_list]
    rgb_norm = [hls_to_rgb(i[0], i[1], i[2]) for i in hls_norm]
    rgb_list = [[i[j] * 255 for j in range(3)] for i in rgb_norm]

    # Get ranges from RGB targets
    rgb_arr = [[0 for j in range(3)] for i in range(2)]  # initialize array
    rgb_arr[0] = [int(max([rgb_list[j][i] for j in range(len(rgb_list))]))
                  for i in range(3)]
    rgb_arr[1] = [int(min([rgb_list[j][i] for j in range(len(rgb_list))]))
                  for i in range(3)]

    return rgb_arr


def show(pic_data, coords):
    """ Display a copy of the input picture with the target color marked
        with a cross.

        Doesn't run if there is none of that color in the picture.

        Args:
            pic_data: <Array> Modified image data from search result
            coords: <2-tuple> x-y coordinates of center of mass of target
        Returns:
            None
       """

    pic = Image.fromarray(pic_data)
    cross = Image.open('Black cross 64.png')

    box_corner = (coords[0] - round(cross.size[0]/2),
                  coords[1] - round(cross.size[1]/2))
    pic.paste(cross, tuple(box_corner), cross)
    pic.show()


def color_com_finder(pic, hls_target, hls_thresh=(20, 50, 50), show_flag=False):
    """ Finds the center of a contiguous blob of color in an image, and
        returns the coordinates.

        Works best on higher saturation targets, with high contrast.

        Args:
            test_pic: <Image> Picture to locate a color blob in
            hls_target: <3-tuple> HLS value (0-255) to search for
            hls_thresh: <3-tuple> Threshold range for picking out target color
            show_flag: <bool> Flag to show_flag a modified, searched copy of
                        the picture
        Returns:
            <2-tuple> Coordinates of center of a detected blob, or (-1,-1)
                    if not found
        """

    global blob_min_size
    global checked_alpha
    blob_min_size = 10
    checked_alpha = 127

    if pic.mode != "RGBA":
        img_data = np.array(pic.convert(mode="RGBA"))
    else:
        img_data = np.array(pic)

    target_arr = gen_rgb_range(hls_target, hls_thresh)
    height, width, _ = img_data.shape
    px_search_list = gen_px_list((height, width))

    hit_stack = deque([])
    hit_px_list = []

    for px in px_search_list:
        if not img_data[px[0]][px[1]][3] == checked_alpha \
                and not pixel_compare(img_data[px[0]][px[1]], target_arr):
            img_data[px[0]][px[1]][3] = checked_alpha

        else:
            # This is still slow, especially on large blotches of hit color
            # TODO make a perimeter search algorithm as another function
            # print("we got one!")
            hit_stack.append(px)
            hit_px_list.append(px)
            while hit_stack:
                x = hit_stack.pop()
                if pixel_compare(img_data[x[0]][x[1]], target_arr):
                    for i in neighbor_px(x, img_data):
                        hit_stack.appendleft(i)
                    hit_px_list.append(x)
                    img_data[x[0]][x[1]][3] = checked_alpha
                    img_data[x[0]][x[1]][0:3] = [255, 255, 255]
            if len(hit_px_list) >= blob_min_size:
                # print("we're done here")
                break
            hit_px_list.clear()
            # print("nevermind")

    if hit_px_list:
        com_x = sum([hit_px_list[i][1] for i in range(len(hit_px_list))])
        com_y = sum([hit_px_list[i][0] for i in range(len(hit_px_list))])
        com_x = int(com_x / len(hit_px_list))
        com_y = int(com_y / len(hit_px_list))
        if show_flag:
            show(img_data, (com_x, com_y))
    else:
        com_x, com_y = (-1, -1)  # Error code, not found
        # print("none of that colour found")

    return com_x, com_y

""" Algorithm notes
credit to James and Vincent for the idea, with their line following
    algorithm expecting the track to start in the center bottom of the screen
OpenCV not available for Python 3, aw

Generate a list of pixels to search in order (start in center, spiral outwards)
Iterate through list, just checking (not checked already) && (not matching)
Set A to 0 to mark checked
If hit, set alpha to 0, add position to hit_list, add pixel to hit_stack
Do DFS with stack to find all contiguous hit px's, marking A to 0
Check that hit_list length is bigger than threshold, get CoM coord, return
Else continue searching list

Rehighlight red pixels from list to debug
Don't hsl convert every pixel, convert targets and thresholds to rgb, then compare
Stop double checking pixels
"""


