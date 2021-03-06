from Queue import queue
import random
from PathFind import Node, a_star

class animal:
    """Class to manage the animal in the simulation"""
    def __init__(self, x, y, animal_range, speed):
        self.x = x
        self.y = y
        self.animal_range = animal_range
        self.speed = speed
        self.hunger = 10
        self.food_near = []
        self.searching_for_food = True
        self.move_queue = queue()
        self.moves = ""

    def move_to_food(self):
        #Boolean for determining if animal has found any food
        has_path = False
        if self.move_queue:
            #If the animal has a queue, they have found a food
            has_path = True

        moved = 0
        for i in range(self.speed):
            empty_queue = False
            moves = self.move_queue.de_q()
            try:
                new_q = moves[1:]
            except TypeError as e:
                if not has_path:
                    self.searching_for_food = True
            try:
                try:
                    move = moves[0]
                except TypeError as t:
                    empty_queue = True
            except IndexError as e:
                empty_queue = True

            if empty_queue:
                """
                If the animal has a path set, an empty queue means
                they have reached their food and should exit
                """
                if has_path:
                    break

                move = random.choice(["U", "D", "L", "R"])
                self.searching_for_food = True

            self.move_queue = queue()
            self.move_queue.add(new_q)

            if move == "U":
                self.y += 1
            elif move == "D":
                self.y -= 1
            elif move == "L":
                self.x -= 1
            elif move == "R":
                self.x += 1

    def reproduce(self, restricted_spots, size, population):
        x_interval = 1
        y_interval = 0

        new_animals = []

        for i in range(2):
            while True:
                new_x = random.randint(1, size)
                new_y = random.randint(1, size)
                try:
                    if restricted_spots[new_x] != new_y:
                        break
                except KeyError as e:
                    break


            ###Create the attributes of the new animals###
            if population > 10:
                mutation_chance = 50
            elif population < 7 and population > 3:
                mutation_chance = 20
            else:
                mutation_chance = 5
            speed_rand = random.randint(1, mutation_chance)
            if speed_rand == 1:
                speed = random.randint(1, 5)
            else:
                speed = self.speed

            range_rand = random.randint(1, mutation_chance)
            if range_rand == 1:
                animal_range = random.randint(5, 10)
            else:
                animal_range = self.animal_range
            #############################################

            restricted_spots[new_x] = new_y

            new_animal = animal(new_x, new_y, animal_range, speed)
            new_animals.append(new_animal)

        return new_animals

    def eat(self, foods):
        x, y = -1, -1
        for food in foods:
            if food.x == self.x and food.y == self.y:
                print (f"📗📗📗{self} yum x: {self.x} y:{self.y}")
                self.searching_for_food = True
                self.hunger += food.type
                x = food.x
                y = food.y
                self.food_near = []
                self.move_queue = queue()
                break
        new_foods = []
        for food in foods:
            if food.x != x or food.y != y:#Fix to error where too much food gets removed
                new_foods.append(food)

        return new_foods, self.searching_for_food

    def find_food(self, board):
        self.searching_for_food = False
        x_area = range(self.x - int(self.animal_range), self.x + int(self.animal_range))
        y_area = range(self.y - int(self.animal_range), self.y + int(self.animal_range))
        area = [x_area, y_area]
        for x in x_area:
            for y in y_area:
                try:
                    if board[x][y] == 1 and x > 0 and y > 0:
                        food = [x, y]
                        self.food_near.append(food)
                except IndexError as e:
                    pass

    def end_found(self, moves, x, y, foodx, foody):
        for move in moves:
            if move == "U":
                y += 1
            elif move == "D":
                y -= 1
            elif move == "L":
                x -= 1
            elif move == "R":
                x += 1
        if x == foodx and y == foody:
            return True
        else:
            return False

    def valid_path(self, moves, x, y):
        for move in moves:
            if move == "U":
                y += 1
            elif move == "D":
                y -= 1
            elif move == "L":
                x -= 1
            elif move == "R":
                x += 1
        if x < 100 and x > 0 and y < 100 and y > 0:
            return True
        else:
            return False


    def find_best_path(self, food, width, height):
        # Find the best path using the a star algorithm
        path = a_star(width, height, [self.x, self.y], food)

        #Add the current route to the q
        new_q = queue()
        new_q.add(path)
        self.move_queue = new_q

if __name__ == '__main__':
    a = animal(5, 5, 5, 5)
    a.find_food()
    #print(a.find_best_path(7, 7))
