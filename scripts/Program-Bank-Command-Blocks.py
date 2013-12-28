import sys
import unicodedata
import re
from pymclevel import mclevel
from pymclevel import nbt
from pymclevel.schematic import MCSchematic
from pymclevel.box import BoundingBox

from pymclevel.nbt import TAG_Compound, TAG_Byte, TAG_List, TAG_Int_Array, TAG_Short, TAG_String, TAG_Int
from pymclevel.box import Vector

def printf(format, *args):
    sys.stdout.write(format % args)

#level = mclevel.fromFile("/home/mcarter/.minecraft/saves/MikeyWorld-Backup/")
world1 = mclevel.loadWorld("New World");

# The root tag must have a name, and so must any tag within a TAG_Compound
#print level

chunkPositions = list(world1.allChunks)
#xPos, zPos = chunkPositions[10];
#print chunkPositions
sorterArr = {}


#Control: 841,10,374  - START-BLOCK

class ErrorWithCode(Exception):
    def __init__(self, code):
        self.code = code
    def __str__(self):
        return repr(self.code)


################################################################################
# Program Bank Counting System V2
################################################################################
#START-BLOCK-COUNTER
#/scoreboard players add @r stone 21
#/scoreboard players add @r stone 21
#/scoreboard players add @r stone 21
#/setblock ~ ~ ~3 minecraft:lava 0 replace
#/setblock ~ ~ ~5 minecraft:hopper 0 destroy {Items:[{id:1,Count:1,Damage:0,Slot:0},{id:408,Count:1,Damage:2,Slot:1},{id:408,Count:1,Damage:2,Slot:2},{id:408,Count:1,Damage:2,Slot:3},{id:408,Count:1,Damage:2,Slot:4}]}
#/scoreboard objectives setdisplay sidebar stone
def setBankV2(start, t, x_offset, z_offset, score, itemID, itemSubID, count, total):
   setItemsTo=int(total-count);

   if (setItemsTo < 1):
     print "Too many items! ("+str(score)+" - "+str(setItemsTo)+")"
     sys.exit(2)


   if t["x"].value == (start["x"].value+x_offset) and t["z"].value == (start["z"].value-z_offset) and t["y"].value == (start["y"].value + 1) and t["id"].value == "Hopper":
       if "Items" in t:
         for item in t["Items"]:
             if item["Slot"].value == 0:
               item["id"] = TAG_Short(itemID)
               item["Damage"] = TAG_Short(itemSubID)
               item["Count"] = TAG_Short(setItemsTo)
             else:
               item["id"] = TAG_Short(408)
               item["Damage"] = TAG_Short(2)
               item["Count"] = TAG_Short(1)

   if t["x"].value == (start["x"].value+x_offset) and t["z"].value == (start["z"].value-z_offset+1) and t["y"].value == (start["y"].value + 3) and (t["id"].value == "Sign"):
       t["Text1"] = TAG_String(str(score))
       t["Text2"] = TAG_String(str(itemID))
       t["Text3"] = TAG_String(str(itemSubID))
       #print "R: "+t["id"].value + ": " + str(t["x"].value) + "," + str(t["y"].value) + "," + str(t["z"].value) + "  - " + t["Command"].value

   if t["x"].value == (start["x"].value+x_offset) and t["z"].value == (start["z"].value-z_offset) and t["y"].value == (start["y"].value + 3) and t["id"].value == "Control":
       t["Command"] = TAG_String("/scoreboard players add @r "+str(score)+" "+str(int(count/3)))
       #print "R: "+t["id"].value + ": " + str(t["x"].value) + "," + str(t["y"].value) + "," + str(t["z"].value) + "  - " + t["Command"].value

   if t["x"].value == (start["x"].value+x_offset) and t["z"].value == (start["z"].value-z_offset-1) and t["y"].value == (start["y"].value + 2) and t["id"].value == "Control":
       t["Command"] = TAG_String("/scoreboard players add @r "+str(score)+" "+str(int(count/3)))
       #print "R: "+t["id"].value + ": " + str(t["x"].value) + "," + str(t["y"].value) + "," + str(t["z"].value) + "  - " + t["Command"].value

   if t["x"].value == (start["x"].value+x_offset) and t["z"].value == (start["z"].value-z_offset-2) and t["y"].value == (start["y"].value + 2) and t["id"].value == "Control":
       t["Command"] = TAG_String("/scoreboard players add @r "+str(score)+" "+str(int(count/3)))
       #print "R: "+t["id"].value + ": " + str(t["x"].value) + "," + str(t["y"].value) + "," + str(t["z"].value) + "  - " + t["Command"].value

   if t["x"].value == (start["x"].value+x_offset) and t["z"].value == (start["z"].value-z_offset-3) and t["y"].value == (start["y"].value + 1) and t["id"].value == "Control":
       t["Command"] = TAG_String("/setblock ~ ~ ~3 minecraft:lava 0 replace")
       #print "R: "+t["id"].value + ": " + str(t["x"].value) + "," + str(t["y"].value) + "," + str(t["z"].value) + "  - " + t["Command"].value

   if t["x"].value == (start["x"].value+x_offset) and t["z"].value == (start["z"].value-z_offset-5) and t["y"].value == (start["y"].value + 1) and t["id"].value == "Control":
       t["Command"] = TAG_String("/setblock ~ ~ ~5 minecraft:hopper 0 destroy {Items:[{id:"+str(itemID)+",Count:"+str(setItemsTo)+",Damage:"+str(itemSubID)+",Slot:0},{id:408,Count:1,Damage:2,Slot:1},{id:408,Count:1,Damage:2,Slot:2},{id:408,Count:1,Damage:2,Slot:3},{id:408,Count:1,Damage:2,Slot:4}]}")
       #print "R: "+t["id"].value + ": " + str(t["x"].value) + "," + str(t["y"].value) + "," + str(t["z"].value) + "  - " + t["Command"].value

   if t["x"].value == (start["x"].value+x_offset) and t["z"].value == (start["z"].value-z_offset-6) and t["y"].value == (start["y"].value + 1) and t["id"].value == "Control":
       t["Command"] = TAG_String("/scoreboard objectives setdisplay sidebar "+str(score))
       print "R: "+t["id"].value + ": " + str(t["x"].value) + "," + str(t["y"].value) + "," + str(t["z"].value) + "  - " + t["Command"].value
       print "/scoreboard objectives add "+str(score)+" dummy"

   x_offset=x_offset+3
   if (x_offset > 49):
     z_offset=z_offset+10
     x_offset=2

   return (x_offset,z_offset)

count=0
item_common=63
item_rare=18
item_veryrare=3
item_single=3
item_16=15

# Locate Start Block(s)
for (xPos, zPos) in chunkPositions:
    chunk = world1.getChunk(xPos, zPos)
    for st in chunk.TileEntities:
      if st["id"].value == "Control" and st["Command"].value == "START-BLOCK-COUNTER":
          count=count+1
          start = st
          Start_xPos = xPos
          Start_zPos = zPos
          print "Detected start block at: " + str(xPos) + " " + str(zPos) +" : x="+str(start["x"].value)+",y="+str(start["y"].value)+",z="+str(start["z"].value)

          for (xPos, zPos) in chunkPositions:
            if xPos >= Start_xPos and zPos <= Start_zPos and xPos < (Start_xPos +4) and zPos > (Start_zPos -12):
              chunk = world1.getChunk(xPos, zPos)
              chunk.chunkChanged();
              for t in chunk.TileEntities:
                if t["id"].value == "Control" or t["id"].value == "Hopper" or t["id"].value == "Sign":
                  if t["y"].value >= start["y"].value and t["y"].value <= (start["y"].value+3) and t["x"].value >= start["x"].value and t["x"].value <= (start["x"].value+51) and t["z"].value <= start["z"].value and t["z"].value >= (start["z"].value-181):
                     t["CustomName"] = TAG_String("Counter-v2")
                     #Z Limits: 307-127

                     # Row - 1
                     x_offset=2
                     z_offset=2
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "grass",           "2",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "dirt",            "3",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "podzol",          "3",   "2", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "cobblestone",     "4",   "0", item_common, 64)  
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "planks_oak",      "5",   "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "planks_spruce",   "5",   "1", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "planks_birch",    "5",   "2", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "planks_jungle",   "5",   "3", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "planks_acacia",   "5",   "4", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "planks_dark_oak", "5",   "5", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "sapling_oak",     "6",   "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "sapling_spruce",  "6",   "1", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "sapling_birch",   "6",   "2", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "sapling_jungle",  "6",   "3", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "sapling_acacia",  "6",   "4", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "sapling_d_oak",   "6",   "5", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "sand",            "12",  "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "red_sand",        "12",  "1", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "gravel",          "13",  "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "gold_ore",        "14",  "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "iron_ore",        "15",  "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "coal_ore",        "16",  "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "oak",             "17",  "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "spruce",          "17",  "1", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "birch",           "17",  "2", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "jungle",          "17",  "3", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "glass",           "20",  "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "lapis_ore",       "21",  "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "lapis_block",     "22",  "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "dispenser",       "23",  "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "sandstone",       "24",  "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "c_sandstone",     "24",  "1", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "s_sandstone",     "24",  "2", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "powered_rail",    "27",  "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "detector_rail",   "28",  "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "sticky_piston",   "29",  "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "piston",          "33",  "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "wool_white",      "35",  "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "wool_orange",     "35",  "1", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "wool_magenta",    "35",  "2", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "wool_lblue",      "35",  "3", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "wool_yellow",     "35",  "4", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "wool_lime",       "35",  "5", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "wool_pink",       "35",  "6", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "wool_gray",       "35",  "7", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "wool_lgray",      "35",  "8", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "wool_cyan",       "35",  "9", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "wool_purple",     "35",  "10", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "wool_blue",       "35",  "11", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "wool_brown",      "35",  "12", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "wool_green",      "35",  "13", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "wool_red",        "35",  "14", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "wool_black",      "35",  "15", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "dandelion",       "37",  "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "poppy",           "38",  "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "blue_orchid",     "38",  "1", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "allium",          "38",  "2", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "azure_bluet",     "38",  "3", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "red_tulip",       "38",  "4", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "orange_tulip",    "38",  "5", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "white_tulip",     "38",  "6", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "pink_tulip",      "38",  "7", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "oxeye_daisy",     "38",  "8", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "brown_mushroom",  "39",  "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "red_mushroom",    "40",  "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "gold_block",      "41",  "0", item_veryrare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "iron_block",      "42",  "0", item_veryrare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone_slab",      "44",  "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "brick_block",     "45",  "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "TNT",             "46", "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "bookshelf",       "47",  "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "mos_cobblestone", "48",  "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "obsidian",        "49",  "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "torch",           "50",  "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "chest",           "54",  "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "diamond_ore",     "56",  "0", item_veryrare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "diamond_block",   "57",  "0", item_veryrare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "craft_table",     "58",  "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "furnace",         "61",  "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "rail",            "66",  "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "ladder",          "65",  "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "lever",           "69",  "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "pressure_stone",  "70",  "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "pressure_wood",   "72",  "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "redstone_ore",    "73",  "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "redstone_torch",  "76", "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "button_stone",    "77",  "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "ice",             "79",  "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "snow",            "80",  "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "cactus",          "81",  "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "clay",            "82",  "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "fence",           "85",  "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "pumpkin",         "86", "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "netherrack",      "87",  "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "soul_sand",       "88",  "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "glowstone",       "89",  "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "lit_pumpkin",     "91", "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "glass_white",     "95",  "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "glass_orange",    "95",  "1", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "glass_magenta",   "95",  "2", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "glass_lblue",     "95",  "3", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "glass_yellow",    "95",  "4", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "glass_lime",      "95",  "5", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "glass_pink",      "95",  "6", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "glass_gray",      "95",  "7", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "glass_lgray",     "95",  "8", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "glass_cyan",      "95",  "9", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "glass_purple",    "95",  "10", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "glass_blue",      "95",  "11", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "glass_brown",     "95",  "12", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "glass_green",     "95",  "13", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "glass_red",       "95",  "14", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "glass_black",     "95",  "15", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "trapdoor",        "96",  "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stonebrick",      "98",  "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "b_mushroom_blk",  "99",  "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "r_mushroom_blk",  "100", "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "iron_bars",       "101", "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "glass_pane",      "102", "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "melon_block",     "103", "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "vines",           "106", "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "fence_gate",      "107", "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "mycelium",        "110", "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "waterlily",       "111", "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "nether_brick",    "112", "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "nether_fence",    "113", "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "nether_stairs",   "114", "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "redstone_lamp",   "123", "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "emerald_ore",     "129", "0", item_veryrare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "tripwire_hook",   "131", "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "emerald_block",   "133", "0", item_veryrare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "cobblestone_w",   "139", "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "button_wood",     "143", "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "trapped_chest",   "146", "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "pressure_gold",   "147", "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "pressure_iron",   "148", "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "redstone_block",  "152", "0", item_veryrare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "quartz_ore",      "153", "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "hopper",          "154", "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "quartz_block",    "155", "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "quartz_stairs",   "156", "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "activator_rail",  "157", "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "dropper",         "158", "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "clay_white",      "159", "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "clay_orange",     "159", "1", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "clay_magenta",    "159", "2", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "clay_lblue",      "159", "3", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "clay_yellow",     "159", "4", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "clay_lime",       "159", "5", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "clay_pink",       "159", "6", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "clay_gray",       "159", "7", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "clay_lgray",      "159", "8", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "clay_cyan",       "159", "9", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "clay_purple",     "159", "10", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "clay_blue",       "159", "11", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "clay_brown",      "159", "12", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "clay_green",      "159", "13", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "clay_red",        "159", "14", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "clay_black",      "159", "15", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "glass_p_white",   "160", "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "glass_p_orange",  "160", "1", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "glass_p_magenta", "160", "2", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "glass_p_lblue",   "160", "3", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "glass_p_yellow",  "160", "4", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "glass_p_lime",    "160", "5", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "glass_p_pink",    "160", "6", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "glass_p_gray",    "160", "7", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "glass_p_lgray",   "160", "8", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "glass_p_cyan",    "160", "9", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "glass_p_purple",  "160", "10", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "glass_p_blue",    "160", "11", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "glass_p_brown",   "160", "12", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "glass_p_green",   "160", "13", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "glass_p_red",     "160", "14", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "glass_p_black",   "160", "15", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "acacia",          "162", "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "dark_oak",        "162", "1", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "hay_bale",        "170", "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "hard_clay",       "172", "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "coal_block",      "173", "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "sunflower",       "175", "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "lilac",           "175", "1", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "fern",            "175", "2", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "rose",            "175", "4", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "peony",           "175", "5", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "apple",           "260", "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "arrow",           "262", "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "coal",            "263", "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "charcoal",        "263", "1", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "diamond",         "264", "0", item_veryrare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "iron_ingot",      "265", "0", item_veryrare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "gold_ingot",      "266", "0", item_veryrare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stick",           "280", "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "string",          "287", "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "feather",         "288", "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "gunpowder",       "289", "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "wheat",           "296", "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "seed",            "295", "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "flint",           "318", "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "raw_pork",        "319", "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "cook_pork",       "320", "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "painting",        "321", "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "gold_apple",      "322", "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "e_gold_apple",    "322", "1", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "sign",            "323", "0", item_16, 16)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "bucket",          "325", "0", item_16, 16)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "redstone",        "331", "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "snowball",        "332", "0", item_16, 16)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "leather",         "334", "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "brick",           "336", "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "clay_ball",       "337", "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "sugar_cane",      "338", "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "paper",           "339", "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "slimeball",       "341", "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "egg",             "344", "0", item_16, 16)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "glowstone_dust",  "348", "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "raw_fish",        "349", "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "raw_salmon",      "349", "1", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "clownfish",       "349", "2", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "pufferfish",      "349", "3", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "cook_fish",       "350", "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "cook_salmon",     "350", "1", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "ink_sack",        "351", "1", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "cocoa",           "351", "3", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "bonemeal",        "351", "15", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "bone",            "352", "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "sugar",           "353", "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "repeater",        "356", "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "melon",           "360", "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "pumpkin_seed",    "361", "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "melon_seed",      "362", "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "raw_beef",        "363", "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "steak",           "364", "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "raw_chicken",     "365", "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "cook_chicken",    "366", "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "rotten_flesh",    "367", "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "ender_pearl",     "368", "0", item_single,16)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "blaze_rod",       "369", "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "ghast_tear",      "370", "0", item_veryrare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "gold_nuget",      "371", "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "nether_wart",     "372", "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "glass_bottle",    "374", "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "spider_eye",      "375", "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "blaze_powder",    "377", "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "magma_cream",     "378", "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "eye_of_ender",    "381", "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "emerald",         "388", "0", item_veryrare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "item_frame",      "389", "0", item_veryrare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "carrot",          "391", "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "potato",          "392", "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "baked_potato",    "393", "0", item_common, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "pos_potato",      "394", "0", item_veryrare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "gold_carrot",     "396", "0", item_veryrare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "comparator",      "404", "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "nether_brick",    "405", "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "nether_quartz",   "406", "0", item_rare, 64)
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "lead",            "420", "0", item_rare, 64)

                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   
                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "stone",           "1",   "0", item_common, 64)   

