from enum import Enum
import random
import numpy
import copy
import math
import matplotlib.pyplot as plt
import pandas as pd

CROSS_PROBABILITY = 0.2
MUTATION_PROBABILITY = 0.5
POPULATION_SIZE = 100
NUMBER_OF_ITERATIONS = 1000


class Direction(Enum):
    SAME_LEVEL = 0
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class Propabilities(Enum):
    ZERO_GOOD_DIR = [1 / 3, 1 / 3, 1 / 3]
    ONE_GOOD_DIR = [0.9, 0.05, 0.05]
    TWO_GOOD_DIR = [0.45, 0.45, 0.1]
    START = [0.45, 0.45, 0.05, 0.05]
    START_SAME_LEVEL = [0.85, 0.05, 0.05, 0.05]


def get_available_directions(last_dir):
    if last_dir == Direction.UP:
        directions = [Direction.RIGHT, Direction.LEFT, Direction.UP]
    elif last_dir == Direction.DOWN:
        directions = [Direction.RIGHT, Direction.LEFT, Direction.DOWN]
    elif last_dir == Direction.RIGHT:
        directions = [Direction.RIGHT, Direction.DOWN, Direction.UP]
    elif last_dir == Direction.LEFT:
        directions = [Direction.LEFT, Direction.DOWN, Direction.UP]
    else:
        directions = [Direction.LEFT, Direction.RIGHT, Direction.DOWN, Direction.UP]

    return directions


def get_opposite_direction(direction):
    if direction == Direction.DOWN:
        return Direction.UP
    elif direction == Direction.UP:
        return Direction.DOWN
    elif direction == Direction.RIGHT:
        return Direction.LEFT
    else:
        return Direction.RIGHT


def is_horizontal(direction):
    return direction == Direction.LEFT or direction == Direction.RIGHT


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_outside_plate(self, edge_x, edge_y):
        return self.x not in range(0, edge_x) or self.y not in range(0, edge_y)

    def update_point_coordinates(self, step):
        if step.direction == Direction.UP:
            self.y += step.step_length
        elif step.direction == Direction.DOWN:
            self.y -= step.step_length
        elif step.direction == Direction.LEFT:
            self.x -= step.step_length
        elif step.direction == Direction.RIGHT:
            self.x += step.step_length

    def get_next_point(self, direction, step):
        next_point = Point(self.x, self.y)
        if direction == Direction.UP:
            next_point.y += step
        elif direction == Direction.DOWN:
            next_point.y -= step
        elif direction == Direction.LEFT:
            next_point.x -= step
        elif direction == Direction.RIGHT:
            next_point.x += step
        return next_point

    def __str__(self):
        return f"({self.x},{self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(self.x) ^ hash(self.y)


def choose_next_dir_x_y(start, end, axis):
    if start < end:
        direction = 1 * axis
    elif start == end:
        direction = Direction.SAME_LEVEL
    else:
        direction = 2 * axis
    return direction


def arr_intersection(availible_dir, right_dir):
    result = list(filter(lambda x: x in availible_dir, right_dir))
    if len(result) == 1:
        availible_dir.insert(0, availible_dir.pop(availible_dir.index(result[0])))
        if len(availible_dir) == 3:
            return availible_dir, Propabilities.ONE_GOOD_DIR
        else:
            return availible_dir, Propabilities.START_SAME_LEVEL
    elif len(result) == 2:
        availible_dir.insert(0, availible_dir.pop(availible_dir.index(result[0])))
        availible_dir.insert(1, availible_dir.pop(availible_dir.index(result[1])))
        if len(availible_dir) == 3:
            return availible_dir, Propabilities.TWO_GOOD_DIR
        else:
            return availible_dir, Propabilities.START

    else:
        return availible_dir, Propabilities.ZERO_GOOD_DIR


