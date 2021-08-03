import numpy as np
from numpy.linalg import norm

def point_line_distance(p1,p2,p3):
    p1 = np.array(p1)
    p2 = np.array(p2)
    p3 = np.array(p3)

    d = norm(np.cross(p2-p1, p1-p3))/norm(p2-p1)
    return d

def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y


# Find turning points   x_{i-1} < x_i > x_{i+1}
def turningpoints(x):
    top = []
    bot = []
    for i in range(1, len(x)-1):
        if ((x[i-1] < x[i] and x[i+1] < x[i])):
            top.append(i)
        elif (x[i-1] > x[i] and x[i+1] > x[i]):
            bot.append(i)
    return top, bot


def cal_angle(points):

    (x1,y1), (x2,y2), (x3,y3) = points

    matrix = np.array(([1,x1,y1],[1,x2,y2],[1,x3,y3]))
    area = 1/2*np.linalg.det(matrix)
    
    base = np.sqrt((x1-x3)**2 + (y1-y3)**2)
    height = 2*area/base

    # Radians
    angle = np.arctan(2*height/base)

    return angle

def find_triplets(points, x, y):
    size=len(x)
    angles = np.zeros((size, size, size))

    triplets = []

    # Fix the first element
    for i in range(len(points)-2):
        # Fix the second element
        for j in range(i+1,len(points)-1):
            # Now look for the third point
            for k in range(j + 1, len(points)):
                x1 = x[points[i]]
                x2 = x[points[j]]
                x3 = x[points[k]]
                y1 = y[points[i]]
                y2 = y[points[j]]
                y3 = y[points[k]]

                angle = cal_angle(((x1,y1), (x2,y2), (x3,y3)))
                angles[points[i],points[j],points[k]] = angle

                # exclude points that are too close to each other
                if (x2 - x1) < 0.03 or (x3-x2) < 0.03:
                    continue
                
                if np.abs(angle) < 0.05:
                    triplets.append((points[i],points[j],points[k]))

    return triplets, angles


def find_triangles(top, bot, x, y):
    top_triplets, top_angles = find_triplets(top, x, y)
    bot_triplets, bot_angles = find_triplets(bot, x, y)
    sym_tri = []

    for line1 in top_triplets:
        index_1 = line1[0]
        index_2 = line1[2]
        x1 = x[index_1]
        y1 = y[index_1]
        x2 = x[index_2]
        y2 = y[index_2]

        slope1 = (y2 - y1)/(x2-x1)

        # points in between can't be higher than the top line. 
        if (top_angles[index_1, :, index_2] < -0.2).sum() != 0:
            continue

        # 1. Slope for top lines must has positive slope and in a reasonable range.
        # 2. The range of the line must be bigger than 20 days (0.2 = 20/100)
        if not( -1 < slope1 < -0.29 and x2-x1 > 0.15):
            continue 
        else:
            for line2 in bot_triplets:

                index_3 = line2[0]
                index_4 = line2[2]
                x3 = x[index_3]
                y3 = y[index_3]
                x4 = x[index_4]
                y4 = y[index_4]

                slope2 = (y4 - y3)/(x4-x3)

                # points in between can't be lower than the bot line. 
                if (bot_angles[index_3, :, index_4] > 0.2).sum() != 0:
                    continue

                # 1. the sum of slope should be close to 0.
                # 3. two lines should not be too far away to each other.
                if 0.29 < slope2 < 1  and abs(slope1+slope2) <0.2 and abs(x3-x1) < 0.15 and abs(x4-x2) < 0.15\
                        and x2 > x3 and x4 > x1 and x4-x3 > 0.15:

                    # the intersection point should be in between two lines.
                    line1 = [(x1,y1),(x2,y2)]
                    line2 = [(x3,y3),(x4,y4)]

                    int_pt = line_intersection(line1,line2)

                    if y2 < int_pt[1] or int_pt[1] < y4:
                        continue

                    sym_tri.append(([index_1,index_2],[index_3,index_4]))
        # sym_tri = filter(sym_tri, x, y)                
    return sym_tri


