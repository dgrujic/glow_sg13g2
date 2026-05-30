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

LEF_LICENSE = \
"""
/*
Copyright 2026 Dr. Dušan Grujić (dusan.grujic@etf.bg.ac.rs)
 
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/
"""

from enum import auto, Enum
import numpy as np

class LEF_PINTYPE(Enum):
    # LEF pin type enum
    # Signals can be of direction IN, OUT and INOUT
    # Power pins can be POWER or GROUND and are always of direction INOUT
    IN = ("SIGNAL", "INPUT")
    OUT = ("SIGNAL", "OUTPUT")
    INOUT = ("SIGNAL", "INOUT")
    POWER = ("POWER", "INOUT")
    GROUND = ("GROUND", "INOUT")

class LEF_site():
    @staticmethod
    def gen_tabs(ntabs):
        return "\t" * ntabs  
        
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.site_class = "CORE"
        self.symmetry = "Y"

    def to_str(self, tab_level = 0):
        tabs = self.gen_tabs(tab_level)
        tabs1 = self.gen_tabs(tab_level + 1)
        res = tabs +"SITE\t" + self.name + "\n"
        res += tabs1 + "CLASS\t" + self.site_class + " ;\n"
        res += tabs1 + "SYMMETRY\t" + self.symmetry + " ;\n"
        res += tabs1 + "SIZE\t" + str(self.size[0]) + " BY " + str(self.size[1]) + " ;\n"
        res += tabs + "END " + self.name
        return res

class LEF_rect():
    @staticmethod
    def gen_tabs(ntabs):
        return "\t" * ntabs    
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
    def to_str(self, tab_level = 2):
        x1 = str(round(self.point1[0],4))
        y1 = str(round(self.point1[1],4))
        x2 = str(round(self.point2[0],4))
        y2 = str(round(self.point2[1],4))
        res = self.gen_tabs(tab_level) + "RECT " + x1 + " " + y1 + " " + x2 + " " + y2 + " ;\n"
        return res

class LEF_polygon():
    points_per_row = 4
    @staticmethod
    def gen_tabs(ntabs):
        return "\t" * ntabs    
    def __init__(self, points):
        self.points = points
    def to_str(self, tab_level = 2):
        tabs = self.gen_tabs(tab_level)
        tabs1 = self.gen_tabs(tab_level + 1)
        res = tabs + "POLYGON "
        cnt = 0
        for point in self.points:
            res += str(round(point[0],4)) + " " + str(round(point[1],4)) + " "
            cnt += 1
            if cnt == self.points_per_row:
                cnt = 0
                res += "\n" + tabs1
        res = res.rstrip() + " ;\n"
        return res
    @staticmethod
    def is_inside(points: np.ndarray, polygon: np.ndarray) -> np.ndarray:
        """
        Function to check if points are inside a polygon.
        """
        x, y = points[:, 0], points[:, 1]
        num_verts = len(polygon)
        inside = np.zeros(len(points), dtype=bool)

        p1x, p1y = polygon[0]
        for i in range(num_verts + 1):
            p2x, p2y = polygon[i % num_verts]
            # Condition 1: Point is vertically between the two edge vertices
            y_cond = (y > min(p1y, p2y)) & (y <= max(p1y, p2y))
            # Condition 2: Point is to the left of the edge ray intersection
            # Avoid division by zero by checking if p1y != p2y implicitly via y_cond
            with np.errstate(divide="ignore", invalid="ignore"):
                x_intersect = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
            x_cond = x < x_intersect
            # Toggle state if both conditions are met
            inside ^= y_cond & x_cond
            p1x, p1y = p2x, p2y
        return inside  

    def to_rectangles(self) -> list[LEF_rect]:
        """
        Decompose a polygon to a minimum number of rectangles.
        """
        vertices = np.array(self.points)
        xs = sorted(list(set(vertices[:, 0])))
        ys = sorted(list(set(vertices[:, 1])))

        grid_w = len(xs) - 1
        grid_h = len(ys) - 1
        grid = np.zeros((grid_h, grid_w), dtype=bool)

        # 1. Generate test points at cell centers
        mid_xs = [(xs[c] + xs[c + 1]) / 2.0 for c in range(grid_w)]
        mid_ys = [(ys[r] + ys[r + 1]) / 2.0 for r in range(grid_h)]

        test_points = []
        cell_mapping = []
        for r in range(grid_h):
            for c in range(grid_w):
                test_points.append((mid_xs[c], mid_ys[r]))
                cell_mapping.append((r, c))

        test_points = np.array(test_points)
        inside_flags = self.is_inside(test_points, vertices)

        for flag, (r, c) in zip(inside_flags, cell_mapping):
            if flag:
                grid[r, c] = True

        # 2. Strategy A: Sweep horizontally first, then expand vertically
        rects_horiz = []
        visited_h = np.zeros_like(grid, dtype=bool)
        for r in range(grid_h):
            c = 0
            while c < grid_w:
                if grid[r, c] and not visited_h[r, c]:
                    c_end = c
                    while (
                        c_end < grid_w
                        and grid[r, c_end]
                        and not visited_h[r, c_end]
                    ):
                        c_end += 1

                    r_end = r
                    possible = True
                    while r_end < grid_h and possible:
                        for i in range(c, c_end):
                            if not grid[r_end, i] or visited_h[r_end, i]:
                                possible = False
                                break
                        if possible:
                            r_end += 1

                    visited_h[r:r_end, c:c_end] = True
                    rects_horiz.append(((xs[c], ys[r]), (xs[c_end], ys[r_end])))
                    c = c_end
                else:
                    c += 1

        # 3. Strategy B: Sweep vertically first, then expand horizontally
        rects_vert = []
        visited_v = np.zeros_like(grid, dtype=bool)
        for c in range(grid_w):
            r = 0
            while r < grid_h:
                if grid[r, c] and not visited_v[r, c]:
                    r_end = r
                    while (
                        r_end < grid_h
                        and grid[r_end, c]
                        and not visited_v[r_end, c]
                    ):
                        r_end += 1

                    c_end = c
                    possible = True
                    while c_end < grid_w and possible:
                        for i in range(r, r_end):
                            if not grid[i, c_end] or visited_v[i, c_end]:
                                possible = False
                                break
                        if possible:
                            c_end += 1

                    visited_v[r:r_end, c:c_end] = True
                    rects_vert.append(((xs[c], ys[r]), (xs[c_end], ys[r_end])))
                    r = r_end
                else:
                    r += 1

        # 4. Choose the optimal partition strategy that outputs fewer shapes
        best_rect_coords = ( rects_horiz if len(rects_horiz) <= len(rects_vert) else rects_vert )

        return [LEF_rect(c1, c2) for c1, c2 in best_rect_coords]