#                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "wood_door",       "324", "0", item_single,1)
#                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "bucket_water",    "326", "0", item_single,1)
#                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "bucket_lava",     "327", "0", item_single,1)
#                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "iron_door",       "330", "0", item_single,1)
#                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "minecart",        "328", "0", item_single, 1)
#                     (x_offset,z_offset)=setBankV2(start, t, x_offset, z_offset, "bucket_milk",     "335", "0", item_single, 1)
                    
                     
                     if t["id"].value == "Control":
                       print "C2: "+t["CustomName"].value + ": " + str(t["x"].value) + "," + str(t["y"].value) + "," + str(t["z"].value) + "  - " + t["Command"].value
                   
world1.saveInPlace();
sys.exit(1)


################################################################################
# Program Acquisition System
################################################################################

def setSummon(start, t, x_offset, z_offset, itemID, itemSubID, count):
   if t["x"].value == (start["x"].value+x_offset) and t["z"].value == (start["z"].value+z_offset) and t["y"].value == start["y"].value and t["id"].value == "Control":
       t["Command"] = TAG_String("/summon Item ~ ~5 ~ {Item:{id:"+str(itemID)+",Count:"+str(count)+",Damage:"+str(itemSubID)+"}}")
       print "R: "+t["id"].value + ": " + str(t["x"].value) + "," + str(t["y"].value) + "," + str(t["z"].value) + "  - " + t["Command"].value

def setRemove(start, t, x_offset, z_offset, item, count):
   if t["x"].value == (start["x"].value+x_offset) and t["z"].value == (start["z"].value+z_offset) and t["y"].value == (start["y"].value+1) and t["id"].value == "Control":
       t["Command"] = TAG_String("/scoreboard players remove @p[r=8] "+str(item)+" "+str(count))
       print "R: "+t["id"].value + ": " + str(t["x"].value) + "," + str(t["y"].value) + "," + str(t["z"].value) + "  - " + t["Command"].value

def setDetect(start, t, x_offset, z_offset, item, count):
   if t["x"].value == (start["x"].value+x_offset) and t["z"].value == (start["z"].value+z_offset) and t["y"].value == (start["y"].value+1) and t["id"].value == "Control":
       t["Command"] = TAG_String("/testfor @p[score_"+str(item)+"_min="+str(count)+",r=8]")
       print "R: "+t["id"].value + ": " + str(t["x"].value) + "," + str(t["y"].value) + "," + str(t["z"].value) + "  - " + t["Command"].value

one_item=1
#some_item=20
#full_item=64

some_item=1
full_item=1


# Locate Start Block
for (xPos, zPos) in chunkPositions:
  chunk = world1.getChunk(xPos, zPos)
  for t in chunk.TileEntities:
    if t["id"].value == "Control" and t["Command"].value == "AQUIRE-START":
        start = t
        Start_xPos = xPos
        Start_zPos = zPos
        print "Detected Acquisition block at: " + str(xPos) + " " + str(zPos)
        print t

# xPos >= Start_xPos and xPos < (Start_xPos +3)
for (xPos, zPos) in chunkPositions:
  if zPos >= Start_zPos and zPos < (Start_zPos +12) and xPos >= (Start_xPos -4) and xPos < (Start_xPos +5):
    chunk = world1.getChunk(xPos, zPos)
    chunk.chunkChanged();
    for t in chunk.TileEntities:
      if t["id"].value == "Control":
        #print t["id"].value + ": " + str(t["x"].value) + "," + str(t["y"].value) + "," + str(t["z"].value) + "  - " + t["Command"].value
#        if t["y"].value > start["y"].value and t["y"].value < start["y"].value+13 and t["x"].value >= start["x"].value and t["z"].value < start["z"].value:

#             * R
#             |
#             |
#        ----   ----
#        ----   ----
#        ----   ----
#             |
#             |
#             |
        x1=-2
        x2=-1
        x3=-5
        z1=2

        setSummon(start, t, x1, z1, 1, 0, full_item)     # Stone
        setRemove(start, t, x2, z1, "stone", full_item)  # Stone
        setDetect(start, t, x3, z1, "stone", full_item)  # Stone
        z1=z1+3

        setSummon(start, t, x1, z1, 3, 0, full_item)    # Dirt
        setRemove(start, t, x2, z1, "dirt", full_item)  # Dirt
        setDetect(start, t, x3, z1, "dirt", full_item)  # Dirt
        z1=z1+3

        setSummon(start, t, x1, z1, 24, 0, some_item)        # sandstone
        setRemove(start, t, x2, z1, "sandstone", some_item)  # sandstone
        setDetect(start, t, x3, z1, "sandstone", some_item)  # sandstone
        z1=z1+3

        setSummon(start, t, x1, z1, 24, 1, some_item)        # c_sandstone
        setRemove(start, t, x2, z1, "c_sandstone", some_item)  # c_sandstone
        setDetect(start, t, x3, z1, "c_sandstone", some_item)  # c_sandstone
        z1=z1+3

        setSummon(start, t, x1, z1, 24, 2, some_item)        # s_sandstone
        setRemove(start, t, x2, z1, "s_sandstone", some_item)  # s_sandstone
        setDetect(start, t, x3, z1, "s_sandstone", some_item)  # s_sandstone
        z1=z1+3

        setSummon(start, t, x1, z1, 12, 0, some_item)   # sand
        setRemove(start, t, x2, z1, "sand", some_item)  # sand
        setDetect(start, t, x3, z1, "sand", some_item)  # sand
        z1=z1+3

        setSummon(start, t, x1, z1, 12, 1, some_item)       # red_sand
        setRemove(start, t, x2, z1, "red_sand", some_item)  # red_sand
        setDetect(start, t, x3, z1, "red_sand", some_item)  # red_sand
        z1=z1+3

        setSummon(start, t, x1, z1, -1, 0, some_item)    # dirt (duplicate)
        setRemove(start, t, x2, z1, "test", some_item)  # dirt (duplicate)
        setDetect(start, t, x3, z1, "test", some_item)  # dirt (duplicate)
        z1=z1+3

        setSummon(start, t, x1, z1, -1, 0, some_item)    # dirt (duplicate)
        setRemove(start, t, x2, z1, "test", some_item)  # dirt (duplicate)
        setDetect(start, t, x3, z1, "test", some_item)  # dirt (duplicate)
        z1=z1+3

        setSummon(start, t, x1, z1, 139, 0, some_item)           # cobblestone wall
        setRemove(start, t, x2, z1, "cobblestone_w", some_item)  # cobblestone wall
        setDetect(start, t, x3, z1, "cobblestone_w", some_item)  # cobblestone wall
        z1=z1+3

        setSummon(start, t, x1, z1, 44, 0, some_item)           # stone slab
        setRemove(start, t, x2, z1, "stone_slab", some_item)  # stone slab
        setDetect(start, t, x3, z1, "stone_slab", some_item)  # stone slab
        z1=z1+3

        setSummon(start, t, x1, z1, 48, 0, some_item)           # mossy cobblestone 
        setRemove(start, t, x2, z1, "mos_cobblestone", some_item)  # mossy cobblestone 
        setDetect(start, t, x3, z1, "mos_cobblestone", some_item)  # mossy cobblestone 
        z1=z1+3

        setSummon(start, t, x1, z1, 89, 0, some_item)           # glowstone
        setRemove(start, t, x2, z1, "glowstone", some_item)  # glowstone
        setDetect(start, t, x3, z1, "glowstone", some_item)  # glowstone
        z1=z1+3

        setSummon(start, t, x1, z1, 98, 0, some_item)           # stone brick
        setRemove(start, t, x2, z1, "stonebrick", some_item)  # stone brick
        setDetect(start, t, x3, z1, "stonebrick", some_item)  # stone brick
        z1=z1+3

        setSummon(start, t, x1, z1, 107, 0, one_item)           # fence gate
        setRemove(start, t, x2, z1, "fence_gate", one_item)  # fence gate
        setDetect(start, t, x3, z1, "fence_gate", one_item)  # fence gate
        z1=z1+3

        setSummon(start, t, x1, z1, 85, 0, some_item)           # fence
        setRemove(start, t, x2, z1, "fence", some_item)  # fence
        setDetect(start, t, x3, z1, "fence", some_item)  # fence
        z1=z1+3

        setSummon(start, t, x1, z1, 82, 0, some_item)           # clay
        setRemove(start, t, x2, z1, "clay", some_item)  # clay
        setDetect(start, t, x3, z1, "clay", some_item)  # clay
        z1=z1+3

        setSummon(start, t, x1, z1, 79, 0, some_item)           # ice
        setRemove(start, t, x2, z1, "ice", some_item)  # ice
        setDetect(start, t, x3, z1, "ice", some_item)  # ice
        z1=z1+3

        setSummon(start, t, x1, z1, 110, 0, some_item)           # mycelium
        setRemove(start, t, x2, z1, "mycelium", some_item)  # mycelium
        setDetect(start, t, x3, z1, "mycelium", some_item)  # mycelium
        z1=z1+3

        setSummon(start, t, x1, z1, 88, 0, some_item)           # soul sand
        setRemove(start, t, x2, z1, "soul_sand", some_item)  # soul sand
        setDetect(start, t, x3, z1, "soul_sand", some_item)  # soul sand
        z1=z1+3

#           L * 
#             |
#             |
#        ----   ----
#        ----   ----
#        ----   ----
#             |
#             |
#             |
        x1=-10
        x2=-11
        x3=-7
        z1=2

        setSummon(start, t, x1, z1, 2, 0,    some_item)     # grass
        setRemove(start, t, x2, z1, "grass", some_item)  # grass
        setDetect(start, t, x3 , z1, "grass", some_item)  # grass
        z1=z1+3

        setSummon(start, t, x1, z1, 4, 0, full_item)    # Dirt
        setRemove(start, t, x2, z1, "cobblestone", full_item)  # Dirt
        setDetect(start, t, x3 , z1, "cobblestone", full_item)  # Dirt
        z1=z1+3

        setSummon(start, t, x1, z1, 14, 0, one_item)        # gold_ore
        setRemove(start, t, x2, z1, "gold_ore", one_item)  # gold_ore
        setDetect(start, t, x3 , z1, "gold_ore", one_item)  # gold_ore
        z1=z1+3

        setSummon(start, t, x1, z1, 15, 1, one_item)        # iron_ore
        setRemove(start, t, x2, z1, "iron_ore", one_item)  # iron_ore
        setDetect(start, t, x3, z1, "iron_ore", one_item)  # iron_ore
        z1=z1+3

        setSummon(start, t, x1, z1, 56, 2, one_item)        # diamond_ore
        setRemove(start, t, x2, z1, "diamond_ore", one_item)  # diamond_ore
        setDetect(start, t, x3, z1, "diamond_ore", one_item)  # diamond_ore
        z1=z1+3

        setSummon(start, t, x1, z1, 73, 0, one_item)   # redstone_ore
        setRemove(start, t, x2, z1, "redstone_ore", one_item)  # redstone_ore
        setDetect(start, t, x3, z1, "redstone_ore", one_item)  # redstone_ore
        z1=z1+3

        setSummon(start, t, x1, z1, 129, 0, one_item)       # emerald_ore
        setRemove(start, t, x2, z1, "emerald_ore", one_item)  # emerald_ore
        setDetect(start, t, x3, z1, "emerald_ore", one_item)  # emerald_ore
        z1=z1+3

        setSummon(start, t, x1, z1, 153, 0, some_item)    # quartz_ore
        setRemove(start, t, x2, z1, "quartz_ore", some_item)  # quartz_ore
        setDetect(start, t, x3, z1, "quartz_ore", some_item)  # quartz_ore
        z1=z1+3


        setSummon(start, t, x1, z1, 16, 0, some_item)    # coal_ore
        setRemove(start, t, x2, z1, "coal_ore", some_item)  # coal_ore
        setDetect(start, t, x3, z1, "coal_ore", some_item)  # coal_ore
        z1=z1+3

        setSummon(start, t, x1, z1, 41, 0, one_item)           # gold_block
        setRemove(start, t, x2, z1, "gold_block", one_item)  # gold_block
        setDetect(start, t, x3, z1, "gold_block", one_item)  # gold_block
        z1=z1+3

        setSummon(start, t, x1, z1, 42, 0, one_item)           # iron_block
        setRemove(start, t, x2, z1, "iron_block", one_item)  # iron_block
        setDetect(start, t, x3, z1, "iron_block", one_item)  # iron_block
        z1=z1+3


        setSummon(start, t, x1, z1, 45, 0, some_item)           # brick_block
        setRemove(start, t, x2, z1, "brick_block", some_item)  # brick_block
        setDetect(start, t, x3, z1, "brick_block", some_item)  # brick_block
        z1=z1+3

        setSummon(start, t, x1, z1, 57, 0, one_item)           # diamond_block
        setRemove(start, t, x2, z1, "diamond_block", one_item)  # diamond_block
        setDetect(start, t, x3, z1, "diamond_block", one_item)  # diamond_block
        z1=z1+3

        setSummon(start, t, x1, z1, 133, 0, one_item)           # emerald_block
        setRemove(start, t, x2, z1, "emerald_block", one_item)  # emerald_block
        setDetect(start, t, x3, z1, "emerald_block", one_item)  # emerald_block
        z1=z1+3

        setSummon(start, t, x1, z1, 152, 0, some_item)           # redstone_block
        setRemove(start, t, x2, z1, "redstone_block", some_item)  # redstone_block
        setDetect(start, t, x3, z1, "redstone_block", some_item)  # redstone_block
        z1=z1+3

        setSummon(start, t, x1, z1, 155, 0, some_item)           # quartz_block
        setRemove(start, t, x2, z1, "quartz_block", some_item)  # quartz_block
        setDetect(start, t, x3, z1, "quartz_block", some_item)  # quartz_block
        z1=z1+3

        setSummon(start, t, x1, z1, 156, 0, some_item)           # quartz_stairs
        setRemove(start, t, x2, z1, "quartz_stairs", some_item)  # quartz_stairs
        setDetect(start, t, x3, z1, "quartz_stairs", some_item)  # quartz_stairs
        z1=z1+3

        setSummon(start, t, x1, z1, 21, 0, some_item)           # lapis_ore
        setRemove(start, t, x2, z1, "lapis_ore", some_item)  # lapis_ore
        setDetect(start, t, x3, z1, "lapis_ore", some_item)  # lapis_ore
        z1=z1+3

        setSummon(start, t, x1, z1, 22, 0, some_item)           # lapis_block
        setRemove(start, t, x2, z1, "lapis_block", some_item)  # lapis_block
        setDetect(start, t, x3, z1, "lapis_block", some_item)  # lapis_block
        z1=z1+3

        setSummon(start, t, x1, z1, 87, 0, some_item)           # netherrack
        setRemove(start, t, x2, z1, "netherrack", some_item)  # netherrack
        setDetect(start, t, x3, z1, "netherrack", some_item)  # netherrack
        z1=z1+3

