import argparse
from PIL import Image
import os
import sys


def get_parser_args():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--inputfile',
        required=True,
        help='Path to image file. Required parameter'
    )
    parser.add_argument(
        '-w', '--width',
        type=int,
        help='New width value. Ignored if --scale is used'
    )
    parser.add_argument(
        '-ht', '--height',
        type=int,
        help='New height value. Doesn\'t work without --width'
    )
    parser.add_argument(
        '-o', '--outpath',
        help='Path for saving output file. '
             'The same as input path by default, if not entered'
    )
    parser.add_argument(
        '-s', '--scale',
        type=float,
        help='Value to scale input image. Can be < 1'
    )

    return parser.parse_args()


def check_args_errors():
    if not args.inputfile:
        print('File is incorrect or missed')
        return False
    if args.scale and (args.width or args.height):
        print('You can specify only scale apart or width and height')
        return False
    if not any([args.scale, args.width]):
        print('You have to specify scale or width')
        return False
    return True


def treat_args(original_image, scale, width, height, path_to_result):
    if not path_to_result:
        path_to_result = os.path.dirname(args.inputfile)
    if not scale and not height:
        height = int(
            (original_image.height * width) / original_image.width
        )
    if scale:
        width = round(original_image.width * scale)
        height = round(original_image.height * scale)

    return path_to_result, width, height


def resize_image(original_image, width, height):

    return original_image.resize((width, height), Image.ANTIALIAS)


def save_image(resized_image, path_to_result, original_image):

    fullname = os.path.basename(original_image)
    filename, extension = os.path.splitext(fullname)
    resized_image.save(
        '{}\{}__{}x{}{}'.format(
            path_to_result,
            filename,
            resized_image.width,
            resized_image.height,
            extension
        )
    )


if __name__ == '__main__':

    args = get_parser_args()
    if not check_args_errors():
        sys.exit()
    image = Image.open(args.inputfile)

    path_to_result, width, height = treat_args(
        image,
        args.scale,
        args.width,
        args.height,
        args.outpath
    )

    resized_image = resize_image(
        image,
        width,
        height
    )
    save_image(resized_image, path_to_result, args.inputfile)
