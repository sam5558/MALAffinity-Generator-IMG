#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

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

while len(friend_names) > 0: # while the list isn't empty
    friend = friend_names[0] # get the first name
    print("Comparing {}'s list to {}...".format(username, friend))
    try:
        # calculate affinity
        affinity, shared = af.calculate_affinity(friend, service="MyAnimeList")
        # save the result
        results[friend] = round(affinity, 2)
        # remove that friend from the list
        friend_names.remove(friend)
    except RateLimitExceededError:
        print("We exceeded the rate limit!")
        # wait for a while and then try again
        time.sleep(10)
        continue
    except NoAffinityError as ne:
        print("{}".format(ne))
        # ignore this user
        friend_names.remove(friend)
        continue
    except InvalidUserError:
        print("Couldnt download list for {}. This may be because their list is private.".format(friend))
        # ignore this user
        friend_names.remove(friend)
        continue
    except DecimalException:
        # see here:
        # https://github.com/erkghlerngm44/aniffinity/blob/master/aniffinity/calcs.py#L32
        # this can happen when a user has no ratings or rates everything the same
        print("Division by zero error while trying to process list for {}...".format(friend))
        # ignore this user
        friend_names.remove(friend)
        continue
    except Exception as e:
        # exit on any other error
        print("Exception for {}: `{}`".format(friend, e))
        break

newresult = OrderedDict(sorted(results.items(), key=lambda t: t[1], reverse=True))
for key in range(11,len(ufriends["friends"])):
    del newresult[key]
print(newresult)
# print(tabulate([v for v in newresult.items()], headers=["Friend", "Affinity"]))
#print(type(result))

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
message = "TOP MyAnimeList Friends !"
color = 'rgb(0, 0, 0)' # black color
draw.text((x, y), message, fill=color, font=font)

(x, y) = (1100, 50)
lasttime = "last updated : " + dt_string
color = 'rgb(143,188,143)'
draw.text((x, y), lasttime, fill=color, font=updatefont)

# draw the message on the background

name0 = str([v for v in newresult.items()][0][0])
val1 = str([v for v in newresult.items()][0][1])
name1 = str([v for v in newresult.items()][1][0])
val2 = str([v for v in newresult.items()][1][1])
name2 = str([v for v in newresult.items()][2][0])
val3 = str([v for v in newresult.items()][2][1])

color = 'rgb(255, 255, 255)' # white color
(x, y) = (150, 150)
draw.text((x, y), name0, fill=color, font=font)
(x, y) = (150, 200)
draw.text((x, y), name1, fill=color, font=font)
(x, y) = (150, 250)
draw.text((x, y), name2, fill=color, font=font)
(x, y) = (800, 150)
draw.text((x, y), val1, fill=color, font=font)
(x, y) = (800, 200)
draw.text((x, y), val2, fill=color, font=font)
(x, y) = (800, 250)
draw.text((x, y), val3, fill=color, font=font)

# save the edited image

image.save('new-top-friends.png')
