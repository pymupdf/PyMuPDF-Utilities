"""
Alias Removal
-------------

This utility replaces old PyMuPDF method and attribute names by the new ones.

Parameter is either a file name or a folder name.
If a folder name, all of the Python files contained therein or in any of its
sub-folders recursively are changed.

If backups are requested, then oldfile.py is renamed to 'oldfile.py.bak'.

@copyright: (c) 2021 Jorj McKie

Disclaimer
-----------
This script is intended to help migrating to the new naming standard of
PyMuPDF and provided in the hope to be useful.
Use it at your own risk! There is absolutely no guarantee for correct functioning.
You are urged to use the '--backup' option and then confirm that the output
script contains intended changes only by comparing old and new file.

"""
import os
import sys
import argparse


def alias_changer(infile, backup):
    try:
        oldtext = open(infile, "rb").read()
    except:
        print("Unsupported characters in", infile)
        return
    text = oldtext.replace(b".chapterCount", b".chapter_count")
    text = text.replace(b".chapterPageCount", b".chapter_page_count")
    text = text.replace(b".convertToPDF", b".convert_to_pdf")
    text = text.replace(b".copyPage", b".copy_page")
    text = text.replace(b".deletePage", b".delete_page")
    text = text.replace(b".deletePageRange", b".delete_pages")
    text = text.replace(b".embeddedFileAdd", b".embfile_add")
    text = text.replace(b".embeddedFileCount", b".embfile_count")
    text = text.replace(b".embeddedFileDel", b".embfile_del")
    text = text.replace(b".embeddedFileGet", b".embfile_get")
    text = text.replace(b".embeddedFileInfo", b".embfile_info")
    text = text.replace(b".embeddedFileNames", b".embfile_names")
    text = text.replace(b".embeddedFileUpd", b".embfile_upd")
    text = text.replace(b".extractFont", b".extract_font")
    text = text.replace(b".extractImage", b".extract_image")
    text = text.replace(b".findBookmark", b".find_bookmark")
    text = text.replace(b".fullcopyPage", b".fullcopy_page")
    text = text.replace(b".getCharWidths", b".get_char_widths")
    text = text.replace(b".getOCGs", b".get_ocgs")
    text = text.replace(b".getPageFontList", b".get_page_fonts")
    text = text.replace(b".getPageImageList", b".get_page_images")
    text = text.replace(b".getPagePixmap", b".get_page_pixmap")
    text = text.replace(b".getPageText", b".get_page_text")
    text = text.replace(b".getPageXObjectList", b".get_page_xobjects")
    text = text.replace(b".getSigFlags", b".get_sigflags")
    text = text.replace(b".getToC", b".get_toc")
    text = text.replace(b".getXmlMetadata", b".get_xml_metadata")
    text = text.replace(b".insertPage", b".insert_page")
    text = text.replace(b".insertPDF", b".insert_pdf")
    text = text.replace(b".isDirty", b".is_dirty")
    text = text.replace(b".isFormPDF", b".is_form_pdf")
    text = text.replace(b".isPDF", b".is_pdf")
    text = text.replace(b".isEncrypted", b".is_encrypted")
    text = text.replace(b".isReflowable", b".is_reflowable")
    text = text.replace(b".isRepaired", b".is_repaired")
    text = text.replace(b".isStream", b".is_stream")
    text = text.replace(b".lastLocation", b".last_location")
    text = text.replace(b".loadPage", b".load_page")
    text = text.replace(b".makeBookmark", b".make_bookmark")
    text = text.replace(b".metadataXML", b".xref_xml_metadata")
    text = text.replace(b".movePage", b".move_page")
    text = text.replace(b".needsPass", b".needs_pass")
    text = text.replace(b".newPage", b".new_page")
    text = text.replace(b".nextLocation", b".next_location")
    text = text.replace(b".pageCount", b".page_count")
    text = text.replace(b".pageCropBox", b".page_cropbox")
    text = text.replace(b".pageXref", b".page_xref")
    text = text.replace(b".PDFCatalog", b".pdf_catalog")
    text = text.replace(b".PDFTrailer", b".pdf_trailer")
    text = text.replace(b".previousLocation", b".prev_location")
    text = text.replace(b".resolveLink", b".resolve_link")
    text = text.replace(b".searchPageFor", b".search_page_for")
    text = text.replace(b".setLanguage", b".set_language")
    text = text.replace(b".setMetadata", b".set_metadata")
    text = text.replace(b".setToC", b".set_toc")
    text = text.replace(b".setXmlMetadata", b".set_xml_metadata")
    text = text.replace(b".updateObject", b".update_object")
    text = text.replace(b".updateStream", b".update_stream")
    text = text.replace(b".xrefLength", b".xref_length")
    text = text.replace(b".xrefObject", b".xref_object")
    text = text.replace(b".xrefStream", b".xref_stream")
    text = text.replace(b".xrefStreamRaw", b".xref_stream_raw")
    text = text.replace(b"._isWrapped", b".is_wrapped")
    text = text.replace(b".addCaretAnnot", b".add_caret_annot")
    text = text.replace(b".addCircleAnnot", b".add_circle_annot")
    text = text.replace(b".addFileAnnot", b".add_file_annot")
    text = text.replace(b".addFreetextAnnot", b".add_freetext_annot")
    text = text.replace(b".addHighlightAnnot", b".add_highlight_annot")
    text = text.replace(b".addInkAnnot", b".add_ink_annot")
    text = text.replace(b".addLineAnnot", b".add_line_annot")
    text = text.replace(b".addPolygonAnnot", b".add_polygon_annot")
    text = text.replace(b".addPolylineAnnot", b".add_polyline_annot")
    text = text.replace(b".addRectAnnot", b".add_rect_annot")
    text = text.replace(b".addRedactAnnot", b".add_redact_annot")
    text = text.replace(b".addSquigglyAnnot", b".add_squiggly_annot")
    text = text.replace(b".addStampAnnot", b".add_stamp_annot")
    text = text.replace(b".addStrikeoutAnnot", b".add_strikeout_annot")
    text = text.replace(b".addTextAnnot", b".add_text_annot")
    text = text.replace(b".addUnderlineAnnot", b".add_underline_annot")
    text = text.replace(b".addWidget", b".add_widget")
    text = text.replace(b".cleanContents", b".clean_contents")
    text = text.replace(b"._cleanContents", b".clean_contents")
    text = text.replace(b".CropBox", b".cropbox")
    text = text.replace(b".CropBoxPosition", b".cropbox_position")
    text = text.replace(b".deleteAnnot", b".delete_annot")
    text = text.replace(b".deleteLink", b".delete_link")
    text = text.replace(b".deleteWidget", b".delete_widget")
    text = text.replace(b".derotationMatrix", b".derotation_matrix")
    text = text.replace(b".drawBezier", b".draw_bezier")
    text = text.replace(b".drawCircle", b".draw_circle")
    text = text.replace(b".drawCurve", b".draw_curve")
    text = text.replace(b".drawLine", b".draw_line")
    text = text.replace(b".drawOval", b".draw_oval")
    text = text.replace(b".drawPolyline", b".draw_polyline")
    text = text.replace(b".drawQuad", b".draw_quad")
    text = text.replace(b".drawRect", b".draw_rect")
    text = text.replace(b".drawSector", b".draw_sector")
    text = text.replace(b".drawSquiggle", b".draw_squiggle")
    text = text.replace(b".drawZigzag", b".draw_zigzag")
    text = text.replace(b".firstAnnot", b".first_annot")
    text = text.replace(b".firstLink", b".first_link")
    text = text.replace(b".firstWidget", b".first_widget")
    text = text.replace(b".getContents", b".get_contents")
    text = text.replace(b".getDisplayList", b".get_displaylist")
    text = text.replace(b".getDrawings", b".get_drawings")
    text = text.replace(b".getFontList", b".get_fonts")
    text = text.replace(b".getImageBbox", b".get_image_bbox")
    text = text.replace(b".getImageList", b".get_images")
    text = text.replace(b".getLinks", b".get_links")
    text = text.replace(b".getPixmap", b".get_pixmap")
    text = text.replace(b".getSVGimage", b".get_svg_image")
    text = text.replace(b".getText", b".get_text")
    text = text.replace(b".getTextBlocks", b".get_text_blocks")
    text = text.replace(b".getTextbox", b".get_textbox")
    text = text.replace(b".getTextPage", b".get_textpage")
    text = text.replace(b".getTextWords", b".get_text_words")
    text = text.replace(b".insertFont", b".insert_font")
    text = text.replace(b".insertImage", b".insert_image")
    text = text.replace(b".insertLink", b".insert_link")
    text = text.replace(b".insertText", b".insert_text")
    text = text.replace(b".insertTextbox", b".insert_textbox")
    text = text.replace(b".loadAnnot", b".load_annot")
    text = text.replace(b".loadLinks", b".load_links")
    text = text.replace(b".MediaBox", b".mediabox")
    text = text.replace(b".MediaBoxSize", b".mediabox_size")
    text = text.replace(b".newShape", b".new_shape")
    text = text.replace(b".readContents", b".read_contents")
    text = text.replace(b".rotationMatrix", b".rotation_matrix")
    text = text.replace(b".searchFor", b".search_for")
    text = text.replace(b".setCropBox", b".set_cropbox")
    text = text.replace(b".setMediaBox", b".set_mediabox")
    text = text.replace(b".setRotation", b".set_rotation")
    text = text.replace(b".showPDFpage", b".show_pdf_page")
    text = text.replace(b".transformationMatrix", b".transformation_matrix")
    text = text.replace(b".updateLink", b".update_link")
    text = text.replace(b".wrapContents", b".wrap_contents")
    text = text.replace(b".writeText", b".write_text")
    text = text.replace(b".drawBezier", b".draw_bezier")
    text = text.replace(b".drawCircle", b".draw_circle")
    text = text.replace(b".drawCurve", b".draw_curve")
    text = text.replace(b".drawLine", b".draw_line")
    text = text.replace(b".drawOval", b".draw_oval")
    text = text.replace(b".drawPolyline", b".draw_polyline")
    text = text.replace(b".drawQuad", b".draw_quad")
    text = text.replace(b".drawRect", b".draw_rect")
    text = text.replace(b".drawSector", b".draw_sector")
    text = text.replace(b".drawSquiggle", b".draw_squiggle")
    text = text.replace(b".drawZigzag", b".draw_zigzag")
    text = text.replace(b".insertText", b".insert_text")
    text = text.replace(b".insertTextbox", b".insert_textbox")
    text = text.replace(b".getText", b".get_text")
    text = text.replace(b".getTextbox", b".get_textbox")
    text = text.replace(b".fileGet", b".get_file")
    text = text.replace(b".fileUpd", b".update_file")
    text = text.replace(b".getPixmap", b".get_pixmap")
    text = text.replace(b".getTextPage", b".get_textpage")
    text = text.replace(b".lineEnds", b".line_ends")
    text = text.replace(b".setBlendMode", b".set_blendmode")
    text = text.replace(b".setBorder", b".set_border")
    text = text.replace(b".setColors", b".set_colors")
    text = text.replace(b".setFlags", b".set_flags")
    text = text.replace(b".setInfo", b".set_info")
    text = text.replace(b".setLineEnds", b".set_line_ends")
    text = text.replace(b".setName", b".set_name")
    text = text.replace(b".setOpacity", b".set_opacity")
    text = text.replace(b".setRect", b".set_rect")
    text = text.replace(b".setOC", b".set_oc")
    text = text.replace(b".soundGet", b".get_sound")
    text = text.replace(b".writeText", b".write_text")
    text = text.replace(b".fillTextbox", b".fill_textbox")
    text = text.replace(b".getPixmap", b".get_pixmap")
    text = text.replace(b".getTextPage", b".get_textpage")
    text = text.replace(b".setAlpha", b".set_alpha")
    text = text.replace(b".gammaWith", b".gamma_with")
    text = text.replace(b".tintWith", b".tint_with")
    text = text.replace(b".clearWith", b".clear_with")
    text = text.replace(b".copyPixmap", b".copy")
    text = text.replace(b".getImageData", b".tobytes")
    text = text.replace(b".getPNGData", b".tobytes")
    text = text.replace(b".getPNGdata", b".tobytes")
    text = text.replace(b".writeImage", b".save")
    text = text.replace(b".writePNG", b".save")
    text = text.replace(b".pillowWrite", b".pil_save")
    text = text.replace(b".pillowData", b".pil_tobytes")
    text = text.replace(b".invertIRect", b".invert_irect")
    text = text.replace(b".setPixel", b".set_pixel")
    text = text.replace(b".setOrigin", b".set_origin")
    text = text.replace(b".setRect", b".set_rect")
    text = text.replace(b".setResolution", b".set_dpi")
    text = text.replace(b".getPDFstr", b".get_pdf_str")
    text = text.replace(b".getPDFnow", b".get_pdf_now")
    text = text.replace(b".PaperSize", b".paper_size")
    text = text.replace(b".PaperRect", b".paper_rect")
    text = text.replace(b".paperSizes", b".paper_sizes")
    text = text.replace(b".ImageProperties", b".image_properties")
    text = text.replace(b".planishLine", b".planish_line")
    text = text.replace(b".getTextLength", b".get_text_length")
    text = text.replace(b".getArea", b".get_area")
    text = text.replace(b".getRectArea", b".get_area")
    text = text.replace(b".includePoint", b".include_point")
    text = text.replace(b".includeRect", b".include_rect")
    text = text.replace(b".isInfinite", b".is_infinite")
    text = text.replace(b".isEmpty", b".is_empty")
    text = text.replace(b".isRectangular", b".is_rectangular")
    text = text.replace(b".isRectilinear", b".is_rectilinear")
    text = text.replace(b".isConvex", b".is_convex")
    text = text.replace(b".preRotate", b".prerotate")
    text = text.replace(b".preScale", b".prescale")
    text = text.replace(b".preShear", b".preshear")
    text = text.replace(b".preTranslate", b".pretranslate")
    if oldtext == text:
        print("Nothing to change: '%s'." % infile)
        return
    else:
        print("Updating: '%s'." % infile)
    if backup:
        bak_name = infile + ".bak"
        if os.path.exists(bak_name):
            os.remove(bak_name)
        os.rename(infile, bak_name)
    outfile = open(infile, "wb")
    outfile.write(text)
    outfile.close()


def main():
    parser = argparse.ArgumentParser(
        description="Renew old PyMuPDF method and attribute names."
    )
    parser.add_argument("folder", type=str, help="folder or file")
    parser.add_argument(
        "-B",
        "--backup",
        action="store_true",
        help="take backups: keep 'file.py' as 'file.py.bak'",
    )
    args = parser.parse_args()
    folder = args.folder
    backup = args.backup
    print("Taking backups: %s" % backup)
    if not folder:
        sys.exit("Need file or folder.")
    me = os.path.basename(__file__)
    files = []
    if os.path.isfile(folder):
        print("Processing file '%s'" % folder)
        files.append(folder)
    elif os.path.isdir(folder):
        print("Processing folder '%s' and its sub-folders." % folder)
        for root, _, fles in os.walk(folder):
            for f in fles:
                if not f.endswith(".py"):
                    continue
                fullname = os.path.join(root, f).replace("\\", "/")
                if fullname.endswith(me):
                    print("Skipping", fullname)
                    continue
                files.append(fullname)
    else:
        sys.exit("no such file or folder: " + folder)

    for f in files:
        alias_changer(f, backup)


if __name__ == "__main__":
    main()