#           (x=748, z=198)
#             | 
#             |
#             |   
#        ----   ---*T  (x=750, z=264)
#        ----   ----
#        ----   ----
#             |
#             |
#             |
        x1=2
        z1=67
        z2=66
        z3=70

        setSummon(start, t, x1, z1, 20, 0,    some_item)     # grass
        setRemove(start, t, x1, z2, "glass", some_item)  # grass
        setDetect(start, t, x1, z3, "glass", some_item)  # grass
        x1=x1+3

        setSummon(start, t, x1, z1, 95, 0,    one_item)     # stained glass white
        setRemove(start, t, x1, z2, "glass_white", one_item)  # stained glass white
        setDetect(start, t, x1, z3, "glass_white", one_item)  # stained glass white
        x1=x1+3

        setSummon(start, t, x1, z1, 95, 1,    one_item)     # stained glass white
        setRemove(start, t, x1, z2, "glass_orange", one_item)  # stained glass orange
        setDetect(start, t, x1, z3, "glass_orange", one_item)  # stained glass orange
        x1=x1+3
        setSummon(start, t, x1, z1, 95, 2,    one_item)     # stained glass magenta
        setRemove(start, t, x1, z2, "glass_magenta", one_item)  # stained glass magenta
        setDetect(start, t, x1, z3, "glass_magenta", one_item)  # stained glass magenta
        x1=x1+3
        setSummon(start, t, x1, z1, 95, 3,    one_item)     # stained glass light blue
        setRemove(start, t, x1, z2, "glass_lblue", one_item)  # stained glass light blue
        setDetect(start, t, x1, z3, "glass_lblue", one_item)  # stained glass light blue
        x1=x1+3
        setSummon(start, t, x1, z1, 95, 4,    one_item)     # stained glass yellow
        setRemove(start, t, x1, z2, "glass_yellow", one_item)  # stained glass yellow
        setDetect(start, t, x1, z3, "glass_yellow", one_item)  # stained glass yellow
        x1=x1+3
        setSummon(start, t, x1, z1, 95, 5,    one_item)     # stained glass lime
        setRemove(start, t, x1, z2, "glass_lime", one_item)  # stained glass lime
        setDetect(start, t, x1, z3, "glass_lime", one_item)  # stained glass lime
        x1=x1+3
        setSummon(start, t, x1, z1, 95, 6,    one_item)     # stained glass pink
        setRemove(start, t, x1, z2, "glass_pink", one_item)  # stained glass pink
        setDetect(start, t, x1, z3, "glass_pink", one_item)  # stained glass pink
        x1=x1+3
        setSummon(start, t, x1, z1, 95, 7,    one_item)     # stained glass gray
        setRemove(start, t, x1, z2, "glass_gray", one_item)  # stained glass gray
        setDetect(start, t, x1, z3, "glass_gray", one_item)  # stained glass gray
        x1=x1+3
        setSummon(start, t, x1, z1, 95, 8,    one_item)     # stained glass light gray
        setRemove(start, t, x1, z2, "glass_lgray", one_item)  # stained glass light gray
        setDetect(start, t, x1, z3, "glass_lgray", one_item)  # stained glass light gray
        x1=x1+3
        setSummon(start, t, x1, z1, 95, 9,    one_item)     # stained glass cyan
        setRemove(start, t, x1, z2, "glass_cyan", one_item)  # stained glass cyan
        setDetect(start, t, x1, z3, "glass_cyan", one_item)  # stained glass cyan
        x1=x1+3
        setSummon(start, t, x1, z1, 95, 10,    one_item)     # stained glass purple
        setRemove(start, t, x1, z2, "glass_purple", one_item)  # stained glass purple
        setDetect(start, t, x1, z3, "glass_purple", one_item)  # stained glass purple
        x1=x1+3
        setSummon(start, t, x1, z1, 95, 11,    one_item)     # stained glass blue
        setRemove(start, t, x1, z2, "glass_blue", one_item)  # stained glass blue
        setDetect(start, t, x1, z3, "glass_blue", one_item)  # stained glass blue
        x1=x1+3
        setSummon(start, t, x1, z1, 95, 12,    one_item)     # stained glass brown
        setRemove(start, t, x1, z2, "glass_brown", one_item)  # stained glass brown
        setDetect(start, t, x1, z3, "glass_brown", one_item)  # stained glass brown
        x1=x1+3
        setSummon(start, t, x1, z1, 95, 13,    one_item)     # stained glass green
        setRemove(start, t, x1, z2, "glass_green", one_item)  # stained glass green
        setDetect(start, t, x1, z3, "glass_green", one_item)  # stained glass green
        x1=x1+3
        setSummon(start, t, x1, z1, 95, 14,    one_item)     # stained glass red
        setRemove(start, t, x1, z2, "glass_red", one_item)  # stained glass red
        setDetect(start, t, x1, z3, "glass_red", one_item)  # stained glass red
        x1=x1+3
        setSummon(start, t, x1, z1, 95, 15,    one_item)     # stained glass black
        setRemove(start, t, x1, z2, "glass_black", one_item)  # stained glass black
        setDetect(start, t, x1, z3, "glass_black", one_item)  # stained glass black
        x1=x1+3
        setSummon(start, t, x1, z1, 101, 0,    one_item)     # iron_bars
        setRemove(start, t, x1, z2, "iron_bars", one_item)  # iron_bars
        setDetect(start, t, x1, z3, "iron_bars", one_item)  # iron_bars
        x1=x1+3
        setSummon(start, t, x1, z1, 111, 0,    one_item)     # waterlily
        setRemove(start, t, x1, z2, "waterlily", one_item)  # waterlily
        setDetect(start, t, x1, z3, "waterlily", one_item)  # waterlily
        x1=x1+3
        setSummon(start, t, x1, z1, 154, 0,    one_item)     # hopper
        setRemove(start, t, x1, z2, "hopper", one_item)  # hopper
        setDetect(start, t, x1, z3, "hopper", one_item)  # hopper
        x1=x1+3


#           (x=748, z=198)
#             | 
#             |
#             |   
#        ----   ---*B  (x=750, z=270)
#        ----   ----
#        ----   ----
#             |
#             |
#             |
        x1=2
        z1=75
        z2=76
        z3=72

        setSummon(start, t, x1, z1, 102, 0,    some_item)     # glass pane
        setRemove(start, t, x1, z2, "glass_pane", some_item)  # glass pane
        setDetect(start, t, x1, z3, "glass_pane", some_item)  # glass pane
        x1=x1+3

        setSummon(start, t, x1, z1, 160, 0,    one_item)     # stained glass pane white
        setRemove(start, t, x1, z2, "glass_p_white", one_item)  # stained glass pane white
        setDetect(start, t, x1, z3, "glass_p_white", one_item)  # stained glass pane white
        x1=x1+3

        setSummon(start, t, x1, z1, 160, 1,    one_item)     # stained glass pane white
        setRemove(start, t, x1, z2, "glass_p_orange", one_item)  # stained glass pane orange
        setDetect(start, t, x1, z3, "glass_p_orange", one_item)  # stained glass pane orange
        x1=x1+3
        setSummon(start, t, x1, z1, 160, 2,    one_item)     # stained glass pane magenta
        setRemove(start, t, x1, z2, "glass_p_magenta", one_item)  # stained glass pane magenta
        setDetect(start, t, x1, z3, "glass_p_magenta", one_item)  # stained glass pane magenta
        x1=x1+3
        setSummon(start, t, x1, z1, 160, 3,    one_item)     # stained glass pane light blue
        setRemove(start, t, x1, z2, "glass_p_lblue", one_item)  # stained glass pane light blue
        setDetect(start, t, x1, z3, "glass_p_lblue", one_item)  # stained glass pane light blue
        x1=x1+3
        setSummon(start, t, x1, z1, 160, 4,    one_item)     # stained glass pane yellow
        setRemove(start, t, x1, z2, "glass_p_yellow", one_item)  # stained glass pane yellow
        setDetect(start, t, x1, z3, "glass_p_yellow", one_item)  # stained glass pane yellow
        x1=x1+3
        setSummon(start, t, x1, z1, 160, 5,    one_item)     # stained glass pane lime
        setRemove(start, t, x1, z2, "glass_p_lime", one_item)  # stained glass pane lime
        setDetect(start, t, x1, z3, "glass_p_lime", one_item)  # stained glass pane lime
        x1=x1+3
        setSummon(start, t, x1, z1, 160, 6,    one_item)     # stained glass pane pink
        setRemove(start, t, x1, z2, "glass_p_pink", one_item)  # stained glass pane pink
        setDetect(start, t, x1, z3, "glass_p_pink", one_item)  # stained glass pane pink
        x1=x1+3
        setSummon(start, t, x1, z1, 160, 7,    one_item)     # stained glass pane gray
        setRemove(start, t, x1, z2, "glass_p_gray", one_item)  # stained glass pane gray
        setDetect(start, t, x1, z3, "glass_p_gray", one_item)  # stained glass pane gray
        x1=x1+3
        setSummon(start, t, x1, z1, 160, 8,    one_item)     # stained glass pane light gray
        setRemove(start, t, x1, z2, "glass_p_lgray", one_item)  # stained glass pane light gray
        setDetect(start, t, x1, z3, "glass_p_lgray", one_item)  # stained glass pane light gray
        x1=x1+3
        setSummon(start, t, x1, z1, 160, 9,    one_item)     # stained glass pane cyan
        setRemove(start, t, x1, z2, "glass_p_cyan", one_item)  # stained glass pane cyan
        setDetect(start, t, x1, z3, "glass_p_cyan", one_item)  # stained glass pane cyan
        x1=x1+3
        setSummon(start, t, x1, z1, 160, 10,    one_item)     # stained glass pane purple
        setRemove(start, t, x1, z2, "glass_p_purple", one_item)  # stained glass pane purple
        setDetect(start, t, x1, z3, "glass_p_purple", one_item)  # stained glass pane purple
        x1=x1+3
        setSummon(start, t, x1, z1, 160, 11,    one_item)     # stained glass pane blue
        setRemove(start, t, x1, z2, "glass_p_blue", one_item)  # stained glass pane blue
        setDetect(start, t, x1, z3, "glass_p_blue", one_item)  # stained glass pane blue
        x1=x1+3
        setSummon(start, t, x1, z1, 160, 12,    one_item)     # stained glass pane brown
        setRemove(start, t, x1, z2, "glass_p_brown", one_item)  # stained glass pane brown
        setDetect(start, t, x1, z3, "glass_p_brown", one_item)  # stained glass pane brown
        x1=x1+3
        setSummon(start, t, x1, z1, 160, 13,    one_item)     # stained glass pane green
        setRemove(start, t, x1, z2, "glass_p_green", one_item)  # stained glass pane green
        setDetect(start, t, x1, z3, "glass_p_green", one_item)  # stained glass pane green
        x1=x1+3
        setSummon(start, t, x1, z1, 160, 14,    one_item)     # stained glass pane red
        setRemove(start, t, x1, z2, "glass_p_red", one_item)  # stained glass pane red
        setDetect(start, t, x1, z3, "glass_p_red", one_item)  # stained glass pane red
        x1=x1+3
        setSummon(start, t, x1, z1, 160, 15,    one_item)     # stained glass pane black
        setRemove(start, t, x1, z2, "glass_p_black", one_item)  # stained glass pane black
        setDetect(start, t, x1, z3, "glass_p_black", one_item)  # stained glass pane black
        x1=x1+3
        setSummon(start, t, x1, z1, 47, 0,    one_item)     # bookshelf
        setRemove(start, t, x1, z2, "bookshelf", one_item)  # bookshelf
        setDetect(start, t, x1, z3, "bookshelf", one_item)  # bookshelf
        x1=x1+3
        setSummon(start, t, x1, z1, 158, 0,    one_item)     # dropper
        setRemove(start, t, x1, z2, "dropper", one_item)  # dropper
        setDetect(start, t, x1, z3, "dropper", one_item)  # dropper
        x1=x1+3
        setSummon(start, t, x1, z1, 23, 0,    one_item)     # dispenser
        setRemove(start, t, x1, z2, "dispenser", one_item)  # dispenser
        setDetect(start, t, x1, z3, "dispenser", one_item)  # dispenser
        x1=x1+3

#           (x=748, z=198)
#             | 
#             |
#             |   
#        ----   ----  
#        ----   ---*T (x=750, z=283)
#        ----   ----
#             |
#             |
#             |
        x1=2
        z1=67+19
        z2=66+19
        z3=70+19

        setSummon(start, t, x1, z1, 49, 0,      some_item)   # obsidian
        setRemove(start, t, x1, z2, "obsidian", some_item)   # obsidian
        setDetect(start, t, x1, z3, "obsidian", some_item)   # obsidian
        x1=x1+3

        setSummon(start, t, x1, z1, 35, 0,    one_item)     # wool white
        setRemove(start, t, x1, z2, "wool_white", one_item)  # wool white
        setDetect(start, t, x1, z3, "wool_white", one_item)  # wool white
        x1=x1+3

        setSummon(start, t, x1, z1, 35, 1,    one_item)     # wool orange
        setRemove(start, t, x1, z2, "wool_orange", one_item)  # wool orange
        setDetect(start, t, x1, z3, "wool_orange", one_item)  # wool orange
        x1=x1+3
        setSummon(start, t, x1, z1, 35, 2,    one_item)     # wool magenta
        setRemove(start, t, x1, z2, "wool_magenta", one_item)  # wool magenta
        setDetect(start, t, x1, z3, "wool_magenta", one_item)  # wool magenta
        x1=x1+3
        setSummon(start, t, x1, z1, 35, 3,    one_item)     # wool light blue
        setRemove(start, t, x1, z2, "wool_lblue", one_item)  # wool light blue
        setDetect(start, t, x1, z3, "wool_lblue", one_item)  # wool light blue
        x1=x1+3
        setSummon(start, t, x1, z1, 35, 4,    one_item)     # wool yellow
        setRemove(start, t, x1, z2, "wool_yellow", one_item)  # wool yellow
        setDetect(start, t, x1, z3, "wool_yellow", one_item)  # wool yellow
        x1=x1+3
        setSummon(start, t, x1, z1, 35, 5,    one_item)     # wool lime
        setRemove(start, t, x1, z2, "wool_lime", one_item)  # wool lime
        setDetect(start, t, x1, z3, "wool_lime", one_item)  # wool lime
        x1=x1+3
        setSummon(start, t, x1, z1, 35, 6,    one_item)     # wool pink
        setRemove(start, t, x1, z2, "wool_pink", one_item)  # wool pink
        setDetect(start, t, x1, z3, "wool_pink", one_item)  # wool pink
        x1=x1+3
        setSummon(start, t, x1, z1, 35, 7,    one_item)     # wool gray
        setRemove(start, t, x1, z2, "wool_gray", one_item)  # wool gray
        setDetect(start, t, x1, z3, "wool_gray", one_item)  # wool gray
        x1=x1+3
        setSummon(start, t, x1, z1, 35, 8,    one_item)     # wool light gray
        setRemove(start, t, x1, z2, "wool_lgray", one_item)  # wool light gray
        setDetect(start, t, x1, z3, "wool_lgray", one_item)  # wool light gray
        x1=x1+3
        setSummon(start, t, x1, z1, 35, 9,    one_item)     # wool cyan
        setRemove(start, t, x1, z2, "wool_cyan", one_item)  # wool cyan
        setDetect(start, t, x1, z3, "wool_cyan", one_item)  # wool cyan
        x1=x1+3
        setSummon(start, t, x1, z1, 35, 10,    one_item)     # wool purple
        setRemove(start, t, x1, z2, "wool_purple", one_item)  # wool purple
        setDetect(start, t, x1, z3, "wool_purple", one_item)  # wool purple
        x1=x1+3
        setSummon(start, t, x1, z1, 35, 11,    one_item)     # wool blue
        setRemove(start, t, x1, z2, "wool_blue", one_item)  # wool blue
        setDetect(start, t, x1, z3, "wool_blue", one_item)  # wool blue
        x1=x1+3
        setSummon(start, t, x1, z1, 35, 12,    one_item)     # wool brown
        setRemove(start, t, x1, z2, "wool_brown", one_item)  # wool brown
        setDetect(start, t, x1, z3, "wool_brown", one_item)  # wool brown
        x1=x1+3
        setSummon(start, t, x1, z1, 35, 13,    one_item)     # wool green
        setRemove(start, t, x1, z2, "wool_green", one_item)  # wool green
        setDetect(start, t, x1, z3, "wool_green", one_item)  # wool green
        x1=x1+3
        setSummon(start, t, x1, z1, 35, 14,    one_item)     # wool red
        setRemove(start, t, x1, z2, "wool_red", one_item)  # wool red
        setDetect(start, t, x1, z3, "wool_red", one_item)  # wool red
        x1=x1+3
        setSummon(start, t, x1, z1, 35, 15,    one_item)     # wool black
        setRemove(start, t, x1, z2, "wool_black", one_item)  # wool black
        setDetect(start, t, x1, z3, "wool_black", one_item)  # wool black
        x1=x1+3
        setSummon(start, t, x1, z1, 50, 0,    one_item)     # torch
        setRemove(start, t, x1, z2, "torch", one_item)  # torch
        setDetect(start, t, x1, z3, "torch", one_item)  # torch
        x1=x1+3
        setSummon(start, t, x1, z1, 54, 0,    one_item)     # chest
        setRemove(start, t, x1, z2, "chest", one_item)  # chest
        setDetect(start, t, x1, z3, "chest", one_item)  # chest
        x1=x1+3
        setSummon(start, t, x1, z1, 146, 0,    one_item)     # trapped_chest
        setRemove(start, t, x1, z2, "trapped_chest", one_item)  # trapped_chest
        setDetect(start, t, x1, z3, "trapped_chest", one_item)  # trapped_chest
        x1=x1+3

