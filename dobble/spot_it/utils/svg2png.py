#!/usr/bin/env python

from cairosvg import svg2png
from xml.dom import minidom
import os,sys
sys.path.append("./")



def convert_svg2png(output_dir,expt_no):
    dir_path = os.path.join(output_dir,expt_no)
    files_list = [f for f in os.listdir(dir_path) if '.svg' in f]

    if not os.path.isdir(f'{dir_path}_png'):
        os.makedirs(f'{dir_path}_png')

    for file in files_list:
        svg_file_path = f'{dir_path}/{file}'
        png_file_path = f'{dir_path}_png/card_{file}'.replace('.svg','.png')
        svg2png(url=svg_file_path,write_to=png_file_path)
       

# convert_svg2png('./svg')