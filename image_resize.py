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
        help='New width value.'
    )
    parser.add_argument(
        '-ht', '--height',
        type=int,
        help="New height value."
    )
    parser.add_argument(
        '-o', '--outpath',
        help='Path to resized file. '
             'The same as input path by default, if not entered'
    )
    parser.add_argument(
        '-s', '--scale',
        type=float,
        help='Value to scale input image. Can be < 1'
    )

    return parser.parse_args()


def check_args_errors():
    if args.scale and (args.width or args.height):
        print('You can specify only scale apart or width and height')
        return False
    if not any([args.scale, args.width, args.height]):
        print('You have to specify scale, width or height')
        return False
    if args.outpath and os.path.isdir(args.outpath):
        print('The path you specified is a directory')
        return False
    if args.outpath and os.path.exists(args.outpath):
        print('Specified file exists')
        return False

    return True


def check_aspect_ratio(
        width,
        height,
        original_image_width,
        original_image_height
):
    if (width / height) != (original_image_width / original_image_height):
        print('Warning!!! Aspect ratio of resized image will be different')


def calculate_width_and_height(
        original_image_width,
        original_image_height,
        scale,
        width,
        height
):
    if not scale and not height:
        height = int(
            (original_image_height * width) / original_image_width
        )
    if not scale and not width:
        width = int(
            (original_image_width * height) / original_image_height
        )
    if scale:
        width = round(original_image_width * scale)
        height = round(original_image_height * scale)

    return width, height


def resize_image(original_image, width, height):

    return original_image.resize((width, height), Image.ANTIALIAS)


def save_image(resized_image, path_to_result, source_image_name):
    if path_to_result:
        resized_image.save(path_to_result)
    else:
        filename, extension = os.path.splitext(source_image_name)
        path_to_result = ('{}__{}x{}{}'.format(
                filename,
                resized_image.width,
                resized_image.height,
                extension
            )
        )
        resized_image.save(path_to_result)


if __name__ == '__main__':

    args = get_parser_args()
    image = Image.open(args.inputfile)
    if not check_args_errors():
        sys.exit()
    if args.width and args.height:
        check_aspect_ratio(args.width, args.height, image.width, image.height)
    width, height = calculate_width_and_height(
        image.width,
        image.height,
        args.scale,
        args.width,
        args.height
    )

    resized_image = resize_image(
        image,
        width,
        height
    )
    save_image(resized_image, args.outpath, args.inputfile)
