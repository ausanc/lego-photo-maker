import sys
from PIL import Image


# convert an input image into a minimised greyscale image
def create_minimised_image(input_image):
    image = input_image.convert("L")
    return image.resize((48, 48))


# TODO: create a template for building from a minimised image
def min_to_template(min_image):
    return min_image.resize((480, 480), Image.NEAREST)  # placeholder


# TODO: convert a greyscale minimised image to the lego colour palette
def convert_to_lego_colors(min_image):
    pass


def main():
    if len(sys.argv) > 1:
        image = Image.open("testimg.jpg")
        image = create_minimised_image(image)
        image = min_to_template(image)
        image.save("output.jpg")
    else:
        print("No argument supplied.")


if __name__ == '__main__':
    main()
