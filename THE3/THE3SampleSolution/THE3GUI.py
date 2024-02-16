import pygame
import pygame.gfxdraw
import samplesolution
import os
import pickle

if not os.path.exists("cases"):
    os.mkdir("cases")


def storetestcase(case_quad, case_triangle, expected_output):
    files = os.listdir("cases")
    file_name = ""
    for file_number in range(1, 155):
        file_name = "case_" + str(file_number) + ".dat"
        if file_name not in files:
            break
    if file_name != "":
        pickle.dump(
            [case_quad, case_triangle, expected_output],
            open("cases/" + file_name, "wb"),
        )
        print("Case stored...")


class CornerPoint(pygame.sprite.Sprite):
    def __init__(self, width, height, pos_x, pos_y, color, index, name):
        super().__init__()
        self.name = name
        self.index = index
        # = pygame.Surface([width, height])
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.gfxdraw.aacircle(self.image, width // 2, height // 2, height // 2, color)
        pygame.gfxdraw.filled_circle(
            self.image, width // 2, height // 2, height // 2, color
        )
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]


pygame.init()

screen = pygame.display.set_mode((640, 640))
pygame.display.set_caption("THE3")
CENTER_X = 320
CENTER_Y = 320

GAP_SIZE = 20

font = pygame.font.Font("freesansbold.ttf", 16)


# given sample
quad = [(8, 0), (-6, 0), (-6, 5), (8, 5)]
triangle = [(-11, 5), (12, 6), (1, -3)]

triangle_group = pygame.sprite.Group()
triangle_corner_point_list = []
triangle_vertices = [
    (a[0] * GAP_SIZE + CENTER_X, CENTER_Y - a[1] * GAP_SIZE) for a in triangle
]

for i, p in enumerate(triangle_vertices):
    if i == 0:
        color = (255, 0, 0)
    else:
        color = (255, 255, 0)

    point = CornerPoint(11, 11, p[0], p[1], color, index=i, name="triangle")
    triangle_group.add(point)
    triangle_corner_point_list.append(point)


quad_group = pygame.sprite.Group()
quad_corner_point_list = []
quad_vertices = [(a[0] * GAP_SIZE + CENTER_X, CENTER_Y - a[1] * GAP_SIZE) for a in quad]

for i, p in enumerate(quad_vertices):
    if i == 0:
        color = (255, 0, 0)
    else:
        color = (255, 255, 0)
    point = CornerPoint(11, 11, p[0], p[1], color, index=i, name="quad")
    quad_group.add(point)
    quad_corner_point_list.append(point)


button_pressed = False
selected_point = None
text_content = [""] * 8
text_content[3] = " "


def checkQuadConvexness(quad):
    points = quad + quad[:2]
    for i in range(len(points) - 2):
        p1 = points[i]
        p2 = points[i + 1]
        p3 = points[i + 2]

        v1 = samplesolution.getVector(p1, p2)
        v2 = samplesolution.getVector(p2, p3)

        if samplesolution.crossProduct(v1, v2) > 0:
            return False
    return True


def displayCoordinates():
    print("Triangle:")
    triangle = []
    quad = []
    for i, p in enumerate(triangle_vertices):
        x, y = p
        original_x = (x - CENTER_X) // GAP_SIZE
        original_y = (CENTER_Y - y) // GAP_SIZE
        print("%3s :%3s" % (original_x, original_y))
        text_content[i] = "%3s :%3s" % (int(original_x), int(original_y))
        triangle.append((original_x, original_y))
    print("Quad:")
    for i, p in enumerate(quad_vertices):
        x, y = p
        original_x = (x - CENTER_X) // GAP_SIZE
        original_y = (CENTER_Y - y) // GAP_SIZE
        print("%3s :%3s" % (original_x, original_y))
        text_content[i + 4] = "%3s :%3s" % (int(original_x), int(original_y))
        quad.append((original_x, original_y))

    if checkQuadConvexness(quad) is False:
        print("***Quadrilateral is not convex***")
        return -1, []
    area, points = samplesolution.area(quad, triangle)

    transformed_poinst = [
        (a[0] * GAP_SIZE + CENTER_X, CENTER_Y - a[1] * GAP_SIZE) for a in points[::-1]
    ]
    print(f"area({quad},{triangle})->{'Area : %f' % area}")
    return area, transformed_poinst