#           (x=748, z=198)
#             | 
#             |
#             |   
#        ----   ----  
#        ----   ---*B (x=750, z=283)
#        ----   ----
#             |
#             |
#             |
        x1=2
        z1=75+19
        z2=76+19
        z3=72+19

        setSummon(start, t, x1, z1, 337, 0,    one_item)     # clay_ball
        setRemove(start, t, x1, z2, "clay_ball", one_item)  # clay_ball
        setDetect(start, t, x1, z3, "clay_ball", one_item)  # clay_ball
        x1=x1+3

        setSummon(start, t, x1, z1, 159, 0,    one_item)     # clay white
        setRemove(start, t, x1, z2, "clay_white", one_item)  # clay white
        setDetect(start, t, x1, z3, "clay_white", one_item)  # clay white
        x1=x1+3

        setSummon(start, t, x1, z1, 159, 1,    one_item)     # clay white
        setRemove(start, t, x1, z2, "clay_orange", one_item)  # clay orange
        setDetect(start, t, x1, z3, "clay_orange", one_item)  # clay orange
        x1=x1+3
        setSummon(start, t, x1, z1, 159, 2,    one_item)     # clay magenta
        setRemove(start, t, x1, z2, "clay_magenta", one_item)  # clay magenta
        setDetect(start, t, x1, z3, "clay_magenta", one_item)  # clay magenta
        x1=x1+3
        setSummon(start, t, x1, z1, 159, 3,    one_item)     # clay light blue
        setRemove(start, t, x1, z2, "clay_lblue", one_item)  # clay light blue
        setDetect(start, t, x1, z3, "clay_lblue", one_item)  # clay light blue
        x1=x1+3
        setSummon(start, t, x1, z1, 159, 4,    one_item)     # clay yellow
        setRemove(start, t, x1, z2, "clay_yellow", one_item)  # clay yellow
        setDetect(start, t, x1, z3, "clay_yellow", one_item)  # clay yellow
        x1=x1+3
        setSummon(start, t, x1, z1, 159, 5,    one_item)     # clay lime
        setRemove(start, t, x1, z2, "clay_lime", one_item)  # clay lime
        setDetect(start, t, x1, z3, "clay_lime", one_item)  # clay lime
        x1=x1+3
        setSummon(start, t, x1, z1, 159, 6,    one_item)     # clay pink
        setRemove(start, t, x1, z2, "clay_pink", one_item)  # clay pink
        setDetect(start, t, x1, z3, "clay_pink", one_item)  # clay pink
        x1=x1+3
        setSummon(start, t, x1, z1, 159, 7,    one_item)     # clay gray
        setRemove(start, t, x1, z2, "clay_gray", one_item)  # clay gray
        setDetect(start, t, x1, z3, "clay_gray", one_item)  # clay gray
        x1=x1+3
        setSummon(start, t, x1, z1, 159, 8,    one_item)     # clay light gray
        setRemove(start, t, x1, z2, "clay_lgray", one_item)  # clay light gray
        setDetect(start, t, x1, z3, "clay_lgray", one_item)  # clay light gray
        x1=x1+3
        setSummon(start, t, x1, z1, 159, 9,    one_item)     # clay cyan
        setRemove(start, t, x1, z2, "clay_cyan", one_item)  # clay cyan
        setDetect(start, t, x1, z3, "clay_cyan", one_item)  # clay cyan
        x1=x1+3
        setSummon(start, t, x1, z1, 159, 10,    one_item)     # clay purple
        setRemove(start, t, x1, z2, "clay_purple", one_item)  # clay purple
        setDetect(start, t, x1, z3, "clay_purple", one_item)  # clay purple
        x1=x1+3
        setSummon(start, t, x1, z1, 159, 11,    one_item)     # clay blue
        setRemove(start, t, x1, z2, "clay_blue", one_item)  # clay blue
        setDetect(start, t, x1, z3, "clay_blue", one_item)  # clay blue
        x1=x1+3
        setSummon(start, t, x1, z1, 159, 12,    one_item)     # clay brown
        setRemove(start, t, x1, z2, "clay_brown", one_item)  # clay brown
        setDetect(start, t, x1, z3, "clay_brown", one_item)  # clay brown
        x1=x1+3
        setSummon(start, t, x1, z1, 159, 13,    one_item)     # clay green
        setRemove(start, t, x1, z2, "clay_green", one_item)  # clay green
        setDetect(start, t, x1, z3, "clay_green", one_item)  # clay green
        x1=x1+3
        setSummon(start, t, x1, z1, 159, 14,    one_item)     # clay red
        setRemove(start, t, x1, z2, "clay_red", one_item)  # clay red
        setDetect(start, t, x1, z3, "clay_red", one_item)  # clay red
        x1=x1+3
        setSummon(start, t, x1, z1, 159, 15,    one_item)     # clay black
        setRemove(start, t, x1, z2, "clay_black", one_item)  # clay black
        setDetect(start, t, x1, z3, "clay_black", one_item)  # clay black
        x1=x1+3
        setSummon(start, t, x1, z1, 336, 0,    one_item)     # brick
        setRemove(start, t, x1, z2, "brick", one_item)  # brick
        setDetect(start, t, x1, z3, "brick", one_item)  # brick
        x1=x1+3
        setSummon(start, t, x1, z1, 324, 0,    one_item)     # wood_door
        setRemove(start, t, x1, z2, "wood_door", one_item)  # wood_door
        setDetect(start, t, x1, z3, "wood_door", one_item)  # wood_door
        x1=x1+3
        setSummon(start, t, x1, z1, 330, 0,    one_item)     # iron_door
        setRemove(start, t, x1, z2, "iron_door", one_item)  # iron_door
        setDetect(start, t, x1, z3, "iron_door", one_item)  # iron_door
        x1=x1+3

#           (x=748, z=198)
#             | 
#             |
#             |   
#        ----   ----  
#        ----   ----
#        ----   ---*T (x=750, z=302)
#             |
#             |
#             |
        x1=2
        z1=67+19+19
        z2=66+19+19
        z3=70+19+19

        setSummon(start, t, x1, z1, 37, 0,      one_item)   # dandelion
        setRemove(start, t, x1, z2, "dandelion", one_item)   # dandelion
        setDetect(start, t, x1, z3, "dandelion", one_item)   # dandelion
        x1=x1+3

        setSummon(start, t, x1, z1, 38, 0,   one_item)   # poppy
        setRemove(start, t, x1, z2, "poppy", one_item)   # poppy
        setDetect(start, t, x1, z3, "poppy", one_item)   # poppy
        x1=x1+3

        setSummon(start, t, x1, z1, 38, 1,   one_item)         # blue_orchid
        setRemove(start, t, x1, z2, "blue_orchid", one_item)   # blue_orchid
        setDetect(start, t, x1, z3, "blue_orchid", one_item)   # blue_orchid
        x1=x1+3

        setSummon(start, t, x1, z1, 38, 2,   one_item)         # allium
        setRemove(start, t, x1, z2, "allium", one_item)   # allium
        setDetect(start, t, x1, z3, "allium", one_item)   # allium
        x1=x1+3

        setSummon(start, t, x1, z1, 38, 3,   one_item)         # azure_bluet
        setRemove(start, t, x1, z2, "azure_bluet", one_item)   # azure_bluet
        setDetect(start, t, x1, z3, "azure_bluet", one_item)   # azure_bluet
        x1=x1+3

        setSummon(start, t, x1, z1, 38, 4,   one_item)         # red_tulip
        setRemove(start, t, x1, z2, "red_tulip", one_item)   # red_tulip
        setDetect(start, t, x1, z3, "red_tulip", one_item)   # red_tulip
        x1=x1+3

        setSummon(start, t, x1, z1, 38, 5,   one_item)         # orange_tulip
        setRemove(start, t, x1, z2, "orange_tulip", one_item)   # orange_tulip
        setDetect(start, t, x1, z3, "orange_tulip", one_item)   # orange_tulip
        x1=x1+3
        setSummon(start, t, x1, z1, 38, 6,   one_item)         # white_tulip
        setRemove(start, t, x1, z2, "white_tulip", one_item)   # white_tulip
        setDetect(start, t, x1, z3, "white_tulip", one_item)   # white_tulip
        x1=x1+3
        setSummon(start, t, x1, z1, 38, 7,   one_item)         # pink_tulip
        setRemove(start, t, x1, z2, "pink_tulip", one_item)   # pink_tulip
        setDetect(start, t, x1, z3, "pink_tulip", one_item)   # pink_tulip
        x1=x1+3
        setSummon(start, t, x1, z1, 38, 8,   one_item)         # oxeye_daisy
        setRemove(start, t, x1, z2, "oxeye_daisy", one_item)   # oxeye_daisy
        setDetect(start, t, x1, z3, "oxeye_daisy", one_item)   # oxeye_daisy
        x1=x1+3
        setSummon(start, t, x1, z1, 175, 0,   one_item)         # sunflower
        setRemove(start, t, x1, z2, "sunflower", one_item)   # sunflower
        setDetect(start, t, x1, z3, "sunflower", one_item)   # sunflower
        x1=x1+3
        setSummon(start, t, x1, z1, 175, 1,   one_item)         # lilac
        setRemove(start, t, x1, z2, "lilac", one_item)   # lilac
        setDetect(start, t, x1, z3, "lilac", one_item)   # lilac
        x1=x1+3
        setSummon(start, t, x1, z1, 175, 2,   one_item)         # fern
        setRemove(start, t, x1, z2, "fern", one_item)   # fern
        setDetect(start, t, x1, z3, "fern", one_item)   # fern
        x1=x1+3
        setSummon(start, t, x1, z1, 175, 4,   one_item)         # rose
        setRemove(start, t, x1, z2, "rose", one_item)   # rose
        setDetect(start, t, x1, z3, "rose", one_item)   # rose
        x1=x1+3
        setSummon(start, t, x1, z1, 175, 5,   one_item)         # peony
        setRemove(start, t, x1, z2, "peony", one_item)   # peony
        setDetect(start, t, x1, z3, "peony", one_item)   # peony
        x1=x1+3
        setSummon(start, t, x1, z1, 3, 2,   one_item)         # podzol
        setRemove(start, t, x1, z2, "podzol", one_item)   # podzol
        setDetect(start, t, x1, z3, "podzol", one_item)   # podzol
        x1=x1+3
        setSummon(start, t, x1, z1, 323, 0,   one_item)         # sign
        setRemove(start, t, x1, z2, "sign", one_item)   # sign
        setDetect(start, t, x1, z3, "sign", one_item)   # sign
        x1=x1+3
        setSummon(start, t, x1, z1, 280, 0,   one_item)         # stick
        setRemove(start, t, x1, z2, "stick", one_item)   # stick
        setDetect(start, t, x1, z3, "stick", one_item)   # stick
        x1=x1+3
        setSummon(start, t, x1, z1, 96, 0,   one_item)         # trapdoor
        setRemove(start, t, x1, z2, "trapdoor", one_item)   # trapdoor
        setDetect(start, t, x1, z3, "trapdoor", one_item)   # trapdoor
        x1=x1+3
        setSummon(start, t, x1, z1, 262, 0,   one_item)         # arrow
        setRemove(start, t, x1, z2, "arrow", one_item)   # arrow
        setDetect(start, t, x1, z3, "arrow", one_item)   # arrow
        x1=x1+3

