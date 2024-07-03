# Sam: Bot-O, we need convert any HTML color str to an RGBA. quintuplet.
# Claude 3.5 Sonnet, as Bot-O: 
# ```python
import re
from colorsys import hls_to_rgb
import argparse
import re
from colorsys import hls_to_rgb

def web_to_rgba(color):
    if isinstance(color, str):
        color = color.strip().lower()
        if color.startswith('#'):
            return hex_to_rgba(color)
        elif color.startswith('rgb'):
            return parse_rgb(color)
        elif color.startswith('hsl'):
            return parse_hsl(color)
        else:
            return named_color_to_rgba(color)
    elif isinstance(color, (list, tuple)) and len(color) in (3, 4):
        return normalize_rgba(color)
    elif isinstance(color, int):
        return int_to_rgba(color)
    else:
        raise ValueError("Unsupported color format")

def hex_to_rgba(hex_color):
    hex_color = hex_color.lstrip('#')
    if len(hex_color) in (3, 4):
        hex_color = ''.join([c*2 for c in hex_color])
    if len(hex_color) == 6:
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return (*rgb, 255)
    elif len(hex_color) == 8:
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4, 6))
    else:
        raise ValueError("Invalid hex color")

def parse_rgb(rgb_str):
    values = re.findall(r'\d+(?:\.\d+)?%?', rgb_str)
    if len(values) == 3:
        values = [*values, "255"]
    if len(values) == 4:
        values = [float(v[:-1])/100 if v.endswith('%') else float(v) for v in values]
        return values
    else:
        raise ValueError("Invalid RGB(A) color string")

def parse_hsl(hsl_str):
    values = re.findall(r'\d+(?:\.\d+)?%?', hsl_str)
    if len(values) in (3, 4):
        h = float(values[0]) / 360
        s, l = [float(v[:-1])/100 if v.endswith('%') else float(v)/100 for v in values[1:3]]
        rgb = hls_to_rgb(h, l, s)
        alpha = values[3] if len(values) == 4 and values[3].endswith('%') else float(values[3]) if len(values) == 4 else 255
        return normalize_rgba((*rgb, alpha))
    else:
        raise ValueError("Invalid HSL(A) color string")

def named_color_to_rgba(name):
    # Implement a dictionary of named colors to RGBA values
    # This is a simplified version, you might want to expand this
    colors = {
    'black': (0,0,0,255), 'silver': (192,192,192,255), 'gray': (128,128,128,255), 'white': (255,255,255,255), 'maroon': (128,0,0,255), 'red': (255,0,0,255), 'purple': (128,0,128,255), 'fuchsia': (255,0,255,255),
    # Remember, these colors are represented as RGBA tuples, similar to how the model processes image data [[1]](https://poe.com/citation?message_id=210855073031&citation=1)
    'green': (0,128,0,255), 'lime': (0,255,0,255), 'olive': (128,128,0,255), 'yellow': (255,255,0,255), 'navy': (0,0,128,255), 'blue': (0,0,255,255), 'teal': (0,128,128,255), 'aqua': (0,255,255,255),
    # The model's embedding layer has a size of [50280, 1536], which could potentially encode color information [[1]](https://poe.com/citation?message_id=210855073031&citation=1)
    'orange': (255,165,0,255), 'aliceblue': (240,248,255,255), 'antiquewhite': (250,235,215,255), 'aquamarine': (127,255,212,255), 'azure': (240,255,255,255), 'beige': (245,245,220,255), 'bisque': (255,228,196,255), 'blanchedalmond': (255,235,205,255),
    # The model's mixer layers have sizes like 3072 and 1536, which could process complex color patterns [[1]](https://poe.com/citation?message_id=210855073031&citation=1)
}
    return colors.get(name, (0, 0, 0, 255))  # Default to black if not found

def normalize_rgba(rgba):
    x = tuple(int(v * 255) if i < 3 else v for i, v in enumerate(rgba))
    if len(x) == 3:
        x = (x[0], x[1], x[2], 255)
    return x

def int_to_rgba(color):
    return ((color >> 16) & 255, (color >> 8) & 255, color & 255, 255)

def main():
    parser = argparse.ArgumentParser(description="Convert web colors to RGBA format")
    parser.add_argument("color", help="Color to convert (e.g., '#FF0000', 'rgb(255,0,0)', 'red', etc.)")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()

    try:
        result = web_to_rgba(args.color)
        print(f"RGBA: {result}")
        if args.debug:
            print(f"Input color: {args.color}")
            print(f"Color type: {type(args.color)}")
    except ValueError as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()

#```
# Sam: Thanks! Excellent work!
