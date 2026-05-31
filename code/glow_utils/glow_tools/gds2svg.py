########################################################################
#
# Copyright 2026 Dr. Dušan Grujić (dusan.grujic@etf.bg.ac.rs)
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#    https://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
########################################################################

import argparse
import gdstk

settings = {
    "scale" : 1000,
    "background" : "000000",
    "zorder-nostipple" : ["nwell", "activ", "psd", "poly", "m1", "contact", "text", "prBoundary"],
    "zorder-stipple" : ["nwell-stipple", "activ", "psd", "poly", "m1-stipple", "contact", "text", "prBoundary"],
    "nwell" : { "layer" : 31, "datatype" : 0, "fill" : "#268c6b", "stroke" : "#268c6b", "stroke_width" : 1.0, "opacity" : 0.5},
    "nwell-stipple" : { "layer" : 31, "datatype" : 0, "fill" : "url(#nwell-stipple)", "stroke" : "#268c6b", "stroke_width" : 1.0, "opacity" : 1.0},
    "activ" : { "layer" : 1, "datatype" : 0, "fill" : "#00ff00", "stroke" : "#00ff00", "stroke_width" : 1.0, "opacity" : 0.5},
    "activ-stipple" : { "layer" : 1, "datatype" : 0, "fill" : "url(#act-stipple)", "stroke" : "#00ff00", "stroke_width" : 1.0, "opacity" : 1.0},
    "psd" : { "layer" : 14, "datatype" : 0, "fill" : "#ccb899", "stroke" : "#ccb899", "stroke_width" : 1.0, "opacity" : 0.3},
    "psd-stipple" : { "layer" : 14, "datatype" : 0, "fill" : "url(#psd-stipple)", "stroke" : "#ccb899", "stroke_width" : 1.0, "opacity" : 1.0},
    "poly" : { "layer" : 5, "datatype" : 0, "fill" : "#bf4026", "stroke" : "#bf4026", "stroke_width" : 1.0, "opacity" : 1.0},
    "m1" : { "layer" : 8, "datatype" : 0, "fill" : "#39bfff", "stroke" : "39bfff", "stroke_width" : 1.0, "opacity" : 0.8},
    "m1-stipple" : { "layer" : 8, "datatype" : 0, "fill" : "url(#m1-stipple)", "stroke" : "#39bfff", "stroke_width" : 1.0, "opacity" : 1.0},
    "contact" : { "layer" : 6, "datatype" : 0, "fill" : "#ffffff", "stroke" : "#000000", "stroke_width" : 1.0, "opacity" : 1.0},
    "prBoundary" : { "layer" : 189, "datatype" : 0, "fill" : None, "stroke" : "#9900e6", "stroke_width" : 1.0, "opacity" : 0.5},
    "text" : { "layer" : 63, "datatype" : 0, "fill" : None, "stroke" : "#ffffff", "stroke_width" : 1.0, "opacity" : 0.8},
    "labelColor" : "#000000",
    "labelColor-stipple" :"#FFEE00",
    "labelSize"  : 160.0,
    "labelStroke" : "#113444",
    "labelStroke-stipple" : "#060F13",
    "labelStrokeWidth" :1.5,
    "labelStrokeWidth-stipple" : 3,
    "labelFont" : "Arial"
}

    
def printlogo():
    print("\t",r"           _     ____                 ")
    print("\t",r"  __ _  __| |___|___ \ _____   ____ _ ")
    print("\t",r" / _` |/ _` / __| __) / __\ \ / / _` |")
    print("\t",r"| (_| | (_| \__ \/ __/\__ \\ V / (_| |")
    print("\t",r" \__, |\__,_|___/_____|___/ \_/ \__, |")
    print("\t",r" |___/                          |___/ ")

def printusage():
    print("*"*80)
    printlogo()
    print("")
    print("gds2svg is an utility to generate SVG from GDSII")
    print("Usage:")
    print("gds2svg input_file [options]")
    print("Options:")
    print("\t", "-c, --cells", "\t", "Cells to work on. Single cells or a list of cell can be given")
    print("\t", "-n, --no_stipple", "\t", "Don't use stipple, draw all layers as solid filled.")
    print("\t", "-x, --no_cross", "\t", "Don't draw x over contacts.")
    print("*"*80)

def parse_string_names(str_arr):
    cells = []
    for x in str_arr:
        if " " in x:
            tmp = x.split(" ")
            for name in tmp:
                cells.append(name)
        else:
            cells.append(x)
    return cells

def find_cell(name, lib):
    """
    Find a cell with given name in a list of given libraries.
    First occurence of a cell is returned, or None if not found.
    """
    for cell in lib.cells:
        if cell.name == name:
            return cell
    return None

def svg_header(bounding_box, color, stipple=True):
    bl, tr = bounding_box
    x0, y0 = bl
    x1, y1 = tr
    x0 *= settings["scale"]
    x1 *= settings["scale"]
    y0 *= settings["scale"]
    y1 *= settings["scale"]
    height = y1-y0
    width = x1-x0
    yt = -height-2*y0
    header = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg 
  version="1.1"
  xmlns="http://www.w3.org/2000/svg"
  height="100%" width="100%"
  viewBox="{x0} {y0} {width} {height}">

