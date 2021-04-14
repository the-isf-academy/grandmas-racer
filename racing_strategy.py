from quest.strategy import Strategy
from random import random, randint, uniform
from math import tau, sin, cos

class RaceStrategy(Strategy):
    """ A strategy which causes the sprite to try and finish the race, with some chance 
    of changing direction at each step.

    Arguments:
        change_prob (float): The probability (between 0 and 1) that the sprite will choose
        a new direction on a step.
    """
    def __init__(self, change_prob=0.1):
        self.change_prob = change_prob
        # self.set_random_direction()
        # self.random_movement = uniform(-2,2)
        self.random_movement = 0

        self.change_x = .1
        self.change_y = .1

    def choose_course(self, sprite, game):
        """Keeps going left to win the race 

        Arguments:
            sprite: The sprite who is about to act.
            game: The game object (to access attributes useful in choosing the course).
        """

        near_wall_list = sprite.near_wall(game,sprite.hit_box_radius)
        far_wall_list = sprite.near_wall(game,150)

        # print(random_movement)


        if sprite.heading['curr'] == 0 and near_wall_list[0]==0:
            self.change_y = sprite.speed 
            self.change_x += self.random_movement
    
        elif sprite.heading['curr'] == 1 and near_wall_list[1] == 0:
            self.change_x = sprite.speed 
            self.change_y += self.random_movement

        elif sprite.heading['curr'] == 2 and near_wall_list[2] == 0:
            self.change_y = -sprite.speed
            self.change_x += self.random_movement

        elif sprite.heading['curr'] == 3 and near_wall_list[3] == 0:
            self.change_x = -sprite.speed
            self.change_y += self.random_movement



        self.check_direction(sprite,near_wall_list, far_wall_list)
        # print(change_x,change_y)

        return (self.change_x,self.change_y)
       

    def check_direction(self,sprite, near_wall_list, far_wall_list):
        """
        Checks if it can keep going forward. If not, turns lefts. Debates if it should add realistic movement (re: drift). 
        """



        original_heading = sprite.heading['curr']
        new_heading = sprite.heading['list'].index(original_heading) -1
        
        random_change = randint(0,15)


        if near_wall_list[original_heading] != 0: 

            while near_wall_list[new_heading] != 0 and new_heading != original_heading:
                new_heading = sprite.heading['list'].index(new_heading) -1
            sprite.heading['curr'] = sprite.heading['list'][new_heading]

        elif near_wall_list[original_heading] == 0 and random_change == 0:

            self.drift(sprite,near_wall_list)

        # elif far_wall_list[new_heading] == 0 and random_change == 3:
        #     print('change',far_wall_list)
        #     sprite.heading['curr'] = sprite.heading['list'][new_heading]





    def drift(self,sprite, near_wall_list):
        "slightly more realistic movement to NPC if it has space to do so..."

        drift_num_pos =uniform(0,2)
        drift_num_neg = uniform(-2,0)

        if sprite.heading['curr'] == 0:
            if near_wall_list[-1]==0:
                self.change_x = drift_num_neg
            elif near_wall_list[1]==0:
                self.change_x = drift_num_pos
            else:
                self.change_x = .1

    
        elif sprite.heading['curr'] == 1:
            if near_wall_list[0] == 0:
                self.change_y = drift_num_pos
            elif near_wall_list[2] == 0:
                self.change_y = drift_num_neg
            else:
                self.change_y = .1

            # print(self.change_y)

        elif sprite.heading['curr'] == 2:
            if near_wall_list[1] == 0:
                self.change_x = drift_num_pos
            elif near_wall_list[3] == 0:
                self.change_x = drift_num_neg
            else:
                self.change_x = .1

        elif sprite.heading['curr'] == 3:
            if near_wall_list[1] == 0:
                self.change_y = drift_num_neg
            elif near_wall_list[2] == 0:
                self.change_y = drift_num_pos
            else:
                self.change_y = .1


        # return sprite.set_course((change_x,change_y))




    