import argparse
from PIL import Image
import os


def parser_args():

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


def scale_image(original_image, scale):

    original_width = original_image.width
    original_height = original_image.height
    width = round(original_width * scale)
    height = round(original_height * scale)

    return original_image.resize((width, height), Image.ANTIALIAS)


def resize_image(original_image, width, height):

    if not args.height:
        original_width = original_image.width
        original_height = original_image.height
        height = int((original_height * width) / original_width)

    return original_image.resize((width, height), Image.ANTIALIAS)


def save_image(resized_image, path_to_result):

    if not args.outpath:
        path_to_result = os.path.dirname(args.inputfile)

    basename = os.path.basename(args.inputfile)
    filename = os.path.splitext(basename)
    resized_image_width = resized_image.width
    resized_image_height = resized_image.height
    resized_image.save(
        '{}\{}__{}x{}{}'.format(
            path_to_result,
            filename[0],
            resized_image_width,
            resized_image_height,
            filename[1]
        )
    )


if __name__ == '__main__':
    try:
        args = parser_args()
        image = Image.open(args.inputfile)

        if args.scale:
            resized_image = scale_image(image, args.scale)
        else:
            resized_image = resize_image(image, args.width, args.height)

        save_image(resized_image, args.outpath)
    except FileNotFoundError:
        print('File is incorrect or missed')
    except TypeError:
        print('You have to specify scale or width')
    except ValueError:
        print('Values must be > 0')
