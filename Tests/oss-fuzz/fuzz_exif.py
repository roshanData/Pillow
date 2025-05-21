#!/usr/bin/env python3

# Copyright 2025 Google LLC

import atheris
from atheris.import_hook import instrument_imports

with instrument_imports():
    import io
    import sys
    from PIL import Image, ExifTags

def TestOneInput(data):
    if len(data) < 10:
        return

    try:
        image_io = io.BytesIO(data)

        with Image.open(image_io) as img:
            try:
                exif = img._getexif()
                if exif:
                    for tag_id, value in exif.items():
                        if tag_id == 34853:  # GPSInfo tag
                            for gps_tag, gps_value in value.items():
                                _ = ExifTags.GPSTAGS.get(gps_tag, gps_tag)
            except Exception:
                pass

            try:
                if hasattr(img, 'getexif'):
                    exif = img.getexif()
                    if exif and hasattr(exif, 'get_thumbnail'):
                        thumbnail = exif.get_thumbnail()
                        if thumbnail:
                            thumb_img = Image.open(io.BytesIO(thumbnail))
                            thumb_img.load()
            except Exception:
                pass

    except Exception:
        pass

def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()

if __name__ == "__main__":
    main()
