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
world1 = mclevel.loadWorld("Metazoa-Backup");

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

for (xPos, zPos) in chunkPositions:
  chunk = world1.getChunk(xPos, zPos)
  
  for t in chunk.Entities:
    if t["id"].value == "EntityHorse":
       # Variant: 
       #          
       # All normal horses are of Type 0, donkeys are of Type 1, mules are of Type 2, zombie horses are of Type 3, and skeletal horses are of Type 4.
       #
       # 		White 	Creamy 	Chestnut 	Brown 	Black 	Gray 	Dark Brown
       # None 		0 	1 	2 		3 	4 	5 	6
       # White 		256 	257 	258 		259 	260 	261 	262
       # White Field 	512 	513 	514 		515 	516 	517 	518
       # White Dots 	768 	769 	770 		771 	772 	773 	774
       # Black Dots 	1024 	1025 	1026 		1027 	1028 	1029 	1030
       # 
       # http://minecraft.gamepedia.com/Item_id#Horse_Variants

       
       print "%-30s (x=%d,y=%d,z=%d)" % (t["id"].value+"-"+str(t["Variant"].value), t["Pos"][0].value, t["Pos"][1].value, t["Pos"][2].value)
    elif t["id"].value == "Item":
       print "%-30s (x=%d,y=%d,z=%d)" % (t["id"].value+"-"+str(t["Item"]["id"].value)+":"+str(t["Item"]["Damage"].value), t["Pos"][0].value, t["Pos"][1].value, t["Pos"][2].value)
    else:
       print "%-30s (x=%d,y=%d,z=%d)" % (t["id"].value, t["Pos"][0].value, t["Pos"][1].value, t["Pos"][2].value)
 
#  for t in chunk.Entities:
#    if t["id"].value == "EntityHorse":
#      print t


