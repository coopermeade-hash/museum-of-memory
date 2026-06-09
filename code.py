
import os
import random
import time


from adafruit_magtag.magtag import MagTag
 

magtag = MagTag()

#Note constants
NOTE_C4 = 262
NOTE_D4 = 294
NOTE_E4 = 330
NOTE_F4 = 349
NOTE_G4 = 392
NOTE_A4 = 440
NOTE_B4 = 494


#Direction constants
LEFT = (-1, 0)
RIGHT = (1, 0)
UP = (0, 1)
DOWN = (0, -1)

#Setup all the sound jingles that will be used.
def bleep_move_fail():
    magtag.peripherals.play_tone(NOTE_E4, 0.1)
    magtag.peripherals.play_tone(NOTE_C4, 0.1)


def bleep_move_succeed():
    magtag.peripherals.play_tone(NOTE_F4, 0.1)


def bleep_yoink():
    magtag.peripherals.play_tone(NOTE_C4, 0.2)
    magtag.peripherals.play_tone(NOTE_E4, 0.1)
    magtag.peripherals.play_tone(NOTE_F4, 0.1)


def bleep_use():
    magtag.peripherals.play_tone(NOTE_C4, 0.1)
    magtag.peripherals.play_tone(NOTE_E4, 0.1)
    magtag.peripherals.play_tone(NOTE_F4, 0.1)
    magtag.peripherals.play_tone(NOTE_A4, 0.25)

def bleep_use_fail():
    magtag.peripherals.play_tone(NOTE_A4, 0.1)
    magtag.peripherals.play_tone(NOTE_F4, 0.1)
    magtag.peripherals.play_tone(NOTE_E4, 0.1)
    magtag.peripherals.play_tone(NOTE_C4, 0.25)

#Add the text which will be displayed.
magtag.add_text(
    text_anchor_point = (0, 0),
    text_scale=1,
)

#Open text_dump.txt, get the data, split it into lines, then close the file.
TEXT_DUMP_FILE = open("text_dump.txt","r")
TEXT_DUMP = [line.strip() for line in TEXT_DUMP_FILE]
TEXT_DUMP_FILE.close()

#Make sure the newline text
for i in range(len(TEXT_DUMP)):
    TEXT_DUMP[i] = TEXT_DUMP[i].replace("\\n","\n")
TEXT_DUMP = tuple(TEXT_DUMP)
    
#set the inital text.
start_text = TEXT_DUMP[0]

# all the avalible rooms
ROOMS = {
    (0, 0)  : TEXT_DUMP[1],
    (0, 1)  : TEXT_DUMP[2],
    (-1, 1) : TEXT_DUMP[3],
    (1, 1)  : TEXT_DUMP[4],
}
# All the rooms with items. format is [Name, Pickup text, New room Text]
ROOMS_WITH_ITEMS = {
    (-1, 1): ["WHITE_KEY", TEXT_DUMP[5], TEXT_DUMP[6] ],
}
#All the rooms with doors. format is [Item needed, use text, fail text, new room text.]
ROOMS_WITH_DOORS = {
    (1, 1): ["WHITE_KEY", TEXT_DUMP[7], TEXT_DUMP[8], TEXT_DUMP[9]],
}


#PLAYER_ITEMS
pos = (0, 0)

INVENTORY = []


def try_move(direction : tuple):
    global pos #Needs position to be global for some reason...
    #get the new position
    new_position = (pos[0] + direction[0], pos[1] + direction[1])
    
    #Check if rooms has that position
    if new_position in ROOMS:
        #If rooms has it, make position the new one and update
        pos = new_position
        bleep_move_succeed()
        magtag.set_text(ROOMS[new_position])
    else:
        bleep_move_fail()


def pickup_item():
    bleep_yoink()
    #add the item to the inventory, change the room description, and display the pickup text
    INVENTORY.append(ROOMS_WITH_ITEMS[pos][0])
    ROOMS[pos] = ROOMS_WITH_ITEMS[pos][2]
    magtag.set_text(ROOMS_WITH_ITEMS[pos][1])
    time.sleep(len(ROOMS_WITH_ITEMS[pos][1]) * 0.1)
    magtag.set_text(ROOMS[pos])



def try_use_item():
    current_instance = ROOMS_WITH_DOORS[pos]
    if current_instance[0] in INVENTORY:
        bleep_use()
        magtag.set_text(current_instance[1])
        ROOMS[pos] = current_instance[3]
        time.sleep(len(current_instance[1]) * 0.1)
    else:
        bleep_use_fail()
        magtag.set_text(current_instance[2])
        time.sleep(len(current_instance[2]) * 0.1)
    magtag.set_text(ROOMS[pos])


#magtag.peripherals.neopixel_disable = False
#magtag.peripherals.neopixels.fill((16, 16, 16) )


def main():
    magtag.set_text(start_text)
    # main loop
    while True:

        if magtag.peripherals.button_a_pressed: #LEFT
            try_move( LEFT )
        if magtag.peripherals.button_b_pressed: #UP
            if pos in ROOMS_WITH_DOORS:
                try_use_item()
            else:
                try_move( UP )
        if magtag.peripherals.button_c_pressed: #DOWN

            if pos in ROOMS_WITH_ITEMS:
                pickup_item()
            else:
                try_move( DOWN )
        if magtag.peripherals.button_d_pressed: #RIGHT
            try_move( RIGHT )
        

main()

