def goAnimations(communication_line):
	from os import name
	from sys import exit
	from time import sleep, time

	import tkinter as tk

	from PIL import ImageTk, Image
	from screeninfo import get_monitors

	from airportAgent_functions import cache_clearer

	# start fresh
	cache_clearer()

	# Explore screen's resolution
	windowinfo = get_monitors()
	w = windowinfo[0].width
	h = windowinfo[0].height





	# Read from settings.txt
	with open("docs/settings.txt", "r") as f:
		settings = [i.rstrip() for i in f.readlines()]
		# Set Settings
		fullscreen =  int(settings[1].split(" = ")[-1])
		go_to_monitor_index_of = int(settings[2].split(" = ")[-1])
		rotation_speed = float(settings[3].split(" = ")[-1])
		spinning_animation = int(settings[4].split(" = ")[-1])
		speaking_animations = int(settings[5].split(" = ")[-1])
		animaton_size = [int(i) for i in settings[6].split(" = ")[-1].lower().split("x")]
		animation_popBackAndForth = int(settings[8].split(" = ")[-1])
		animation_goBackAndForth = int(settings[15].split(" = ")[-1])
	class SimpleApp():
		bg_color = "white"
		img_pos = 0
		imgGoUp = True
		imgs_folder = "animations"

		def __init__(self, master, w, h):
			self.master = master
			self.master["bg"] = "white"
			self.master.title('Airport Agent')
			self.canvas = tk.Canvas(master, width=w, height=h,
									highlightthickness=0)
			self.canvas["bg"] = "white"
			self.canvas.pack()
			self.update = self.draw().__next__
			master.after(1000, self.update)

		def draw(self):
			angle = 0
			size = 1

			while True:
				try:
					if speaking_animations:
						state = communication_line.value.decode()
						if state[0] == '1':
							size = (1.04 if animation_popBackAndForth else 1)
							# When the agent speaks, go from current point to 170 then to 8
							if SimpleApp.img_pos < 24:
								SimpleApp.img_pos += (1 if SimpleApp.imgGoUp else -1)
							elif SimpleApp.img_pos >= 24:
								SimpleApp.img_pos += (1 if SimpleApp.imgGoUp else -1)
							if animation_goBackAndForth:
								if SimpleApp.img_pos > 24:
									SimpleApp.imgGoUp = False
								elif SimpleApp.img_pos < 8:
									SimpleApp.imgGoUp = True
							sleep(0.01)
						# Stay at 0 when idle
						else:
							size = 1
							if SimpleApp.img_pos >= 2:
								SimpleApp.img_pos += -2
								SimpleApp.imgGoUp = True
						# Check if color spitted in the comm. channel
						if "go_white" in state:
							SimpleApp.imgs_folder = "animations"
							self.master["bg"] = "white"
							self.canvas["bg"] = "white"

						elif "go_red" in state:
							SimpleApp.imgs_folder = "animations_red"
							SimpleApp.bg_color = "red"
							self.master["bg"] = "red"
							self.canvas["bg"] = "red"
					image = Image.open(f"docs/{SimpleApp.imgs_folder}/{SimpleApp.img_pos}.png")
					image = image.resize((int(animaton_size[0] * size), int(animaton_size[-1] * size)))
					tkimage = ImageTk.PhotoImage(image.rotate(angle, fillcolor=((255, 0, 0, 255) if SimpleApp.bg_color == "red" else (255, 255, 255, 255))))
					canvas_obj = self.canvas.create_image(
					    int(w/2), int(h/2), image=tkimage)
					self.master.after_idle(self.update)
					yield
					self.canvas.delete(canvas_obj)
					if spinning_animation:
						angle += rotation_speed
						angle %= 360
				except FileNotFoundError:
					pass
				except Exception as e:
					print(e)

	root = tk.Tk()
	root.config(cursor="none")

	# On top of everything
	if fullscreen:
		# Linux
		if name != "nt":
			root.wm_attributes('-type', 'splash')
		# Windows
		else:
			root.overrideredirect(1)



	# To the extended screen
	if go_to_monitor_index_of > -1:
		root.geometry(f"%dx%d+%d+0" % (int(get_monitors()[go_to_monitor_index_of].width), h, int(get_monitors()[go_to_monitor_index_of].x)))
	else:
		root.geometry("%dx%d+0+0" % (w, h))

	try:
		app = SimpleApp(root, w, h)
		root.mainloop()
	except StopIteration:
		pass
	except Exception as e:
		print(e)



def main():
    # Check if the dependencies are installed
	from error_checker import check_for_dependencies

	if check_for_dependencies():
		import ctypes
		import multiprocessing
		from os import getpid

		from agent import goAirportAgent

		communication_line = multiprocessing.Array(ctypes.c_char, b"0"*20)
		communication_line.value = b"0"

		agent = multiprocessing.Process(target=goAirportAgent, args=(getpid(), communication_line))
		agent.start()
		goAnimations(communication_line)
	else:
		print("Errors found. Please refer to the error_checker.py script for further details.")


if __name__ == "__main__":
    main()
