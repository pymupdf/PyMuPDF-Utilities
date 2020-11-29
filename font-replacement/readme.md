# Replacing Fonts in a PDF with PyMuPDF

Using PyMuPDF v1.17.6 or later, replacing fonts in an existing PDF becomes possible. This describes the How-To and some technical background.
## Features
It supports the following features:

* Replaces one or more fonts in a PDF.
* Always **embeds** new fonts.
* Keeps table of contents, annotations, links, images, etc. in place.
* Rewrites selected text with a new font maintaining the original layout as closely as possible.
* Builds subsets for new fonts based on their usage, thus reducing file size.

This makes it e.g. possible to replace **Courier** by a nicer monospaced font, or to take a modern sans-serifed font instead of Times-Roman, or similar.

## Technical Approach

* Each page is searched for text that is written with one of the obsolete fonts.
* These text pieces are inspected for their used unicodes.
* For each new font, a subset is built based on the used unicodes.
* Remove the text pieces, then rewrite them with the respective new font.

The script makes heavy use of and is dependent on MuPDF's page cleaning and text extraction facilities, `Page.cleanContents()` and `Page.getText("dict")`.

## Choosing Replacement Fonts
The actual font replacing script expects a JSON file which specifies, which old font should be replaced by which new font. You must execute a utility script which creates this JSON file. Then edit this file.

Here is an example:

```json
[
  {
    "oldfont": "",  # may happen - requires trial & error!
    "newfont": "keep",
    "info": "Not embedded!"  # always consider replacing this
  },
  {
    "oldfont": "Helvetica",
    "newfont": "keep",
    "info": "44 glyphs, size 3047, serifed, subset font"
  },
  {
    "oldfont": "Helvetica-BoldOblique",
    "newfont": "keep",
    "info": "7 glyphs, size 689, serifed, italic, bold, subset font"
  },
  {
    "oldfont": "TT5A5Ao00",
    "newfont": "keep",
    "info": "6 glyphs, size 1651, serifed, subset font"
  }
]
```

Now replace **"keep"** with the new desired font.

Use "info" to make up your decision. For example, if the old font has only a few used glyphs and / or has a small size, you might want to leave it untouched. Other information like "bold", "mono", etc. may also help choosing the right replacement.

Keep in mind however, that this latter information (provided by the font creator) is not reliable: you may see "serifed" although it is a "sans" font, or "mono" is missing even though it is a monospaced font, etc.

Use the following values to replace **"keep"** with a new font name:

