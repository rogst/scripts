#!/usr/bin/env python
# encoding: utf-8

"""
sort-images.py

Copyright (c) Roger Steneteg. All rights reserved.
"""

import os
import sys

from imagefile import ImageFile


def sort_images(source, destination, structure, use_modified_date=False):
    """Sort images"""

    if not os.path.exists(source):
        raise Exception("Source directory does not exist.")

    # Walk through the source looking for new images
    for root, folders, files in os.walk(source):
        for file in files:
            full_path = root.rstrip("/") + "/" + file.lstrip("/")

            # Ignore directories
            if os.path.isdir(full_path):
                continue

            # Create a ImageFile wrapper object for the file
            imagefile = ImageFile(
                full_path,
                use_modified_date=use_modified_date)

            # If no date is found ignore the file
            date = imagefile.get_timestamp()
            if date is None:
                continue

            # Generate destination path
            destination_path = "{}/{}/".format(
                destination.rstrip("/"),
                date.strftime(structure))

            # Move file
            imagefile.move(destination_path)

            print("Moved {} to {}.\n".format(
                full_path,
                imagefile.file_path))


def main():
    """Parse command line arguments."""
    import argparse
    parser = argparse.ArgumentParser(description="Sort Images into date based \
        hierarchy")
    parser.add_argument("source", type=str, help="Source directory")
    parser.add_argument("destination", type=str, help="Destination directory")
    parser.add_argument("--use-modified-date",
                        action="store_true",
                        help="Use file modified date if no EXIF data is found")
    parser.add_argument("--structure", type=str, default="%Y/%m/%d",
                        help="subfolder structure, default is %%Y/%%m/%%d which \
                        gives Year/Month/Day")
    args = parser.parse_args()

    try:
        sort_images(args.source,
                    args.destination,
                    use_modified_date=args.use_modified_date,
                    structure=args.structure)
    except Exception as e:
        print(e)
        sys.exit(1)
    except:
        print("An unknown error occured")
        sys.exit(1)


if __name__ == '__main__':
    main()