def find_ascending_triangles(top, bot, x, y):
    top_triplets, top_angles = find_triplets(top, x, y)
    bot_triplets, bot_angles = find_triplets(bot, x, y)


    asc_tri = []
    for line1 in top_triplets:

        index_1 = line1[0]
        index_2 = line1[2]
        x1 = x[index_1]
        y1 = y[index_1]
        x2 = x[index_2]
        y2 = y[index_2]

        slope1 = (y2 - y1)/(x2-x1)

        # points in between can't be higher than the top line. 
        if (top_angles[index_1, :, index_2] < -0.2).sum() != 0:
            continue

        # 1. Slope for top horizontal line should be close to zero.
        # 2. The range of the line must be bigger than 20 days (0.2 = 20/100)
        if not( -0.05 < slope1 < 0.05 and x2-x1 > 0.15):
            continue 
        else:
            for line2 in bot_triplets:
                index_3 = line2[0]
                index_4 = line2[2]
                x3 = x[index_3]
                y3 = y[index_3]
                x4 = x[index_4]
                y4 = y[index_4]

                slope2 = (y4 - y3)/(x4-x3)

                # points in between can't be lower than the bot line. 
                if (bot_angles[index_3, :, index_4] > 0.2).sum() != 0:
                    continue

                # Ascending line has an angle between 30 degree ~ 60 degree
                if 0.29 < slope2 < 1:
                    if abs(x3-x1) < 0.15 and abs(x4-x2) < 0.15 and x2 > x3 and x4 > x1 and x4-x3 > 0.15:
                        # the intersection point should be in between two lines.
                        line1 = [(x1,y1),(x2,y2)]
                        line2 = [(x3,y3),(x4,y4)]

                        int_pt = line_intersection(line1,line2)

                        if y2 < int_pt[1] or int_pt[1] < y4:
                            continue

                        asc_tri.append(([index_1,index_2],[index_3,index_4]))
        # asc_tri = filter(asc_tri, x, y)
    return asc_tri


def find_descending_triangles(top, bot, x, y):
    top_triplets, top_angles = find_triplets(top, x, y)
    bot_triplets, bot_angles = find_triplets(bot, x, y)

    des_tri = []
    for line1 in bot_triplets:
        index_1 = line1[0]
        index_2 = line1[2]
        x1 = x[index_1]
        y1 = y[index_1]
        x2 = x[index_2]
        y2 = y[index_2]

        slope1 = (y2 - y1)/(x2-x1)

        # points in between can't be lower than the bot line. 
        if (bot_angles[index_1, :, index_2] > 0.2).sum() != 0:
            continue

        # 1. Slope for top horizontal line should be close to zero.
        # 2. The range of the line must be bigger than 20 days (0.2 = 20/100)

        if not( -0.05 < slope1 < 0.05 and x2-x1 > 0.15):
            continue 
        else:
            for line2 in top_triplets:
                index_3 = line2[0]
                index_4 = line2[2]
                x3 = x[index_3]
                y3 = y[index_3]
                x4 = x[index_4]
                y4 = y[index_4]

                slope2 = (y4 - y3)/(x4-x3)

                # points in between can't be higher than the top line. 
                if (top_angles[index_3, :, index_4] < -0.2).sum() != 0:
                    continue

                # Ascending line has an angle between 30 degree ~ 60 degree
                if  -1 < slope2 < -0.29:
                    if abs(x3-x1) < 0.15 and abs(x4-x2) < 0.15 and x2 > x3 and x4 > x1 and x4-x3 > 0.15:
                        # the intersection point should be in between two lines.
                        line1 = [(x1,y1),(x2,y2)]
                        line2 = [(x3,y3),(x4,y4)]

                        int_pt = line_intersection(line1,line2)

                        if y2 > int_pt[1] or int_pt[1] > y4:
                            continue

                        des_tri.append(([index_1,index_2],[index_3,index_4]))
        # des_tri = filter(des_tri, x, y)
    return des_tri


