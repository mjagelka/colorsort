#!/usr/bin/env python3

import argparse
import logging

from core import (check_path, generate_images, collect_images,
                  create_color_dict, create_folders)

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger()


def main() -> None:
    """Run the workflow."""
    parser = create_parser()
    args = parser.parse_args()
    path = check_path(args.path)

    if args.debug:
        LOG.setLevel(logging.DEBUG)

    if args.action == 'generate':
        images = generate_images(path, args.count, args.filename)
    elif args.action == 'use-existing':
        images = collect_images(path)

    color_dict = create_color_dict()
    create_folders(images, color_dict, path)


def create_parser() -> argparse.ArgumentParser:
    """Create an argument parser."""
    parser = argparse.ArgumentParser(
        description='Tool for image sorting based on average color')
    subparsers = parser.add_subparsers(
        help='Choose the option of image input', dest='action')

    # sub-parser for generated images
    generate_parser = subparsers.add_parser(
        'generate', help='Generate altered color copies of sample image')
    generate_parser.add_argument(
        '--count', type=int, help='Number of generated images')
    generate_parser.add_argument(
        '--filename', help='File name of the prototype image')

    # sub-parser for already existing images
    use_existing_parser = subparsers.add_parser(
        'use-existing', help='Use existing sample images')

    # add common args
    for subparser in [generate_parser, use_existing_parser]:
        subparser.add_argument(
            '--path', help='Absolute or relative path to the folder '
                           'containing sample image(s)')
        subparser.add_argument('--debug', action='store_true',
                               help='Show debug logging')

    return parser


if __name__ == "__main__":
    main()