#           (x=748, z=198)
#             | 
#             |
#             |   
#        ----   ----  
#        ----   ----
#        ----   ---*B (x=750, z=308)
#             |
#             |
#             |
        x1=2
        z1=75+19+19
        z2=76+19+19
        z3=72+19+19

        setSummon(start, t, x1, z1, 103, 0,      one_item)   # melon_block
        setRemove(start, t, x1, z2, "melon_block", one_item)   # melon_block
        setDetect(start, t, x1, z3, "melon_block", one_item)   # melon_block
        x1=x1+3
        setSummon(start, t, x1, z1, 360, 0,      one_item)   # melon
        setRemove(start, t, x1, z2, "melon", one_item)   # melon
        setDetect(start, t, x1, z3, "melon", one_item)   # melon
        x1=x1+3
        setSummon(start, t, x1, z1, 362, 0,      one_item)   # melon_seed
        setRemove(start, t, x1, z2, "melon_seed", one_item)   # melon_seed
        setDetect(start, t, x1, z3, "melon_seed", one_item)   # melon_seed
        x1=x1+3
        setSummon(start, t, x1, z1, 86, 0,      one_item)   # pumpkin
        setRemove(start, t, x1, z2, "pumpkin", one_item)   # pumpkin
        setDetect(start, t, x1, z3, "pumpkin", one_item)   # pumpkin
        x1=x1+3
        setSummon(start, t, x1, z1, 91, 0,      one_item)   # lit_pumpkin
        setRemove(start, t, x1, z2, "lit_pumpkin", one_item)   # lit_pumpkin
        setDetect(start, t, x1, z3, "lit_pumpkin", one_item)   # lit_pumpkin
        x1=x1+3
        setSummon(start, t, x1, z1, 361, 0,      one_item)   # pumpkin_seed
        setRemove(start, t, x1, z2, "pumpkin_seed", one_item)   # pumpkin_seed
        setDetect(start, t, x1, z3, "pumpkin_seed", one_item)   # pumpkin_seed
        x1=x1+3
        setSummon(start, t, x1, z1, 296, 0,      one_item)   # wheat
        setRemove(start, t, x1, z2, "wheat", one_item)   # wheat
        setDetect(start, t, x1, z3, "wheat", one_item)   # wheat
        x1=x1+3
        setSummon(start, t, x1, z1, 295, 0,      one_item)   # seed
        setRemove(start, t, x1, z2, "seed", one_item)   # seed
        setDetect(start, t, x1, z3, "seed", one_item)   # seed
        x1=x1+3
        setSummon(start, t, x1, z1, 170, 0,      one_item)   # hay_bale
        setRemove(start, t, x1, z2, "hay_bale", one_item)   # hay_bale
        setDetect(start, t, x1, z3, "hay_bale", one_item)   # hay_bale
        x1=x1+3
        setSummon(start, t, x1, z1, 392, 0,      one_item)   # potato
        setRemove(start, t, x1, z2, "potato", one_item)   # potato
        setDetect(start, t, x1, z3, "potato", one_item)   # potato
        x1=x1+3
        setSummon(start, t, x1, z1, 393, 0,      one_item)   # baked_potato
        setRemove(start, t, x1, z2, "baked_potato", one_item)   # baked_potato
        setDetect(start, t, x1, z3, "baked_potato", one_item)   # baked_potato
        x1=x1+3
        setSummon(start, t, x1, z1, 391, 0,      one_item)   # carrot
        setRemove(start, t, x1, z2, "carrot", one_item)   # carrot
        setDetect(start, t, x1, z3, "carrot", one_item)   # carrot
        x1=x1+3
        setSummon(start, t, x1, z1, 396, 0,      one_item)   # gold_carrot
        setRemove(start, t, x1, z2, "gold_carrot", one_item)   # gold_carrot
        setDetect(start, t, x1, z3, "gold_carrot", one_item)   # gold_carrot
        x1=x1+3
        setSummon(start, t, x1, z1, 260, 0,      one_item)   # apple
        setRemove(start, t, x1, z2, "apple", one_item)   # apple
        setDetect(start, t, x1, z3, "apple", one_item)   # apple
        x1=x1+3
        setSummon(start, t, x1, z1, 322, 0,      one_item)   # gold_apple
        setRemove(start, t, x1, z2, "gold_apple", one_item)   # gold_apple
        setDetect(start, t, x1, z3, "gold_apple", one_item)   # gold_apple
        x1=x1+3
        setSummon(start, t, x1, z1, 322, 1,      one_item)   # enhanced_gold_apple
        setRemove(start, t, x1, z2, "e_gold_apple", one_item)   # enhanced_gold_apple
        setDetect(start, t, x1, z3, "e_gold_apple", one_item)   # enhanced_gold_apple
        x1=x1+3
        setSummon(start, t, x1, z1, 344, 0,      one_item)   # egg
        setRemove(start, t, x1, z2, "egg", one_item)   # egg
        setDetect(start, t, x1, z3, "egg", one_item)   # egg
        x1=x1+3
        setSummon(start, t, x1, z1, 289, 0,      one_item)   # gunpowder
        setRemove(start, t, x1, z2, "gunpowder", one_item)   # gunpowder
        setDetect(start, t, x1, z3, "gunpowder", one_item)   # gunpowder
        x1=x1+3
        setSummon(start, t, x1, z1, 266, 0,      one_item)   # gold_ingot
        setRemove(start, t, x1, z2, "gold_ingot", one_item)   # gold_ingot
        setDetect(start, t, x1, z3, "gold_ingot", one_item)   # gold_ingot
        x1=x1+3
        setSummon(start, t, x1, z1, 371, 0,      one_item)   # gold_nuget
        setRemove(start, t, x1, z2, "gold_nuget", one_item)   # gold_nuget
        setDetect(start, t, x1, z3, "gold_nuget", one_item)   # gold_nuget
        x1=x1+3

#               (x=748, z=198)
#                      | 
#                      |
#                      |   
# (x=732, z=264) T*---   ----  
#                 ----   ----
#                 ----   ----
#                      |
#                      |
#                      |
        x1=-16
        z1=67
        z2=66
        z3=70

        setSummon(start, t, x1, z1, 363, 0,    some_item)     # raw_beef
        setRemove(start, t, x1, z2, "raw_beef", some_item)  # raw_beef
        setDetect(start, t, x1, z3, "raw_beef", some_item)  # raw_beef
        x1=x1-3
        setSummon(start, t, x1, z1, 364, 0,    some_item)     # steak
        setRemove(start, t, x1, z2, "steak", some_item)  # steak
        setDetect(start, t, x1, z3, "steak", some_item)  # steak
        x1=x1-3
        setSummon(start, t, x1, z1, 365, 0,    some_item)     # raw_chicken
        setRemove(start, t, x1, z2, "raw_chicken", some_item)  # raw_chicken
        setDetect(start, t, x1, z3, "raw_chicken", some_item)  # raw_chicken
        x1=x1-3
        setSummon(start, t, x1, z1, 366, 0,    some_item)     # cook_chicken
        setRemove(start, t, x1, z2, "cook_chicken", some_item)  # cook_chicken
        setDetect(start, t, x1, z3, "cook_chicken", some_item)  # cook_chicken
        x1=x1-3
        setSummon(start, t, x1, z1, 288, 0,    some_item)     # feather
        setRemove(start, t, x1, z2, "feather", some_item)  # feather
        setDetect(start, t, x1, z3, "feather", some_item)  # feather
        x1=x1-3
        setSummon(start, t, x1, z1, 319, 0,    some_item)     # raw_pork
        setRemove(start, t, x1, z2, "raw_pork", some_item)  # raw_pork
        setDetect(start, t, x1, z3, "raw_pork", some_item)  # raw_pork
        x1=x1-3
        setSummon(start, t, x1, z1, 320, 0,    some_item)     # cook_pork
        setRemove(start, t, x1, z2, "cook_pork", some_item)  # cook_pork
        setDetect(start, t, x1, z3, "cook_pork", some_item)  # cook_pork
        x1=x1-3
        setSummon(start, t, x1, z1, 349, 0,    some_item)     # raw_fish
        setRemove(start, t, x1, z2, "raw_fish", some_item)  # raw_fish
        setDetect(start, t, x1, z3, "raw_fish", some_item)  # raw_fish
        x1=x1-3
        setSummon(start, t, x1, z1, 349, 1,    some_item)     # raw_salmon
        setRemove(start, t, x1, z2, "raw_salmon", some_item)  # raw_salmon
        setDetect(start, t, x1, z3, "raw_salmon", some_item)  # raw_salmon
        x1=x1-3
        setSummon(start, t, x1, z1, 349, 2,    some_item)     # clownfish
        setRemove(start, t, x1, z2, "clownfish", some_item)  # clownfish
        setDetect(start, t, x1, z3, "clownfish", some_item)  # clownfish
        x1=x1-3
        setSummon(start, t, x1, z1, 349, 3,    some_item)     # pufferfish
        setRemove(start, t, x1, z2, "pufferfish", some_item)  # pufferfish
        setDetect(start, t, x1, z3, "pufferfish", some_item)  # pufferfish
        x1=x1-3
        setSummon(start, t, x1, z1, 39, 0,    some_item)     # brown_mushroom
        setRemove(start, t, x1, z2, "brown_mushroom", some_item)  # brown_mushroom
        setDetect(start, t, x1, z3, "brown_mushroom", some_item)  # brown_mushroom
        x1=x1-3
        setSummon(start, t, x1, z1, 40, 0,    some_item)     # red_mushroom
        setRemove(start, t, x1, z2, "red_mushroom", some_item)  # red_mushroom
        setDetect(start, t, x1, z3, "red_mushroom", some_item)  # red_mushroom
        x1=x1-3
        setSummon(start, t, x1, z1, 99, 0,    some_item)     # brown_mushroom_block
        setRemove(start, t, x1, z2, "b_mushroom_blk", some_item)  # brown_mushroom_block
        setDetect(start, t, x1, z3, "b_mushroom_blk", some_item)  # brown_mushroom_block
        x1=x1-3
        setSummon(start, t, x1, z1, 100, 0,    some_item)     # red_mushroom_block
        setRemove(start, t, x1, z2, "r_mushroom_blk", some_item)  # red_mushroom_block
        setDetect(start, t, x1, z3, "r_mushroom_blk", some_item)  # red_mushroom_block
        x1=x1-3
        setSummon(start, t, x1, z1, 123, 0,    some_item)     # redstone_lamp
        setRemove(start, t, x1, z2, "redstone_lamp", some_item)  # redstone_lamp
        setDetect(start, t, x1, z3, "redstone_lamp", some_item)  # redstone_lamp
        x1=x1-3
        setSummon(start, t, x1, z1, 348, 0,    some_item)     # glowstone_dust
        setRemove(start, t, x1, z2, "glowstone_dust", some_item)  # glowstone_dust
        setDetect(start, t, x1, z3, "glowstone_dust", some_item)  # glowstone_dust
        x1=x1-3
        setSummon(start, t, x1, z1, 369, 0,    some_item)     # blaze_rod
        setRemove(start, t, x1, z2, "blaze_rod", some_item)  # blaze_rod
        setDetect(start, t, x1, z3, "blaze_rod", some_item)  # blaze_rod
        x1=x1-3
        setSummon(start, t, x1, z1, 377, 0,    some_item)     # blaze_powder
        setRemove(start, t, x1, z2, "blaze_powder", some_item)  # blaze_powder
        setDetect(start, t, x1, z3, "blaze_powder", some_item)  # blaze_powder
        x1=x1-3
        setSummon(start, t, x1, z1, 420, 0,    some_item)     # lead
        setRemove(start, t, x1, z2, "lead", some_item)  # lead
        setDetect(start, t, x1, z3, "lead", some_item)  # lead
        x1=x1-3

#               (x=748, z=198)
#                      | 
#                      |
#                      |   
# (x=732, z=270) B*---   ----  
#                 ----   ----
#                 ----   ----
#                      |
#                      |
#                      |
        x1=-16
        z1=75
        z2=76
        z3=72

        setSummon(start, t, x1, z1, 351, 3,    one_item)     # cocoa
        setRemove(start, t, x1, z2, "cocoa", one_item)  # cocoa
        setDetect(start, t, x1, z3, "cocoa", one_item)  # cocoa
        x1=x1-3
        setSummon(start, t, x1, z1, 338, 0,    one_item)     # sugar_cane
        setRemove(start, t, x1, z2, "sugar_cane", one_item)  # sugar_cane
        setDetect(start, t, x1, z3, "sugar_cane", one_item)  # sugar_cane
        x1=x1-3
        setSummon(start, t, x1, z1, 353, 0,    one_item)     # sugar
        setRemove(start, t, x1, z2, "sugar", one_item)  # sugar
        setDetect(start, t, x1, z3, "sugar", one_item)  # sugar
        x1=x1-3
        setSummon(start, t, x1, z1, 339, 0,    one_item)     # paper
        setRemove(start, t, x1, z2, "paper", one_item)  # paper
        setDetect(start, t, x1, z3, "paper", one_item)  # paper
        x1=x1-3
        setSummon(start, t, x1, z1, 81, 0,    one_item)     # cactus
        setRemove(start, t, x1, z2, "cactus", one_item)  # cactus
        setDetect(start, t, x1, z3, "cactus", one_item)  # cactus
        x1=x1-3
        setSummon(start, t, x1, z1, 352, 0,    one_item)     # bone
        setRemove(start, t, x1, z2, "bone", one_item)  # bone
        setDetect(start, t, x1, z3, "bone", one_item)  # bone
        x1=x1-3
        setSummon(start, t, x1, z1, 351, 15,    one_item)     # bonemeal
        setRemove(start, t, x1, z2, "bonemeal", one_item)  # bonemeal
        setDetect(start, t, x1, z3, "bonemeal", one_item)  # bonemeal
        x1=x1-3
        setSummon(start, t, x1, z1, 350, 0,    one_item)     # cook_fish
        setRemove(start, t, x1, z2, "cook_fish", one_item)  # cook_fish
        setDetect(start, t, x1, z3, "cook_fish", one_item)  # cook_fish
        x1=x1-3
        setSummon(start, t, x1, z1, 350, 1,    one_item)     # cook_salmon
        setRemove(start, t, x1, z2, "cook_salmon", one_item)  # cook_salmon
        setDetect(start, t, x1, z3, "cook_salmon", one_item)  # cook_salmon
        x1=x1-3
        setSummon(start, t, x1, z1, 388, 0,    one_item)     # emerald
        setRemove(start, t, x1, z2, "emerald", one_item)  # emerald
        setDetect(start, t, x1, z3, "emerald", one_item)  # emerald
        x1=x1-3
        setSummon(start, t, x1, z1, 264, 0,    one_item)     # diamond
        setRemove(start, t, x1, z2, "diamond", one_item)  # diamond
        setDetect(start, t, x1, z3, "diamond", one_item)  # diamond
        x1=x1-3
        setSummon(start, t, x1, z1, 265, 0,    one_item)     # iron_ingot
        setRemove(start, t, x1, z2, "iron_ingot", one_item)  # iron_ingot
        setDetect(start, t, x1, z3, "iron_ingot", one_item)  # iron_ingot
        x1=x1-3
        setSummon(start, t, x1, z1, 331, 0,    one_item)     # redstone
        setRemove(start, t, x1, z2, "redstone", one_item)  # redstone
        setDetect(start, t, x1, z3, "redstone", one_item)  # redstone
        x1=x1-3
        setSummon(start, t, x1, z1, 263, 0,    one_item)     # coal
        setRemove(start, t, x1, z2, "coal", one_item)  # coal
        setDetect(start, t, x1, z3, "coal", one_item)  # coal
        x1=x1-3
        setSummon(start, t, x1, z1, 263, 1,    one_item)     # charcoal
        setRemove(start, t, x1, z2, "charcoal", one_item)  # charcoal
        setDetect(start, t, x1, z3, "charcoal", one_item)  # charcoal
        x1=x1-3
        setSummon(start, t, x1, z1, 173, 0,    one_item)     # coal_block
        setRemove(start, t, x1, z2, "coal_block", one_item)  # coal_block
        setDetect(start, t, x1, z3, "coal_block", one_item)  # coal_block
        x1=x1-3
        setSummon(start, t, x1, z1, 381, 0,    one_item)     # eye_of_ender
        setRemove(start, t, x1, z2, "eye_of_ender", one_item)  # eye_of_ender
        setDetect(start, t, x1, z3, "eye_of_ender", one_item)  # eye_of_ender
        x1=x1-3
        setSummon(start, t, x1, z1, 368, 0,    one_item)     # ender_pearl
        setRemove(start, t, x1, z2, "ender_pearl", one_item)  # ender_pearl
        setDetect(start, t, x1, z3, "ender_pearl", one_item)  # ender_pearl
        x1=x1-3
        setSummon(start, t, x1, z1, 341, 0,    one_item)     # slimeball
        setRemove(start, t, x1, z2, "slimeball", one_item)  # slimeball
        setDetect(start, t, x1, z3, "slimeball", one_item)  # slimeball
        x1=x1-3
        setSummon(start, t, x1, z1, 287, 0,    one_item)     # string
        setRemove(start, t, x1, z2, "string", one_item)  # string
        setDetect(start, t, x1, z3, "string", one_item)  # string
        x1=x1-3

