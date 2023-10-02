from typing import Tuple


def hex_to_rgb_percentage(hex_color: str) -> Tuple[float, float, float]:
    """
    Converts a hexadecimal color code to RGB percentage values.

    Args:
        hex_color (str): A string representing a hexadecimal color code.

    Returns:
        A tuple containing the red, green, and blue percentage values as floats in the range [0-1].
    """
    hex_color = hex_color.lstrip("#")
    red = int(hex_color[0:2], 16)
    green = int(hex_color[2:4], 16)
    blue = int(hex_color[4:6], 16)
    red_percentage = red / 255
    green_percentage = green / 255
    blue_percentage = blue / 255
    return (red_percentage, green_percentage, blue_percentage)


def rgb_percentage_to_hex(rgb: Tuple[float, float, float]) -> str:
    """
    Converts an RGB color represented as a tuple of percentages to its hexadecimal representation.

    Args:
        rgb: A tuple of three floats representing the red, green, and blue components of the color,
             respectively, as percentages in the range [0, 1].

    Returns:
        A string representing the hexadecimal representation of the input color, in the format "#RRGGBB",
        where RR, GG, and BB are two-digit hexadecimal numbers representing the red, green, and blue
        components of the color, respectively.

    Example:
        >>> rgb_percentage_to_hex((0.5, 0.75, 1.0))
        '#7FCCFF'
    """
    # Ensure the input percentages are in the valid range [0, 1]
    red_percentage, green_percentage, blue_percentage = rgb

    # Convert the percentages to decimal values
    red = int(red_percentage * 255)
    green = int(green_percentage * 255)
    blue = int(blue_percentage * 255)

    # Convert the decimal values to hexadecimal format
    hex_color = "#{:02X}{:02X}{:02X}".format(red, green, blue)

    return hex_color
