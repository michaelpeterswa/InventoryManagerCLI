import emoji
import argparse
import json
import os 
import binascii

from qrcodegen import QrCode
from cairosvg import svg2png
from PIL import Image, ImageDraw, ImageFont

def generateRandomID():
    idnum = str(binascii.b2a_hex(os.urandom(2)))
    return idnum[2:6]

def createAndSaveQRCode(contents, identifier, output):
    qr0 = QrCode.encode_text(contents, QrCode.Ecc.MEDIUM)
    svg = qr0.to_svg_str(4)
    svg2png(bytestring=svg,write_to=output,scale=6.0)

def createAndSaveTag(pathToImage, output, identifier):
    # pylint: disable=unused-variable 
    # (fix for unused width and height vars)
    img = Image.open(pathToImage, 'r')
    img = img.resize((175, 175), Image.BICUBIC)
    img_w, img_h = img.size
    background = Image.new('RGBA', (400, 200), (255, 255, 255, 255))
    bg_w, bg_h = background.size
    offset = (25, (bg_h - img_h) // 2)
    background.paste(img, offset)
    logo = Image.open("resources/logo.png", 'r')
    logo = logo.resize((125,125), Image.BICUBIC)
    logo_w, logo_h = logo.size
    background.alpha_composite(logo, (250, 15))
    fnt = ImageFont.truetype('resources/FiraCode-Regular.ttf', 20)
    txt = Image.new('RGBA', background.size, (255,255,255,0))
    d = ImageDraw.Draw(txt)
    label = "Identity: " + identifier
    d.text((200,120), label, font=fnt, fill=(0,0,0,255))
    out = Image.alpha_composite(background, txt)
    out.save(output)

def addEmoji(str):
    return emoji.emojize(str, use_aliases=True)

def main():
    title = ":evergreen_tree: Inventory v1.0 :evergreen_tree:"

    parser = argparse.ArgumentParser()
    addOrDelete = parser.add_mutually_exclusive_group()
    addOrDelete.add_argument("--add")
    addOrDelete.add_argument("--delete")
    parser.add_argument("--create", action='store_true')
    parser.add_argument("--list", action='store_true')
    args = parser.parse_args()

    #intro v1.0
    print(addEmoji(title))

    if args.create:
        try:
            print(addEmoji(":zap: Creating Inventory File... :zap:"))
            data = {}
            data['title'] = "Inventory v1.0"
            data['items'] = []

            with open('inventory.json', 'w') as outfile:  
                json.dump(data, outfile, indent=4)
            # Do something with the file
            outfile.close()
        except FileExistsError:
            print("FileExistsError: Inventory File already exists")

    if args.delete:
        try:
            print(addEmoji(":zap: Deleting... :zap:"))
            
            with open('inventory.json', "r") as json_file:
                data = json.load(json_file)

            for idx, item in enumerate(data["items"]):
                if(item["id"]== args.delete):
                    data["items"].pop(idx)

            with open('inventory.json', "w") as json_file:
                json.dump(data, json_file, indent=4)
    
            
        except FileNotFoundError:
            print("FileNotFoundError: Inventory File not accessible")

    if args.add:
        contents = input("Please enter the contents for this item: ")
        identifier = generateRandomID()
        try:
            print(addEmoji(":zap: Adding... :zap:"))
            with open('inventory.json', "r") as json_file:
                data = json.load(json_file)
                
                data['items'].append({
                "id" : str(identifier),
                "name": str(args.add),
                "contents": str(contents)
                })
            with open('inventory.json', "w") as json_file:
                json.dump(data, json_file, indent=4)


            outputQR = "img/qr-" + identifier + ".png"
            output = "img/tag-" + identifier + ".png"
            createAndSaveQRCode(contents, identifier, outputQR)
            createAndSaveTag(outputQR, output, identifier)
    
        except FileNotFoundError:
            print("FileNotFoundError: Inventory File not accessible")

    if args.list:
        try:
            with open('inventory.json') as json_file:
                data = json.load(json_file)
                print(addEmoji(":zap: Listing... :zap:"))
                print("")
                for p in data['items']:
                    print('ID: ' + p['id'])
                    print('Name: ' + p['name'])
                    print('Contents: ' + p['contents'])
                    print('')
        except FileNotFoundError:
            print("FileNotFoundError: Inventory File not accessible")

if __name__== "__main__":
  main()
