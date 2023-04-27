from PIL import Image
from PIL.ExifTags import TAGS
import sys

class Scorpion():
    avoid = ['exif', 'icc_profile', 'XML:com.adobe.xmp']
    def __init__(self, arguments):
        print('initializing')
        for image_file in arguments:
            self.print_file_meta(image_file)
            print('----------')
    def print_file_meta(self, image_file):
        print(f'\nGETTING FILE: {image_file}')
        try:
            image = Image.open(image_file)
        except Exception:
            print(f"Unable to open {image_file}")
            return ;
        meta = {
            "Filename": image.filename,
            "Image Size": image.size,
            "Image Height": image.height,
            "Image Width": image.width,
            "Image Format": image.format,
            "Image Mode": image.mode,
            "Image is Animated": getattr(image, "is_animated", False),
            "Frames in Image": getattr(image, "n_frames", 1)
        }
        print("General")
        for key, value in meta.items():
            if key in self.avoid:
                continue
            print(f'  {key}: {value}')
        print("Other")
        for key, value in image.info.items():
            if key in self.avoid:
                continue
            print(f'  {key}: {value}')
        if ('getexif' not in dir(image)): 
            return 
        exif = image.getexif()
        first = True
        for key, value in exif.items():
            if (first):
                print("\nExif metadata")
                first = False
            data_name = TAGS[key]
            print(f'  {data_name}: {value}')

if (__name__ == '__main__'):
    scorpion = Scorpion(sys.argv[1:])
