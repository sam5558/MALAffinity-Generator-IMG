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

#while len(friend_names) > 0: # while the list isn't empty
#    friend = friend_names[0] # get the first name
#    print("Comparing {}'s list to {}...".format(username, friend))
#    try:
#        # calculate affinity
#        affinity, shared = af.calculate_affinity(friend, service="MyAnimeList")
#        # save the result
#        results[friend] = round(affinity, 2)
#        # remove that friend from the list
#        friend_names.remove(friend)
#    except RateLimitExceededError:
#        print("We exceeded the rate limit!")
#        # wait for a while and then try again
#        time.sleep(10)
#        continue
#    except NoAffinityError as ne:
#        print("{}".format(ne))
#        # ignore this user
#        friend_names.remove(friend)
#        continue
#    except InvalidUserError:
#        print("Couldnt download list for {}. This may be because their list is private.".format(friend))
#        # ignore this user
#        friend_names.remove(friend)
#        continue
#    except DecimalException:
#        # see here:
#        # https://github.com/erkghlerngm44/aniffinity/blob/master/aniffinity/calcs.py#L32
#        # this can happen when a user has no ratings or rates everything the same
#        print("Division by zero error while trying to process list for {}...".format(friend))
#        # ignore this user
#        friend_names.remove(friend)
#        continue
#    except Exception as e:
#        # exit on any other error
#        print("Exception for {}: `{}`".format(friend, e))
#        break

#newresult = OrderedDict(sorted(results.items(), key=lambda t: t[1], reverse=True))
# use the following line to have rapid result (comment line 57 to 95)
newresult = OrderedDict([('LegendOrrin', 71.98), ('AbuelitaDeBatman', 64.43), ('LouysP', 63.81), ('bshak', 62.28), ('Hydroman_', 62.11), ('PafDesChocapiks', 62.03), ('Japy', 59.88), ('KAIKI-DESU', 59.15), ('Blastof_', 58.88), ('S-cryed', 57.86), ('Daante_', 57.62), ('Taikuhatsu', 56.31), ('mcd_78', 55.85), ('Iiiik', 53.66), ('Tenshibana', 53.46), ('anaesan', 53.21), ('HaarWyvern', 53.04), ('Ruqaa', 52.61), ('Wilump', 52.59), ('tristan-h', 51.59), ('Iwolf441', 51.58), ('Naou_', 51.56), ('Souba', 51.06), ('K0NAMI', 50.26), ('21stCenturyBoy_', 50.07), ('Kreya29', 49.93), ('6lk6', 49.65), ('Faith_Navii', 49.16), ('Sakutarou', 48.79), ('itsNotMark', 48.15), ('TuyNOM', 48.11), ('Loleyke', 47.55), ('ezkeeks', 46.93), ('KiSsxShoT', 46.8), ('Noodle_June', 46.69), ('YelloWCl3ar', 46.56), ('ImRenaud', 46.37), ('JojoYabuki', 46.06), ('DatRandomDude', 46.03), ('HaremOverlord', 46.0), ('Afloo', 45.59), ('arthuurop', 44.63), ('Anime-ETF', 44.3), ('darkneff', 44.09), ('DracGaki', 44.02), ('KingDespe', 43.31), ('Zetsubo22', 43.2), ('Laraxs', 42.72), ('GamesRet', 42.7), ('Azuki-ojou', 42.41), ('DesnomLumerian', 41.84), ('Vizioz', 41.46), ('ProfZex', 41.16), ('Hamou', 40.73), ('BenjaminJunior', 40.7), ('paraparaship', 40.51), ('Mangamer', 40.14), ('Kiszaw', 39.38), ('FaliaS', 39.23), ('Kami_yar0', 39.06), ('Benku', 39.06), ('Djidji', 39.03), ('Azdo0m', 39.02), ('Aniki91', 38.65), ('-Nadrel-', 38.46), ('Charlotte1412', 37.78), ('Shiratoria', 37.69), ('Sifedo', 37.51), ('spacecowboy', 36.81), ('FanTaine', 35.97), ('Sreyso', 34.99), ('bAbyLoNE', 34.9), ('LupinYabuki', 32.91), ('Hydraxsfull', 32.87), ('infinico', 32.82), ('Saeba_Ryou', 32.74), ('Jakedax', 32.19), ('BlackTeaLady', 31.87), ('pr4ty', 30.51), ('Matism', 30.0), ('Ha0', 28.8), ('Laeweth', 28.8), ('rek94', 28.37), ('Henatsuka', 24.18), ('firefoxy333', 22.18), ('Apichua', 21.36), ('cynic15m', 20.89), ('Ahmed_paint5', 19.17), ('Radukaii', 17.47), ('Ragnos055', 17.22), ('_r_Felipe', 17.06), ('Chifie', 17.04), ('ProxyLain', 14.98), ('Korsa-', 12.53), ('TopherC17', 11.65), ('QuentiNeicigam', 8.63), ('Lolmortlilol', -3.21)])

#for key in range(11,len(ufriends["friends"])):
#    del newresult[key]
print(newresult)
# print(tabulate([v for v in newresult.items()], headers=["Friend", "Affinity"]))
#print(type(result))

# create Image object with the input image
image = Image.open('top-friends.png').convert('RGBA')

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
color = 'rgb(177,116,104)'
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

color = 'rgb(159, 99, 63)' # white color
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