"""
    if stipple:
        header += """
  <defs>
    <!-- Define the repeating diagonal pattern -->
    <pattern id="nwell-stipple" width="20" height="20" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
      <line x1="00" y1="0" x2="0" y2="20" stroke="#268c6b" stroke-width="10" />
    </pattern>

    <pattern id="m1-stipple" width="40" height="40" patternUnits="userSpaceOnUse" patternTransform="rotate(135)">
      <line x1="00" y1="0" x2="0" y2="40" stroke="#39bfff" stroke-width="20" />
    </pattern>
  </defs>    
"""
    header += f"""
  <rect x="{x0}" y="{y0}" width="{width}" height="{height}" fill="#{color}" />
   <g transform="scale(1, -1) translate(0, {yt})">
"""
    return (header, yt)


def svg_polygon(points, fill_color, stroke_color, stroke_width, opacity, cross=False):
    poly_str = """<polygon 
    points=" """
    xmin = 1e9
    ymin = 1e9
    xmax = -1e9
    ymax = -1e9
    for point in points:
        x, y = point
        x *= settings["scale"]
        y *= settings["scale"]
        xmin = min(x, xmin)
        xmax = max(x, xmax)
        ymin = min(y, ymin)
        ymax = max(y, ymax)
        poly_str += ",".join( (str(x), str(y)) ) + " "
    poly_str += ' "\n'
    if fill_color is not None:
        poly_str += f'fill="{fill_color}"\n'
    else:
        poly_str += 'fill="none"\n'
    if stroke_color is not None:
        poly_str += f'stroke="{stroke_color}"\n'
        poly_str += f'stroke-width="{stroke_width}"\n'
    else:
        poly_str += 'stroke="none"\n'
    poly_str += f'opacity="{opacity}" />\n'
    if cross:
        poly_str += f'<line x1="{xmin}" y1="{ymin}" x2="{xmax}" y2="{ymax}" stroke="{stroke_color}" stroke-width="{stroke_width}" />\n'
        poly_str += f'<line x1="{xmin}" y1="{ymax}" x2="{xmax}" y2="{ymin}" stroke="{stroke_color}" stroke-width="{stroke_width}" />\n'
    return poly_str

def addLabel(position, text, text_size, color, stroke, stroke_width, font):
    x, y = position
    res = f'  <text x="{x}" y="{y}" font-size="{text_size}px" fill="{color}" text-anchor="middle" dominant-baseline="middle" stroke="{stroke}" stroke-width="{stroke_width}" font-family="{font}">\n'
    res += text + '\n'
    res += '</text>\n'
    return res

def process_cell(cell : gdstk.Cell, stipple = True, cont_cross = True):
    # Generate SVG from cell
    print("Generating SVG for cell", cell.name)

    bounding_box = cell.bounding_box()
    svg, yt = svg_header(bounding_box, settings['background'])

    if stipple:
        zorder = settings['zorder-stipple']
    else:
        zorder = settings['zorder-nostipple']

    for layer in zorder:
        lay = settings[layer]['layer']
        dt = settings[layer]['datatype']
        fill = settings[layer]['fill']
        stroke = settings[layer]['stroke']
        stroke_width = settings[layer]['stroke_width'] * settings['scale'] / 100.0
        opacity = settings[layer]['opacity']
        for polygon in cell.polygons:
            if polygon.layer == lay and polygon.datatype == dt:
                if layer == "contact":
                    cross = cont_cross
                else:
                    cross = False
                svg += svg_polygon(polygon.points, fill, stroke, stroke_width, opacity, cross)
    svg += "</g>\n"

    # Add labels
    for label in cell.labels:
        x, y = label.origin
        x *= settings['scale']
        y *= settings['scale']
        y = -y - yt
        if stipple:
            lc = settings["labelColor-stipple"]
            ls = settings["labelStroke-stipple"]
            lw = settings["labelStrokeWidth-stipple"]
        else:
            lc = settings["labelColor"]
            ls = settings["labelStroke"]
            lw = settings["labelStrokeWidth"]
        svg += addLabel((x,y), label.text, settings["labelSize"], lc, ls, lw, settings["labelFont"])
    
    svg += "</svg>\n"
    file_name = cell.name + ".svg"
    with open(file_name, "w") as f:
        f.write(svg)


#
# Main code
#
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file')
    # Cells to work on
    parser.add_argument('-c', '--cells', action='append', default=[])
    parser.add_argument('-s', '--no_stipple', action='store_true')
    parser.add_argument('-x', '--no_cross', action='store_true')

    try:
        args = parser.parse_args()
    except:
        printusage()
        exit(1)

    cells = parse_string_names(args.cells)
    print("Cells to work on [" + str(len(cells)) + "]")
    print("\t", " ".join(cells))

    stipple = True if not args.no_stipple else False
    cross = True if not args.no_cross else False

    try:
        gds = gdstk.read_gds(args.input_file)
    except:
        print("ERROR : Could not read GDSII file", args.input_file)
        exit(1)

    for cell_name in cells:
        cell = find_cell(cell_name, gds)
        if cell is not None:
            process_cell(cell, stipple, cross)
        else:
            print("WARNING : Cell", cell_name, "not found in GDSII file", args.input_file)

if __name__ == "__main__":
    main()
