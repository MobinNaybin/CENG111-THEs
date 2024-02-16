import math
import cv2
import numpy as np

# drawing functions and variables for visualization...

canvas = np.zeros((640, 640, 3))

CENTER_X = 200
CENTER_Y = 400

GAP_SIZE = 20


def drawPoint(img, pt, color):
    x, y = pt
    transformed_x = int(CENTER_X + x * GAP_SIZE)
    transformed_y = int(CENTER_Y - y * GAP_SIZE)
    cv2.circle(img, (transformed_x, transformed_y), 2, color, -1)

def drawLine(img, pt1, pt2, color):
    x1, y1 = pt1
    x2, y2 = pt2

    transformed_x1 = int(CENTER_X + x1 * GAP_SIZE)
    transformed_y1 = int(CENTER_Y - y1 * GAP_SIZE)

    transformed_x2 = int(CENTER_X + x2 * GAP_SIZE)
    transformed_y2 = int(CENTER_Y - y2 * GAP_SIZE)
    
    cv2.line(img, (transformed_x1, transformed_y1), (transformed_x2, transformed_y2), color)

def drawTriangle(img, triangle_points, color, filled=None):
    pt1, pt2, pt3 = triangle_points

    drawLine(img, pt1, pt2, color)
    drawLine(img, pt2, pt3, color)
    drawLine(img, pt1, pt3, color)

    drawPoint(img, pt1, color)
    drawPoint(img, pt2, color)
    drawPoint(img, pt3, color)
    x1, y1 = pt1
    x2, y2 = pt2
    x3, y3 = pt3

    
    transformed_x1 = int(CENTER_X + x1 * GAP_SIZE)
    transformed_y1 = int(CENTER_Y - y1 * GAP_SIZE)

    transformed_x2 = int(CENTER_X + x2 * GAP_SIZE)
    transformed_y2 = int(CENTER_Y - y2 * GAP_SIZE)

    transformed_x3 = int(CENTER_X + x3 * GAP_SIZE)
    transformed_y3 = int(CENTER_Y - y3 * GAP_SIZE)

    triangle_cnt = np.array( [(transformed_x1, transformed_y1), 
                              (transformed_x2, transformed_y2), 
                              (transformed_x3, transformed_y3)] )

    if filled:
        cv2.drawContours(img, [triangle_cnt], 0, (0,255,0), -1)

def drawQuadrilateral(img, quad_points, color):
    pt1, pt2, pt3, pt4 = quad_points

    drawLine(img, pt1, pt2, color)
    drawLine(img, pt2, pt3, color)
    drawLine(img, pt3, pt4, color)
    drawLine(img, pt4, pt1, color)

    drawPoint(img, pt1, color)
    drawPoint(img, pt2, color)
    drawPoint(img, pt3, color)
    drawPoint(img, pt4, color)



# auxiliary functions

def getVector(pt1, pt2):
        return (pt2[0]-pt1[0]), (pt2[1]-pt1[1])

# when a point is on the right hand side of a line, the cross product is negative...
# otherwise positive
def crossProduct(vector1, vector2):
    return vector1[0]*vector2[1] - vector1[1]*vector2[0]

def checkPointInTriangle(triangle, point):
    pt1, pt2, pt3 = triangle
    v1 = getVector(pt1, pt2)
    v2 = getVector(pt1, point)
    if crossProduct(v1, v2) < 0:
        v1 = getVector(pt2, pt3)
        v2 = getVector(pt2, point)
        if crossProduct(v1, v2) < 0:
            v1 = getVector(pt3, pt1)
            v2 = getVector(pt3, point)
            if crossProduct(v1, v2) < 0:
                return True
    return False

def checkPointInQuadrilateral(quad, point):
    pt1, pt2, pt3, pt4 = quad
    return checkPointInTriangle((pt1, pt2, pt3), point) or \
           checkPointInTriangle((pt2, pt3, pt4), point) or \
           checkPointInTriangle((pt3, pt4, pt1), point) or \
           checkPointInTriangle((pt4, pt1, pt2), point)

