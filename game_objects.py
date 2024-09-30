import pygame as pg
from random import randint,choice

class PlayerPaddle:
    
    def __init__(self, window_width, pad_height=150, pad_width=10, movement=10):
        
        self.window_width, self.window_height = window_width
        self.movement = movement
        self.paddle = pg.Rect(self.window_width - pad_width - 3, (self.window_height / 2) - (pad_height / 2), pad_width, pad_height)
    
    def move_paddle(self, directions):
        
        if directions["UP"]:
            
            if self.paddle.top-self.movement <= 0:
                self.paddle.top = 0
            else:
                self.paddle.top -= self.movement
        
        elif directions["DOWN"]:
            
            if self.paddle.bottom + self.movement > self.window_height:
                self.paddle.bottom = self.window_height
            else:
                self.paddle.bottom += self.movement

class OpponentAi:
    
    def __init__(self, window_resolution, pad_height=150, pad_width=10, movement=7):
        
        self.window_width, self.window_height = window_resolution
        self.movement = movement
        self.paddle = pg.Rect(3, (self.window_height / 2) - (pad_height / 2), pad_width, pad_height)
    
    def move_paddle(self, ball):
        
        if ball.ball.top < self.paddle.top and ball.ball.centerx > self.paddle.right:
            
            if self.paddle.top - self.movement < 0:
                self.paddle.top = 0
            else:
                self.paddle.top -= self.movement
        
        elif ball.ball.bottom > self.paddle.bottom and ball.ball.centerx > self.paddle.right:
            
            if self.paddle.bottom + self.movement > self.window_height:
                self.paddle.bottom = self.window_height
            else:
                self.paddle.bottom += self.movement

class Ball:
    
    def __init__(self, window_resolution, ball_radius=20):
        
        self.window_width, self.window_height = window_resolution
        self.ball = pg.Rect(self.window_width / 2 - ball_radius / 2 + 1, self.window_height / 2 - ball_radius / 2 + 1, ball_radius, ball_radius)
        self.ball_movement = { "X": randint(3, 7) * choice([-1, 1]), "Y": randint(3, 7) * choice([-1, 1]) }
    
    def reset(self, player, opponent, timer):
        
        self.ball.center = (self.window_width / 2 + 1, self.window_height / 2 + 1)
        self.ball_movement = { "X": randint(3, 7)  *choice([-1, 1]), "Y": randint(3, 7) * choice([-1, 1]) }
        player.centery = self.window_height / 2
        opponent.centery = self.window_height / 2
        timer.start_time = pg.time.get_ticks() / 1000
        timer.dt = 0
    
    def move_ball(self, player, opponent, score, start_time):
        
        
        if self.ball.top < 0:
            self.ball_movement["Y"] *= -1
            self.ball.top = 0
        if self.ball.bottom > self.window_height:
            self.ball_movement["Y"] *= -1
            self.ball.bottom = self.window_height
        
        self.ball.centery += self.ball_movement["Y"]
        if self.ball.colliderect(player):
            
            if self.ball_movement["Y"] < 0:
                self.ball.top = player.bottom + 1
            if self.ball_movement["Y"] > 0:
                self.ball.bottom = player.top-1
            self.ball_movement["Y"] *= -1
        
        if self.ball.colliderect(opponent):
            if self.ball_movement['Y'] < 0:
                self.ball.top = opponent.bottom + 1
            if self.ball_movement["Y"] > 0:
                self.ball.bottom = opponent.top-1
            self.ball_movement["Y"] *= -1

        self.ball.centerx += self.ball_movement["X"]
        if self.ball.colliderect(player):
            
            if self.ball_movement["X"] > 0:
                self.ball.right = player.left - 1
            if self.ball_movement["X"] < 0:
                self.ball.left = player.right + 1

            if self.ball_movement["X"] < 0:
                self.ball_movement["X"] -= .2
            else:
                self.ball_movement["X"] += .2

            if self.ball_movement["Y"] < 0:
                self.ball_movement["Y"] -= .2
            else:
                self.ball_movement["Y"] += .2
            
            self.ball_movement["X"] *= -1
        
        if self.ball.colliderect(opponent):
            if self.ball_movement["X"] > 0:
                self.ball.right = opponent.left-1
            if self.ball_movement["X"] < 0:
                self.ball.left = opponent.right + 1

            if self.ball_movement["X"] < 0:
                self.ball_movement["X"] -= .2
            else:
                self.ball_movement["X"] += .2

            if self.ball_movement["Y"] < 0:
                self.ball_movement["Y"] -= .2
            else:
                self.ball_movement["Y"] += .2
            
            self.ball_movement["X"] *= -1

        if self.ball.centerx > player.left:
            score.score["OPPONENT"] += 1
            self.reset(player, opponent, start_time)
        if self.ball.centerx < opponent.right:
            score.score["PLAYER"] += 1
            self.reset(player,opponent,start_time)

class Score:
    
    def __init__(self):
        
        self.score = {
            "PLAYER": 0,
            "OPPONENT": 0
        }
        self.font = pg.font.SysFont("Consolas", 20)
    
    def draw_text(self, window, window_resolution):
        
        width,height = window_resolution
        player_score_to_txt = str(self.score["PLAYER"])
        opponent_score_to_txt = str(self.score["OPPONENT"])
        player_score_txt_width = self.font.size(player_score_to_txt)[0]
        opponent_score_txt_width = self.font.size(opponent_score_to_txt)[0]
        player_score_txt_surface = self.font.render(f"{player_score_to_txt}", True, (200, 200, 200))
        opponent_score_txt_surface = self.font.render(f"{opponent_score_to_txt}", True, (200, 200, 200))
        window.blit(player_score_txt_surface, (3 * width / 4 + 5, height / 2 - 8))
        window.blit(opponent_score_txt_surface, (width / 4 - 5 - opponent_score_txt_width, height / 2 - 8))

class Timer:
    
    def __init__(self):
        
        self.start_time = pg.time.get_ticks() / 1000
        self.dt = None
        self.font = pg.font.SysFont("Consolas", 60)

    def draw_text(self, window, window_resolution):
        
        width, height = window_resolution
        timer_txt = str(abs(self.dt - 4))
        timer_txt_surface = self.font.render(f"{timer_txt}", True,(30, 50, 180))
        timer_txt_width, timer_txt_height = self.font.size(timer_txt)
        window.blit(timer_txt_surface, (width / 2 - timer_txt_width / 2, height / 15 - timer_txt_height / 2))