area, intersection_region = displayCoordinates()
intersection_region_filled = 5


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

        if event.type == pygame.KEYDOWN:
            print("Key pressed : ", event.key)
            if event.key == pygame.K_f:
                if intersection_region_filled != 0:
                    intersection_region_filled = 0
                else:
                    intersection_region_filled = 5
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit(0)
            if event.key == pygame.K_s:
                triangle = []
                quad = []
                for i, p in enumerate(triangle_vertices):
                    x, y = p
                    original_x = (x - CENTER_X) // GAP_SIZE
                    original_y = (CENTER_Y - y) // GAP_SIZE
                    triangle.append((original_x, original_y))
                for i, p in enumerate(quad_vertices):
                    x, y = p
                    original_x = (x - CENTER_X) // GAP_SIZE
                    original_y = (CENTER_Y - y) // GAP_SIZE
                    quad.append((original_x, original_y))

                area, points = samplesolution.area(quad, triangle)
                storetestcase(quad, triangle, area)

        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            # print(pos)
            button_pressed = False
            selected_point = None
            # print("Triangle points : ")
            area, intersection_region = displayCoordinates()

        if event.type == pygame.MOUSEBUTTONDOWN:
            button_pressed = True
            pos = pygame.mouse.get_pos()
            clicked_sprites = [
                s for s in triangle_corner_point_list if s.rect.collidepoint(pos)
            ]
            if len(clicked_sprites) > 0:
                print("Selected point : ", clicked_sprites[0].index)
                selected_point = clicked_sprites[0]

            clicked_sprites = [
                s for s in quad_corner_point_list if s.rect.collidepoint(pos)
            ]
            if len(clicked_sprites) > 0:
                print("Selected point : ", clicked_sprites[0].index)
                selected_point = clicked_sprites[0]
            print(pos)
        if event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            # force corner points to move only on the coordinates with integer components...
            pos = (
                round((pos[0] - CENTER_X) // GAP_SIZE) * GAP_SIZE + CENTER_X,
                CENTER_Y - round((-pos[1] + CENTER_Y) // GAP_SIZE) * GAP_SIZE,
            )
            # print(pos)
            if button_pressed:
                if selected_point:
                    if selected_point.name == "triangle":
                        triangle_vertices[selected_point.index] = int(pos[0]), int(
                            pos[1]
                        )
                        triangle_corner_point_list[
                            selected_point.index
                        ].rect.center = pos
                    elif selected_point.name == "quad":
                        quad_vertices[selected_point.index] = int(pos[0]), int(pos[1])
                        quad_corner_point_list[selected_point.index].rect.center = pos
                    area, intersection_region = displayCoordinates()

    screen.fill((41, 41, 41))
    # pygame.draw.polygon(screen, (255, 255, 255), triangle_vertices)
    for i in range(len(triangle_vertices) - 1):
        p1 = triangle_vertices[i]
        p2 = triangle_vertices[i + 1]
        pygame.draw.aaline(screen, (0, 255, 0), p1, p2, 2)
    p1 = triangle_vertices[-1]
    p2 = triangle_vertices[0]
    pygame.draw.aaline(screen, (0, 255, 0), p1, p2, 2)

    for i in range(len(quad_vertices) - 1):
        p1 = quad_vertices[i]
        p2 = quad_vertices[i + 1]
        pygame.draw.aaline(screen, (0, 255, 255), p1, p2)
    p1 = quad_vertices[-1]
    p2 = quad_vertices[0]
    pygame.draw.aaline(screen, (0, 255, 255), p1, p2, 2)

    triangle_group.draw(screen)
    quad_group.draw(screen)
    start_y = 10

    for i, text in enumerate(text_content):
        if text == "":
            continue
        if i < 3:
            color = (0, 255, 0)
        else:
            color = (0, 255, 255)
        text = font.render(
            text,
            True,
            color,
        )
        textRect = text.get_rect()
        textRect.center = (25, start_y)
        screen.blit(text, textRect)
        start_y += 20

    if intersection_region:
        pygame.draw.polygon(
            screen, (255, 0, 0), intersection_region, intersection_region_filled
        )
    pygame.display.flip()


pygame.quit()
