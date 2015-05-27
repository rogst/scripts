#!/usr/bin/env python
# encoding: utf-8

"""
imagefile.py

Copyright (c) Roger Steneteg. All rights reserved.
"""

import exifread  # EXIF Metadata reader
import datetime
import os


class ImageFile():
    """Wrapper for processing image files."""
    def __init__(self, path, use_modified_date=False):
        self.file_path = path
        self.filename = os.path.basename(path)
        self.dir_path = os.path.dirname(path)
        self.image_date = None
        self.modified_date = datetime.datetime.fromtimestamp(
            os.path.getmtime(self.file_path))

        self._parse_exif_date()

    def __str__(self):
        return self.filename

    def _parse_exif_date(self):
        tags = []
        try:
            with open(self.file_path, "rb") as image:
                tags = exifread.process_file(image, details=False)
        except:
            pass

        exif_date_tags = ["Image DateTime",
                          "EXIF DateTimeOriginal",
                          "EXIF DateTimeDigitized",
                          "File Modification Date/Time"]

        timestamp = None
        for tagname in exif_date_tags:
            if tagname not in tags:
                continue

            # Split date and time
            date = tags[tagname]
            date_parts = str(date).strip().split()
            if len(date_parts) < 1:
                continue

            # Split date
            date = date_parts[0]
            date_parts = date.split(":")

            # Form date object
            date = datetime.datetime(int(date_parts[0]),
                                     int(date_parts[1]),
                                     int(date_parts[2]))

            if timestamp is None:
                timestamp = date
            else:
                if date < timestamp:
                    timestamp = date

        self.image_date = timestamp

    def get_timestamp(self, use_modified_date=False):
        if self.image_date is None and use_modified_date is True:
            return self.modified_date

        return self.image_date

    def _generate_unique_filename(self, path):
        """Generate a unique filename by adding a numeric prefix"""
        filename = os.path.basename(path)
        folder = os.path.dirname(path)
        unique_filename = "{}/{}".format(folder, filename)
        prefix = 1
        while os.path.exists(unique_filename):
            unique_filename = "{}/{}_{}".format(folder, prefix, filename)
            prefix += 1

        return unique_filename

    def move(self, destination):
        """Move file to destination folder"""
        if not os.path.exists(destination):
            os.makedirs(destination)

        # Make sure the destination path is unique
        final_destination = self._generate_unique_filename(
            destination.rstrip("/") + "/" + self.filename.lstrip("/"))

        os.rename(self.file_path, final_destination)

        self.file_path = final_destination
        self.filename = os.path.basename(final_destination)
        self.dir_path = os.path.dirname(final_destination)
