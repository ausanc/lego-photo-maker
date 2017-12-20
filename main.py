import argparse
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
from PIL import Image

# TODO: export options: baseplate, tiles instead of plates
# TODO: saturation option
# TODO: simple background removal somehow and replace with yellow studs


# convert an input image into a minimised image
def create_minimised_image(image):
    return image.resize((48, 48))


# TODO: create a template for building from a minimised image
def min_to_template(min_image):
    return min_image.resize((480, 480), Image.NEAREST)  # placeholder


# takes an image and converts it to be in the provided palette
def convert_image_to_palette(image, palette):
    width, height = image.size
    rgb_colors = {}
    for key in palette.keys():
        c = palette[key]
        rgb_colors[key] = sRGBColor(c[0], c[1], c[2], is_upscaled=True)
    # rgb_colors = {key: sRGBColor(c[0], c[1], c[2], is_upscaled=True) for key, c in palette}
    lab_colors = {}
    for key in rgb_colors.keys():
        c = rgb_colors[key]
        lab_colors[key] = convert_color(c, LabColor)
    # lab_colors = {key: convert_color(c, LabColor) for key, c in rgb_colors}
    converted = Image.new('RGB', (width, height))

    counters = {}
    for w in range(width):
        for h in range(height):
            r, g, b = image.getpixel((w, h))
            pixel_color = convert_color(sRGBColor(r, g, b, is_upscaled=True), LabColor)
            differences = {}
            for key in lab_colors.keys():
                c = lab_colors[key]
                differences[key] = delta_e_cie2000(pixel_color, c)
            # differences = {key: delta_e_cie2000(pixel_color, c) for key, c in lab_colors}
            min_key = min(differences, key=differences.get)
            converted.putpixel((w, h), palette[min_key])
            counters[min_key] = counters.get(min_key, 0) + 1
    print(counters)
    return converted, counters


# crop an image to square, centered on the middle of the image
def crop_to_square(image):
    width, height = image.size
    shortest = min(width, height)
    h_crop = int((width - shortest) / 2)
    v_crop = int((height - shortest) / 2)
    return image.crop((h_crop, v_crop, width - h_crop, height - v_crop))


def hex_to_rgb(hex):
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))


def main():
    parser = argparse.ArgumentParser(description='Convert images to Lego greyscale images.')
    parser.add_argument('image', help='the image to be converted')
    args = parser.parse_args()

    greyscale_palette = {"white": (242, 243, 242),
                         "lbley": (163, 162, 164),
                         "dbley": (99, 95, 97),
                         "black": (27, 42, 52)}

    # http://lego.wikia.com/wiki/Colour_Palette
    # http://www.peeron.com/cgi-bin/invcgis/inv/colors
    main_palette = {"white":        hex_to_rgb('F2F3F2'),  # 1
                    "nougat":       hex_to_rgb('CC8E68'),  # 18
                    "red":          hex_to_rgb('C4281B'),  # 21
                    "blue":         hex_to_rgb('0D69AB'),  # 23
                    "yellow":       hex_to_rgb('F5CD2F'),  # 24
                    "black":        hex_to_rgb('1B2A34'),  # 26
                    "green":        hex_to_rgb('287F46'),  # 28
                    "bright green": hex_to_rgb('4B974A'),  # 37
                    "orange":       hex_to_rgb('DA8540'),  # 106
                    "teal":         hex_to_rgb('008F9B'),  # 107
                    "lime":         hex_to_rgb('A4BD46'),  # 119
                    "magenta":      hex_to_rgb('923978'),  # 124
                    "sand blue":    hex_to_rgb('74869C'),  # 135
                    "dark blue":    hex_to_rgb('203A56'),  # 140
                    "dark green":   hex_to_rgb('27462C'),  # 141
                    "sand green":   hex_to_rgb('789081'),  # 151
                    "dark red":     hex_to_rgb('7B2E2F'),  # 154
                    "reddish brown":hex_to_rgb('694027'),  # 192
                    "light grey":   hex_to_rgb('A3A2A4'),  # 194
                    "dark grey":    hex_to_rgb('635F61'),  # 199
                    }

    image = Image.open(args.image)
    image = crop_to_square(image)
    image = create_minimised_image(image)
    image, counters = convert_image_to_palette(image, greyscale_palette)
    image = min_to_template(image)
    image.save("output.jpg")

    # rewrite this section to work with new, generic palette system
    # template_counters = {"white": str(counters["white"]),
    #                      "lbley": str(counters["lbley"]),
    #                      "dbley": str(counters["dbley"]),
    #                      "black": str(counters["black"])}
    #
    # with open("template.xml", "r") as f:
    #     template = f.read().format(**template_counters)
    #     with open("output.xml", "w") as o:
    #         o.write(template)


if __name__ == '__main__':
    main()