class Path:
    def __init__(self, conn_id, point_start, point_end, edge_x, edge_y):
        self.conn_id = conn_id
        self.point_start = point_start
        self.point_end = point_end
        self.edge_x = edge_x
        self.edge_y = edge_y
        self.steps = list()
        self.visited = list()
        self.weight = 1

    def get_right_step_directions(self, current_point):
        if current_point.x < self.point_end.x:
            dir_x = Direction.RIGHT
        elif current_point.x == self.point_end.x:
            dir_x = Direction.SAME_LEVEL
        else:
            dir_x = Direction.LEFT

        if current_point.y < self.point_end.y:
            dir_y = Direction.UP
        elif current_point.y == self.point_end.y:
            dir_y = Direction.SAME_LEVEL
        else:
            dir_y = Direction.DOWN

        if dir_x == Direction.SAME_LEVEL:
            return [dir_y]
        elif dir_y == Direction.SAME_LEVEL:
            return [dir_x]

        return [dir_x, dir_y]

    def normalise_steps(self):
        steps_no_zero = []
        for step in self.steps:
            if step.step_length != 0:
                steps_no_zero.append(step)
        steps_no_opposite = []
        i = 0
        while i < len(steps_no_zero):
            if i == len(steps_no_zero) - 1:
                steps_no_opposite.append(steps_no_zero[i])
            elif get_opposite_direction(steps_no_zero[i + 1].direction) == steps_no_zero[i].direction:
                if steps_no_zero[i + 1].step_length > steps_no_zero[i].step_length:
                    steps_no_zero[i + 1].step_length -= steps_no_zero[i].step_length
                    steps_no_opposite.append(steps_no_zero[i + 1])
                    i += 1
                elif steps_no_zero[i + 1].step_length < steps_no_zero[i].step_length:
                    steps_no_zero[i].step_length -= steps_no_zero[i + 1].step_length
                    steps_no_opposite.append(steps_no_zero[i])
                    i += 1
                else:
                    i += 1
            else:
                steps_no_opposite.append(steps_no_zero[i])
            i += 1
        final_steps = []
        i = 0
        while i < len(steps_no_opposite):
            if i == 0:
                final_steps.append(steps_no_opposite[i])
            elif final_steps[-1].direction == steps_no_opposite[i].direction:
                final_steps[-1].step_length += steps_no_opposite[i].step_length
            else:
                final_steps.append(steps_no_opposite[i])

            i += 1

        self.steps = final_steps

    def normalise_steps_v2(self):
        new_steps = []
        if len(self.steps) < 2:
            return
        for step in self.steps:
            if len(new_steps) == 0:
                new_steps.append(step)
                continue

            last_segment = new_steps[-1]
            last_index = len(new_steps) - 1
            # same direction  = add
            if last_segment.direction == step.direction:
                new_steps[last_index].step_length += step.step_length
                continue
            # opposite direction
            if last_segment.direction == get_opposite_direction(step.direction):
                difference = last_segment.step_length - step.step_length
                # remove if same lengths
                if difference == 0:
                    new_steps.remove(last_segment)
                    continue

                if difference < 0:
                    last_segment.direction = get_opposite_direction(last_segment.direction)

                last_segment.step_length = abs(difference)
                continue

            new_steps.append(step)

        self.steps = new_steps

    def mutate_segment_v3(self):
        if len(self.steps) <= 1:
            moved_step_index = 0
        else:
            moved_step_index = random.randint(0, len(self.steps) - 1)

        mutate_step = self.steps[moved_step_index]
        if is_horizontal(mutate_step.direction):
            move_direction = random.choice([Direction.UP, Direction.DOWN])
            plate_edge = self.edge_y
        else:
            move_direction = random.choice([Direction.LEFT, Direction.RIGHT])
            plate_edge = self.edge_x

        move_step_length = random.randint(1, plate_edge - 1)
        mutation_segments = []
        if mutate_step.step_length > 1 and bool(random.getrandbits(1)):
            split_point = random.randint(1, mutate_step.step_length - 1)
            # mutate before or after split
            # before split
            if bool(random.getrandbits(1)):
                mutation_segments.append(Step(move_direction, move_step_length))
                mutation_segments.append(Step(mutate_step.direction, split_point))
                mutation_segments.append(Step(get_opposite_direction(move_direction), move_step_length))
                mutation_segments.append(Step(mutate_step.direction, mutate_step.step_length - split_point))
            # after split point
            else:
                mutation_segments.append(Step(mutate_step.direction, split_point))
                mutation_segments.append(Step(move_direction, move_step_length))
                mutation_segments.append(Step(mutate_step.direction, mutate_step.step_length - split_point))
                mutation_segments.append(Step(get_opposite_direction(move_direction), move_step_length))
        else:
            mutation_segments.append(Step(move_direction, move_step_length))
            mutation_segments.append(Step(mutate_step.direction, mutate_step.step_length))
            mutation_segments.append(Step(get_opposite_direction(move_direction), move_step_length))

        del self.steps[moved_step_index]
        self.steps[moved_step_index:moved_step_index] = mutation_segments
        self.normalise_steps_v2()
        self.get_all_visited_points()

    def draw_step(self, directions, right_directions, propability, current_point):
        direction = numpy.random.choice(directions, p=propability.value)
        if direction in right_directions:
            if direction == Direction.RIGHT or direction == Direction.LEFT:
                step_length = random.randint(1, abs(current_point.x - self.point_end.x))
            else:
                step_length = random.randint(1, abs(current_point.y - self.point_end.y))
        else:
            # TODO to trzeba zmienic zaleznie od wymiarów płytki i zaleznie od kierunku X Y  w jakim idziemy
            if direction == Direction.RIGHT or direction == Direction.LEFT:
                step_length = random.randint(1, self.edge_x / 2)
            else:
                step_length = random.randint(1, self.edge_y / 2)

        return direction, step_length

    def generate_path(self):
        current_p = Point(self.point_start.x, self.point_start.y)
        last_direction = -1
        while not current_p.__eq__(self.point_end):
            new_segment = self.make_a_step(current_p, last_direction)
            last_direction = new_segment[1]
            current_p = new_segment[0]
        self.get_all_visited_points()

    def print(self):
        for seg in self.steps:
            print(seg)

    def make_a_step(self, current_point, last_dir):
        next_step = Step()
        availible_directions = get_available_directions(last_dir)
        right_directions = self.get_right_step_directions(current_point)
        availible_steps, propability = arr_intersection(availible_directions, right_directions)
        next_step.direction, next_step.step_length = self.draw_step(availible_steps, right_directions, propability,
                                                                    current_point)
        current_point.update_point_coordinates(next_step)
        if self.steps and next_step.direction == self.steps[-1].direction:
            self.steps[-1].step_length += next_step.step_length
        else:
            self.steps.append(next_step)
        return current_point, next_step.direction

    def get_all_visited_points(self):
        visited = list()
        visited.append(self.point_start)
        next_point = self.point_start
        for step in self.steps:
            for i in range(step.step_length):
                next_point = next_point.get_next_point(step.direction, 1)
                visited.append(next_point)
        self.visited = visited

    def get_points_outside_plate(self):
        outside = set()
        for point in self.visited:
            if point.x not in range(0, self.edge_x) or point.y not in range(0, self.edge_y):
                outside.add(point)
        return outside

    def get_sum_of_outside_path_length(self):
        prev_flag = False
        length_outside = 0
        for point in self.visited:
            next_flag = point.is_outside_plate(self.edge_x, self.edge_y)
            if next_flag != prev_flag or next_flag is True:
                length_outside += 1
            prev_flag = next_flag

        return length_outside

    def calculate_total_path_length(self):
        length = 0
        for segment in self.steps:
            length += segment.step_length
        return length

    def __str__(self):
        return f"{self.point_start} -> {self.point_end}"


