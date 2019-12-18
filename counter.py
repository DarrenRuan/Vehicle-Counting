def get_counting_line(line_position, frame_width, frame_height):
    line_positions = ['top', 'bottom', 'left', 'right']
    if line_position == None:
        line_position = 'bottom'
    if line_position not in line_positions:
        raise Exception('Invalid line position specified (options: top, bottom, left, right)')

    if line_position == 'top':
        # counting_line_y = round(1 / 5 * frame_height)

        # Hamburg_Hall_080007032018_000,top
        # counting_line_y = round(3 / 5 * frame_height)

        # Parking1_083915032018_000, top
        # counting_line_y = round(13 / 20 * frame_height)

        # Hamburg_Hall1_073301102019_000, top
        counting_line_y = round(3 / 4 * frame_height)

        return [(0, counting_line_y), (frame_width, counting_line_y)]
    elif line_position == 'bottom':
        # Hamburg_Hall_080007032018_000, bottom
        # counting_line_y = round(13 / 20 * frame_height)

        # Parking1_083915032018_000, bottom
        # counting_line_y = round(2 / 3 * frame_height)

        # Hamburg_Hall1_064721092018_020, bottom
        # counting_line_y = round(3 / 4 * frame_height)

        # Hamburg_Hall1_073301102019_000, bottom
        # counting_line_y = round(7 / 8 * frame_height)

        # Parking2_050101102019_025, bottom
        counting_line_y = round(31 / 128 * frame_height)

        # counting_line_y = round(1 / 2 * frame_height)
        # counting_line_y = round(31 / 128 * frame_height)
        # counting_line_y = round(14 / 16 * frame_height)
        return [(0, counting_line_y), (frame_width, counting_line_y)]
    elif line_position == 'left':
        counting_line_x = round(1 / 5 * frame_width)
        return [(counting_line_x, 0), (counting_line_x, frame_height)]
    elif line_position == 'right':
        counting_line_x = round(4 / 5 * frame_width)
        return [(counting_line_x, 0), (counting_line_x, frame_height)]

def is_passed_counting_line(point, counting_line, line_position):
    if line_position == 'top':
        return point[1] < counting_line[0][1]
    elif line_position == 'bottom':
        return point[1] > counting_line[0][1]
    elif line_position == 'left':
        return point[0] < counting_line[0][0]
    elif line_position == 'right':
        return point[0] > counting_line[0][0]