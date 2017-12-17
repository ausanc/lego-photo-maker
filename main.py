import sys
from PIL import Image

# TODO: count number of 1x1s needed
# TODO: return bricklink xml
# TODO: fix lego color image colors to match proper bleys


# convert an input image into a minimised greyscale image
def create_minimised_image(input_image):
    image = input_image.convert("L")
    return image.resize((48, 48))


# TODO: create a template for building from a minimised image
def min_to_template(min_image):
    return min_image.resize((480, 480), Image.NEAREST)  # placeholder


# TODO: replace this with something which doesn't suck
def get_lego_color(color):
    # F2F3F2, A3A2A4, 635F61, 1B2A34
    # greyscale: 242, 162, 96, 38
    # mid-points: 202, 129, 67
    if color > 202:
        return 242
    elif color > 129:
        return 162
    elif color > 67:
        return 96
    else:
        return 38


# convert a greyscale minimised image to the lego colour palette
def convert_to_lego_colors(min_image):
    counters = {"242": 0, "162": 0, "96": 0, "38": 0}
    width, height = min_image.size
    converted = Image.new('RGB', (width, height))
    for h in range(height):
        for w in range(width):
            c = get_lego_color(min_image.getpixel((w, h)))
            counters[str(c)] = counters[str(c)] + 1
            converted.putpixel((w, h), (c, c, c))
    return converted, counters


def main():
    if len(sys.argv) > 1:
        image = Image.open(sys.argv[1])
        image = create_minimised_image(image)
        image, counters = convert_to_lego_colors(image)
        image = min_to_template(image)
        image.save("output.jpg")
        print(counters)
    else:
        print("No argument supplied.")


if __name__ == '__main__':
    main()