class Plate:
    def __init__(self, plate_x, plate_y, conn_list):
        self.plate_x = plate_x
        self.plate_y = plate_y
        self.conn_list = conn_list
        self.fitness = 0
        self.fitness_retarded = 0
        self.path_list = list()

    def mutate_path_v2(self):
        chance = random.uniform(0, 1)
        if chance >= 1 - MUTATION_PROBABILITY:
            index = random.randrange(len(self.path_list))
            self.path_list[index].mutate_segment_v3()

    def generate_plate(self):
        for conn in self.conn_list:
            self.path_list.append(Path(conn.id, conn.point_start, conn.point_end, self.plate_x, self.plate_y))

        for path in self.path_list:
            path.generate_path()

    def draw_paths(self, i):
        plt.figure(i)
        x = []
        y = []
        for i in range(0, self.plate_x):
            for j in range(0, self.plate_y):
                x.append(i)
                y.append(j)
        plt.plot(x, y, 'o', color='black')
        color_i = '000000'
        for path in self.path_list:
            for (start, end) in zip(path.visited, path.visited[1:]):
                plt.plot([start.x, end.x], [start.y, end.y], color='#' + color_i, linewidth=4)
            color_i = "%06x" % random.randint(0, 0xFFFFFF)
        x = []
        y = []
        dict_intersect = self.get_points_with_intersects()
        for point in dict_intersect.keys():
            if len(dict_intersect[point]) > 1:
                x.append(point.x)
                y.append(point.y)
        plt.plot(x, y, 'o', color="fuchsia")

    def calculate_fitness(self, penalty_weight, path_int_weights, path_out_weights):
        intersection_dict = self.get_points_with_intersects()
        # sum_of_intersects, paths_with_intersects = self.count_sum_of_intersects(intersection_dict)
        total_length, total_segments = self.total_paths_lengths_and_sum_of_segments()
        total_length_out, paths_out = self.get_total_length_outside_plate(path_out_weights)
        intersection_penalty = self.calculate_intersection_penalty(intersection_dict, path_int_weights)

        total_length = total_length * penalty_weight["total_length"]
        total_segments = total_segments * penalty_weight["total_segments"]
        total_length_out = total_length_out * penalty_weight["total_length_out"]
        intersection_penalty = intersection_penalty * penalty_weight["intersection_penalty"]
        num_of_paths_out = len(paths_out) * penalty_weight["num_of_paths_out"]
        #
        print(f"Intersection penalty (adapt): {intersection_penalty}")
        print(f"Total length of paths: {total_length}")
        print(f"Sum of segments: {total_segments}")
        print(f"Number of paths outside plate: {len(paths_out)}")
        print(f"Total sum of parts outside: {total_length_out}")
        total_fitness = total_length + total_segments + total_length_out + intersection_penalty + num_of_paths_out

        self.fitness = total_fitness

    def calculate_fitness_retarded(self, penalty_weight, path_int_weights, path_out_weights):
        intersection_dict = self.get_points_with_intersects()
        # sum_of_intersects, paths_with_intersects = self.count_sum_of_intersects(intersection_dict)
        total_length, total_segments = self.total_paths_lengths_and_sum_of_segments()
        total_length_out, paths_out = self.get_total_length_outside_plate(path_out_weights)
        intersection_penalty = self.calculate_intersection_penalty(intersection_dict, path_int_weights)

        total_length = total_length * penalty_weight["total_length"]
        total_segments = total_segments * penalty_weight["total_segments"]
        total_length_out = total_length_out * penalty_weight["total_length_out"]
        intersection_penalty = intersection_penalty * penalty_weight["intersection_penalty"]
        num_of_paths_out = len(paths_out) * penalty_weight["num_of_paths_out"]
        total_fitness = total_length + total_segments + total_length_out + intersection_penalty + num_of_paths_out

        self.fitness_retarded = total_fitness

    def calculate_intersection_penalty(self, intersection_dict, path_int_weights):
        total = 0
        point_penalty = 1.0
        for key in intersection_dict:
            length = len(intersection_dict[key])
            if length > 1:
                for conn_id in intersection_dict[key]:
                    point_penalty = point_penalty * path_int_weights[conn_id]
                total += point_penalty
                point_penalty = 1.0
        return total

    def get_points_with_intersects(self):
        point_dict = {}
        for path in self.path_list:
            for point in path.visited:
                if point in point_dict:
                    point_dict[point].append(path.conn_id)
                else:
                    point_dict[point] = [path.conn_id]
        return point_dict

    def get_paths_with_intersects(self):
        intersect_dict = self.get_points_with_intersects()
        intersect_paths = set()
        for key in intersect_dict:
            length = len(intersect_dict[key])
            if length > 1:
                intersect_paths.update(intersect_dict[key])
        return intersect_paths

    def print(self):
        for path in self.path_list:
            for seg in path.steps:
                print(seg)

    def get_paths_outside(self):
        paths_outside = list()
        for path in self.path_list:
            path_outside_len = path.get_sum_of_outside_path_length()
            if path_outside_len > 0:
                paths_outside.append(path)
        return paths_outside

    def get_total_length_outside_plate(self, path_out_weights):
        paths_outside = list()
        total_length_outside = 0
        for path in self.path_list:
            path_outside_len = path.get_sum_of_outside_path_length()
            if path_outside_len > 0:
                paths_outside.append(path)
                total_length_outside += path_outside_len * 10 * path_out_weights[path.conn_id]

        return total_length_outside, paths_outside



    def total_paths_lengths_and_sum_of_segments(self):
        length_total = 0
        sum_of_segments = 0
        for path in self.path_list:
            length_total += path.calculate_total_path_length()
            sum_of_segments += len(path.steps)

        return length_total, sum_of_segments

    def __str__(self):
        return f"Plate {self.__hash__()}   fitness {self.fitness}"


