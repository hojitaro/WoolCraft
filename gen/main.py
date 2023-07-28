import glob
import os

import better_main_color as bmc
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np


def hex_txt(v):
    return str(hex(v).replace('0x', '').zfill(2))


def gen_texture(img_file):
    img = Image.open(img_file).convert('RGBA')
    img_data = img.getdata()
    data = [[img_data[i]] for i in range(size[0] * size[1]) if img_data[i][3] != 0]
    if len(data) == 0:
        return

    clusters = bmc.clustering(data, 0, 65536, 1)
    clusters = sorted(clusters, reverse=True, key=lambda x: len(x))

    colors = []
    for c in clusters:
        r = sum(pxl[0] for pxl in c) // len(c)
        g = sum(pxl[1] for pxl in c) // len(c)
        b = sum(pxl[2] for pxl in c) // len(c)
        colors.append([r, g, b])

    wool = Image.open('./white_wool.png').convert('RGB')
    dst = Image.new('RGBA', size)
    main_color = np.array(colors[0])
    ground = np.array((232, 235, 235))

    for i in range(size[0]):
        for j in range(size[1]):
            wool_vec = np.array(wool.getdata()[i * size[0] + j])
            dst.putpixel((j, i), tuple(main_color - (ground - wool_vec)))

    output_path = f'./output_img/adjusted/{os.path.basename(img_file)}'
    dst.save(output_path)
    print(f'finish: {output_path}')

    left = [f'#{hex_txt(co[0])}{hex_txt(co[1])}{hex_txt(co[2])}' for co in colors]
    height = [len(c) for c in clusters]
    plt.bar(left, height, color=left)
    plt.show()


size = (16, 16)

gen_texture('./src_img/cherry_log_top.png')
"""
for file in glob.glob('./src_img/*'):
    gen_texture(file)
"""