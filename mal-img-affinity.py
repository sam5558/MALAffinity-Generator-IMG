#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import os
import sys
import json
import time
from decimal import DecimalException

import objectpath
from collections import OrderedDict

from jikanpy import Jikan
from aniffinity import Aniffinity
from aniffinity.exceptions import RateLimitExceededError, AniffinityException, NoAffinityError, InvalidUserError
from tabulate import tabulate

# datetime object containing current date and time
now = datetime.now()

print("now =", now)
# dd/mm/YY H:M:S
dt_string = now.strftime("%d/%m/%Y %H:%M")


# get username from command line
if len(sys.argv) <= 1:
    print("I expected a username but you didn't give me one!")
    print('Example: python3 anifinity.py "Guts__"')
    sys.exit(1)

username = sys.argv[1].strip()

if len(sys.argv) <= 2:
    usr = username
else:
    usr = sys.argv[2].strip()

jikan = Jikan()

print("Downloading your friends from MyAnimeList...")
# friends info
ufriends = jikan.user(username=usr, request='friends')

print("Downloaded {} friends".format(len(ufriends["friends"])))

# Download the users myanimelist
print("Downloading {}'s animelist...".format(username))
af = Aniffinity(username, base_service="MyAnimeList", wait_time=2)

# e.g. results = {"some_user": affinity_val}
results = {}

# create a list of friend names
friend_names = [f["username"] for f in ufriends["friends"]]

newresult = OrderedDict([('LegendOrrin', 71.93), ('AbuelitaDeBatman', 66.29), ('LouysP', 64.02), ('PafDesChocapiks', 62.21), ('Japy', 60.24), ('KAIKI-DESU', 59.29), ('Hydroman_', 59.22), ('S-cryed', 58.88), ('Blastof_', 58.88), ('bshak', 58.21), ('Daante_', 57.79), ('Taikuhatsu', 56.7), ('Iiiik', 55.69), ('mcd_78', 55.41), ('Tenshibana', 54.86), ('Ruqaa', 54.54), ('KiSsxShoT', 54.51), ('HaarWyvern', 54.02), ('tristan-h', 52.99), ('anaesan', 52.53), ('Naou_', 51.78), ('Iwolf441', 51.58), ('21stCenturyBoy_', 51.25), ('Souba', 50.9), ('Faith_Navii', 50.64), ('K0NAMI', 50.29), ('Kreya29', 50.03), ('6lk6', 49.65), ('itsNotMark', 48.23), ('Sakutarou', 47.68), ('Loleyke', 47.55), ('Noodle_June', 47.06), ('TuyNOM', 46.96), ('YelloWCl3ar', 46.85), ('ImRenaud', 46.79), ('ezkeeks', 46.71), ('Davide_Chikone', 46.32), ('JojoYabuki', 46.25), ('DatRandomDude', 46.24), ('Anime-ETF', 46.11), ('HaremOverlord', 45.97), ('Afloo', 45.64), ('darkneff', 44.98), ('arthuurop', 44.68), ('Railingue', 44.33), ('DracGaki', 44.1), ('Zetsubo22', 43.19), ('KingDespe', 43.17), ('Laraxs', 42.95), ('GamesRet', 42.7), ('Azuki-ojou', 42.14), ('Vizioz', 41.78), ('BenjaminJunior', 41.4), ('paraparaship', 40.38), ('Mangamer', 40.14), ('FaliaS', 39.37), ('Kami_yar0', 39.07), ('Djidji', 38.86), ('Benku', 38.81), ('Aniki91', 38.65), ('-Nadrel-', 38.46), ('Shiratoria', 37.71), ('Charlotte1412', 37.62), ('Sifedo', 37.51), ('Azdo0m', 37.23), ('spacecowboy', 37.07), ('ProfZex', 36.99), ('FanTaine', 36.77), ('Sreyso', 34.88), ('Juliiiiiiiiiiius', 34.76), ('LupinYabuki', 33.78), ('Hydraxsfull', 33.65), ('Saeba_Ryou', 32.58), ('Jakedax', 32.19), ('BlackTeaLady', 31.9), ('pr4ty', 31.12), ('bAbyLoNE', 30.83), ('drakoneel', 29.83), ('infinico', 29.75), ('Matism', 29.19), ('rek94', 28.91), ('Laeweth', 28.52), ('Ha0', 28.14), ('Chifie', 27.15), ('Henatsuka', 25.29), ('cynic15m', 21.41), ('Apichua', 20.85), ('Ahmed_paint5', 20.09), ('Ragnos055', 17.88), ('Radukaii', 17.31), ('_r_Felipe', 15.19), ('ProxyLain', 14.77), ('TopherC17', 13.03), ('Korsa-', 12.23), ('QuentiNeicigam', 8.76)])

