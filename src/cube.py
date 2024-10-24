from adafruit_led_animation.color import RED, ORANGE, AMBER, YELLOW, GOLD, GREEN, JADE, TEAL, AQUA, CYAN, BLUE, PURPLE, MAGENTA, PINK, WHITE
import neopixel
import random

"""
represents an edge unit when going off a 2d face and determines where on the next face to go
direction change is the change in x or y vectors when traversing the flat_cube_arr flatly
"""
class EdgeMapsTo:
    def __init__(self, x, y, direction_change):
        self.x = x
        self.y = y
        self.direction_change = direction_change

"""
Cube object that represents a 3D cube with 6 faces populated by LEDs
Assumes that 3 pins are used and the second pin is the 4 side led panels chained together
"""
class LEDCube:
    def __init__(self, face_width, top_pin, side_pin, bottom_pin, brightness=0.1):
        self.TOP = 0
        self.SIDE_A = 1
        self.SIDE_B = 2
        self.SIDE_C = 3
        self.SIDE_D = 4
        self.BOTTOM = 5

        self.face_width    = face_width
        self.flat_cube_arr = self.instantiate_arr(face_width)
        self.pixels_top    = neopixel.NeoPixel(top_pin,    face_width**2,   brightness=brightness, auto_write=False)
        self.pixels_sides  = neopixel.NeoPixel(side_pin,   face_width**2*4, brightness=brightness, auto_write=False)
        self.pixels_bottom = neopixel.NeoPixel(bottom_pin, face_width**2,   brightness=brightness, auto_write=False)


    """
    the virtual arr stores 3 kinds of values
    - a pixel represented as an RGB tuple like (0,0,0) for each pixel
    - the location of an adjacent pixel over the edge represented as an Edge object
    - an inaccessable pixel represented as -1 which serves no purpose
    """
    def instantiate_arr(self, face_width):
        flat_cube_arr = []
        topFaceLeftEdgeX = 1
        topFaceRightEdgeX = face_width
        sideFaceLeftEdgeX = topFaceRightEdgeX + 3
        sideFaceRightEdgeX = sideFaceLeftEdgeX + face_width - 1
        bottomFaceLeftEdgeX = sideFaceRightEdgeX + 3
        bottomFaceRightEdgeX = bottomFaceLeftEdgeX + face_width - 1

        # top face 
        flat_cube_arr.append([-1] +
                           [EdgeMapsTo(sideFaceLeftEdgeX, 3*face_width - y, (1, 0)) for y in range(face_width)] +
                           [-1])
        flat_cube_arr.extend([EdgeMapsTo(sideFaceLeftEdgeX, 3*face_width + x + 1, (1, 0))] +
                            [0 for y in range(face_width)] +
                            [EdgeMapsTo(sideFaceLeftEdgeX, 2*face_width - x, (1, 0))]
                            for x in range(face_width)) 
        flat_cube_arr.append([-1] +
                           [EdgeMapsTo(sideFaceLeftEdgeX, y + 1, (1,0)) for y in range(face_width)] +
                           [-1])

        # side faces
        flat_cube_arr.append([-1] +
                           [EdgeMapsTo(topFaceRightEdgeX, y + 1, (-1, 0)) for y in range(face_width)] +
                           [EdgeMapsTo(topFaceRightEdgeX - y, face_width, (0, -1)) for y in range(face_width)] +
                           [EdgeMapsTo(topFaceLeftEdgeX, face_width - y, (1, 0)) for y in range(face_width)] +
                           [EdgeMapsTo(topFaceLeftEdgeX + y, 1, (0, 1)) for y in range(face_width)] +
                           [-1])
        flat_cube_arr.extend([EdgeMapsTo(sideFaceLeftEdgeX + x, face_width*4, (0, -1))] +
                            [0 for y in range(face_width*4)] +
                            [EdgeMapsTo(sideFaceLeftEdgeX + x, 1, (0, 1))]
                            for x in range(face_width))
        flat_cube_arr.append([-1] +
                           [EdgeMapsTo(bottomFaceLeftEdgeX, y + 1, (1, 0)) for y in range(face_width)] +
                           [EdgeMapsTo(bottomFaceLeftEdgeX + y, face_width, (0, -1)) for y in range(face_width)] +
                           [EdgeMapsTo(bottomFaceRightEdgeX, face_width - y, (-1, 0)) for y in range(face_width)] +
                           [EdgeMapsTo(bottomFaceRightEdgeX - y, 1, (0, 1)) for y in range(face_width)] +
                           [-1])

        # bottom face
        flat_cube_arr.append([-1] +
                           [EdgeMapsTo(sideFaceRightEdgeX, y + 1, (-1, 0)) for y in range(face_width)] +
                           [-1])
        flat_cube_arr.extend([EdgeMapsTo(sideFaceRightEdgeX, 4 * face_width - x, (-1, 0))] +
                            [0 for _ in range(face_width)] +
                            [EdgeMapsTo(sideFaceRightEdgeX, face_width + x + 1, (-1, 0))]
                            for x in range(face_width))
        flat_cube_arr.append([-1] +
                           [EdgeMapsTo(sideFaceRightEdgeX, 3*face_width - y, (-1, 0)) for y in range(face_width)] +
                           [-1])
        return flat_cube_arr


    def get_flat_cube_xy(self, face, x, y):
        if face == self.TOP:
            return x + 1, y + 1
        elif face == self.BOTTOM:
            return 2*self.face_width + x + 5, y + 1
        else:
            if face == self.SIDE_A:
                return self.face_width + x + 3, y + 1
            elif face == self.SIDE_B:
                return self.face_width + x + 3, self.face_width + y + 1
            elif face == self.SIDE_C:
                return self.face_width + x + 3, 2*self.face_width + y + 1
            elif face == self.SIDE_D:
                return self.face_width + x + 3, 3*self.face_width + y + 1
            else:
                raise ValueError("Invalid face")


    """
    if the coord is a color value, return input values
    if the coord is an EdgeMapsTo object, return the edge's coords and dir
    """
    def confirm_flat_xy(self, x, y, dir):
        type = self.flat_cube_arr[x][y]
        if isinstance(type, EdgeMapsTo):
            edge = type
            return edge.x, edge.y, edge.direction_change
        elif type == -1:
            return None, None, None
        else:
            return x, y, dir

    """
    a given function is applied to every modifiable pixel on the flat_cube_arr
    """
    def function_every_pixel(self, func, flat_cube_arr, *args):
        for x in range(self.face_width):
            for y in range(self.face_width):
                flatx, flaty = self.get_flat_cube_xy(self.TOP, x, y)
                func(flat_cube_arr, flatx, flaty, *args)

                flatx, flaty = self.get_flat_cube_xy(self.BOTTOM, x, y)
                func(flat_cube_arr, flatx, flaty, *args)

            for y in range(self.face_width * 4):
                flatx, flaty = self.get_flat_cube_xy(self.SIDE_A, x, y)
                func(flat_cube_arr, flatx, flaty, *args)


    # set the color of a pixel on the flat_cube_arr based only on the flatarr coords
    def set_flat_cube_pixel(self, flatCubeX, flatCubeY, color):
        self.flat_cube_arr[flatCubeX][flatCubeY] = color


    # turns the xy coordinates of a square face into a linear strip index
    def face_xy_to_strip_index(self, x, y):
        width = self.face_width
        if y % 2 == 0:
            strip_index = (y * width) + x
        else:
            strip_index = (y * width) + width - x - 1
        return strip_index


    # update every pixel color on the top, sides, and bottom strips based on flat_cube_arr then show
    def show_pixels(self):
        for x in range(self.face_width):
            for y in range(self.face_width):
                flatCubeX, flatCubeY = self.get_flat_cube_xy(self.TOP, x, y)
                self.pixels_top[self.face_xy_to_strip_index(x, y)] = self.flat_cube_arr[flatCubeX][flatCubeY]

                flatCubeX, flatCubeY = self.get_flat_cube_xy(self.BOTTOM, x, y)
                self.pixels_bottom[self.face_xy_to_strip_index(x, y)] = self.flat_cube_arr[flatCubeX][flatCubeY]

            for y in range(self.face_width*4):
                flatCubeX, flatCubeY = self.get_flat_cube_xy(self.SIDE_A, x, y)
                self.pixels_sides[self.face_xy_to_strip_index(x, y)] = self.flat_cube_arr[flatCubeX][flatCubeY]

        self.pixels_top.show()
        self.pixels_sides.show()
        self.pixels_bottom.show()


    def deactivate_panels(self):
        self.pixels_top.deinit()
        self.pixels_sides.deinit()
        self.pixels_bottom.deinit()


    def random_color(self):
        colors = [RED, ORANGE, AMBER, YELLOW, GOLD, GREEN, JADE, TEAL, AQUA, CYAN, BLUE, PURPLE, MAGENTA, PINK, WHITE]
        return random.choice(colors)