* One of the Base-14 builtin reserved fontnames for Times-Roman, Helvetica, Courier, Symbol or ZapfDingbats (like "heit" = Helvetica-Oblique, "cobi" = "Courier-BoldOblique", etc.).
* One of the CJK reserved builtin fontnames, e.g. "china-t" for Traditional Chinese.
* One of the builtin fontnames available when [pymupdf-fonts](https://pypi.org/search/?q=pymupdf-fonts) is installed, e.g. "figo" for "FiraGO Regular", or "spacemo" for "Space Mono Regular".
* The file name of a font installed on your system, e.g. `C:/Windows/Fonts/DejaVuSerif-Bold.ttf`. In this case, make sure that the string contains at least one of "`.`", "`/`" or "`\`" to be recognizable as such.

The above example was created for a page with Japanese text. The following changes lead to a very nice and accurate result:

```json
[
  {
    "oldfont": "",
    "newfont": "japan",
    "info": "Not embedded!"
  },
  {
    "oldfont": "Helvetica",
    "newfont": "japan",
    "info": "44 glyphs, size 3047, serifed, subset font"
  },
  {
    "oldfont": "Helvetica-BoldOblique",
    "newfont": "japan",
    "info": "7 glyphs, size 689, serifed, italic, bold, subset font"
  },
  {
    "oldfont": "TT5A5Ao00",
    "newfont": "japan",
    "info": "6 glyphs, size 1651, serifed, subset font"
  }
]
```

All text was rewritten using ``fitz.Font("japan")``, the "Droid Sans Fallback Regular" font. The PDF size was **reduced** from 111 KB to 17 KB.

## Limitations, TODOs, Quality Checks
While this is a set of cool scripts, providing a long-awaited feature, it is not a "silver bullet": it does have its limitations and shortcomings.

In general, and independent from the scripts presented here, there are always issues when replacing a font. They include but are not limited to:

1. You will probably **_see unsatisfactory results_** replacing a **mono-spaced** with a **proportional** font, and vice versa.
2. Even if fonts have similar characteristics (e.g. both are proportional), there usually exist differences for individual characters. This may lead to different text lengths, even if font sizes are equal - just think of Arial vs. Arial Narrow. Because the page is not being completely rewritten, the replacing text piece must stay within the original rectangle by all means. This may or may not require reducing the fontsize - leading to an uneven overall appearance. The contrary may also happen: if the new font is narrower, it will produce shorter text lengths - leading to larger gaps to subsequent text pieces on the same line.
3. **Do not expect** that justified text remains justified!
4. **Do not expect** that every character with the new font will appear at the same position as with the old font.


Existing text is extracted via `page.getText("dict")`. This dictionary is critical for the overall success: while it does contain lots of information about each text span, it is **still not complete**, e.g.

* There is currently no way to determine whether the original text is actually visible. It may be covered by other objects like images (i.e. be in "background"), or be attributed as "hidden" or whatever - we wouldn't know about this. **Rewritten text will always be visible.**
* There is currently no way to tell whether text is under control of some opacity (transparency) instruction. **Rewritten text will be non-transparent**. The only way to "simulate" this is via adapting the script to your needs. For illustration purposes we have included logic that sets opacity to 20% if the font size is 100 or more.
* On rare occasions, inter-character spacing may be incorrectly computed by MuPDF: Words may be erroneously joined or drawn apart.
* Another important, heavily used MuPDF utility function is invoked by `Page.cleanContents()`. It concatenates multiple `/Contents` objects, purifies their command syntax and **synchronizes** the fonts **used,** with the fonts **listed** in the `/Resources` objects.

## Notes on Font Subsetting
A font contains basically two things: (1) code that generates a character's visual appearance (the "glyph") and (2) a mapping between the character code and its glyph. In a simplistic view, a font can be thought of being an array which does this mapping.

Obviously, the larger the set of characters a font supports, the larger will be its size. There are fonts which support many hundred or thousands of characters. For example "Droid Sans Fallback Regular" contains over 50,000 glyphs and has a file size of 3.6 MB.

On the other hand, for any given font in any given PDF, comparatively few of its glpyhs will **actually ever be used**. This used subset is often in the range of low two digit percentages, or even much less. Getting rid of the unused font portions is therefore an important vehicle to control PDF file sizes.

This is what **_font subsetting_** is all about. We use package [fontTools](https://pypi.org/project/fontTools/) to do this for OTF and TTF font types.

**fontTools** cannot create subsets for **_CFF type fonts_** (as far as we know).

However, to support embeddable versions of the old Base-14 fonts, MuPDF unfortunately chooses CFF fonts: the **_"Nimbus"_** font families by **URW++** (developed by _URW Type Foundry GmbH_). So, if you choose one of these to replace their non-embedded twins, the resulting PDF may become larger.

This is not necessarily a big problem: the Nimbus fonts are relatively small (around 50 KB or less - albeit per font weight). But you still may want to consider alternatives that do support subsetting.

There also exist free versions of the Nimbus fonts, **which are subsettable** (OTF or TTF formats). They can be downloaded from [this](https://www.fontsquirrel.com/fonts/) website. Search for nimbus-sans, nimbus-mono or nimbus-roman.

To illustrate the effect of font subsetting, look at the following example numbers of a 4-page PDF, once created as a PDF export of a Word document.

The original size is **240 KB** and it contains
* 63 glyphs sans-serif regular
* 34 glyphs sans-serif bold
* 24 glyphs mono-spaced bold
* 69 glyphs mono-spaced regular

Replacing these by (the non-subsettable) **"helv"** (33 KB), **"hebo"** (34 KB), **"cobo"** (51 KB) and **"cour"** (45 KB) Nimbus fonts respectively leads to the new file size **172 KB**.

When instead taking **"Noto Sans Regular"**, **"Noto Sans Bold"**, **"Space Mono Bold"** and **"Space Mono Regular"** (which all support font subsetting), the resulting file size is only **53 KB** ... and it looks nicer, too!


## How to replace a font with itself
This may sound ridiculous. But imagine you have inserted text in a PDF and now you are disappointed with the resulting file size: large-sized fonts have been pulled in.

You can use this facility as a font subsetting mechanism and **_"replace" fonts with themselves_**.

![screen](multi-language.jpg)

The above multi language page had been created using the large font "Droid Sans Fallback Regular", which resulted in a file size of **1.62 MB**.

The produced JSON file is this:
```json
[
  {
    "oldfont": "Droid Sans Fallback Regular",
    "newfont": "keep",
    "info": "50483 glyphs, size 3556308"
  }
]
```
We replace with "korea" (could have been any of "japan", "china-s" or "china-t"):

```json
[
  {
    "oldfont": "Droid Sans Fallback Regular",
    "newfont": "cjk",
    "info": "50483 glyphs, size 3556308"
  }
]
```

... yielded a new file size of only **16.1 KB** - less than 1% of the original!

A very significant file size reduction in this case!

The run protocol looked like this:

```
python repl-font.py tw-textbox3.pdf
Processing PDF 'tw-textbox3.pdf' with 1 page.

Phase 1: Create unicode subsets.
End of phase 1, 0.03 seconds.

Font replacement overview:
 Droid Sans Fallback Regular replaced by: Droid Sans Fallback Regular.

Building font subsets:
Used 179 glyphs of font 'Droid Sans Fallback Regular'. 3453 KB saved.
Font subsets built, 0.77 seconds.

Phase 2: rebuild document.
End of phase 2, 0.01 seconds
Total duration 0.81 seconds
```
> As you can see, although 6 different languages where used, it was only 180 glyphs out of over 50,000 in this font - about 0.36 percent. Subsetting saved us over 99% of the font's original size.

## Changes
* Version 2020-09-02:
    - Now also supporting text in so-called "Form XObjects", i.e. text not encoded in the page's `/Contents`.
    - The intermediate CSV file containing mappings between old and new font names is now handled as a binary file (read / write options "rb", resp. "wb") to support fontnames encoded as general UTF-8.

* Version 2020-09-10:
    - switched from CSV to JSON format for better support of non-ASCII UTF-8 fontnames.
