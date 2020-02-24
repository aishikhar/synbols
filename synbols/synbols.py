#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cairo
import numpy as np

# from osx_non_free_fonts import LATIN_FONTS, FUNKY_LATIN_FONTS, GREEK_FONTS, CHINESE_FONTS, CYRILLIC_FONTS, CHINESE_SYMBOLS
from google_fonts import LATIN_FONTS, GREEK_FONTS

class Language:
    """Combines fonts and symbols for a given language."""

    def __init__(self, fonts, symbols):
        self.symbols = symbols
        self.fonts = fonts

    def partition(self, ratio_dict, rng=np.random.RandomState(42)):
        """Splits both fonts and symbols into different partitions to define meta-train, meta-valid and meta-test.

        Args:
            ratio_dict: dict mapping the name of the subset to the ratio it should contain
            rng: a random number generator defining the randomness of the split

        Returns:
            A dict mapping the name of the subset to a new Language instance.
        """
        set_names, ratios = zip(*ratio_dict.items())
        symbol_splits = _split(self.symbols, ratios, rng)
        font_splits = _split(self.fonts, ratios, rng)
        return {set_name: Language(fonts, symbols)
                for set_name, symbols, fonts in zip(set_names, symbol_splits, font_splits)}


LANGUAGES = {
    'latin': Language(
        LATIN_FONTS,
        list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")),
    # 'latin': Language(
    #     LATIN_FONTS + FUNKY_LATIN_FONTS,
    #     list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")),
    # 'greek': Language(
    #     GREEK_FONTS,
    #     list(u"ΑαΒβΓγΔδΕεΖζΗηΘθΙιΚκΛλΜμΝνΞξΟοΠπΡρΣσΤτΥυΦφΧχΨψΩω")),
    # 'cyrillic': Language(
    #     CYRILLIC_FONTS,
    #     list(u"АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя")),
    # 'chinese': Language(CHINESE_FONTS, CHINESE_SYMBOLS),
    # # 'korean': Language(CHINESE_FONTS, KOREAN_SYLLABLES)
}


def draw_image(ctxt, attributes):
    """Core function drawing the characters as described in `attributes`

    Args:
        ctxt: cairo context to draw the image
        attributes: Object of type Attributes containing information about the image

    Returns:
        extent: rectangle containing the text in the coordinate of the context
        extent_main_char: rectangle containing the central character in the coordinate of the context
    """
    make_background(ctxt)

    weight = cairo.FONT_WEIGHT_BOLD if attributes.is_bold else cairo.FONT_WEIGHT_NORMAL

    char = attributes.char

    ctxt.set_font_size(0.7)
    ctxt.select_font_face(attributes.font_family, attributes.slant, weight)
    extent = ctxt.text_extents(char)
    if len(char) == 3:
        extent_main_char = ctxt.text_extents(char[1])
    elif len(char) == 1:
        extent_main_char = extent
    else:
        raise Exception("Unexpected length of string: %d. Should be either 3 or 1" % len(char))

    if extent_main_char.width == 0. or extent_main_char.height == 0:
        print(char, attributes.font_family)
        return

    ctxt.translate(0.5, 0.5)
    scale = 0.6 / np.maximum(extent_main_char.width, extent_main_char.height)
    ctxt.scale(scale, scale)
    ctxt.scale(*attributes.scale)

    ctxt.rotate(attributes.rotation)

    if len(char) == 3:
        ctxt.translate(-ctxt.text_extents(char[0]).x_advance - extent_main_char.width / 2., extent_main_char.height / 2)
        ctxt.translate(*attributes.translation)
    else:
        ctxt.translate(-extent.width / 2., extent.height / 2)
        ctxt.translate(*attributes.translation)

    pat = random_pattern(0.8, (0.2, 1), patern_types=('linear',))
    ctxt.set_source(pat)
    ctxt.show_text(char)

    return extent, extent_main_char


class Attributes:
    """Class containing attributes describing the image

    Attributes:
        language: TODO(allac)
        char: string of 1 or more characters in the image
        font_family: string describing the font used to draw characters
        background: TODO(allac)
        slant: one of cairo.FONT_SLANT_ITALIC, cairo.FONT_SLANT_NORMAL, cairo.FONT_SLANT_OBLIQUE
            default: Uniform random
        is_bold: bool describing if char is bold or not
            default: Uniform random
        rotation: float, rotation angle of the text
            default: Normal(0, 0.2)
        scale: float, scale of the text
            default: Normal(0, 0.1)
        translation: relative (x, y) translation of the text
            default: Normal(0.1, 0.2)
        inverse_color: bool describing if color is inverted or not
            default: Uniform random
        pixel_noise_scale: standard deviation of pixel-wise noise
            default: 0.01
        resolution: tuple of int for (width, height) of the image
            default: (32, 32) (TODO(allac) fix bug when width != height)

    """

    def __init__(self, language, char, font_family, background=None,
                 slant=None, is_bold=None, rotation=None, scale=None, translation=None, inverse_color=None,
                 pixel_noise_scale=0.01, resolution=(32, 32), rng=np.random.RandomState(42)):
        self.language = language
        self.char = char
        self.font_family = font_family

        if is_bold is None:
            is_bold = rng.choice([True, False])
        self.is_bold = is_bold

        if slant is None:
            slant = rng.choice((cairo.FONT_SLANT_ITALIC, cairo.FONT_SLANT_NORMAL, cairo.FONT_SLANT_OBLIQUE))
        self.slant = slant

        self.background = background

        if rotation is None:
            rotation = rng.randn() * 0.2
        self.rotation = rotation

        if scale is None:
            scale = tuple(np.exp(rng.randn(2) * 0.1))
        self.scale = scale

        if translation is None:
            translation = tuple(rng.rand(2) * 0.2 - 0.1)
        self.translation = translation

        if inverse_color is None:
            inverse_color = rng.choice([True, False])
        self.inverse_color = inverse_color

        self.resolution = resolution
        self.pixel_noise_scale = pixel_noise_scale
        self.rng = rng

        # populated by make_image
        self.text_rectangle = None
        self.main_char_rectangle = None

    def make_image(self):
        width, height = self.resolution
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        ctxt = cairo.Context(surface)
        ctxt.scale(width, height)  # Normalizing the canvas
        self.text_rectangle, self.main_char_rectangle = draw_image(ctxt, self)
        buf = surface.get_data()
        img = np.ndarray(shape=(width, height, 4), dtype=np.uint8, buffer=buf)
        img = img.astype(np.float32) / 256.
        img = img[:, :, 0:3]
        if self.inverse_color:
            img = 1 - img

        min, max = np.min(img), np.max(img)
        img = (img - min) / (max - min)

        img += self.rng.randn(*img.shape) * self.pixel_noise_scale
        img = np.clip(img, 0., 1.)

        return img


def random_pattern(alpha=0.8, brightness_range=(0, 1), patern_types=('linear', 'radial'), rng=np.random):
    """"Select a random pattern with either radioal or linear gradient."""
    pattern_type = rng.choice(patern_types)
    if pattern_type == 'linear':
        y1, y2 = rng.rand(2)
        pat = cairo.LinearGradient(-1, y1, 2, y2)
    if pattern_type == 'radial':
        x1, y1, x2, y2 = rng.randn(4) * 0.5
        pat = cairo.RadialGradient(x1 * 2, y1 * 2, 2, x2, y2, 0.2)

    def random_color():
        b_delta = brightness_range[1] - brightness_range[0]
        return rng.rand(3) * b_delta + brightness_range[0]

    r, g, b = random_color()
    pat.add_color_stop_rgba(1, r, g, b, alpha)
    r, g, b = random_color()
    pat.add_color_stop_rgba(0.5, r, g, b, alpha)
    r, g, b = random_color()
    pat.add_color_stop_rgba(0, r, g, b, alpha)
    return pat


def solid_pattern(alpha=0.8, brightness_range=(0, 1), rng=np.random):
    def random_color():
        b_delta = brightness_range[1] - brightness_range[0]
        return rng.rand(3) * b_delta + brightness_range[0]

    r, g, b = random_color()
    return cairo.SolidPattern(r, g, b, alpha)


def make_background(ctxt, rng=np.random):
    """Random background combining various patterns."""
    for i in range(5):
        pat = random_pattern(0.4, (0, 0.8), rng=rng)
        ctxt.rectangle(0, 0, 1, 1)  # Rectangle(x0, y0, x1, y1)
        ctxt.set_source(pat)
        ctxt.fill()


def _split(set_, ratios, rng=np.random.RandomState(42)):
    n = len(set_)
    counts = np.round(np.array(ratios) * n).astype(np.int)
    counts[0] = n - np.sum(counts[1:])
    set_ = rng.permutation(set_)
    idx = 0
    sets = []
    for count in counts:
        sets.append(set_[idx:(idx + count)])
        idx += count
    return sets


def make_ds_from_lang(lang, width, height, n_samples, rng=np.random.RandomState(42)):
    """Temporary high level interface for making a dataset"""
    dataset = []
    for char in lang.symbols:
        one_class = []
        print(u"generating sample for char %s" % char)
        for i in range(n_samples):
            font = rng.choice(lang.fonts)
            attributes = Attributes(lang, char, font, resolution=(width, height), rng=rng)
            x = attributes.make_image()
            one_class.append(x)

        dataset.append(np.stack(one_class))
    return dataset
