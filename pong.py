if __name__ == "__main__":
	import pygame as pg, os, sys
	import game_objects
	from pygame.locals import *

	os.environ["SDL_VIDEO_CENTERED"] = "1"
	pg.init()

	height, width = 600, 1024

	window = pg.display.set_mode((width, height))
	pg.display.set_caption("PONG!")
	clock = pg.time.Clock()
	font = pg.font.SysFont("Consolas", 20)

	# GAME VARS

	directions = {
		"UP": False,
		"DOWN":False
	}
	score = game_objects.Score()
	player = game_objects.PlayerPaddle((width, height))
	opponent = game_objects.OpponentAi((width, height))
	ball = game_objects.Ball((width, height))
	timer = game_objects.Timer()

	while True:

		for event in pg.event.get():

			if event.type == QUIT:
				pg.quit()
				sys.exit()

			if event.type == KEYDOWN:

				if event.key == K_UP:
					directions["UP"] = True
				if event.key == K_DOWN:
					directions["DOWN"] = True

			if event.type == KEYUP:

				if event.key == K_UP:
					directions["UP"] = False
				if event.key == K_DOWN:
					directions["DOWN"] = False

		window.fill((0, 0, 0))

		timer.dt = int(pg.time.get_ticks() / 1000 - timer.start_time) + 1

		pg.draw.aaline(window, (200, 200, 200), (width / 2, height / 8), (width / 2, 7 * height / 8))
		score.draw_text(window, (width, height))
		pg.draw.rect(window, (100, 100, 100), player.paddle)
		pg.draw.rect(window, (100, 100, 100), opponent.paddle)
		pg.draw.ellipse(window, (200, 15, 15), ball.ball)
		if timer.dt <= 3:
			timer.draw_text(window, (width, height))

		player.move_paddle(directions)
		opponent.move_paddle(ball)
		if timer.dt > 3:
			ball.move_ball(player.paddle, opponent.paddle, score, timer)

		pg.display.update()
		clock.tick(60)