def checkLineSegmentsIntersect(segment1, segment2):
    a1, a2 = segment1
    b1, b2 = segment2

    v1 = getVector(a1, a2)
    v2 = getVector(a1, b1)
    f1 = crossProduct(v1, v2)

    v3 = getVector(a1, a2)
    v4 = getVector(a1, b2)
    f2 = crossProduct(v3, v4)

    if (f1 < 0 and f2 > 0) or (f1 > 0 and f2 < 0):
        v1 = getVector(b1, b2)
        v2 = getVector(b1, a1)
        f1 = crossProduct(v1, v2)

        v3 = getVector(b1, b2)
        v4 = getVector(b1, a2)
        f2 = crossProduct(v3, v4)
        if (f1 < 0 and f2 > 0) or (f1 > 0 and f2 < 0):
            return True
    return False

def findSegmentIntersectionPoint(segment1, segment2):
    p1, p2 = segment1
    p3, p4 = segment2
    a1, b1 = p1
    a2, b2 = p2

    x1, y1 = p3
    x2, y2 = p4
    if (x2-x1) != 0 and (a2-a1) != 0:
        x_intersection = (y2-(y2-y1)/(x2-x1)*x2-b2+(b2-b1)/(a2-a1)*a2)/((b2-b1)/(a2-a1) - (y2-y1)/(x2-x1))
        y_intersection = (y2-y1)/(x2-x1)*x_intersection+y2 - (y2-y1)/(x2-x1)*x2
    
    # vertical case...
    if (x2-x1) == 0 and (a2-a1) != 0:
        x_intersection = x1
        y_intersection = (b2-b1)*x_intersection/(a2-a1) + b2 - (b2-b1)*a2/(a2-a1)
    
    if (x2-x1) != 0 and (a2-a1) == 0:
        x_intersection = a1
        y_intersection = (y2-y1)/(x2-x1)*x_intersection+y2 - (y2-y1)/(x2-x1)*x2
    return (x_intersection, y_intersection)


def calculateArea(pt1, pt2, pt3):
    x1,y1 = pt1
    x2,y2 = pt2
    x3,y3 = pt3
    return 0.5*abs(x1*(y2-y3)+x2*(y3-y1)+x3*(y1-y2))

# Jarvis's algorithm
def findConvexHull(points):
    if len(points) < 3:
        return []
    points = list(set(points))
    # ys in ascending order...
    points.sort(key=lambda a: a[0])
    
    points_with_same_x = [a for a in points if a[0] == points[0][0]]
    # we are sorting the points with the smallest xs 
    points_with_same_x.sort(key=lambda a: a[1])
    # and picking the bottom point
    initial_point = points_with_same_x[0]
    convex_hull_set = [initial_point]
    Q = None
    P = initial_point
    while Q != initial_point:
        for q in points:
            if q == P:
                continue
            Q = q
            all_left = True
            v1 = getVector(P, Q)
            for r in points:
                if r == P or r == Q:
                    continue
                v2 = getVector(P, r)
                # when point is on the right hand side of a vector, the cross product is negative...
                # otherwise positive
                if crossProduct(v1, v2) > 0:
                    all_left = False
                    break
            if all_left == True:
                if Q != initial_point:
                    convex_hull_set.append(Q)
                P = Q
                break
    # after running points are in ccw order
    # we are reversing them to convert it into cw
    return convex_hull_set[::-1]