# create Image object with the input image
image = Image.open('top-friends.png').convert('RGB')

# initialise the drawing context with
# the image object as background
draw = ImageDraw.Draw(image)


# create font object with the font file and specify
# desired size

font = ImageFont.truetype('Roboto-Bold.ttf', size=45)
updatefont = ImageFont.truetype('Roboto-Bold.ttf', size=30)

# starting position of the message

(x, y) = (50, 50)
message = "TOP 10 MyAnimeList Friends"
color = 'rgb(47,82,162)' # black color
draw.text((x, y), message, fill=color, font=font)

(x, y) = (50, 850)
lasttime = "last updated : " + dt_string
color = 'rgb(224,224,224)'
draw.text((x, y), lasttime, fill=color, font=updatefont)

# draw the message on the background

name0 = str([v for v in newresult.items()][0][0])
val0 = str([v for v in newresult.items()][0][1])+"%"
name1 = str([v for v in newresult.items()][1][0])
val1 = str([v for v in newresult.items()][1][1])+"%"
name2 = str([v for v in newresult.items()][2][0])
val2 = str([v for v in newresult.items()][2][1])+"%"
name3 = str([v for v in newresult.items()][3][0])
val3 = str([v for v in newresult.items()][3][1])+"%"
name4 = str([v for v in newresult.items()][4][0])
val4 = str([v for v in newresult.items()][4][1])+"%"
name5 = str([v for v in newresult.items()][5][0])
val5 = str([v for v in newresult.items()][5][1])+"%"
name6 = str([v for v in newresult.items()][6][0])
val6 = str([v for v in newresult.items()][6][1])+"%"
name7 = str([v for v in newresult.items()][7][0])
val7 = str([v for v in newresult.items()][7][1])+"%"
name8 = str([v for v in newresult.items()][8][0])
val8 = str([v for v in newresult.items()][8][1])+"%"
name9 = str([v for v in newresult.items()][9][0])
val9 = str([v for v in newresult.items()][9][1])+"%"

color = 'rgb(255, 255, 255)' # white color
(x, y) = (150, 150)
draw.text((x, y), name0, fill=color, font=font)
(x, y) = (150, 200)
draw.text((x, y), name1, fill=color, font=font)
(x, y) = (150, 250)
draw.text((x, y), name2, fill=color, font=font)
(x, y) = (150, 300)
draw.text((x, y), name3, fill=color, font=font)
(x, y) = (150, 350)
draw.text((x, y), name4, fill=color, font=font)
(x, y) = (150, 400)
draw.text((x, y), name5, fill=color, font=font)
(x, y) = (150, 450)
draw.text((x, y), name6, fill=color, font=font)
(x, y) = (150, 500)
draw.text((x, y), name7, fill=color, font=font)
(x, y) = (150, 550)
draw.text((x, y), name8, fill=color, font=font)
(x, y) = (150, 600)
draw.text((x, y), name9, fill=color, font=font)
(x, y) = (800, 150)
draw.text((x, y), val0, fill=color, font=font)
(x, y) = (800, 200)
draw.text((x, y), val1, fill=color, font=font)
(x, y) = (800, 250)
draw.text((x, y), val2, fill=color, font=font)
(x, y) = (800, 300)
draw.text((x, y), val3, fill=color, font=font)
(x, y) = (800, 350)
draw.text((x, y), val4, fill=color, font=font)
(x, y) = (800, 400)
draw.text((x, y), val5, fill=color, font=font)
(x, y) = (800, 450)
draw.text((x, y), val6, fill=color, font=font)
(x, y) = (800, 500)
draw.text((x, y), val7, fill=color, font=font)
(x, y) = (800, 550)
draw.text((x, y), val8, fill=color, font=font)
(x, y) = (800, 600)
draw.text((x, y), val9, fill=color, font=font)


# save the edited image

image.save('top-10-friends.png')

os.system('git add .')
os.system('git commit -m "updates"')
os.system('git push origin master')
