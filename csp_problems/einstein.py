import copy
import math

nationalities = ['norwegian', 'danish', 'english', 'german', 'swedish']
colors = ['white', 'green', 'yellow', 'blue', 'red']
drinks = ['tea', 'water', 'milk', 'coffee', 'beer']
tobaccos = ['cigar', 'light', 'no_filter', 'pipe', 'menthol']
pets = ['horse', 'bird', 'fish', 'dog', 'cat']

attributes_list = ['nationality', 'color', 'drink', 'tobacco', 'pet']


class House:
    def __init__(self, number):
        self.attributes = {
            'number': str(number),
            'nationality': '',
            'color': '',
            'drink': '',
            'tobacco': '',
            'pet': ''
        }

    def set_attr(self, attr, val):
        self.attributes[attr] = val

    def __str__(self):
        return f'House: {self.attributes["number"]}\nNationality: {self.attributes["nationality"]}\n' \
               f'Color: {self.attributes["color"]}\nDrink: {self.attributes["drink"]}\n' \
               f'Tobacco: {self.attributes["tobacco"]}\nPet: {self.attributes["pet"]}\n'


class Solution:
    def __init__(self):
        self.solution = []
        self.counter = 0

    def solve(self):
        self.counter = 0
        domain = [nationalities, colors, drinks, tobaccos, pets]
        assignments = [House(1), House(2), House(3), House(4), House(5)]
        res = self.backtracking(0, 0, assignments, domain)
        if res:
            print(self.counter)
            for house in res:
                print(house)
        else:
            print('not found')

    def backtracking(self, attr, attr_val_index, assignment, domain):
        self.counter += 1
        if not Solution.is_valid(assignment):
            return
        if all(len(i) == 0 for i in domain):
            return assignment

        domain_cpy = copy.deepcopy(domain)
        new_attr_val = domain_cpy[attr].pop(0)
        index = (attr_val_index + 1) % 5
        attr_index = attr
        if index == 0:
            attr_index += 1

        for i in range(5):
            if not assignment[i].attributes[attributes_list[attr]]:
                new_assignment = copy.deepcopy(assignment)
                new_assignment[i].set_attr(attributes_list[attr], new_attr_val)
                solution = self.backtracking(attr_index, index, new_assignment, domain_cpy)
                if solution:
                    return solution
                del new_assignment
        return []

    def solve_v2(self):
        self.counter = 0
        domains = [nationalities, colors, drinks, tobaccos, pets]
        domain = []
        for i in range(5):
            cp = copy.deepcopy(domains)
            domain.append(cp)

        assignments = [House(1), House(2), House(3), House(4), House(5)]
        res = self.backtracking_v2(0, 0, assignments, domain)
        if res:
            for house in res:
                print(house)
        else:
            print('not found')

    def backtracking_v2(self, house_index, attr_index, assignment, domain):
        self.counter += 1
        if not Solution.is_valid(assignment):
            return
        if Solution.all_assigned(assignment):
            print(self.counter)
            return assignment

        Solution.lcv(house_index, attr_index, assignment, domain)
        for attr_val in domain[house_index][attr_index]:
            new_assignment = copy.deepcopy(assignment)
            new_domain = copy.deepcopy(domain)

            new_assignment[house_index].set_attr(attributes_list[attr_index], attr_val)
            new_domain[house_index][attr_index] = [attr_val]

            # self.ac_3(house_index, attr_index, attr_val, new_assignment, new_domain)
            h_index, a_index = self.mrv(new_assignment, new_domain)
            solution = self.backtracking_v2(h_index, a_index, new_assignment, new_domain)
            if solution:
                return solution
            del new_assignment
            del new_domain
        return []

    @staticmethod
    def all_assigned(assignment):
        for h in assignment:
            if any(h.attributes[k] == '' for k in h.attributes):
                return False
        return True

    @staticmethod
    def mrv(assignment, domain):
        min_dom_length = math.inf
        house_index = 0
        attr_index = 0
        for h in range(len(domain)):
            for a in range(len(domain[h])):
                if assignment[h].attributes[attributes_list[a]] == '':
                    if len(domain[h][a]) < min_dom_length:
                        house_index = h
                        attr_index = a
                        min_dom_length = len(domain[h][a])

        return house_index, attr_index

    @staticmethod
    def lcv(house_index, attr_index, assignment, domain):
        ordered_attributes = []
        assignment_cpy = copy.deepcopy(assignment)
        for a in domain[house_index][attr_index]:
            counter = 0
            assignment_cpy[house_index].set_attr(attributes_list[attr_index], a)
            for i in range(5):
                for j in range(len(domain[i])):
                    test_cpy = copy.deepcopy(assignment_cpy)
                    for attr_val in domain[i][j]:
                        test_cpy[i].set_attr(attributes_list[j], attr_val)
                        if not Solution.is_valid(test_cpy):
                            counter += 1
                    del test_cpy
            ordered_attributes.append((a, counter))
        del assignment_cpy
        ordered_attributes.sort(key=lambda x: x[1])
        domain[house_index][attr_index] = []
        for a in ordered_attributes:
            domain[house_index][attr_index].append(a[0])

    @staticmethod
    def ac_3(house_index, attr_index, attr_val, assignment, domain):
        for i in range(5):
            if i != house_index:
                if attr_val in domain[i][attr_index]:
                    domain[i][attr_index].remove(attr_val)

        for i in range(5):
            for j in range(0, len(domain[i])):
                assignment_cpy = copy.deepcopy(assignment)
                for x in domain[i][j]:
                    assignment_cpy[i].set_attr(attributes_list[j], x)
                    if not Solution.is_valid(assignment_cpy):
                        domain[i][j].remove(x)
                del assignment_cpy

    @staticmethod
    def is_valid(assignment):
        return all([
            Solution.check_constraint_info(assignment, 'number', '1', 'nationality', 'norwegian'),
            Solution.check_constraint_info(assignment, 'color', 'red', 'nationality', 'english'),
            Solution.check_constraint_left_to(assignment, 'color', 'green', 'color', 'white'),
            Solution.check_constraint_info(assignment, 'nationality', 'danish', 'drink', 'tea'),
            Solution.check_constraint_next_to(assignment, 'tobacco', 'light', 'pet', 'cat'),
            Solution.check_constraint_info(assignment, 'color', 'yellow', 'tobacco', 'cigar'),
            Solution.check_constraint_info(assignment, 'nationality', 'german', 'tobacco', 'pipe'),
            Solution.check_constraint_info(assignment, 'number', '3', 'drink', 'milk'),
            Solution.check_constraint_next_to(assignment, 'tobacco', 'light', 'drink', 'water'),
            Solution.check_constraint_info(assignment, 'tobacco', 'no_filter', 'pet', 'bird'),
            Solution.check_constraint_info(assignment, 'nationality', 'swedish', 'pet', 'dog'),
            Solution.check_constraint_next_to(assignment, 'nationality', 'norwegian', 'color', 'blue'),
            Solution.check_constraint_next_to(assignment, 'pet', 'horse', 'color', 'yellow'),
            Solution.check_constraint_info(assignment, 'tobacco', 'menthol', 'drink', 'beer'),
            Solution.check_constraint_info(assignment, 'color', 'green', 'drink', 'coffee')
        ])

    @staticmethod
    def check_constraint_left_to(assignment, atr1, atr1_val, atr2, atr2_val):
        if assignment[-1].attributes[atr1] and assignment[-1].attributes[atr1] == atr1_val:
            return False

        if assignment[0].attributes[atr2] and assignment[0].attributes[atr2] == atr2_val:
            return False

        for (l_h, r_h) in zip(assignment, assignment[1:]):
            if l_h.attributes[atr1] == atr1_val and r_h.attributes[atr2] and r_h.attributes[atr2] != atr2_val:
                return False
        return True

    @staticmethod
    def check_constraint_info(assignment, atr1, atr1_val, atr2, atr2_val):
        for house in assignment:
            if house.attributes[atr1] == atr1_val and house.attributes[atr2] and house.attributes[atr2] != atr2_val:
                return False
        return True
    
    @staticmethod
    def check_constraint_next_to(assignment, atr1, atr1_val, atr2, atr2_val):
        for i in range(5):
            if assignment[i].attributes[atr1] == atr1_val:
                if i == 0:
                    if assignment[i + 1].attributes[atr2] and assignment[i + 1].attributes[atr2] != atr2_val:
                        return False
                elif i == 4:
                    if assignment[i - 1].attributes[atr2] and assignment[i - 1].attributes[atr2] != atr2_val:
                        return False
                else:
                    if assignment[i - 1].attributes[atr2] and assignment[i - 1].attributes[atr2] != atr2_val and \
                            assignment[i + 1].attributes[atr2] and assignment[i + 1].attributes[atr2] != atr2_val:
                        return False
        return True
