import random
import os
import sys
import pygame
import json

with open("resources/progress.json", "r") as f:
    letter_weights = json.load(f)


class Button():
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.click = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def clicked(self, mouse_pos, event_list): #mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos) and self.click == False:
            for event in event_list:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return True
            

class LevelMaker():
    def __init__(self, keystrokes: int):
        self.keystrokes = keystrokes

    def make_level(self):
        keys = random.choices(list(letter_weights.keys()), weights=list(letter_weights.values()), k=self.keystrokes)
        return keys
    

class Player():
    def __init__(self, player_frames, screen):
        self.player_frames = player_frames
        self.screen = screen
        self.frame = 0

    def draw(self, x, y):
        frame_to_use = self.player_frames[self.frame]
        player_rect = frame_to_use.get_rect(center=(x, y))
        self.screen.blit(frame_to_use, player_rect)

    def update_frame(self):
        if self.frame == 2:
            self.frame = 0
        self.frame += 1


class TypeGame():
    def __init__(self):
        pygame.init()
        self.game_progress = 0
        self.player_y = 488
        self.game_keys = []
        self.game_started = 0
        self.difficulty = 0
        self.score = 0
        self.screen = pygame.display.set_mode((1080, 600))
        pygame.display.set_caption("TypeClimber")
        self.restart_button = Button(540, 390, "resources/assets/restart.png")
        img_1 = pygame.image.load("resources/assets/anim1.png")
        img_2 = pygame.image.load("resources/assets/anim2.png")
        img_3 = pygame.image.load("resources/assets/anim3.png")
        self.player = Player([img_1, img_2, img_3], self.screen)
        self.bg = pygame.image.load("resources/assets/bg.png")
        self.building = pygame.image.load("resources/assets/building1.png")
        self.easy_button = Button(540, 220, "resources/assets/easy.png")
        self.medium_button = Button(540, 300, "resources/assets/medium.png")
        self.hard_button = Button(540, 380, "resources/assets/hard.png")
        self.board_img = pygame.image.load("resources/assets/board.png")
        self.clock = pygame.time.Clock()
        self.base_font = pygame.font.Font(None, 40)
        self.font = pygame.font.Font("resources/assets/Blockhead.ttf", 40)
        self.keys_img = {}

        for file in os.scandir("resources/keys"):
            if file.name.endswith(".png"):
                name = file.name.split(".png")[0]
                if name == "forwardslash":
                    name = "/"
                self.keys_img[name] = pygame.image.load(file.path)

        self.gamestate = "pre_game"
        self.star_1 = pygame.image.load("resources/assets/star1.png")
        self.star_2 = pygame.image.load("resources/assets/star2.png")
        self.star_3 = pygame.image.load("resources/assets/star3.png")
        
        self.mainloop()
        
    def pre_game(self, event_list):
        self.screen.blit(self.bg, (0,0))
        welcome_surface = self.font.render("WELCOME BACK!",  True, (247, 255, 94))
        welcome_rect = welcome_surface.get_rect(center=(540, 125))
        main_surface = self.font.render("Select Difficulty Level",  True, (247, 255, 94))
        main_rect = main_surface.get_rect(center=(540, 160))
        self.screen.blit(welcome_surface, welcome_rect)
        self.screen.blit(main_surface, main_rect)
        self.easy_button.draw(self.screen)
        self.medium_button.draw(self.screen)
        self.hard_button.draw(self.screen)
        mouse_pos = pygame.mouse.get_pos()
        self.player.frame = 0
        self.player_y = 468
        self.score = 0
        if self.easy_button.clicked(mouse_pos, event_list):
            self.difficulty = 50
            self.up_velocity = 9
            self.game_started = pygame.time.get_ticks()
            self.game_progress = 0
            self.gamestate = "start_game"
            self.level_maker = LevelMaker(self.difficulty)
            self.game_keys = self.level_maker.make_level()
            print(self.game_keys)
        if self.medium_button.clicked(mouse_pos, event_list):
            self.difficulty = 100
            self.up_velocity = 4.5
            self.game_started = pygame.time.get_ticks()
            self.game_progress = 0
            self.gamestate = "start_game"
            self.level_maker = LevelMaker(self.difficulty)
            self.game_keys = self.level_maker.make_level()
        if self.hard_button.clicked(mouse_pos, event_list):
            self.difficulty = 150
            self.up_velocity = 2.9
            self.game_started = pygame.time.get_ticks()
            self.game_progress = 0
            self.gamestate = "start_game"
            self.level_maker = LevelMaker(self.difficulty)
            self.game_keys = self.level_maker.make_level()
    
    def start_game(self, event_list):
        current_time = pygame.time.get_ticks()
        self.screen.blit(self.bg, (0,0))
        self.screen.blit(self.building, (465,22))
        if self.game_progress >= self.difficulty:
            self.gamestate = "end_game"
            return 0
        if (current_time - self.game_started)/1000 >= 60:
            self.gamestate = "end_game"
            return 0
        #timer
        time_left = int(60-(current_time-self.game_started)/1000)
        time_left = str(time_left).zfill(2)
        self.screen.blit(self.board_img, (984,0))
        time_surface = self.base_font.render(time_left,  True, (247, 255, 94))
        time_rect = time_surface.get_rect(center=(1032, 32))
        self.screen.blit(time_surface, time_rect)
        self.screen.blit(
            self.keys_img[self.game_keys[self.game_progress]], (490, 300))
        self.player.draw(450, self.player_y)
        for event in event_list:
            if event.type == pygame.KEYDOWN:
                self.player_y -= self.up_velocity
                self.player.update_frame()
                if self.game_keys[self.game_progress] == event.unicode.lower():
                    num = letter_weights[self.game_keys[self.game_progress]]
                    if letter_weights[self.game_keys[self.game_progress]] > 0.4:
                        letter_weights[self.game_keys[self.game_progress]] = round(num-0.4, 1)
                    self.score += 1
                else:
                    letter_weights[self.game_keys[self.game_progress]] += 0.4
                self.game_progress += 1
    
    def end_game(self, event_list):
        mouse_pos = pygame.mouse.get_pos()
        self.screen.blit(self.bg, (0,0))
        if (self.score/self.difficulty) < 0.5:
            self.screen.blit(self.star_1, (340, 50))
        elif (self.score/self.difficulty) < 0.95:
            self.screen.blit(self.star_2, (340, 50))
        else:
            self.screen.blit(self.star_3, (340, 50))
        self.restart_button.draw(self.screen)

        if self.restart_button.clicked(mouse_pos=mouse_pos, event_list=event_list):
            self.gamestate = "pre_game"
            return 0
        
    def mainloop(self):
        while True:
            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
                    with open("resources/progress.json", "w") as f:
                        json.dump(letter_weights, f)
                    pygame.quit()
                    sys.exit()
            
            if self.gamestate == "pre_game":
                self.pre_game(event_list)
            elif self.gamestate == "start_game":
                self.start_game(event_list)
            elif self.gamestate == "end_game":
                self.end_game(event_list)
            pygame.display.update()
            self.clock.tick(120)

if __name__ == "__main__":
    game = TypeGame()
