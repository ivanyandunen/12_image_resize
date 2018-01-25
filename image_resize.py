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
        help='Path to resized file. '
             'The same as input path by default, if not entered'
    )
    parser.add_argument(
        '-s', '--scale',
        type=float,
        help='Value to scale input image. Can be < 1'
    )

    return parser.parse_args()


def check_args_errors(original_image):
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


def check_aspect_ratio(original_image):
    if args.width and args.height:
        if ((args.width / args.height)
                != (original_image.width / original_image.height)):
            print(
                'Warning!!! Aspect ratio of resized image will be different'
            )


def calculate_width_and_height(original_image, scale, width, height):
    if not scale and not height:
        height = int(
            (original_image.height * width) / original_image.width
        )
    if not scale and not width:
        width = int(
            (original_image.width * height) / original_image.height
        )
    if scale:
        width = round(original_image.width * scale)
        height = round(original_image.height * scale)

    return width, height


def resize_image(original_image, width, height):

    return original_image.resize((width, height), Image.ANTIALIAS)


def save_image(resized_image, path_to_result, original_image):
    if path_to_result:
        resized_image.save(path_to_result)
    else:
        filename, extension = os.path.splitext(original_image)
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
    if not check_args_errors(image):
        sys.exit()
    check_aspect_ratio(image)
    width, height = calculate_width_and_height(
        image,
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
