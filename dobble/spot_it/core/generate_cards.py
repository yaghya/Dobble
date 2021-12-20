from math import exp
import sys,os

sys.path.append("./")
from spot_it.utils.svg2png import convert_svg2png
from spot_it.core.dobble import dobble_pipeline

def save_image_names(img_file_path,expt_no,output_dir):
    file1 = open(img_file_path,'r+')
    path = os.path.join(output_dir,expt_no)
    if not os.path.isdir(path):
        os.makedirs(path)
    output_file = open(os.path.join(path,'image_names.txt'),'w')
    for line in file1.readlines():
        image_name = line.split('/')[-1].split('.png')[0]
        output_file.write(f"{image_name}\n")

if __name__ == "__main__":
    img_file_path = "./data/image_names.txt"
    order = 7
    expt_no = "1"
    output_dir = './generated'
    save_image_names(img_file_path,expt_no,output_dir)
    pipeline = dobble_pipeline(order,img_file_path,output_dir,expt_no)
    pipeline.create_cards()
    convert_svg2png(output_dir,expt_no)
    print("cards_created",expt_no)