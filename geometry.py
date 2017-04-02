class Intersection:
    NONE = 'None'
    VERTICAL = 'Vertical'
    HORIZONTAL = 'Horizontal'


class Rect:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    @property
    def max_x(self):
        return self.x + self.width

    @property
    def max_y(self):
        return self.y + self.height

    def intersect(self, line, offset_factor):
        '''
            Embarrassing - I can barely do grade 7 math.
            Can't handle perpendicular lines where one is vertical
        '''
        def line_intersection(l0, l1):
            a_x = float(l0[0][0])
            a_y = float(l0[0][1])
            b_x = float(l0[1][0])
            b_y = float(l0[1][1])
            c_x = float(l1[0][0])
            c_y = float(l1[0][1])
            d_x = float(l1[1][0])
            d_y = float(l1[1][1])

            if a_x == b_x or c_x == d_x:
                a_x, a_y = a_y, a_x
                b_x, b_y = b_y, b_x
                c_x, c_y = c_y, c_x
                d_x, d_y = d_y, d_x

            slope_0 = (b_y - a_y) / (b_x - a_x)
            intercept_0 = a_y - slope_0 * a_x

            slope_1 = (c_y - d_y) / (c_x - d_x)
            intercept_1 = c_y - slope_1 * c_x

            x_intersection = (intercept_1 - intercept_0) / (slope_0 - slope_1)

            return all([
                x_intersection >= min(a_x, b_x) - offset_factor,
                x_intersection <= max(b_x, a_x) + offset_factor,
                x_intersection >= min(c_x, d_x) - offset_factor,
                x_intersection <= max(c_x, d_x) + offset_factor,
            ])


        horizontal_lines = [
            ((self.x, self.y), (self.x + self.width, self.y)),
            ((self.x, self.y + self.height), (self.x + self.width, self.y + self.height)),
        ]

        vertical_lines = [
            ((self.x, self.y), (self.x, self.y + self.height)),
            ((self.x + self.width, self.y), (self.x + self.width, self.y + self.height)),
        ]

        if any(line_intersection(l, line) for l in horizontal_lines):
            return Intersection.HORIZONTAL

        if any(line_intersection(l, line) for l in vertical_lines):
            return Intersection.VERTICAL

        return Intersection.NONE