def find_flags(top, bot, x, y):
    top_triplets, top_angles = find_triplets(top, x, y)
    bot_triplets, bot_angles = find_triplets(bot, x, y)
    flags = []

    for line1 in top_triplets:
        index_1 = line1[0]
        index_2 = line1[2]
        x1 = x[index_1]
        y1 = y[index_1]
        x2 = x[index_2]
        y2 = y[index_2]

        slope1 = (y2 - y1)/(x2-x1)


        # points in between can't be higher than the top line. 
        if (top_angles[index_1, :, index_2] < -0.1).sum() != 0:
            continue

        # 1. Slope for top lines must has positive slope and in a reasonable range.
        # 2. The range of the line must be bigger than 20 days (0.2 = 20/100)
        if not( x2-x1 > 0.15):
            continue 
        else:
            for line2 in bot_triplets:
                index_3 = line2[0]
                index_4 = line2[2]
                x3 = x[index_3]
                y3 = y[index_3]
                x4 = x[index_4]
                y4 = y[index_4]

                slope2 = (y4 - y3)/(x4-x3)

                # points in between can't be lower than the bot line. 
                if (bot_angles[index_3, :, index_4] > 0.1).sum() != 0:
                    continue
                
                # 1. the sum of slope should be close to 0.
                # 3. two lines should not be too far away to each other.
                if abs(slope1-slope2) <0.1 and abs(x3-x1) < 0.15 and abs(x4-x2) < 0.15\
                        and x2 > x3 and x4 > x1 and x4-x3 > 0.15:

                    # the intersection point should be in between two lines.
                    # line1 = [(x1,y1),(x2,y2)]
                    # line2 = [(x3,y3),(x4,y4)]

                    # int_pt = line_intersection(line1,line2)

                    # if y2 < int_pt[1] or int_pt[1] < y4:
                    #     continue
                    dis1 = point_line_distance((x1,y1),(x2,y2),(x3,y3))
                    dis2 = point_line_distance((x1,y1),(x2,y2),(x4,y4))

                    if dis1 < 0.1 or dis2 < 0.1:
                        continue
                    flags.append(([index_1,index_2],[index_3,index_4]))
                    
        # flags = filter(flags, x, y)
    return flags


def filter(patterns, x, y):
    length = len(patterns)

    if length == 0:
        return patterns

    filtered_pattern = [patterns[0]]

    distance = -1 * np.ones((length, length))
    for i in range(length-1):
        for j in range(i+1, length):
            index_1, index_2 = patterns[i][0]
            index_3, index_4 = patterns[i][1]
            
            x1 = x[index_1]
            y1 = y[index_1]
            x2 = x[index_2]
            y2 = y[index_2]
            x3 = x[index_3]
            y3 = y[index_3]
            x4 = x[index_4]
            y4 = y[index_4]

            index_5, index_6 = patterns[j][0]
            index_7, index_8 = patterns[j][1]

            x5 = x[index_5]
            y5 = y[index_5]
            x6 = x[index_6]
            y6 = y[index_6]
            x7 = x[index_7]
            y7 = y[index_7]
            x8 = x[index_8]
            y8 = y[index_8]

            dist = (x1-x5)**2 + (y1-y5)**2 + (x2-x6)**2 + (y2-y6)**2 + (x3-x7)**2 + (y3-y7)**2 + (x4-x8)**2 + (y4-y8)**2

            distance[i, j] = dist

    remove_list = {}
    for i in range(length-1):
        if i in remove_list.keys():
            continue
        for j in range(i+1, length):
            if distance[i,j] > 0.005 and j not in remove_list.keys():
                filtered_pattern.append(patterns[j])
                remove_list[j] = 1
            else:
                remove_list[j] = 1

    return filtered_pattern


def find_pattern(history, name='sym'):
    data = history['close']

    # Covert to numpy array
    y = data.to_numpy()
    x = np.array(list(range(len(y))))

    date = data.index

    # Smoothing if needed
    # tck = splrep(x, y, s=0)
    # x = np.linspace(x.min(), x.max(), 50)     
    # y = splev(x, tck, der=0)

    # Find turning points
    top, bot = turningpoints(y)

    # Min Max Normalize
    # avoid RuntimeWarning: invalid value encountered in true_divide when price are same during the period, which can happen for few stocks
    if (y.max() != y.min()) and (x.max() != x.min()):
        norm_y = (y - y.min()) / (y.max() - y.min())
        norm_x = (x - x.min())  / (x.max()-x.min())
    else:
        norm_y = y
        norm_x = x

    if name == 'sym':
        patterns = find_triangles(top,bot,norm_x,norm_y)
    elif name == 'asc':
        patterns = find_ascending_triangles(top,bot,norm_x,norm_y)
    elif name == 'des':
        find_descending_triangles(top,bot,norm_x,norm_y)
    elif name == 'flag':
        patterns = find_flags(top,bot,norm_x,norm_y)

    if len(patterns) == 0:
        return (None, None)

    pattern = patterns[-1]

    x1 = date[pattern[0][0]]
    x2 = date[pattern[0][1]]

    x1 = date[pattern[0][0]]
    x2 = date[pattern[0][1]]

    y1 = y[pattern[0][0]]
    y2 = y[pattern[0][1]]

    x3 = date[pattern[1][0]]
    x4 = date[pattern[1][1]]

    y3 = y[pattern[1][0]]
    y4 = y[pattern[1][1]]

    points = {}
    points['line1'] = [(x1,y1),(x2,y2)]
    points['line2'] = [(x3,y3),(x4,y4)]

    return points, y
    