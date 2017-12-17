import sys
from PIL import Image

# TODO: fix output image colors to match proper lego colors
# TODO: crop input images to square
# TODO: export options: baseplate, tiles instead of plates
# TODO: saturation option
# TODO: simple background removal somehow and replace with yellow studs


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

        template_counters = {"white": str(counters["242"]),
        "lbley": str(counters["162"]),
        "dbley": str(counters["96"]),
        "black": str(counters["38"])}

        with open("template.xml", "r") as f:
            template = f.read().format(**template_counters)
            print(template)
            with open("output.xml", "w") as o:
                o.write(template)

        print(counters)
    else:
        print("No argument supplied.")


if __name__ == '__main__':
    main()
