import pygame


class Animation:
    def __init__(self):
        pass


LERP_FACTOR = 0.01
minimum_distance = 0.01
maximum_distance = 1000.0


def follow(pos_start, pos_end):
    target_vector = pygame.math.Vector2(*pos_start)
    follower_vector = pygame.math.Vector2(*pos_end)
    new_follower_vector = pygame.math.Vector2(*pos_end)

    distance = follower_vector.distance_to(target_vector)
    # print(distance)
    # print(distance)
    if distance > minimum_distance:
        direction_vector = (target_vector - follower_vector) / distance
        min_step = max(0, int(distance - maximum_distance))
        max_step = distance - minimum_distance
        step_distance = min_step + (max_step - min_step) * LERP_FACTOR
        new_follower_vector = follower_vector + direction_vector * step_distance
    return new_follower_vector.x, new_follower_vector.y