#               (x=748, z=198)
#                      | 
#                      |
#                      |   
#                 ----   ----  
# (x=732, z=283) T*---   ----
#                 ----   ----
#                      |
#                      |
#                      |
        x1=-16
        z1=67+19
        z2=66+19
        z3=70+19

        setSummon(start, t, x1, z1, 378, 0,    one_item)     # magma_cream
        setRemove(start, t, x1, z2, "magma_cream", one_item)  # magma_cream
        setDetect(start, t, x1, z3, "magma_cream", one_item)  # magma_cream
        x1=x1-3
        setSummon(start, t, x1, z1, 325, 0,    one_item)     # bucket
        setRemove(start, t, x1, z2, "bucket", one_item)  # bucket
        setDetect(start, t, x1, z3, "bucket", one_item)  # bucket
        x1=x1-3
        setSummon(start, t, x1, z1, 335, 0,    one_item)     # bucket_milk
        setRemove(start, t, x1, z2, "bucket_milk", one_item)  # bucket_milk
        setDetect(start, t, x1, z3, "bucket_milk", one_item)  # bucket_milk
        x1=x1-3
        setSummon(start, t, x1, z1, 326, 0,    one_item)     # bucket_water
        setRemove(start, t, x1, z2, "bucket_water", one_item)  # bucket_water
        setDetect(start, t, x1, z3, "bucket_water", one_item)  # bucket_water
        x1=x1-3
        setSummon(start, t, x1, z1, 327, 0,    one_item)     # bucket_lava
        setRemove(start, t, x1, z2, "bucket_lava", one_item)  # bucket_lava
        setDetect(start, t, x1, z3, "bucket_lava", one_item)  # bucket_lava
        x1=x1-3
        setSummon(start, t, x1, z1, 372, 0,    one_item)     # nether_wart
        setRemove(start, t, x1, z2, "nether_wart", one_item)  # nether_wart
        setDetect(start, t, x1, z3, "nether_wart", one_item)  # nether_wart
        x1=x1-3
        setSummon(start, t, x1, z1, 370, 0,    one_item)     # ghast_tear
        setRemove(start, t, x1, z2, "ghast_tear", one_item)  # ghast_tear
        setDetect(start, t, x1, z3, "ghast_tear", one_item)  # ghast_tear
        x1=x1-3
        setSummon(start, t, x1, z1, 375, 0,    one_item)     # spider_eye
        setRemove(start, t, x1, z2, "spider_eye", one_item)  # spider_eye
        setDetect(start, t, x1, z3, "spider_eye", one_item)  # spider_eye
        x1=x1-3
        setSummon(start, t, x1, z1, 367, 0,    one_item)     # rotten_flesh
        setRemove(start, t, x1, z2, "rotten_flesh", one_item)  # rotten_flesh
        setDetect(start, t, x1, z3, "rotten_flesh", one_item)  # rotten_flesh
        x1=x1-3
        setSummon(start, t, x1, z1, 334, 0,    one_item)     # leather
        setRemove(start, t, x1, z2, "leather", one_item)  # leather
        setDetect(start, t, x1, z3, "leather", one_item)  # leather
        x1=x1-3
        setSummon(start, t, x1, z1, 389, 0,    one_item)     # item_frame
        setRemove(start, t, x1, z2, "item_frame", one_item)  # item_frame
        setDetect(start, t, x1, z3, "item_frame", one_item)  # item_frame
        x1=x1-3
        setSummon(start, t, x1, z1, 321, 0,    one_item)     # painting
        setRemove(start, t, x1, z2, "painting", one_item)  # painting
        setDetect(start, t, x1, z3, "painting", one_item)  # painting
        x1=x1-3
        setSummon(start, t, x1, z1, 332, 0,    one_item)     # snowball
        setRemove(start, t, x1, z2, "snowball", one_item)  # snowball
        setDetect(start, t, x1, z3, "snowball", one_item)  # snowball
        x1=x1-3
        setSummon(start, t, x1, z1, 80, 0,    one_item)     # snow
        setRemove(start, t, x1, z2, "snow", one_item)  # snow
        setDetect(start, t, x1, z3, "snow", one_item)  # snow
        x1=x1-3
        setSummon(start, t, x1, z1, 374, 0,    one_item)     # glass_bottle
        setRemove(start, t, x1, z2, "glass_bottle", one_item)  # glass_bottle
        setDetect(start, t, x1, z3, "glass_bottle", one_item)  # glass_bottle
        x1=x1-3
        setSummon(start, t, x1, z1, 318, 0,    one_item)     # flint
        setRemove(start, t, x1, z2, "flint", one_item)  # flint
        setDetect(start, t, x1, z3, "flint", one_item)  # flint
        x1=x1-3
        setSummon(start, t, x1, z1, 33, 0,    one_item)     # piston
        setRemove(start, t, x1, z2, "piston", one_item)  # piston
        setDetect(start, t, x1, z3, "piston", one_item)  # piston
        x1=x1-3
        setSummon(start, t, x1, z1, 29, 0,    one_item)     # sticky_piston
        setRemove(start, t, x1, z2, "sticky_piston", one_item)  # sticky_piston
        setDetect(start, t, x1, z3, "sticky_piston", one_item)  # sticky_piston
        x1=x1-3
        setSummon(start, t, x1, z1, 131, 0,    one_item)     # tripwire_hook
        setRemove(start, t, x1, z2, "tripwire_hook", one_item)  # tripwire_hook
        setDetect(start, t, x1, z3, "tripwire_hook", one_item)  # tripwire_hook
        x1=x1-3
        setSummon(start, t, x1, z1, 69, 0,    one_item)     # lever
        setRemove(start, t, x1, z2, "lever", one_item)  # lever
        setDetect(start, t, x1, z3, "lever", one_item)  # lever
        x1=x1-3

#               (x=748, z=198)
#                      | 
#                      |
#                      |   
#                 ----   ----  
# (x=732, z=289) B*---   ----
#                 ----   ----
#                      |
#                      |
#                      |
        x1=-16
        z1=75+19
        z2=76+19
        z3=72+19

        setSummon(start, t, x1, z1, 17, 0,    one_item)     # oak
        setRemove(start, t, x1, z2, "oak", one_item)  # oak
        setDetect(start, t, x1, z3, "oak", one_item)  # oak
        x1=x1-3
        setSummon(start, t, x1, z1, 17, 1,    one_item)     # spruce
        setRemove(start, t, x1, z2, "spruce", one_item)  # spruce
        setDetect(start, t, x1, z3, "spruce", one_item)  # spruce
        x1=x1-3
        setSummon(start, t, x1, z1, 17, 2,    one_item)     # birch
        setRemove(start, t, x1, z2, "birch", one_item)  # birch
        setDetect(start, t, x1, z3, "birch", one_item)  # birch
        x1=x1-3
        setSummon(start, t, x1, z1, 17, 3,    one_item)     # jungle
        setRemove(start, t, x1, z2, "jungle", one_item)  # jungle
        setDetect(start, t, x1, z3, "jungle", one_item)  # jungle
        x1=x1-3
        setSummon(start, t, x1, z1, 162, 0,    one_item)     # acacia
        setRemove(start, t, x1, z2, "acacia", one_item)  # acacia
        setDetect(start, t, x1, z3, "acacia", one_item)  # acacia
        x1=x1-3
        setSummon(start, t, x1, z1, 162, 1,    one_item)     # dark_oak
        setRemove(start, t, x1, z2, "dark_oak", one_item)  # dark_oak
        setDetect(start, t, x1, z3, "dark_oak", one_item)  # dark_oak
        x1=x1-3
        setSummon(start, t, x1, z1, 6, 0,    one_item)     # sapling_oak
        setRemove(start, t, x1, z2, "sapling_oak", one_item)  # sapling_oak
        setDetect(start, t, x1, z3, "sapling_oak", one_item)  # sapling_oak
        x1=x1-3
        setSummon(start, t, x1, z1, 6, 1,    one_item)     # sapling_spruce
        setRemove(start, t, x1, z2, "sapling_spruce", one_item)  # sapling_spruce
        setDetect(start, t, x1, z3, "sapling_spruce", one_item)  # sapling_spruce
        x1=x1-3
        setSummon(start, t, x1, z1, 6, 2,    one_item)     # sapling_birch
        setRemove(start, t, x1, z2, "sapling_birch", one_item)  # sapling_birch
        setDetect(start, t, x1, z3, "sapling_birch", one_item)  # sapling_birch
        x1=x1-3
        setSummon(start, t, x1, z1, 6, 3,    one_item)     # sapling_jungle
        setRemove(start, t, x1, z2, "sapling_jungle", one_item)  # sapling_jungle
        setDetect(start, t, x1, z3, "sapling_jungle", one_item)  # sapling_jungle
        x1=x1-3
        setSummon(start, t, x1, z1, 6, 4,    one_item)     # sapling_acacia
        setRemove(start, t, x1, z2, "sapling_acacia", one_item)  # sapling_acacia
        setDetect(start, t, x1, z3, "sapling_acacia", one_item)  # sapling_acacia
        x1=x1-3
        setSummon(start, t, x1, z1, 6, 5,    one_item)     # sapling_d_oak
        setRemove(start, t, x1, z2, "sapling_d_oak", one_item)  # sapling_d_oak
        setDetect(start, t, x1, z3, "sapling_d_oak", one_item)  # sapling_d_oak
        x1=x1-3
        setSummon(start, t, x1, z1, 5, 0,    one_item)     # planks_oak
        setRemove(start, t, x1, z2, "planks_oak", one_item)  # planks_oak
        setDetect(start, t, x1, z3, "planks_oak", one_item)  # planks_oak
        x1=x1-3
        setSummon(start, t, x1, z1, 5, 1,    one_item)     # planks_spruce
        setRemove(start, t, x1, z2, "planks_spruce", one_item)  # planks_spruce
        setDetect(start, t, x1, z3, "planks_spruce", one_item)  # planks_spruce
        x1=x1-3
        setSummon(start, t, x1, z1, 5, 2,    one_item)     # planks_birch
        setRemove(start, t, x1, z2, "planks_birch", one_item)  # planks_birch
        setDetect(start, t, x1, z3, "planks_birch", one_item)  # planks_birch
        x1=x1-3
        setSummon(start, t, x1, z1, 5, 3,    one_item)     # planks_jungle
        setRemove(start, t, x1, z2, "planks_jungle", one_item)  # planks_jungle
        setDetect(start, t, x1, z3, "planks_jungle", one_item)  # planks_jungle
        x1=x1-3
        setSummon(start, t, x1, z1, 5, 4,    one_item)     # planks_acacia
        setRemove(start, t, x1, z2, "planks_acacia", one_item)  # planks_acacia
        setDetect(start, t, x1, z3, "planks_acacia", one_item)  # planks_acacia
        x1=x1-3
        setSummon(start, t, x1, z1, 5, 5,    one_item)     # sapling_d_oak
        setRemove(start, t, x1, z2, "planks_dark_oak", one_item)  # planks_dark_oak
        setDetect(start, t, x1, z3, "planks_dark_oak", one_item)  # planks_dark_oak
        x1=x1-3
        setSummon(start, t, x1, z1, 76, 0,    one_item)     # redstone_torch
        setRemove(start, t, x1, z2, "redstone_torch", one_item)  # redstone_torch
        setDetect(start, t, x1, z3, "redstone_torch", one_item)  # redstone_torch
        x1=x1-3
        setSummon(start, t, x1, z1, 46, 0,    one_item)     # TNT
        setRemove(start, t, x1, z2, "TNT", one_item)  # TNT
        setDetect(start, t, x1, z3, "TNT", one_item)  # TNT
        x1=x1-3

#               (x=748, z=198)
#                      | 
#                      |
#                      |   
#                 ----   ----  
#                 ----   ----
# (x=732, z=302) T*---   ----
#                      |
#                      |
#                      |
        x1=-16
        z1=67+19+19
        z2=66+19+19
        z3=70+19+19

        setSummon(start, t, x1, z1, 356, 0,    one_item)     # repeater
        setRemove(start, t, x1, z2, "repeater", one_item)  # repeater
        setDetect(start, t, x1, z3, "repeater", one_item)  # repeater
        x1=x1-3
        setSummon(start, t, x1, z1, 404, 0,    one_item)     # comparator
        setRemove(start, t, x1, z2, "comparator", one_item)  # comparator
        setDetect(start, t, x1, z3, "comparator", one_item)  # comparator
        x1=x1-3
        setSummon(start, t, x1, z1, 77, 0,    one_item)     # button_stone
        setRemove(start, t, x1, z2, "button_stone", one_item)  # button_stone
        setDetect(start, t, x1, z3, "button_stone", one_item)  # button_stone
        x1=x1-3
        setSummon(start, t, x1, z1, 143, 0,    one_item)     # button_wood
        setRemove(start, t, x1, z2, "button_wood", one_item)  # button_wood
        setDetect(start, t, x1, z3, "button_wood", one_item)  # button_wood
        x1=x1-3
        setSummon(start, t, x1, z1, 72, 0,    one_item)     # pressure_wood
        setRemove(start, t, x1, z2, "pressure_wood", one_item)  # pressure_wood
        setDetect(start, t, x1, z3, "pressure_wood", one_item)  # pressure_wood
        x1=x1-3
        setSummon(start, t, x1, z1, 70, 0,    one_item)     # pressure_stone
        setRemove(start, t, x1, z2, "pressure_stone", one_item)  # pressure_stone
        setDetect(start, t, x1, z3, "pressure_stone", one_item)  # pressure_stone
        x1=x1-3
        setSummon(start, t, x1, z1, 147, 0,    one_item)     # pressure_gold
        setRemove(start, t, x1, z2, "pressure_gold", one_item)  # pressure_gold
        setDetect(start, t, x1, z3, "pressure_gold", one_item)  # pressure_gold
        x1=x1-3
        setSummon(start, t, x1, z1, 148, 0,    one_item)     # pressure_iron
        setRemove(start, t, x1, z2, "pressure_iron", one_item)  # pressure_iron
        setDetect(start, t, x1, z3, "pressure_iron", one_item)  # pressure_iron
        x1=x1-3
        setSummon(start, t, x1, z1, 66, 0,    one_item)     # test
        setRemove(start, t, x1, z2, "rail", one_item)  # test
        setDetect(start, t, x1, z3, "rail", one_item)  # test
        x1=x1-3
        setSummon(start, t, x1, z1, 27, 0,    one_item)     # test
        setRemove(start, t, x1, z2, "powered_rail", one_item)  # test
        setDetect(start, t, x1, z3, "powered_rail", one_item)  # test
        x1=x1-3
        setSummon(start, t, x1, z1, 28, 0,    one_item)     # test
        setRemove(start, t, x1, z2, "detector_rail", one_item)  # test
        setDetect(start, t, x1, z3, "detector_rail", one_item)  # test
        x1=x1-3
        setSummon(start, t, x1, z1, 157, 0,    one_item)     # test
        setRemove(start, t, x1, z2, "activator_rail", one_item)  # test
        setDetect(start, t, x1, z3, "activator_rail", one_item)  # test
        x1=x1-3
        setSummon(start, t, x1, z1, 328, 0,    one_item)     # minecart
        setRemove(start, t, x1, z2, "minecart", one_item)  # minecart
        setDetect(start, t, x1, z3, "minecart", one_item)  # minecart
        x1=x1-3
        setSummon(start, t, x1, z1, 65, 0,    one_item)     # ladder
        setRemove(start, t, x1, z2, "ladder", one_item)  # ladder
        setDetect(start, t, x1, z3, "ladder", one_item)  # ladder
        x1=x1-3
        setSummon(start, t, x1, z1, -1, 0,    one_item)     # test
        setRemove(start, t, x1, z2, "test", one_item)  # test
        setDetect(start, t, x1, z3, "test", one_item)  # test
        x1=x1-3
        setSummon(start, t, x1, z1, -1, 0,    one_item)     # test
        setRemove(start, t, x1, z2, "test", one_item)  # test
        setDetect(start, t, x1, z3, "test", one_item)  # test
        x1=x1-3
        setSummon(start, t, x1, z1, -1, 0,    one_item)     # test
        setRemove(start, t, x1, z2, "test", one_item)  # test
        setDetect(start, t, x1, z3, "test", one_item)  # test
        x1=x1-3
        setSummon(start, t, x1, z1, -1, 0,    one_item)     # test
        setRemove(start, t, x1, z2, "test", one_item)  # test
        setDetect(start, t, x1, z3, "test", one_item)  # test
        x1=x1-3
        setSummon(start, t, x1, z1, -1, 0,    one_item)     # test
        setRemove(start, t, x1, z2, "test", one_item)  # test
        setDetect(start, t, x1, z3, "test", one_item)  # test
        x1=x1-3
        setSummon(start, t, x1, z1, -1, 0,    one_item)     # test
        setRemove(start, t, x1, z2, "test", one_item)  # test
        setDetect(start, t, x1, z3, "test", one_item)  # test
        x1=x1-3