def area(quad, triangle):
    q_segment1 = quad[0], quad[1]
    q_segment2 = quad[1], quad[2]
    q_segment3 = quad[2], quad[3]
    q_segment4 = quad[3], quad[0]

    t_segment1 = triangle[0], triangle[1]
    t_segment2 = triangle[1], triangle[2]
    t_segment3 = triangle[2], triangle[0]

    enclosed_region = []  

    for t_segment in [t_segment1, t_segment2, t_segment3]:
        start_point = t_segment[0]

        if checkPointInQuadrilateral(quad, start_point):
            enclosed_region.append(start_point)

        intersections = []
        for q_segment in [q_segment1, q_segment2, q_segment3, q_segment4]:
            if checkLineSegmentsIntersect(t_segment, q_segment):
                intersection = findSegmentIntersectionPoint(t_segment, q_segment)
                intersections.append(intersection)
        if len(intersections) == 1:
            intersection_point = intersections[0]
            enclosed_region.append(intersection_point)

        elif len(intersections) == 2:
            p1 = intersections[0]
            p2 = intersections[1]          
            enclosed_region.append(p1)
            enclosed_region.append(p2)
              

    if checkPointInTriangle(triangle, quad[0]):
        enclosed_region.append(quad[0])

    if checkPointInTriangle(triangle, quad[1]):
        enclosed_region.append(quad[1])

    if checkPointInTriangle(triangle, quad[2]):
        enclosed_region.append(quad[2])

    if checkPointInTriangle(triangle, quad[3]):
        enclosed_region.append(quad[3])

    convex_hull = findConvexHull(enclosed_region)

    if len(convex_hull) == 0: # intersection can be empty...
        return 0, []

    queue = convex_hull[:]
    stack = []

    stack.append(queue.pop(0))
    stack.append(queue.pop(0))
    stack.append(queue.pop(0))

    total_area = 0
    triangles = 0
    # divide the intersection region into triangles and sum the areas of the triangles..
    while len(stack) > 0:

        pt3 = stack.pop()
        pt2 = stack.pop()
        pt1 = stack.pop()
        triangles += 1
        total_area += calculateArea(pt1,pt2,pt3)
        if len(queue) > 0:
            stack.append(pt1)
            stack.append(pt3)
            stack.append(queue.pop(0))
    return total_area, convex_hull

# given sample  
quad = [(4,2), (1,7), (5,10), (11,5)]
triangle = [(4,4), (5,8), (13,5)]

#quad = [(-1,0), (-1,5), (3,5), (3,0)]
#triangle = [(-2,1), (1,6), (4,1)]

# some random sample...
#quad = [(4,1),(2,7),(6,4),(7,2)]
#triangle = [(2,2),(1,6), (7,3)]
# 
# # Figure 1, sample shapes: (row, column) each starts with 1 and goes from left to right and top to bottom...
# 1,1
#quad = [(-2,6),(0,12),(12,10),(10,-6)]
#triangle = [(-4,4),(2,14), (14,0)]
# # # 1,2
#quad = [(-4,6),(-2,12),(14,14),(12,2)]
#triangle = [(-6,2),(4,8), (12,0)]
# 1,3
#quad = [(-6,4),(-4,10),(12,12),(10,0)]
#triangle = [(-2,8),(6,14), (8,6)]
# # # 2,1
#quad = [(2,0),(0,4),(4,8),(10,6)]
#triangle = [(0,-2),(-4,10), (16,8)]
# # # 2,2
# quad = [(10-8,0),(2-8,4),(8-8, 12),(18-8,6)]
# triangle = [(8-8,2),(6-8,8), (12-8,6)]
# # # 2,3
# quad = [(-4,14-5),(2,18-5),(12, 16-5),(10,2-5)]
# triangle = [(2,14-5),(-2,22-5), (6,18-5 )]
# # # 3,1
# quad = [(4,6),(6,10),(14, 8),(12,2)]
# triangle = [(14,0),(0,6), (8,8)]
# # 3,2
# quad = [(0,10),(4,14),(12, 12),(8,4)]
# triangle = [(-4,10),(6,16),(10, 0)]
# # 3,3
# quad = [(4,8),(6,12),(10, 14),(12,6)]
# triangle = [(-8,2),(-2,10),(8, 4)]

# drawTriangle(canvas, triangle, (255, 0, 255))
# drawQuadrilateral(canvas, quad, (255, 255, 0))
# 
# 
total_area, intersection_poligon = area(quad, triangle)
print(total_area, intersection_poligon)
# print(total_area)
# print(total_area)
# for p in poligon:
#     drawPoint(canvas, p, (0, 255, 255))
# 
# cv2.imshow("Canvas", canvas)
# cv2.waitKey(0)