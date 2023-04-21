import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.colors import ListedColormap
import noise

def generate_map():
    width = width_var.get()
    height = height_var.get()
    scale = 100.0
    octaves = 6
    persistence = 0.5
    lacunarity = 2.0
    base_frequency = continents_var.get() * frequency_multiplier_var.get()

    world_map = np.zeros((height, width))
    for i in range(height):
        for j in range(width):
            world_map[i][j] = noise.pnoise2(i / scale * base_frequency,
                                            j / scale * base_frequency,
                                            octaves=octaves,
                                            persistence=persistence,
                                            lacunarity=lacunarity,
                                            repeatx=1024,
                                            repeaty=1024,
                                            base=42)

    sea_level = 0
    colors = np.zeros(world_map.shape)
    colors[world_map <= sea_level] = 0  # 海洋
    colors[world_map > sea_level] = 1  # 陆地

    fig.clear()
    ax = fig.add_subplot(111)
    cmap = ListedColormap(['blue', 'green'])
    ax.imshow(colors, cmap=cmap)
    canvas.draw()

root = tk.Tk()
root.title("随机地图生成器")

main_frame = ttk.Frame(root, padding="10")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

width_label = ttk.Label(main_frame, text="地图宽度：")
width_label.grid(row=0, column=0, sticky=tk.W)
width_var = tk.IntVar()
width_var.set(100)
width_entry = ttk.Entry(main_frame, textvariable=width_var)
width_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))

height_label = ttk.Label(main_frame, text="地图高度：")
height_label.grid(row=1, column=0, sticky=tk.W)
height_var = tk.IntVar()
height_var.set(100)
height_entry = ttk.Entry(main_frame, textvariable=height_var)
height_entry.grid(row=1, column=1, sticky=(tk.W, tk.E))

continents_label = ttk.Label(main_frame, text="大陆数量：")
continents_label.grid(row=2, column=0, sticky=tk.W)
continents_var = tk.DoubleVar()
continents_var.set(1)
continents_entry = ttk.Entry(main_frame, textvariable=continents_var)
continents_entry.grid(row=2, column=1, sticky=(tk.W, tk.E))

frequency_multiplier_label = ttk.Label(main_frame, text="基本频率倍数：")
frequency_multiplier_label.grid(row=3, column=0, sticky=tk.W)
frequency_multiplier_var = tk.DoubleVar()
frequency_multiplier_var.set(1)
frequency_multiplier_entry = ttk.Entry(main_frame, textvariable=frequency_multiplier_var)
frequency_multiplier_entry.grid(row=3, column=1, sticky=(tk.W, tk.E))

generate_button = ttk.Button(main_frame, text="生成地图", command=generate_map)
generate_button.grid(row=4, columnspan=2)

fig = plt.figure()
canvas = FigureCanvasTkAgg(fig, main_frame)
canvas.get_tk_widget().grid(row=5, column=0, columnspan=2)

root.mainloop()
