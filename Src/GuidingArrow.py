import math


def get_angle(tail, head):
    angle = math.atan2(-(tail[1] - head[1]), tail[0] - head[0])
    angle = math.degrees(angle)
    return 180 - angle


def distance(tail, head):
    dx = tail[0] - head[0]
    dy = tail[1] - head[1]
    return math.sqrt(dx ** 2 + dy ** 2)
