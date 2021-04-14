from quest.game import QuestGame
from quest.map import TiledMap
from quest.dialogue import Dialogue
from quest.modal import Modal, DialogueModal
from quest.sprite import QuestSprite, Player, Wall, NPC, Background
from quest.helpers import scale, resolve_resource_path
from quest.strategy import RandomWalk, Strategy
from quest.contrib.maze_walk_strategy import MazeWalkStrategy
from racing_strategy import RaceStrategy
import arcade
import os
from pathlib import Path
from arcade import Point

class RacingGame(QuestGame):

    player_sprite_image = resolve_resource_path("images/boy_simple.png")
    screen_width = 800
    screen_height = 480
    screen_title = "Grandma Racer"
    # left_viewport_margin = 96                            
    # right_viewport_margin = 96
    # bottom_viewport_margin = 96
    # top_viewport_margin = 96
    player_initial_x = 150
    player_initial_y = 140
    player_speed = 3

    def __init__(self):
        super().__init__()
  
        self.items = []
        self.game_over = False
        self.player_initial_y
        self.game_winner = None

    def setup_maps(self):
        """Sets up the standard island map.
        """
        super().setup_maps()
        sprite_classes = {
            "Obstacles": Wall,
            "Playable": Background,
            "Finish" : Finish
        }
        self.add_map(TiledMap(resolve_resource_path("images/racing/racing_map.tmx"), sprite_classes))

    def setup_walls(self):
        """As in other examples, assigns all sprites in the "Obstacles" layer to be walls.
        """
        self.wall_list = self.get_current_map().get_layer_by_name("Obstacles").sprite_list

    def setup_npcs(self):
        """Assigns `self.npc_list` to be all the sprites in the map's "loot" layer.
        """

        self.npc_list = self.get_current_map().get_layer_by_name("Finish").sprite_list

        npc_data = [
            [Grandma, "images/people/grandma.png", 2, 250, 50],
            [PowerUp, "images/items/carrots.png", 1, 500, 140],
            [PowerUp, "images/items/tomatos.png", 1, 650, 240],
            [SlowDown, "images/items/coin.png", .1, 430, 375]
        ]

        for sprite_class, image, scale, x, y in npc_data:
            sprite = sprite_class(resolve_resource_path(image), scale)
            sprite.center_x = x
            sprite.center_y = y
            self.npc_list.append(sprite)

        self.setup_physics_engine()


        grandma = self.npc_list[4]
        walk = RaceStrategy()
        # walk = Strategy() 
        grandma.strategy = walk

 
    def update_viewport(self):
        """Prevents viewport from moving relative to player
        """
        

    def message(self):
        """Returns a string 
        """
        ### FIX THIS PLZ
        if self.game_over:
            self.game_over_screen()
            return "{} won!".format(self.game_winner)

    def change_speed(self,num):
        """ Changes player speed
        """
        # print(self.player_speed)
        #changes speed of player
        self.player.speed = self.player.speed + num
        print(self.player_speed)

    def game_over_screen(self):
        """ Draws game over screen and displays winner. 
        """
        arcade.set_background_color(arcade.csscolor.SKY_BLUE)
        arcade.start_render()
        # arcade.finish_render()
    
       
class Finish(NPC):
    """Loot is a NPC which shows up in the game as a star. Its only job is to
    get collected by the player.
    """

    repel_distance = 1

    def on_collision(self, sprite, game):
        """When the player collides with a Loot, it calls :py:meth:`quest.maze.MazeMap.on_loot_collected` to tell
        the game to make needed updates. Then the Loot kills itself.
        """

        if self.reverse_check(sprite):
            self.repel(sprite)

        if game.game_over == False and not self.reverse_check(sprite):
            game.npc_list[0].speed = 0

            if sprite in game.npc_list:
                game.game_winner = 'Grandma'
            else:
                game.game_winner = 'Player'
            
            print ("{} won!".format(game.game_winner))

            game.game_over = True
            game.running = False
        

    def reverse_check(self,sprite):
        return (sprite.center_y+10 < self.center_y)

    def repel(self, sprite):
        "Backs the sprite away from self"
        away = (self.center_x - sprite.center_x, self.center_y - sprite.center_y)
        away_x, away_y = scale(away, self.repel_distance)
        sprite.center_x = sprite.center_x - away_x
        sprite.center_y = sprite.center_y - away_y
        sprite.stop()


        

class Grandma(NPC):
    """Grandma is an NPC. 

    Attributes:
        repel_distance: How far back the player should be pushed after colliding
            with Grandma. This is necessary because otherwise when the dialogue modal 
            closed, it would immediately reopen. Grandma is interesting, but not that 
            interesting.
    """
    repel_distance = 1
    speed = 3
    heading = {'curr': 1, 'prev': None,'list': [0,1,2,3]}
    hit_box_radius = 20


    def near_wall(self,game,distance):
        """
        Creates a matrix of if walls are within a certain distance.
        """

        near_wall_list = []

        
        near_wall_list.append(len(
            arcade.get_sprites_at_point([self.center_x,self.center_y+distance],game.wall_list)))
        near_wall_list.append(len(
            arcade.get_sprites_at_point([self.center_x+distance,self.center_y],game.wall_list)))
        near_wall_list.append(len(
            arcade.get_sprites_at_point([self.center_x,self.center_y-distance],game.wall_list)))
        near_wall_list.append(len(
            arcade.get_sprites_at_point([self.center_x-distance,self.center_y],game.wall_list)))
        
        return near_wall_list    

            


    def on_collision(self, sprite, game):
        """When the player collides with a Loot, it calls :py:meth:`quest.maze.MazeMap.on_loot_collected` to tell
        the game to make needed updates. Then the Loot kills itself.
        """

        if sprite == game.player:
            self.repel(sprite)  


    def repel(self, sprite):
        "Backs the sprite away from self"
        away = (self.center_x - sprite.center_x, self.center_y - sprite.center_y)
        away_x, away_y = scale(away, self.repel_distance)
        sprite.center_x = sprite.center_x - away_x
        sprite.center_y = sprite.center_y - away_y
        sprite.stop()

    def change_speed(self,new_speed):
        self.speed += new_speed


class PowerUp(NPC):
    """A PowerUp NPC that can be picked up resulting in faster speed. 
    """
    description = "item"

    def on_collision(self, sprite, game):
        """When the player collides with a PowerUp, it tells the game to speed up the specific sprite and then 
        kills itself.
        """
 
        
        if sprite == game.player:
            game.change_speed(2)

        elif sprite in game.npc_list:
            sprite.change_speed(2)
        self.kill()
       

class SlowDown(NPC):
    """A PowerUp NPC that can be picked up resulting in faster speed. 
    """
    description = "item"

    def on_collision(self, sprite, game):
        """When the player collides with a PowerUp, it tells the game to speed up the specific sprite and then 
        kills itself.
        """
 
        
        if sprite == game.player:
            game.change_speed(-3)

        elif sprite in game.npc_list:
            sprite.change_speed(-2)
        self.kill()
       

       
        
if __name__ == '__main__':
    game = RacingGame()
    game.run()