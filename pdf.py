from wand.image import Image
from wand.color import Color

i=0
with Image(filename="postprocessing.pdf", resolution=300) as img:
    for seq in img.sequence:
        with Image(width=seq.width, height=seq.height, background=Color("white")) as bg:
            bg.composite(seq,0,0)
            bg.save(filename="sap"+str(i)+".png")
        i += 1