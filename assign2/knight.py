"""
File: knight.py
---------------------
Assignment 2: Quest for the Holy Grail
Course: CS 41
Name: Mamadou Diallo
SUNet: mamadou

Teach a dragon to fly and learn to fight!
"""
import math

class Dragon:
    """Implement your Dragon here!"""

    def fly(self, *fly_to):

        # Decompose calculations
        def calculate_orientation(destination):
            orientation = math.degrees(math.atan(destination[1] / destination[0]))
            return orientation

        def calculate_ascent(destination):
            hypotenuse = math.sqrt((destination[0] * destination[0]) + (destination[1] * destination[1]))
            ascent = math.degrees(math.atan(destination[2] / hypotenuse))
            return ascent

        def calculate_distance(destination):
            hypotenuse = math.sqrt((destination[0] * destination[0]) + (destination[1] * destination[1]))
            distance = math.sqrt(hypotenuse * hypotenuse + destination[2] * destination[2])
            return distance

        # Initialize current location
        coordinates = [0, 0, 0]
        orientation_ascent = [90, 0]     # this will hold the orientation and the ascent respectively

        tuple_list = []     # to later populate
        for location in fly_to:

            # Subtract these coordinates by the last locationed coordnates to figure out where to move to
            travel_to = [location[0] - coordinates[0], location[1] - coordinates[1], location[2] - coordinates[2]]

            orientation = calculate_orientation(travel_to)
            ascent = calculate_ascent(travel_to)
            distance = calculate_distance(travel_to)

            tuple_list.append((orientation_ascent[0] - orientation, ascent - orientation_ascent[1], distance))  # add the change in travel

            coordinates = [location[0], location[1], location[2]]    # the old coordinates
            orientation_ascent = [orientation, ascent]

        return tuple_list


class Knight:
    """Implement your Knight here!"""

    name = "Mamadou Diallo"
    dragon = Dragon()


    def fight(self):
        # guess and check magic
        return [1, 3, 0, 1, 0, 1, 2, 2, 2, 1, 2, 2, 2]

    def make_potions(self, pantry, market, potions):
        # There are too many options and I do not not know how to explore all of these options
        print("Pantry: ")
        print(pantry)
        print("Market: ")
        print(market)
        print("Potion: ")
        print(potions)
        return 2













print("Done")