class Step:
    def __init__(self, direction=Direction.SAME_LEVEL, step_length=0):
        self.direction = direction
        self.step_length = step_length

    def __str__(self):
        return f"{self.direction} -> {self.step_length}"


class Population:
    def __init__(self):
        self.plate_x = 0
        self.plate_y = 0
        self.conn_list = list()
        self.path_int_weights = list()
        self.path_out_weights = list()

        self.path_int_weights_retarded = list()
        self.path_out_weights_retarded = list()
        self.penalty_weights = {'total_length': 0.1,
                                'total_segments': 0.05,
                                'total_length_out': 0.5,
                                'num_of_paths_out': 0.5,
                                'intersection_penalty': 0.2}
        self.penalty_weights_retarded = {'total_length': 0.1,
                                'total_segments': 0.05,
                                'total_length_out': 10,
                                'num_of_paths_out': 0.5,
                                'intersection_penalty': 8}
        self.pandas_data_frame = {'Best 1': [],
                                  'Worst 1': [],
                                  'Avg 1': [],
                                  'STDEV 1': [],
                                  'Best 2': [],
                                  'Worst 2': [],
                                  'Avg 2': [],
                                  'STDEV 2': [],
                                  'Best 3': [],
                                  'Worst 3': [],
                                  'Avg 3': [],
                                  'STDEV 3': [],
                                  'Best 4': [],
                                  'Worst 4': [],
                                  'Avg 4': [],
                                  'STDEV 4': [],
                                  'Best 5': [],
                                  'Worst 5': [],
                                  'Avg 5': [],
                                  'STDEV 5': [],
                                  'Best 6': [],
                                  'Worst 6': [],
                                  'Avg 6': [],
                                  'STDEV 6': [],
                                  'Best 7': [],
                                  'Worst 7': [],
                                  'Avg 7': [],
                                  'STDEV 7': [],
                                  'Best 8': [],
                                  'Worst 8': [],
                                  'Avg 8': [],
                                  'STDEV 8': [],
                                  'Best 9': [],
                                  'Worst 9': [],
                                  'Avg 9': [],
                                  'STDEV 9': [],
                                  'Best 10': [],
                                  'Worst 10': [],
                                  'Avg 10': [],
                                  'STDEV 10': []}

    def calc_fitness_and_sort(self, population):
        for ind in population:
            ind.calculate_fitness(self.penalty_weights, self.path_int_weights, self.path_out_weights)
        population.sort(key=lambda x: x.fitness)
        return population

    def calc_fitness_and_sort_retarded(self, population):
        for ind in population:
            ind.calculate_fitness_retarded(self.penalty_weights_retarded, self.path_int_weights_retarded, self.path_out_weights_retarded)
        population.sort(key=lambda x: x.fitness_retarded, reverse=True)
        return population

    def roulette_selection(self, population):
        total_fitness = 0
        probabilities = []
        for individual in population:
            total_fitness += individual.fitness

        for individual in population:
            probabilities.append(1 / individual.fitness / total_fitness)

        parent_a = random.choices(population, probabilities)[0]
        parent_b = random.choices(population, probabilities)[0]
        while parent_a is parent_b:
            parent_b = random.choices(population, probabilities)[0]

        return [parent_a, parent_b]

    def tournament_selection(self, population, group_size):
        candidates = []
        for i in range(group_size):
            candidate = random.choice(population)
            while candidate in candidates:
                candidate = random.choice(population)
            candidates.append(candidate)

        candidates.sort(key=lambda x: x.fitness)
        best_cand_one = candidates[0]
        best_cand_two = candidates[1]
        return [best_cand_one, best_cand_two]

    def cross_two_individuals(self, ind_one, ind_two):
        child_one = copy.deepcopy(ind_one)
        child_two = copy.deepcopy(ind_two)
        probability = random.uniform(0, 1)
        if probability >= 1 - CROSS_PROBABILITY:
            gene_swap_index = random.randrange(1, len(child_one.path_list))
            for i in range(gene_swap_index):
                temp_path = copy.deepcopy(child_one.path_list[i])
                child_one.path_list[i] = copy.deepcopy(child_two.path_list[i])
                child_two.path_list[i] = temp_path

        return child_one, child_two

    def test_cross(self):
        plate1 = Plate(self.plate_x, self.plate_y, self.conn_list)
        plate1.generate_plate()

        plate1.print()
        plate1.draw_paths(1)
        plate1.path_list[0].normalise_steps()
        list_plate = []
        for i in range(100):
            plate1.mutate_path_v2()
            list_plate.append(copy.deepcopy(plate1))

        plate1.print()

    def test_mutation(self):
        list_plate = []
        plate = Plate(self.plate_x, self.plate_y, self.conn_list)
        plate.generate_plate()
        for i in range(15):
            plate.mutate_path_v2()
            plate.draw_paths(i)
            list_plate.append(copy.deepcopy(plate))
        print("asasas")
        plt.show()

    def read_plate_from_file(self, filename):
        with open(filename) as file:
            for count, line in enumerate(file):
                data = line.rstrip("\n").split(";")
                if count == 0:
                    self.plate_x = int(data[0])
                    self.plate_y = int(data[1])
                else:
                    self.conn_list.append(Connection(count - 1,
                                                     Point(int(data[0]), int(data[1])),
                                                     Point(int(data[2]), int(data[3]))))
                    self.path_int_weights.append(1)
                    self.path_out_weights.append(1)
                    self.path_int_weights_retarded.append(1)
                    self.path_out_weights_retarded.append(1)

    def print_population(self, population):
        i = 0
        for ind in population:
            print(ind.fitness)
            ind.draw_paths(i)
            i += 1
        plt.show()

    def genetic_alg(self,repeats):
        self.pandas_data_frame = {'Best 1': [],
                                  'Worst 1': [],
                                  'Avg 1': [],
                                  'STDEV 1': [],
                                  'Best 2': [],
                                  'Worst 2': [],
                                  'Avg 2': [],
                                  'STDEV 2': [],
                                  'Best 3': [],
                                  'Worst 3': [],
                                  'Avg 3': [],
                                  'STDEV 3': [],
                                  'Best 4': [],
                                  'Worst 4': [],
                                  'Avg 4': [],
                                  'STDEV 4': [],
                                  'Best 5': [],
                                  'Worst 5': [],
                                  'Avg 5': [],
                                  'STDEV 5': [],
                                  'Best 6': [],
                                  'Worst 6': [],
                                  'Avg 6': [],
                                  'STDEV 6': [],
                                  'Best 7': [],
                                  'Worst 7': [],
                                  'Avg 7': [],
                                  'STDEV 7': [],
                                  'Best 8': [],
                                  'Worst 8': [],
                                  'Avg 8': [],
                                  'STDEV 8': [],
                                  'Best 9': [],
                                  'Worst 9': [],
                                  'Avg 9': [],
                                  'STDEV 9': [],
                                  'Best 10': [],
                                  'Worst 10': [],
                                  'Avg 10': [],
                                  'STDEV 10': []}
        for repeat in range(repeats):
            population = []
            for i in range(len(self.path_out_weights)):
                self.path_out_weights[i] = 1
                self.path_int_weights[i] = 1

            last_fitness = math.inf
            for i in range(POPULATION_SIZE):
                plate = Plate(self.plate_x, self.plate_y, self.conn_list)
                plate.generate_plate()
                population.append(plate)
            for i in range(700):
                print(f"{i} - {repeat}")
                population = self.calc_fitness_and_sort(population)
                self.write_to_csv(population, repeat + 1)
                best_ind = population[0]
                if i % 690== 0:
                    best_ind.draw_paths(i)
                    plt.show()
                next_population = [best_ind]
                if last_fitness <= best_ind.fitness:
                    self.update_intersection_weights(best_ind.get_paths_with_intersects())
                    self.update_outside_weights(best_ind.get_paths_outside())
                last_fitness = best_ind.fitness
                while len(next_population) < POPULATION_SIZE:
                    parents = self.roulette_selection(population)
                    children = self.cross_two_individuals(parents[0], parents[1])
                    children[0].mutate_path_v2()
                    next_population.append(children[0])
                    children[1].mutate_path_v2()
                    next_population.append(children[1])
                if len(next_population) > POPULATION_SIZE:
                    next_population.pop()
                population = next_population[:]

        self.panda_to_csv()

    def update_intersection_weights(self, intersection_paths):
        for conn in intersection_paths:
            self.path_int_weights[conn] += 1

    def update_outside_weights(self, outside_paths):
        for conn in outside_paths:
            self.path_out_weights[conn.conn_id] += 1

    def write_to_csv(self, population,repeat):
        population = self.calc_fitness_and_sort_retarded(population)
        best_ind = 1/(population[0].fitness_retarded *10)
        worst_ind = 1/population[-1].fitness_retarded
        best_ind = population[0].fitness*0.1
        worst_ind = population[-1].fitness*0.1
        average = numpy.mean([ind.fitness*0.1 for ind in population])
        stdev = numpy.std([ind.fitness*0.1 for ind in population])
        self.pandas_data_frame[f'Best {repeat}'].append(best_ind)
        self.pandas_data_frame[f'Worst {repeat}'].append(worst_ind)
        self.pandas_data_frame[f'Avg {repeat}'].append(average)
        self.pandas_data_frame[f'STDEV {repeat}'].append(stdev)
        with open('population_100_zad1', 'w', newline='') as file:
            writer = csv.writer(file)
            # writer.writerow(["Best", "Worst", "Average", "Stdev"])
            writer.writerow([best_ind, worst_ind, average, stdev])

    def panda_to_csv(self):
        df = pd.DataFrame(self.pandas_data_frame,columns=['Best 1','Best 2','Best 3','Best 4','Best 5',
                                                          'Worst 1','Worst 2','Worst 3','Worst 4','Worst 5',
                                                          'Avg 1','Avg 2','Avg 3','Avg 4','Avg 5',
                                                          'STDEV 1','STDEV 2','STDEV 3','STDEV 4','STDEV 5'])

        df.to_csv('iteration_700_zad2.csv', header=True, sep='\t',decimal=',')

class Connection:
    def __init__(self, id, point_start, point_end):
        self.id = id
        self.point_start = point_start
        self.point_end = point_end
        self.weight = 1


if __name__ == '__main__':
    population = Population()
    population.read_plate_from_file("zad2.txt")
    population.genetic_alg(5)
