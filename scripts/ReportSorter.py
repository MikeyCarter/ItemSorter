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
world1 = mclevel.loadWorld("MikeyWorld-Backup");

# The root tag must have a name, and so must any tag within a TAG_Compound
#print level



chunkPositions = list(world1.allChunks)
#xPos, zPos = chunkPositions[10];
#print chunkPositions
sorterArr = {}

#-5    -   -15
# 6    -    11

name_array = { (20 ,0): "Glass",
               (102,0): "GlassPane",
               (420,0): "Lead",
               (341,0): "Slimeball",
               (35,0): "WhiteWool",
               (35,1): "OrangeWool",
               (35,2): "MagentaWool",
               (35,3): "LightBlueWool",
               (35,4): "YellowWool",
               (35,5): "LimeWool",
               (35,6): "PinkWool",
               (35,7): "GrayWool",
               (35,8): "LightGrayWool",
               (35,9): "CyanWool",
               (35,10): "PurpleWool",
               (35,11): "BlueWool",
               (35,12): "BrownWool",
               (35,13): "GreenWool",
               (35,14): "RedWool",
               (35,15): "BlackWool",

               (56,0):  'DiamondOre',
               (73,0):  'RedstoneOre',
               (129,0): 'EmeraldOre',
               (14,0):  'GoldOre',
               (15,0):  'IronOre',
               (16,0):  'CoalOre',
               (21,0):  'LapisLazuliOre',
               (41,0):  'GoldBlock',
               (42,0):  'IronBlock',
               (57,0):  'DiamondBlock',
               (133,0): 'EmeraldBlock',
               (152,0): 'RedstoneBlock',
               (155,0): 'QuartzBlock',
               (173,0): 'CoalBlock',
               (263,0): 'Coal',
               (263,1): 'Charcoal',
               (318,0): 'Flint',
               (331,0): 'Redstone',
               (80,0):  'SnowBlock',
               (79,0):  'Ice',

               (81,0):  'Cactus',
               (83,0):  'SugarCane',
               (86,0):  'Pumpkin',
               (103,0): 'MelonBlock',
               (391,0): 'Carrots',
               (392,0): 'Potatoes',
               (170,0): 'HayBale',
               (260,0): 'Apple',
               (295,0): 'WheatSeeds',
               (296,0): 'Wheat',
               (297,0): 'Bread',
               (319,0): 'RawPorkchop',
               (320,0): 'CookedPorkchop',
               (322,0): 'GoldenApple',
               (338,0): 'Sugarcane',
               (344,1): 'Egg',
               (349,0): 'RawFish',
               (354,0): 'Cake',
               (353,0): 'Sugar',
               (357,0): 'Cookie',

               (360,0): 'Melon',
               (361,0): 'PumpkinSeeds',
               (362,0): 'MelonSeeds',
               (363,0): 'RawBeef',
               (364,0): 'Steak',
               (365,0): 'RawChicken',
               (366,0): 'CookedChicken',
               (367,0): 'RottenFlesh',
               (375,0): 'SpiderEye',
               (382,0): 'GlisteringMelon',
               (297,0): 'Bread',
               (319,0): 'RawPorkchop',
               (320,0): 'CookedPorkchop',
               (322,0): 'GoldenApple',
               (338,0): 'Sugarcane',
               (393,0): 'BakedPotato',
               (394,0): 'PoisonousPotato',
               (396,0): 'GoldenCarrot',
               (400,0): 'Pumpkin Pie',
               (334,0): 'Leather',

               (  1,0): 'Stone',
               (  3,0): 'Dirt',
               (  4,0): 'Cobblestone',
               ( 17,0): 'OakWood',
               ( 17,1): 'SpruceWood',
               ( 17,2): 'BirchWood',
               ( 17,3): 'JungleWood',
               ( 12,0): 'Sand',
               ( 13,0): 'Gravel',
               ( 24,0): 'Sandstone',
               ( 24,1): 'ChiseledSandstone',
               ( 24,2): 'SmoothSandstone',
               ( 87,0): 'Netherrack',
               ( 88,0): 'SoulSand',
               ( 89,0): 'Glowstone',
               (101,0): 'IronBars',
               (336,0): 'ClayBrick',
               (337,0): 'ClayBalls',
               (405,0): 'NetherBrick',
               ( 45,0): 'Brick',

               (106,0): 'Vines',
               (110,0): 'Mycelium',
               (111,0): 'LilyPad',
               ( 50,0): 'Torch',
               ( 49,0): 'Obsidian',
               ( 48,0): 'MossyCobblestone',
               ( 65,0): 'Ladder',
               (287,0): 'String',
               (288,0): 'Feather',
               (289,0): 'Sulphur',
               (323,1): 'Sign',
               (321,2): 'Painting',
               (389,0): 'Frame',
               (339,0): 'Paper',
               (340,0): 'Book',
               (155,1): 'ChiseledQuartz',
               (155,2): 'PillarQuartz',
               (352,0): 'Bone',
               ( 38,0): 'Rose',
               ( 37,0): 'Dandelion',

               ( 76,0): 'RedstoneTorch',
               ( 77,0): 'StoneButton',
               (143,0): 'WoodButton',
               ( 69,0): 'Lever',
               (154,0): 'Hopper',
               (158,0): 'Dropper',
               ( 23,0): 'Dispenser',
               ( 29,0): 'StickyPiston',
               ( 33,0): 'Piston',
               ( 27,0): 'PoweredRail',
               ( 28,0): 'DetectorRail',
               (157,0): 'ActivatorRail',
               ( 66,0): 'Rails',
               ( 70,0): 'StonePressurePlate',
               ( 72,0): 'WoodPressurePlate',
               (123,0): 'RedstoneLamp',
               (131,0): 'TripwireHook',
               (356,0): 'Repeater',
               (404,0): 'Comparator',
               ( 46,0): 'TNT',

               ( 39,0): 'BrownMushroom',
               ( 40,0): 'RedMushroom',
               ( 47,0): 'Bookshelf',
               (172,0): 'HardenedClay',
               (159,0): 'WhiteStanedClay',
               (159,1): 'OrangeStanedClay',
               (159,2): 'MagentaStanedClay',
               (159,3): 'LightBlueStanedClay',
               (159,4): 'YellowStanedClay',
               (159,5): 'LimeStanedClay',
               (159,6): 'PinkStanedClay',
               (159,7): 'GrayStanedClay',
               (159,8): 'LightGrayStainedClay',
               (159,9): 'CyanStanedClay',
               (159,10): 'PurpleStainedClay',
               (159,11): 'BlueStainedClay',
               (159,12): 'BrownStainedClay',
               (159,13): 'GreenStainedClay',
               (159,14): 'RedStainedClay',
               (159,15): 'BlackStainedClay',

               (368,0): 'EnderPearl',
               (369,0): 'BlazeRod', 
               (370,0): 'GhastTear',
               (371,0): 'GoldNugget',
               (372,0): 'NetherWartSeeds',
               (374,0): 'GlassBottle',
               (381,0): 'EyeOfEnder',
               (351,0): 'InkSack',
               (  6,0): 'OakSapling',
               (  6,1): 'SpruceSapling',
               (  6,2): 'BirchSapling',
               (  6,3): 'JungleSapling',
               (  5,0): 'OakWoodPlank',
               (  5,1): 'SpruceWoodPlank',
               (  5,2): 'BirchWoodPlank',
               (  5,3): 'JungleWoodPlank',
               ( 98,0): 'StoneBrick',
               ( 98,1): 'MossyStoneBrick',
               ( 98,3): 'ChiseledStoneBrick',
               (153,0): 'NetherQuartzOre',

               (  7,0): 'Open'

             }