#               (x=748, z=198)
#                      | 
#                      |
#                      |   
#                 ----   ----  
#                 ----   ----
# (x=732, z=308) B*---   ----
#                      |
#                      |
#                      |
        x1=-16
        z1=75+19+19
        z2=76+19+19
        z3=72+19+19

        setSummon(start, t, x1, z1, -1, 0,  one_item)     # test
        setRemove(start, t, x1, z2, "test", one_item)  # test
        setDetect(start, t, x1, z3, "test", one_item)  # test
        x1=x1-3
        setSummon(start, t, x1, z1, -1, 0,  one_item)     # test
        setRemove(start, t, x1, z2, "test", one_item)  # test
        setDetect(start, t, x1, z3, "test", one_item)  # test
        x1=x1-3
        setSummon(start, t, x1, z1, -1, 0,  one_item)     # test
        setRemove(start, t, x1, z2, "test", one_item)  # test
        setDetect(start, t, x1, z3, "test", one_item)  # test
        x1=x1-3
        setSummon(start, t, x1, z1, -1, 0,  one_item)     # test
        setRemove(start, t, x1, z2, "test", one_item)  # test
        setDetect(start, t, x1, z3, "test", one_item)  # test
        x1=x1-3
        setSummon(start, t, x1, z1, -1, 0,  one_item)     # test
        setRemove(start, t, x1, z2, "test", one_item)  # test
        setDetect(start, t, x1, z3, "test", one_item)  # test
        x1=x1-3
        setSummon(start, t, x1, z1, -1, 0,  one_item)     # test
        setRemove(start, t, x1, z2, "test", one_item)  # test
        setDetect(start, t, x1, z3, "test", one_item)  # test
        x1=x1-3
        setSummon(start, t, x1, z1, -1, 0,  one_item)     # test
        setRemove(start, t, x1, z2, "test", one_item)  # test
        setDetect(start, t, x1, z3, "test", one_item)  # test
        x1=x1-3
        setSummon(start, t, x1, z1, -1, 0,  one_item)     # test
        setRemove(start, t, x1, z2, "test", one_item)  # test
        setDetect(start, t, x1, z3, "test", one_item)  # test
        x1=x1-3
        setSummon(start, t, x1, z1, -1, 0,  one_item)     # test
        setRemove(start, t, x1, z2, "test", one_item)  # test
        setDetect(start, t, x1, z3, "test", one_item)  # test
        x1=x1-3
        setSummon(start, t, x1, z1, -1, 0,  one_item)     # test
        setRemove(start, t, x1, z2, "test", one_item)  # test
        setDetect(start, t, x1, z3, "test", one_item)  # test
        x1=x1-3
        setSummon(start, t, x1, z1, -1, 0,  one_item)     # test
        setRemove(start, t, x1, z2, "test", one_item)  # test
        setDetect(start, t, x1, z3, "test", one_item)  # test
        x1=x1-3
        setSummon(start, t, x1, z1, -1, 0,  one_item)     # test
        setRemove(start, t, x1, z2, "test", one_item)  # test
        setDetect(start, t, x1, z3, "test", one_item)  # test
        x1=x1-3
        setSummon(start, t, x1, z1, -1, 0,  one_item)     # test
        setRemove(start, t, x1, z2, "test", one_item)  # test
        setDetect(start, t, x1, z3, "test", one_item)  # test
        x1=x1-3
        setSummon(start, t, x1, z1, -1, 0,  one_item)     # test
        setRemove(start, t, x1, z2, "test", one_item)  # test
        setDetect(start, t, x1, z3, "test", one_item)  # test
        x1=x1-3
        setSummon(start, t, x1, z1, -1, 0,  one_item)     # test
        setRemove(start, t, x1, z2, "test", one_item)  # test
        setDetect(start, t, x1, z3, "test", one_item)  # test
        x1=x1-3
        setSummon(start, t, x1, z1, -1, 0,  one_item)     # test
        setRemove(start, t, x1, z2, "test", one_item)  # test
        setDetect(start, t, x1, z3, "test", one_item)  # test
        x1=x1-3
        setSummon(start, t, x1, z1, -1, 0,  one_item)     # test
        setRemove(start, t, x1, z2, "test", one_item)  # test
        setDetect(start, t, x1, z3, "test", one_item)  # test
        x1=x1-3
        setSummon(start, t, x1, z1, -1, 0,  one_item)     # test
        setRemove(start, t, x1, z2, "test", one_item)  # test
        setDetect(start, t, x1, z3, "test", one_item)  # test
        x1=x1-3
        setSummon(start, t, x1, z1, -1, 0,  one_item)     # test
        setRemove(start, t, x1, z2, "test", one_item)  # test
        setDetect(start, t, x1, z3, "test", one_item)  # test
        x1=x1-3
        setSummon(start, t, x1, z1, -1, 0,  one_item)     # test
        setRemove(start, t, x1, z2, "test", one_item)  # test
        setDetect(start, t, x1, z3, "test", one_item)  # test
        x1=x1-3

#  "z": TAG_Int(198),
#  "y": TAG_Int(9),
#  "x": TAG_Int(748),

world1.saveInPlace();

#/scoreboard players remove @p grass 20
#/summon Item ~ ~5 ~ {Item:{id:2,Count:20}}
#/testfor @p[score_grass_min=20,r=6]

################################################################################
# Program Bank Counting System
################################################################################

def setCMDBlock(count, start, t, x_offset, y_offset, item1, id1, subid1, item2, id2, subid2):
   x = -5 - x_offset
   z1 = 1
   z2 = 9
   y = 0 - y_offset

   if len(item1) > 16: 
      raise ErrorWithCode(1)
   if len(item2) > 16:
      raise ErrorWithCode(2)

   if t["x"].value == (start["x"].value+x_offset) and t["z"].value == (start["z"].value-3) and t["y"].value == (start["y"].value+y_offset):
       t["Command"] = TAG_String("/scoreboard players add @r "+item1+" 1")
       print "B: "+t["CustomName"].value + ": " + str(t["x"].value) + "," + str(t["y"].value) + "," + str(t["z"].value) + "  - " + t["Command"].value
   if t["x"].value == (start["x"].value+x_offset) and t["z"].value == (start["z"].value-5) and t["y"].value == (start["y"].value+y_offset):
       t["Command"] = TAG_String("/scoreboard objectives add "+item1+" dummy")
       print "B: "+t["CustomName"].value + ": " + str(t["x"].value) + "," + str(t["y"].value) + "," + str(t["z"].value) + "  - " + t["Command"].value
   if t["x"].value == (start["x"].value+x_offset) and t["z"].value == (start["z"].value-7) and t["y"].value == (start["y"].value+y_offset):
       t["Command"] = TAG_String("/testforblock ~"+str(x)+" ~"+str(y)+" ~"+str(z1)+" dropper 1 {Items:[0:{Slot:0b,id:"+id1+"s,Damage:"+subid1+"s,Count:1b}]}")
       print "B: "+t["CustomName"].value + ": " + str(t["x"].value) + "," + str(t["y"].value) + "," + str(t["z"].value) + "  - " + t["Command"].value

   if t["x"].value == (start["x"].value+x_offset) and t["z"].value == (start["z"].value-19) and t["y"].value == (start["y"].value+y_offset):
       t["Command"] = TAG_String("/scoreboard players add @r "+item2+" 1")
       print "B: "+t["CustomName"].value + ": " + str(t["x"].value) + "," + str(t["y"].value) + "," + str(t["z"].value) + "  - " + t["Command"].value
   if t["x"].value == (start["x"].value+x_offset) and t["z"].value == (start["z"].value-17) and t["y"].value == (start["y"].value+y_offset):
       t["Command"] = TAG_String("/scoreboard objectives add "+item2+" dummy")
       print "B: "+t["CustomName"].value + ": " + str(t["x"].value) + "," + str(t["y"].value) + "," + str(t["z"].value) + "  - " + t["Command"].value
   if t["x"].value == (start["x"].value+x_offset) and t["z"].value == (start["z"].value-15) and t["y"].value == (start["y"].value+y_offset):
       t["Command"] = TAG_String("/testforblock ~"+str(x)+" ~"+str(y)+" ~"+str(z2)+" dropper 1 {Items:[0:{Slot:0b,id:"+id2+"s,Damage:"+subid2+"s,Count:1b}]}")
       print "B: "+t["CustomName"].value + ": " + str(t["x"].value) + "," + str(t["y"].value) + "," + str(t["z"].value) + "  - " + t["Command"].value