class LEF_pin_geom():
    @staticmethod
    def gen_tabs(ntabs):
        return "\t" * ntabs
    def __init__(self):
        self.shapes = []
    def add_shape(self, shape):
        if isinstance(shape, list) or isinstance(shape, tuple):
            for x in shape:
                self.shapes.append(x)
        else:
            self.shapes.append(shape)
    def to_str(self, tab_level = 2):
        res = ""
        for shape in self.shapes:
            res += shape.to_str(tab_level)
        return res

class LEF_pin():
    default_pin_layer = "Metal1"
    default_power_net = "VDD VDD!"
    default_gnd_net = "VSS VSS!"
    @staticmethod
    def gen_tabs(ntabs):
        return "\t" * ntabs
    
    def __init__(self, pin_name : str, pin_type : LEF_PINTYPE, pin_geom : LEF_pin_geom):
        self.pin_name = pin_name
        self.pin_type = pin_type
        if (pin_type == LEF_PINTYPE.POWER) or (pin_type == LEF_PINTYPE.GROUND):
            self.shape = "ABUTMENT"
            if pin_type == LEF_PINTYPE.POWER:
                self.netexpr = self.default_power_net
            else:
                self.netexpr = self.default_gnd_net
        else:
            self.shape = None
            self.netexpr = None
        self.pin_layer = self.default_pin_layer
        self.pin_geom = pin_geom
        self.antenna_model = "OXIDE1"
        self.antenna_gatearea = 0.0
        self.antenna_diffarea = 0.0
        self.antenna_scale = 1e12
    def to_str(self, tab_level = 1):
        # Generate LEF pin string representation
        tabs = self.gen_tabs(tab_level)
        tabs1 = self.gen_tabs(tab_level + 1)
        tabs2 = self.gen_tabs(tab_level + 2)
        res =  tabs + "PIN " + self.pin_name + "\n"
        pin_sig, pin_dir = self.pin_type.value
        res += tabs1 + "DIRECTION " + pin_dir + " ;\n"
        res += tabs1 + "USE " + pin_sig + " ;\n"
        if self.shape is not None:
            res += tabs1 + "SHAPE " + self.shape + " ;\n"
        if self.netexpr is not None:
            res += tabs1 + "NETEXPR \"" + self.netexpr + "\" ;\n"
        if self.antenna_diffarea > 0:
            res += tabs1 + "ANTENNADIFFAREA "
            res += str(self.antenna_diffarea * self.antenna_scale)
            res += " LAYER " + self.pin_layer +" ;\n"
        if self.antenna_gatearea > 0:
            res += tabs1
            res += "ANTENNAMODEL " + self.antenna_model + " ;\n" 
            res += tabs1 + "ANTENNAGATEAREA "
            res += str(self.antenna_gatearea * self.antenna_scale)
            res += " LAYER " + self.pin_layer +" ;\n"
        # Pin geometry
        res += tabs1 + "PORT\n"
        res += tabs2 + "LAYER " + self.pin_layer +" ;\n"
        res += self.pin_geom.to_str(tab_level + 2)
        res += tabs1 + "END\n"
        res += tabs + "END " + self.pin_name + "\n"
        return res 