for xPos in range( -17, -4):
 for zPos in range( 3,  14):
  chunk = world1.getChunk(xPos, zPos)
  
  for t in chunk.TileEntities:
     if t["y"].value == 11:
       if t["id"].value == "Hopper":
         #print "Chunk: " + str(xPos) + ", " + str(zPos)
         try:
           itemID    = t["Items"][0]["id"].value
           subItemID = t["Items"][0]["Damage"].value
           name      = name_array[(itemID, subItemID)]

           sorterArr[int(t["x"].value),int(t["z"].value)] = {'ID': itemID, 'subID': subItemID, 'Name': name}
         
           if (t["Items"][0]["id"].value > 0 and 
               t["Items"][0]["id"].value == t["Items"][1]["id"].value and 
               t["Items"][1]["id"].value == t["Items"][2]["id"].value and 
               t["Items"][2]["id"].value == t["Items"][3]["id"].value and
               t["Items"][3]["id"].value == t["Items"][4]["id"].value and
               t["Items"][4]["id"].value == t["Items"][0]["id"].value):
  
             if subItemID > 0:
                printf("... Hopper OK: %20s %8s %23s %s\n", name, str(itemID) + ":" + str(subItemID), "(x="+str(t["x"].value)+",y="+str(t["y"].value)+",z="+str(t["z"].value)+")", "Chunk: " + str(xPos) + ", " + str(zPos))
             else:
                printf("... Hopper OK: %20s %8s %23s %s\n", name, str(itemID), "(x="+str(t["x"].value)+",y="+str(t["y"].value)+",z="+str(t["z"].value)+")", "Chunk: " + str(xPos) + ", " + str(zPos))

           else:
              print "... Hopper Bad: " + name + "  " + str(itemID) + ":" + str(subItemID) + " (x="+str(t["x"].value)+",y="+str(t["y"].value)+",z="+str(t["z"].value)+")   Chunk: " + str(xPos) + ", " + str(zPos)
              print t
              
         except IndexError:
           print  "Fail: "
           print t
       if t["id"].value == "Command":
         print t  



for xPos in range( -17, -4):
 for zPos in range( 3,  14):
  chunk = world1.getChunk(xPos, zPos)
  
  for t in chunk.TileEntities:
     if t["y"].value < 12:
       if t["id"].value == "Chest":


#print sorterArr

#for y in range(0, 16):
#  for x in range(0, 16):
#    for z in range(0, 16):
#      blockType = chunk.Blocks[x,z,y]
#      if blockType == 54: 
#        print blockType

#blockType = chunk.Blocks[0,0,64]

#box = BoundingBox((-60, 16, 120), (-201, 0, 80))

##for (chunk, slices, point) in world1.getAllChunkSlices():   
#for (chunk, slices, point) in world1.getChunkSlices(box):   
#   for t in chunk.TileEntities:
#      print t  