count=0
# Locate Start Block(s)
for (xPos, zPos) in chunkPositions:
    chunk = world1.getChunk(xPos, zPos)
    for t in chunk.TileEntities:
      if t["id"].value == "Control" and t["Command"].value == "START-BLOCK":
          count=count+1
          start = t
          Start_xPos = xPos
          Start_zPos = zPos
          print "Detected start block at: " + str(xPos) + " " + str(zPos) +" : x="+str(start["x"].value)+",y="+str(start["y"].value)+",z="+str(start["z"].value)

          for (xPos, zPos) in chunkPositions:
            if xPos >= Start_xPos and zPos <= Start_zPos and xPos < (Start_xPos +3) and zPos > (Start_zPos -2):
              chunk = world1.getChunk(xPos, zPos)
              chunk.chunkChanged();
              for t in chunk.TileEntities:
                if t["id"].value == "Control":
                  if t["y"].value >= (start["y"].value-3) and t["y"].value <= (start["y"].value+13) and t["x"].value < start["x"].value and t["x"].value > (start["x"].value-12) and t["z"].value <= start["z"].value and t["z"].value >= (start["z"].value-22):
                     pattern  = re.compile(r"minecraft[:](bedrock|air)")
                     pattern2 = re.compile(r"hopper[ ]4")
                     pattern3 = re.compile(r"hopper[ ]2")
                     
                     if pattern.search(t["Command"].value):
                       t["CustomName"] = TAG_String("Counter-"+str(count)+"-door")
                     elif pattern2.search(t["Command"].value):
                       t["CustomName"] = TAG_String("Counter-"+str(count)+"-U")
                     elif pattern3.search(t["Command"].value):
                       t["CustomName"] = TAG_String("Counter-"+str(count)+"-K")
                     else:
                       t["CustomName"] = TAG_String("Counter-"+str(count))
      
                     print "O: "+t["CustomName"].value + ": " + str(t["x"].value) + "," + str(t["y"].value) + "," + str(t["z"].value) + "  - " + t["Command"].value
                
                  if t["y"].value >= start["y"].value and t["y"].value <= (start["y"].value+13) and t["x"].value >= start["x"].value and t["x"].value <= (start["x"].value+39) and t["z"].value <= start["z"].value and t["z"].value >= (start["z"].value-22):
                     t["CustomName"] = TAG_String("Counter-"+str(count))

                     # Row 1
                     setCMDBlock(count, start, t, 0,  0, "stone",          "1",   "0",  "grass",           "2",   "0")
                     setCMDBlock(count, start, t, 2,  0, "dirt",           "3",   "0",  "cobblestone",     "4",   "0")
                     setCMDBlock(count, start, t, 4,  0, "sandstone",      "24",  "0",  "gold_ore",        "14",  "0")
                     setCMDBlock(count, start, t, 6,  0, "c_sandstone",    "24",  "1",  "iron_ore",        "15",  "0")
                     setCMDBlock(count, start, t, 8,  0, "s_sandstone",    "24",  "2",  "diamond_ore",     "56",  "0")
                     setCMDBlock(count, start, t, 10, 0, "sand",           "12",  "0",  "redstone_ore",    "73",  "0")
                     setCMDBlock(count, start, t, 12, 0, "red_sand",       "12",  "1",  "emerald_ore",     "129", "0")
                     setCMDBlock(count, start, t, 14, 0, "dirt",           "3",   "0",  "quartz_ore",      "153", "0")
                     setCMDBlock(count, start, t, 16, 0, "dirt",           "3",   "0",  "coal_ore",        "16",  "0")
                     setCMDBlock(count, start, t, 18, 0, "cobblestone_w",  "139", "0",  "gold_block",      "41",  "0")
                     setCMDBlock(count, start, t, 20, 0, "stone_slab",     "44",  "0",  "iron_block",      "42",  "0")
                     setCMDBlock(count, start, t, 22, 0, "mos_cobblestone","48",  "0",  "brick_block",     "45",  "0")
                     setCMDBlock(count, start, t, 24, 0, "glowstone",      "89",  "0",  "diamond_block",   "57",  "0")
                     setCMDBlock(count, start, t, 26, 0, "stonebrick",     "98",  "0",  "emerald_block",   "133", "0")
                     setCMDBlock(count, start, t, 28, 0, "fence_gate",     "107", "0",  "redstone_block",  "152", "0")
                     setCMDBlock(count, start, t, 30, 0, "fence",          "85",  "0",  "quartz_block",    "155", "0")
                     setCMDBlock(count, start, t, 32, 0, "clay",           "82",  "0",  "quartz_stairs",   "156", "0")
                     setCMDBlock(count, start, t, 34, 0, "ice",            "79",  "0",  "lapis_ore",       "21",  "0")
                     setCMDBlock(count, start, t, 36, 0, "mycelium",       "110", "0",  "lapis_block",     "22",  "0")
                     setCMDBlock(count, start, t, 38, 0, "soul_sand",      "88",  "0",  "netherrack",      "87",  "0")
           
                     # Row 2
                     setCMDBlock(count, start, t, 0,  2, "glass",          "20",  "0",  "glass_pane",      "102", "0") #1
                     setCMDBlock(count, start, t, 2,  2, "glass_white",    "95",  "0",  "glass_p_white",   "160", "0") #2
                     setCMDBlock(count, start, t, 4,  2, "glass_orange",   "95",  "1",  "glass_p_orange",  "160", "1") #3
                     setCMDBlock(count, start, t, 6,  2, "glass_magenta",  "95",  "2",  "glass_p_magenta", "160", "2") #4
                     setCMDBlock(count, start, t, 8,  2, "glass_lblue",    "95",  "3",  "glass_p_lblue",   "160", "3") #5
                     setCMDBlock(count, start, t, 10, 2, "glass_yellow",   "95",  "4",  "glass_p_yellow",  "160", "4") #6
                     setCMDBlock(count, start, t, 12, 2, "glass_lime",     "95",  "5",  "glass_p_lime",    "160", "5") #7
                     setCMDBlock(count, start, t, 14, 2, "glass_pink",     "95",  "6",  "glass_p_pink",    "160", "6") #8
                     setCMDBlock(count, start, t, 16, 2, "glass_gray",     "95",  "7",  "glass_p_gray",    "160", "7") #9
                     setCMDBlock(count, start, t, 18, 2, "glass_lgray",    "95",  "8",  "glass_p_lgray",   "160", "8") #10
                     setCMDBlock(count, start, t, 20, 2, "glass_cyan",     "95",  "9",  "glass_p_cyan",    "160", "9") #11
                     setCMDBlock(count, start, t, 22, 2, "glass_purple",   "95",  "10", "glass_p_purple",  "160", "10") #12
                     setCMDBlock(count, start, t, 24, 2, "glass_blue",     "95",  "11", "glass_p_blue",    "160", "11") #13
                     setCMDBlock(count, start, t, 26, 2, "glass_brown",    "95",  "12", "glass_p_brown",   "160", "12") #14
                     setCMDBlock(count, start, t, 28, 2, "glass_green",    "95",  "13", "glass_p_green",   "160", "13") #15
                     setCMDBlock(count, start, t, 30, 2, "glass_red",      "95",  "14", "glass_p_red",     "160", "14") #16
                     setCMDBlock(count, start, t, 32, 2, "glass_black",    "95",  "15", "glass_p_black",   "160", "15") #17
                     setCMDBlock(count, start, t, 34, 2, "iron_bars",      "101", "0",  "bookshelf",       "47",  "0") #18
                     setCMDBlock(count, start, t, 36, 2, "waterlily",      "111", "0",  "dropper",         "158", "0") #19
                     setCMDBlock(count, start, t, 38, 2, "hopper",         "154", "0",  "dispenser",       "23",  "0") #20
           
                     # Row 3
                     setCMDBlock(count, start, t, 0,  4, "obsidian",       "49",  "0",  "clay_ball",    "337", "0") #1
                     setCMDBlock(count, start, t, 2,  4, "wool_white",     "35",  "0",  "clay_white",   "159", "0") #2
                     setCMDBlock(count, start, t, 4,  4, "wool_orange",    "35",  "1",  "clay_orange",  "159", "1") #3
                     setCMDBlock(count, start, t, 6,  4, "wool_magenta",   "35",  "2",  "clay_magenta", "159", "2") #4
                     setCMDBlock(count, start, t, 8,  4, "wool_lblue",     "35",  "3",  "clay_lblue",   "159", "3") #5
                     setCMDBlock(count, start, t, 10, 4, "wool_yellow",    "35",  "4",  "clay_yellow",  "159", "4") #6
                     setCMDBlock(count, start, t, 12, 4, "wool_lime",      "35",  "5",  "clay_lime",    "159", "5") #7
                     setCMDBlock(count, start, t, 14, 4, "wool_pink",      "35",  "6",  "clay_pink",    "159", "6") #8
                     setCMDBlock(count, start, t, 16, 4, "wool_gray",      "35",  "7",  "clay_gray",    "159", "7") #9
                     setCMDBlock(count, start, t, 18, 4, "wool_lgray",     "35",  "8",  "clay_lgray",   "159", "8") #10
                     setCMDBlock(count, start, t, 20, 4, "wool_cyan",      "35",  "9",  "clay_cyan",    "159", "9") #11
                     setCMDBlock(count, start, t, 22, 4, "wool_purple",    "35",  "10", "clay_purple",  "159", "10") #12
                     setCMDBlock(count, start, t, 24, 4, "wool_blue",      "35",  "11", "clay_blue",    "159", "11") #13
                     setCMDBlock(count, start, t, 26, 4, "wool_brown",     "35",  "12", "clay_brown",   "159", "12") #14
                     setCMDBlock(count, start, t, 28, 4, "wool_green",     "35",  "13", "clay_green",   "159", "13") #15
                     setCMDBlock(count, start, t, 30, 4, "wool_red",       "35",  "14", "clay_red",     "159", "14") #16
                     setCMDBlock(count, start, t, 32, 4, "wool_black",     "35",  "15", "clay_black",   "159", "15") #17
                     setCMDBlock(count, start, t, 34, 4, "torch",          "50",  "0",  "brick",        "336", "0") #18
                     setCMDBlock(count, start, t, 36, 4, "chest",          "54",  "0",  "wood_door",    "324",  "0") #19
                     setCMDBlock(count, start, t, 38, 4, "trapped_chest",  "146", "0",  "iron_door",    "330",  "0") #20
           
                     # Row 4
                     setCMDBlock(count, start, t, 0,  6, "dandelion",      "37",  "0",  "melon_block",  "103", "0") #1
                     setCMDBlock(count, start, t, 2,  6, "poppy",          "38",  "0",  "melon",        "360", "0") #2
                     setCMDBlock(count, start, t, 4,  6, "blue_orchid",    "38",  "1",  "melon_seed",   "362", "0") #3
                     setCMDBlock(count, start, t, 6,  6, "allium",         "38",  "2",  "pumpkin",      "86", "0") #4
                     setCMDBlock(count, start, t, 8,  6, "azure_bluet",    "38",  "3",  "lit_pumpkin",  "91", "0") #5
                     setCMDBlock(count, start, t, 10, 6, "red_tulip",      "38",  "4",  "pumpkin_seed", "361", "0") #6
                     setCMDBlock(count, start, t, 12, 6, "orange_tulip",   "38",  "5",  "wheat",        "296", "0") #7
                     setCMDBlock(count, start, t, 14, 6, "white_tulip",    "38",  "6",  "seed",         "295", "0") #8
                     setCMDBlock(count, start, t, 16, 6, "pink_tulip",     "38",  "7",  "hay_bale",     "170", "0") #9
                     setCMDBlock(count, start, t, 18, 6, "oxeye_daisy",    "38",  "8",  "potato",       "392", "0") #10
                     setCMDBlock(count, start, t, 20, 6, "sunflower",      "175", "0",  "baked_potato", "393", "0") #11
                     setCMDBlock(count, start, t, 22, 6, "lilac",          "175", "1",  "carrot",       "391", "0") #12
                     setCMDBlock(count, start, t, 24, 6, "fern",           "175", "2",  "gold_carrot",  "396", "0") #13
                     setCMDBlock(count, start, t, 26, 6, "rose",           "175", "4",  "apple",        "260", "0") #14
                     setCMDBlock(count, start, t, 28, 6, "peony",          "175", "5",  "gold_apple",   "322", "0") #15
                     setCMDBlock(count, start, t, 30, 6, "podzol",         "3",   "2",  "e_gold_apple", "322", "1") #16
                     setCMDBlock(count, start, t, 32, 6, "sign",           "323", "0",  "egg",          "344", "0") #17
                     setCMDBlock(count, start, t, 34, 6, "stick",          "280", "0",  "gunpowder",    "289", "0") #18
                     setCMDBlock(count, start, t, 36, 6, "trapdoor",       "96",  "0",  "gold_ingot",   "266", "0") #19
                     setCMDBlock(count, start, t, 38, 6, "arrow",          "262", "0",  "gold_nuget",   "371", "0") #20

                     # Row 5
                     setCMDBlock(count, start, t, 0,  8, "raw_beef",       "363", "0",  "cocoa",         "351", "3")
                     setCMDBlock(count, start, t, 2,  8, "steak",          "364", "0",  "sugar_cane",    "338", "0")
                     setCMDBlock(count, start, t, 4,  8, "raw_chicken",    "365", "0",  "sugar",         "353", "0")
                     setCMDBlock(count, start, t, 6,  8, "cook_chicken",   "366", "0",  "paper",         "339", "0")
                     setCMDBlock(count, start, t, 8,  8, "feather",        "288", "0",  "cactus",        "81",  "0")
                     setCMDBlock(count, start, t, 10, 8, "raw_pork",       "319", "0",  "bone",          "352", "0")
                     setCMDBlock(count, start, t, 12, 8, "cook_pork",      "320", "0",  "bonemeal",      "351", "15")
                     setCMDBlock(count, start, t, 14, 8, "raw_fish",       "349", "0",  "cook_fish",     "350", "0")
                     setCMDBlock(count, start, t, 16, 8, "raw_salmon",     "349", "1",  "cook_salmon",   "350", "1")
                     setCMDBlock(count, start, t, 18, 8, "clownfish",      "349", "2",  "emerald",       "388", "0")
                     setCMDBlock(count, start, t, 20, 8, "pufferfish",     "349", "3",  "diamond",       "264", "0")
                     setCMDBlock(count, start, t, 22, 8, "brown_mushroom", "39",  "0",  "iron_ingot",    "265", "0")
                     setCMDBlock(count, start, t, 24, 8, "red_mushroom",   "40",  "0",  "redstone",      "331", "0")
                     setCMDBlock(count, start, t, 26, 8, "b_mushroom_blk", "99",  "0",  "coal",          "263", "0")
                     setCMDBlock(count, start, t, 28, 8, "r_mushroom_blk", "100", "0",  "charcoal",      "263", "1")
                     setCMDBlock(count, start, t, 30, 8, "redstone_lamp",  "123", "0",  "coal_block",    "173", "0")
                     setCMDBlock(count, start, t, 32, 8, "glowstone_dust", "348", "0",  "eye_of_ender",  "381", "0")
                     setCMDBlock(count, start, t, 34, 8, "blaze_rod",      "369", "0",  "ender_pearl",   "368", "0")
                     setCMDBlock(count, start, t, 36, 8, "blaze_powder",   "377", "0",  "slimeball",     "341", "0")
                     setCMDBlock(count, start, t, 38, 8, "lead",           "420", "0",  "string",        "287", "0")

                     # Row 6
                     setCMDBlock(count, start, t, 0, 10, "magma_cream",    "378", "0", "oak",            "17", "0")
                     setCMDBlock(count, start, t, 2, 10, "bucket",         "325", "0", "spruce",         "17", "1")
                     setCMDBlock(count, start, t, 4, 10, "bucket_milk",    "335", "0", "birch",          "17", "2")
                     setCMDBlock(count, start, t, 6, 10, "bucket_water",   "326", "0", "jungle",         "17", "3")
                     setCMDBlock(count, start, t, 8, 10, "bucket_lava",    "327", "0", "acacia",         "162", "0")
                     setCMDBlock(count, start, t, 10,10, "nether_wart",    "372", "0", "dark_oak",       "162", "1")
                     setCMDBlock(count, start, t, 12,10, "ghast_tear",     "370", "0", "sapling_oak",    "6", "0")
                     setCMDBlock(count, start, t, 14,10, "spider_eye",     "375", "0", "sapling_spruce", "6", "1")
                     setCMDBlock(count, start, t, 16,10, "rotten_flesh",   "367", "0", "sapling_birch",  "6", "2")
                     setCMDBlock(count, start, t, 18,10, "leather",        "334", "0", "sapling_jungle", "6", "3")
                     setCMDBlock(count, start, t, 20,10, "item_frame",     "389", "0", "sapling_acacia", "6", "4")
                     setCMDBlock(count, start, t, 22,10, "painting",       "321", "0", "sapling_d_oak",  "6", "5")
                     setCMDBlock(count, start, t, 24,10, "snowball",       "332", "0", "planks_oak",     "5", "0")
                     setCMDBlock(count, start, t, 26,10, "snow",           "80",  "0", "planks_spruce",  "5", "1")
                     setCMDBlock(count, start, t, 28,10, "glass_bottle",   "374", "0", "planks_birch",   "5", "2")
                     setCMDBlock(count, start, t, 30,10, "flint",          "318", "0", "planks_jungle",  "5", "3")
                     setCMDBlock(count, start, t, 32,10, "piston",         "33",  "0", "planks_acacia",  "5", "4")
                     setCMDBlock(count, start, t, 34,10, "sticky_piston",  "29",  "0", "planks_dark_oak","5", "5")
                     setCMDBlock(count, start, t, 36,10, "tripwire_hook",  "131", "0", "redstone_torch", "76", "0")
                     setCMDBlock(count, start, t, 38,10, "lever",          "69",  "0", "TNT",            "46", "0")

                     # Row 7
                     setCMDBlock(count, start, t, 0, 12, "repeater",       "356", "0", "x", "x", "0")
                     setCMDBlock(count, start, t, 2, 12, "comparator",     "404", "0", "x", "x", "0")
                     setCMDBlock(count, start, t, 4, 12, "button_stone",   "77",  "0", "x", "x", "0")
                     setCMDBlock(count, start, t, 6, 12, "button_wood",    "143", "0", "x", "x", "0")
                     setCMDBlock(count, start, t, 8, 12, "pressure_wood",  "72",  "0", "x", "x", "0")
                     setCMDBlock(count, start, t, 10,12, "pressure_stone", "70",  "0", "x", "x", "0")
                     setCMDBlock(count, start, t, 12,12, "pressure_gold",  "147", "0", "x", "x", "0")
                     setCMDBlock(count, start, t, 14,12, "pressure_iron",  "148", "0", "x", "x", "0")
                     setCMDBlock(count, start, t, 16,12, "rail",           "66",  "0", "x", "x", "0")
                     setCMDBlock(count, start, t, 18,12, "powered_rail",   "27",  "0", "x", "x", "0")
                     setCMDBlock(count, start, t, 20,12, "detector_rail",  "28",  "0", "x", "x", "0")
                     setCMDBlock(count, start, t, 22,12, "activator_rail", "157", "0", "x", "x", "0")
                     setCMDBlock(count, start, t, 24,12, "minecart",       "328", "0", "x", "x", "0")
                     setCMDBlock(count, start, t, 26,12, "ladder",         "65",  "0", "x", "x", "0")
                     setCMDBlock(count, start, t, 28,12, "x", "x", "0", "x", "x", "0")
                     setCMDBlock(count, start, t, 30,12, "x", "x", "0", "x", "x", "0")
                     setCMDBlock(count, start, t, 32,12, "x", "x", "0", "x", "x", "0")
                     setCMDBlock(count, start, t, 34,12, "x", "x", "0", "x", "x", "0")
                     setCMDBlock(count, start, t, 36,12, "x", "x", "0", "x", "x", "0")
                     setCMDBlock(count, start, t, 38,12, "x", "x", "0", "x", "x", "0")


#          setCMDBlock(count, start, t, 0,  8, "x", "x", "0", "x", "x", "0")
#          setCMDBlock(count, start, t, 2,  8, "x", "x", "0", "x", "x", "0")
#          setCMDBlock(count, start, t, 4,  8, "x", "x", "0", "x", "x", "0")
#          setCMDBlock(count, start, t, 6,  8, "x", "x", "0", "x", "x", "0")
#          setCMDBlock(count, start, t, 8,  8, "x", "x", "0", "x", "x", "0")
#          setCMDBlock(count, start, t, 10, 8, "x", "x", "0", "x", "x", "0")
#          setCMDBlock(count, start, t, 12, 8, "x", "x", "0", "x", "x", "0")
#          setCMDBlock(count, start, t, 14, 8, "x", "x", "0", "x", "x", "0")
#          setCMDBlock(count, start, t, 16, 8, "x", "x", "0", "x", "x", "0")
#          setCMDBlock(count, start, t, 18, 8, "x", "x", "0", "x", "x", "0")
#          setCMDBlock(count, start, t, 20, 8, "x", "x", "0", "x", "x", "0")
#          setCMDBlock(count, start, t, 22, 8, "x", "x", "0", "x", "x", "0")
#          setCMDBlock(count, start, t, 24, 8, "x", "x", "0", "x", "x", "0")
#          setCMDBlock(count, start, t, 26, 8, "x", "x", "0", "x", "x", "0")
#          setCMDBlock(count, start, t, 28, 8, "x", "x", "0", "x", "x", "0")
#          setCMDBlock(count, start, t, 30, 8, "x", "x", "0", "x", "x", "0")
#          setCMDBlock(count, start, t, 32, 8, "x", "x", "0", "x", "x", "0")
#          setCMDBlock(count, start, t, 34, 8, "x", "x", "0", "x", "x", "0")
#          setCMDBlock(count, start, t, 36, 8, "x", "x", "0", "x", "x", "0")
#          setCMDBlock(count, start, t, 38, 8, "x", "x", "0", "x", "x", "0")

# To add:
### ** Still need to program hopper direction command block
### Colour any output
### Name any command blocks
### remember to make cocoa farm!
### remember cactus farm (into bank)
### remember to shovel snow blocks

#Control: 841,10,367  - 
#Control: 841,10,369  - 
#Control: 841,10,371  - 


world1.saveInPlace();


#Control: 841,10,355  - 
#Control: 841,10,357  - 
#Control: 841,10,359  - 
#Control: 841,10,367  - /testforblock ~-5 ~ ~1 dropper 1 {Items:[0:{Slot:0b,id:1s,Damage:0s,Count:1b}]}
#Control: 841,10,369  - /scoreboard objectives add stone dummy
#Control: 841,10,371  - /scoreboard players add @r stone 1
      
      
#   355   357   359   367   369   371  (s: 374)
   
#   841 - 879  (s: 841)

# /testforblock ~-5 ~ ~1 dropper 1 {Items:[0:{Slot:0b,id:1s,Damage:0s,Count:1b}]}
# /scoreboard objectives add grass dummy
# /scoreboard players add @r grass 1




