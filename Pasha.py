from superwires import games, color
import pygame
import random

games.init(screen_width=850, screen_height=750, fps=50)
pygame.display.set_caption('Сумасшедший Павлундий')

class Pan(games.Sprite):
	"""Сковорода в которую игрок будет ловить падающую пиццу"""

	image = games.load_image("pan.bmp")

	def __init__(self):
		"""Инициализирует объект класса Pan и создает объект Text для отображения счета"""

		super(Pan, self).__init__(image=Pan.image,
		                          x=games.mouse.x,
		                          bottom=games.screen.height,)
		self.score = games.Text(value=0, size=40, color=color.purple,
		                        top=5, right=games.screen.width-10)
		games.screen.add(self.score)

	def update(self):
		"""Передвигает точку по горизонтали в точку с абциссой, как у указателя мыши"""
		self.x = games.mouse.x
		if self.left < 0:
			self.left = 0
		if self.right > games.screen.width:
			self.right = games.screen.width
		self.check_catch()

	def check_catch(self):
		"""Проверяет, поймал ли игрок летящую пиццу"""
		for pizza in self.overlapping_sprites:
			self.score.value += 10
			self.score.right = games.screen.width - 10
			pizza.handle_caught()

class Pizza(games.Sprite):
	"""Круги пиццы падающие на землю"""

	image = games.load_image("pizza.bmp")
	speed = 4

	def __init__(self, x, y=90):
		"""Инициализирует объект Pizza"""
		super(Pizza, self).__init__(image=Pizza.image,
		                            x=x,y=y,
		                            dy=Pizza.speed)

	def update(self):
		"""Проверяет упала ли пицца на землю"""
		if self.bottom > games.screen.height:
			self.end_game()
			self.destroy()


	def handle_caught(self):
		"""Разрушает объект пойманый игроком"""
		self.destroy()

	def end_game(self):
		"""Завершает игру"""
		end_message = games.Message(value="Конец игры",
		                            size=90,
		                            color=color.dark_red,
		                            x=games.screen.width/2,
		                            y=games.screen.height/2,
		                            lifetime=5*games.screen.fps,
		                            after_death=games.screen.quit)
		games.screen.add(end_message)

class Chief(games.Sprite):
	"""Обезумевший Паша, который разбрасывает пиццу"""
	image=games.load_image("Pasha.png")

	def __init__(self, y=55, speed=2, ods_change=200):
		super(Chief, self).__init__(image=Chief.image,
		                            x=games.screen.width/2,
		                            y=y,
		                            dx=speed)
		self.ods_change=ods_change
		self.time_til_drop = 0

	def update(self):
		"""Определите надо ли сменить направление"""
		if self.left < 0 or self.right > games.screen.width:
			self.dx = -self.dx
		elif random.randrange(self.ods_change) == 0:
			self.dx = -self.dx
		self.check_drop()

	def check_drop(self):
		"""Уменьшает интервал ожидания на секунду или сбрасывает очередную пиццу
		и восстанавливает интервал ожидания"""
		if self.time_til_drop > 0:
			self.time_til_drop -= 1
		else:
			new_pizza = Pizza(x=self.x)
			games.screen.add(new_pizza)
		# Зазор между падающими кругами пиццы равен 30%
			self.time_til_drop = int(new_pizza.height*1.3/Pizza.speed)+1

def main():
	"""Непосредственно игровой прлцесс"""
	wall_img = games.load_image("gameWall.jpeg", transparent=False)
	games.screen.background = wall_img
	the_chief = Chief()
	games.screen.add(the_chief)
	the_pan = Pan()
	games.screen.add(the_pan)
	games.mouse.is_visible = False
	games.screen.event_grab = True
	games.screen.mainloop()

# Погнали!
main()






















