from PIL import Image,ImageDraw, ImageFont, ImageColor
from rembg import remove

def make_background_transparent(image_path):
    input = Image.open(image_path)
    output = remove(input)
    return output

def compile(logo_path, bg_path, product_path, copy):

    img1 = Image.open(bg_path) 
    img1 = img1.resize((1024, 600))
    img2 = make_background_transparent(product_path)
    logo = make_background_transparent(logo_path)
    logo = logo.resize((100, 100))
    img2 = img2.convert("RGBA")
    img2 = img2.resize((400, 400))
    w1, h1 = img1.size
    w2, h2 = img2.size
    
    img1.paste(img2, ((3 * w1 // 4) - (w2//2), (h1 // 2) - (h2//2)), mask=img2)  
    img1.paste(logo, (50,50), mask=logo)
    
    draw = ImageDraw.Draw(img1)
    font = ImageFont.truetype('./JosefinSans-Bold.ttf', 45)
    draw.text((50, 400), copy, font=font, fill='white')
    
    img1.show()
    img1.save("output.png")