class LEF_obs():
    # LEF obstruction
    default_obs_layer = "Metal1"

    @staticmethod
    def gen_tabs(ntabs):
        return "\t" * ntabs
    
    def __init__(self, obs_geom : LEF_pin_geom):
        self.obs_layer = self.default_obs_layer
        self.obs_geom = obs_geom
    def to_str(self, tab_level = 1):
        # Generate LEF obstruction string representation
        tabs = self.gen_tabs(tab_level)
        tabs1 = self.gen_tabs(tab_level + 1)
        tabs2 = self.gen_tabs(tab_level + 2)
        # Obstruction geometry
        res = tabs1 + "OBS\n"
        res += tabs2 + "LAYER " + self.obs_layer +" ;\n"
        res += self.obs_geom.to_str(tab_level + 2)
        res += tabs1 + "END\n"
        return res 

class LEF_macro():
    @staticmethod
    def gen_tabs(ntabs):
        return "\t" * ntabs

    # LEF macro class
    def __init__(self, name : str, site : LEF_site, size : tuple, geom):
        # name is the macro name
        # site is a defined LEF site
        # size is a tuple (X_size, Y_size) of the macro
        # geom is a list of LEF pins and obstacles that define a macro geometry

        self.name = name
        self.macro_class = "CORE"
        self.site = site
        self.origin = (0, 0)
        self.foreign_name = name
        self.foreign_origin = (0, 0)
        # TODO : Check if size is compatible with site
        self.size = size
        self.symmetry = "X Y"
        self.geom = geom
    
    def to_str(self, tab_level = 0):
        tabs = self.gen_tabs(tab_level)
        tabs1 = self.gen_tabs(tab_level + 1)
        res = tabs + "MACRO " + self.name + "\n"
        res += tabs1 + "CLASS " + self.macro_class + " ;\n"
        res += tabs1 + "ORIGIN " + str(self.origin[0]) + " " + str(self.origin[1]) + " ;\n"
        res += tabs1 + "FOREIGN " + self.foreign_name + " " + str(self.foreign_origin[0]) + " " + str(self.foreign_origin[1]) + " ;\n"
        res += tabs1 + "SIZE " + str(self.size[0]) + " BY " + str(self.size[1]) + " ;\n"
        res += tabs1 + "SYMMETRY " + self.symmetry + " ;\n"
        res += tabs1 + "SITE " + self.site.name + " ;\n"
        for shape in self.geom:
            res += shape.to_str(tab_level + 1)
        res += tabs + "END " + self.name + "\n"
        return res

    def write_to_file(self, file_name):
        res = self.to_str()
        with open(file_name, "w") as f:
            f.write(res)

class LEF_macro_str():
    """
    LEF macro that contains only string representation.
    Can be used for LEF library assembly.
    """
    def __init__(self, macro_string : str):
        self.macro_string = macro_string
        
    def to_str(self, tab_level = 0):
        return self.macro_string
    
    def read_from_file(self, file_name):
        # Read macro definition from a text file
        with open(file_name, "r") as f:
            self.macro_string = f.read()
        
class LEF_lib():
    def __init__(self, properties, sites, macros):
        self.version = "5.7"
        self.busbitchars = "[]"
        self.dividechar = "/"
        self.license = LEF_LICENSE
        self.properties = properties
        self.sites = sites
        self.macros = macros

    def to_str(self):
        res = LEF_LICENSE
        res += "\n\n"
        res += "VERSION " + self.version + " ;\n"
        res += "BUSBITCHARS \"" + self.busbitchars + "\" ;"
        res += "DIVIDERCHAR \"" + self.dividechar + "\" ;"

        for property in self.properties:
            res += property.to_str()
            res += "\n"

        for site in self.sites:
            res += site.to_str()
            res += "\n"
        
        for macro in self.macros:
            res += macro.to_str()
            res += "\n"

        res += "END LIBRARY\n"
        return res
    
    def write_to_file(self, file_name):
        res = self.to_str()
        with open(file_name, "w") as f:
            f.write(res)
