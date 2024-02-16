import copy
import math


# Finds Triangels Area
def triangel_area(T):
    return abs(
        (
            T[0][0] * (T[1][1] - T[2][1])
            + T[1][0] * (T[2][1] - T[0][1])
            + T[2][0] * (T[0][1] - T[1][1])
        )
        / 2.0
    )


# Finds Quadrilaterals Area
def quadrilateral_area(Q):
    return abs(
        (
            (
                (Q[0][0] * Q[1][1])
                + (Q[1][0] * Q[2][1])
                + (Q[2][0] * Q[3][1])
                + (Q[3][0] * Q[0][1])
            )
            - (
                (Q[0][1] * Q[1][0])
                + (Q[1][1] * Q[2][0])
                + (Q[2][1] * Q[3][0])
                + (Q[3][1] * Q[0][0])
            )
        )
        / 2.0
    )


# Checks if Quadrilateral is in the Triangel
def QinT(Q, T):
    countpoints = 0
    Tarea = triangel_area(T)
    for i in range(4):
        A1 = triangel_area([Q[i]] + T[1:])
        A2 = triangel_area([T[0]] + [Q[i]] + [T[2]])
        A3 = triangel_area(T[:2] + [Q[i]])
        if Tarea != (A1 + A2 + A3):
            countpoints += 1
            if countpoints == 4:
                return None
    if countpoints != 0:
        return False
    elif countpoints == 0:
        return True


# Checkes if Triangel is in the Quadrilateral
def TinQ(Q, T):
    countpoints = 0
    Qarea = quadrilateral_area(Q)
    for i in range(3):
        A1 = triangel_area([T[i]] + Q[:2])
        A2 = triangel_area([T[i]] + Q[1:3])
        A3 = triangel_area([T[i]] + Q[2:4])
        A4 = triangel_area([T[i]] + [Q[-1]] + [Q[0]])
        if Qarea != (A1 + A2 + A3 + A4):
            countpoints += 1
            if countpoints == 4:
                return None
    if countpoints != 0:
        return False
    elif countpoints == 0:
        return True


# Finds intersection point of two line segemts
def find_intersection_point(A1, A2, B1, B2):
    # Calculate slopes and intercepts
    m1 = (
        (A2[1] - A1[1]) / (A2[0] - A1[0]) if A1[0] != A2[0] else float("inf")
    )  # Handling vertical line
    b1 = A1[1] - m1 * A1[0]

    m2 = (
        (B2[1] - B1[1]) / (B2[0] - B1[0]) if B1[0] != B2[0] else float("inf")
    )  # Handling vertical line
    b2 = B1[1] - m2 * B1[0]

    # Check if lines are parallel
    if m1 == m2:
        return None

    # Check if one of the lines is vertical
    if m1 == float("inf"):
        x_intersection = A1[0]
        y_intersection = m2 * x_intersection + b2
    elif m2 == float("inf"):
        x_intersection = B1[0]
        y_intersection = m1 * x_intersection + b1
    else:
        # Calculate intersection point
        x_intersection = (b2 - b1) / (m1 - m2)
        y_intersection = m1 * x_intersection + b1

    bigx1 = max(A1[0], A2[0])
    smallx1 = min(A1[0], A2[0])
    bigy1 = max(A1[1], A2[1])
    smally1 = min(A1[1], A2[1])
    bigx2 = max(B1[0], B2[0])
    smallx2 = min(B1[0], B2[0])
    bigy2 = max(B1[1], B2[1])
    smally2 = min(B1[1], B2[1])

    if (
        x_intersection <= bigx1
        and x_intersection <= bigx2
        and x_intersection >= smallx1
        and x_intersection >= smallx2
    ):
        if (
            y_intersection <= bigy1
            and y_intersection <= bigy2
            and y_intersection >= smally1
            and y_intersection >= smally2
        ):
            return x_intersection, y_intersection


# Finds the intersections of quadrilateral and triangel
def intersections(Q, T):
    lst = []
    Qcopy = copy.deepcopy(Q)
    Tcopy = copy.deepcopy(T)
    Qcopy.append(Qcopy[0])
    Tcopy.append(Tcopy[0])
    for t in range(3):
        for q in range(4):
            intersection = find_intersection_point(
                Tcopy[t], Tcopy[t + 1], Qcopy[q], Qcopy[q + 1]
            )
            if intersection != None:
                lst.append(intersection)
    return lst


# Finds the points inside the triangel
def pointsinT(Q, T):
    lst = []
    Tarea = triangel_area(T)
    for i in range(4):
        A1 = triangel_area([Q[i]] + T[1:])
        A2 = triangel_area([T[0]] + [Q[i]] + [T[2]])
        A3 = triangel_area(T[:2] + [Q[i]])
        if Tarea == (A1 + A2 + A3):
            lst.append(Q[i])
    return lst


# Finds the points inside the quadrilateral
def pointsinQ(Q, T):
    lst = []
    Qarea = quadrilateral_area(Q)
    for i in range(3):
        A1 = triangel_area([T[i]] + Q[:2])
        A2 = triangel_area([T[i]] + Q[1:3])
        A3 = triangel_area([T[i]] + Q[2:4])
        A4 = triangel_area([T[i]] + [Q[-1]] + [Q[0]])
        if Qarea == (A1 + A2 + A3 + A4):
            lst.append(T[i])
    return lst


# Sorts the list of coordinates in clockwise
def sort_clockwise(coordinates):
    def calculate_angle(point, reference_point):
        x, y = point[0] - reference_point[0], point[1] - reference_point[1]
        return math.atan2(y, x)

    centroid = (
        sum(x for x, y in coordinates) / len(coordinates),
        sum(y for x, y in coordinates) / len(coordinates),
    )

    sorted_coordinates = sorted(
        coordinates, key=lambda point: -calculate_angle(point, centroid)
    )

    return sorted_coordinates


# Finds the area of the given coordinates
def areaCalculator(points):
    pointsCopy = copy.deepcopy(points)
    pointsCopy.append(pointsCopy[0])
    sum1 = 0
    sum2 = 0
    for i in range(len(points)):
        sum1 += pointsCopy[i][0] * pointsCopy[i + 1][1]
        sum2 += pointsCopy[i][1] * pointsCopy[i + 1][0]
    return abs((sum1 - sum2) / 2.0)


def area(Q, T):
    # check if Quadrilateral is in Triangel
    if QinT(Q, T):
        return quadrilateral_area(Q)
    # check if Triangel is in Quadrilateral
    elif TinQ(Q, T):
        return triangel_area(T)
    # check if Both are seperated
    elif (QinT(Q, T) == None) and (TinQ(Q, T) == None):
        return 0
    # check the Intersections
    intersectionlst = intersections(Q, T)
    if len(intersectionlst) == 0:
        return 0
    intersectionlst = sort_clockwise(
        list(set(intersectionlst + pointsinT(Q, T) + pointsinQ(Q, T)))
    )
    return areaCalculator(intersectionlst)
