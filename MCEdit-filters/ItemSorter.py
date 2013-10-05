import sys
import unicodedata
import re
from pymclevel import mclevel
from pymclevel.schematic import MCSchematic
from pymclevel.box import BoundingBox

from pymclevel.nbt import TAG_Compound, TAG_Byte, TAG_List, TAG_Int_Array, TAG_Short, TAG_String, TAG_Int
from pymclevel.box import Vector

displayName = "001 ItemSorter"

inputs = (
        ("Authorized Personal", ("string", "value=MikeyCarter")),
)

TotalCenter = 20  # Change this value (Total number of items in centre)
TotalRows   = 10   # Added this so we can calculate how big it's going to be
IS_Path     = "/u2/Common-Projects/CF_Applications/minecraft/ItemSorter/MCEdit-schematics/"
x_axis = -1
y_axis = 0
length = 0
 


formatCode = unichr(167)
c_bgreen = "a"
c_aqua   = "b"
c_red    = "c"

def CentreRight(level, box, length, x_axis, y_axis):
  # Closing Centre Block
  cr = mclevel.fromFile(IS_Path+"ItemSorter-CR.schematic")
  schematic_cr = cr.extractSchematic(cr.bounds)
  level.copyBlocksFrom(schematic_cr, schematic_cr.bounds, box.origin+(x_axis,y_axis,length), create=True);

  x_axis = x_axis+cr.Width
  length = 0
  return (length, x_axis)

def CentreLeft(level, box, length, x_axis, y_axis, itemID, itemName, subID):
  cl = mclevel.fromFile(IS_Path+"ItemSorter-CL.schematic")
  updateCB(cl, itemID, itemName, subID);
  schematic_cl = cl.extractSchematic(cl.bounds)
  level.copyBlocksFrom(schematic_cl, schematic_cl.bounds, box.origin+(x_axis,y_axis,length), create=True);
  return length + cl.Length


def CentreBlock(level, box, length, x_axis, y_axis, itemID, itemName, subID):
  # Add Yellow Wool
  cc = mclevel.fromFile(IS_Path+"ItemSorter-CC.schematic")
  updateCB(cc, itemID, itemName, subID);
  schematic_cc = cc.extractSchematic(cc.bounds)
  level.copyBlocksFrom(schematic_cc, schematic_cc.bounds, box.origin+(x_axis,y_axis,length), create=True);
  return length + cc.Length


def updateTP(level, options):
  for (chunk, slices, point) in level.getChunkSlices(level.bounds):
     for t in chunk.TileEntities:
	if t["id"].value == "Control":
          if 'MikeyCarter' in t["Command"].value:
            cmd = t["Command"].value
            cmd = re.sub("MikeyCarter", options["Authorized Personal"], cmd)
            t["Command"] = t["Command"] = TAG_String(cmd)
            print t

 
def updateCB(level, itemID, itemName, subID):
  for (chunk, slices, point) in level.getChunkSlices(level.bounds):
     for t in chunk.TileEntities:
  	x = t["x"].value
	y = t["y"].value
	z = t["z"].value
 
        chunk.dirty = True

        # Find Sign with item title
        if t["id"].value == "Sign":
          print t
          if t["Text1"].value == "item001":
            t["Text1"] = TAG_String(formatCode+c_aqua+itemName)
            print t

        # replace the items in the hopper
        if t["id"].value == "Hopper":
          if "Items" in t:
            for item in t["Items"]:
                if item["id"].value == 7:
                   item["id"] = TAG_Short(itemID)
                   item["Damage"] = TAG_Short(subID)

                print item



        # Modify the command blocks
	if t["id"].value == "Control":
          cmd = t["Command"].value

	  if 'say' in t["Command"].value:
	     t["CustomName"].value = "Item Sorter"
          else:
             t["CustomName"].value = "Item Select"

          # Turns command into string so I can manipulate it
          #cmd = unicodedata.normalize('NFKD', t["Command"].value).encode('ascii','ignore')

          cmd = re.sub('item001', itemName, cmd)
          cmd = re.sub(formatCode+c_red, "", cmd)
          cmd = re.sub(formatCode+c_bgreen, "", cmd)
          
          if 'empty' in cmd:
            cmd = re.sub('/?say ', 'say '+formatCode+c_red, cmd)
          else:
            cmd = re.sub('/?say ', 'say '+formatCode+c_bgreen, cmd)
                    
          t["Command"] = t["Command"] = TAG_String(cmd)
                    
          sys.stdout.write(t["id"].value + ": [" + t["CustomName"].value + "] " + t["Command"].value + "\n")
          sys.stdout.flush()

          
			
  return level 


def perform(level, box, options):
  print box

  br = mclevel.fromFile(IS_Path+"ItemSorter-BR.schematic")
  cr = mclevel.fromFile(IS_Path+"ItemSorter-CR.schematic")
  fr = mclevel.fromFile(IS_Path+"ItemSorter-FR.schematic")
  
  TotalWidth = br.Width + (cr.Width * TotalRows) + fr.Width
  print "Width Total.: " + str(TotalWidth)
  print "Height Total: " + str(br.Height)


 
  bl = mclevel.fromFile(IS_Path+"ItemSorter-BL.schematic")
  bc = mclevel.fromFile(IS_Path+"ItemSorter-BC.schematic")
  br = mclevel.fromFile(IS_Path+"ItemSorter-BR.schematic")


  schematic_bl = bl.extractSchematic(bl.bounds)
  schematic_bc = bc.extractSchematic(bc.bounds)
  schematic_br = br.extractSchematic(br.bounds)

  x_axis = 0 - TotalWidth
  length = 0
 
  # Rear Blocks
  level.copyBlocksFrom(schematic_bl, schematic_bl.bounds, box.origin+(x_axis,y_axis,length), create=True);
  length = length + bl.Length

  for x in range(0, TotalCenter-1):
     level.copyBlocksFrom(schematic_bc, schematic_bc.bounds, box.origin+(x_axis,y_axis,length), create=True);
     length = length + bc.Length
     
  level.copyBlocksFrom(schematic_br, schematic_br.bounds, box.origin+(x_axis,y_axis,length), create=True);
  print length;

  # Row 1 (Wool, Glass, Misc)
  x_axis = x_axis+bl.Width
  length = 0
  length = CentreLeft (level, box, length, x_axis, y_axis, 20,  'Glass', 0)		#1
  length = CentreBlock(level, box, length, x_axis, y_axis, 102, 'GlassPane',0)		#2
  length = CentreBlock(level, box, length, x_axis, y_axis, 420, 'Lead', 0)		#3
  length = CentreBlock(level, box, length, x_axis, y_axis, 341, 'Slimeball',0)		#4
  length = CentreBlock(level, box, length, x_axis, y_axis, 35,  'WhiteWool', 0)		#5
  length = CentreBlock(level, box, length, x_axis, y_axis, 35,  'OrangeWool',1)		#6
  length = CentreBlock(level, box, length, x_axis, y_axis, 35,  'MagentaWool',2)	#7
  length = CentreBlock(level, box, length, x_axis, y_axis, 35,  'LightBlueWool',3)	#8
  length = CentreBlock(level, box, length, x_axis, y_axis, 35,  'YellowWool',4)		#9
  length = CentreBlock(level, box, length, x_axis, y_axis, 35,  'LimeWool',5)		#10
  length = CentreBlock(level, box, length, x_axis, y_axis, 35,  'PinkWool',6)		#11
  length = CentreBlock(level, box, length, x_axis, y_axis, 35,  'GrayWool',7)		#12
  length = CentreBlock(level, box, length, x_axis, y_axis, 35,  'LightGrayWool',8)	#13
  length = CentreBlock(level, box, length, x_axis, y_axis, 35,  'CyanWool',9)		#14
  length = CentreBlock(level, box, length, x_axis, y_axis, 35,  'PurpleWool',10)	#15
  length = CentreBlock(level, box, length, x_axis, y_axis, 35,  'BlueWool',11)		#16
  length = CentreBlock(level, box, length, x_axis, y_axis, 35,  'BrownWool',12)		#17
  length = CentreBlock(level, box, length, x_axis, y_axis, 35,  'GreenWool',13)		#18
  length = CentreBlock(level, box, length, x_axis, y_axis, 35,  'RedWool',14)		#19
  length = CentreBlock(level, box, length, x_axis, y_axis, 35,  'BlackWool',15)		#20
  (length, x_axis) = CentreRight(level, box, length, x_axis, y_axis);


  # Row 2 (Ores)
  length = 0
  length = CentreLeft (level, box, length, x_axis, y_axis, 56,  'DiamondOre', 0)	#1
  length = CentreBlock(level, box, length, x_axis, y_axis, 73,  'RedstoneOre', 0)	#2
  length = CentreBlock(level, box, length, x_axis, y_axis, 129, 'EmeraldOre',0)		#3
  length = CentreBlock(level, box, length, x_axis, y_axis, 14,  'GoldOre',0)		#4
  length = CentreBlock(level, box, length, x_axis, y_axis, 15,  'IronOre',0)		#5
  length = CentreBlock(level, box, length, x_axis, y_axis, 16,  'CoalOre',0)		#6
  length = CentreBlock(level, box, length, x_axis, y_axis, 21,  'LapisLazuliOre',0)	#7
  length = CentreBlock(level, box, length, x_axis, y_axis, 41,  'GoldBlock',0)		#8
  length = CentreBlock(level, box, length, x_axis, y_axis, 42,  'IronBlock',0)		#9
  length = CentreBlock(level, box, length, x_axis, y_axis, 57,  'DiamondBlock',0)	#10
  length = CentreBlock(level, box, length, x_axis, y_axis, 133, 'EmeraldBlock',0)	#11
  length = CentreBlock(level, box, length, x_axis, y_axis, 152, 'RedstoneBlock',0)	#12
  length = CentreBlock(level, box, length, x_axis, y_axis, 155, 'QuartzBlock',0)	#13
  length = CentreBlock(level, box, length, x_axis, y_axis, 173, 'CoalBlock',0)		#14
  length = CentreBlock(level, box, length, x_axis, y_axis, 263, 'Coal',0)		#15
  length = CentreBlock(level, box, length, x_axis, y_axis, 263, 'Charcoal',1)		#16
  length = CentreBlock(level, box, length, x_axis, y_axis, 318, 'Flint',0)		#17
  length = CentreBlock(level, box, length, x_axis, y_axis, 331, 'Redstone',0)		#18
  length = CentreBlock(level, box, length, x_axis, y_axis, 80,  'SnowBlock',0)		#19
  length = CentreBlock(level, box, length, x_axis, y_axis, 79,  'Ice',0)		#20
  (length, x_axis) = CentreRight(level, box, length, x_axis, y_axis);

  # Row 3 (Food)
  length = 0
  length = CentreLeft (level, box, length, x_axis, y_axis, 81,  'Cactus', 0)		#1
  length = CentreBlock(level, box, length, x_axis, y_axis, 83,  'SugarCane', 0)		#2
  length = CentreBlock(level, box, length, x_axis, y_axis, 86,  'Pumpkin',0)		#3
  length = CentreBlock(level, box, length, x_axis, y_axis, 103, 'MelonBlock',0)		#4
  length = CentreBlock(level, box, length, x_axis, y_axis, 391, 'Carrots',0)		#5
  length = CentreBlock(level, box, length, x_axis, y_axis, 392, 'Potatoes',0)		#6
  length = CentreBlock(level, box, length, x_axis, y_axis, 170, 'HayBale',0)		#7
  length = CentreBlock(level, box, length, x_axis, y_axis, 260, 'Apple',0)		#8
  length = CentreBlock(level, box, length, x_axis, y_axis, 295, 'WheatSeeds',0)		#9
  length = CentreBlock(level, box, length, x_axis, y_axis, 296, 'Wheat',0)		#10
  length = CentreBlock(level, box, length, x_axis, y_axis, 297, 'Bread',0)		#11
  length = CentreBlock(level, box, length, x_axis, y_axis, 319, 'RawPorkchop',0)	#12
  length = CentreBlock(level, box, length, x_axis, y_axis, 320, 'CookedPorkchop',0)	#13
  length = CentreBlock(level, box, length, x_axis, y_axis, 322, 'GoldenApple',0)	#14
  length = CentreBlock(level, box, length, x_axis, y_axis, 338, 'Sugarcane',0)		#15
  length = CentreBlock(level, box, length, x_axis, y_axis, 344, 'Egg',1)		#16
  length = CentreBlock(level, box, length, x_axis, y_axis, 349, 'RawFish',0)		#17
  length = CentreBlock(level, box, length, x_axis, y_axis, 354, 'Cake',0)		#18
  length = CentreBlock(level, box, length, x_axis, y_axis, 353, 'Sugar',0)		#19
  length = CentreBlock(level, box, length, x_axis, y_axis, 357, 'Cookie',0)		#20
  (length, x_axis) = CentreRight(level, box, length, x_axis, y_axis);

  # Row 4 (Food, Other)
  length = 0
  length = CentreLeft (level, box, length, x_axis, y_axis, 360, 'Melon', 0)		#1
  length = CentreBlock(level, box, length, x_axis, y_axis, 361, 'PumpkinSeeds', 0)	#2
  length = CentreBlock(level, box, length, x_axis, y_axis, 362, 'MelonSeeds',0)		#3
  length = CentreBlock(level, box, length, x_axis, y_axis, 363, 'RawBeef',0)		#4
  length = CentreBlock(level, box, length, x_axis, y_axis, 364, 'Steak',0)		#5
  length = CentreBlock(level, box, length, x_axis, y_axis, 365, 'RawChicken',0)		#6
  length = CentreBlock(level, box, length, x_axis, y_axis, 366, 'CookedChicken',0)	#7
  length = CentreBlock(level, box, length, x_axis, y_axis, 367, 'RottenFlesh',0)	#8
  length = CentreBlock(level, box, length, x_axis, y_axis, 375, 'SpiderEye',0)		#9
  length = CentreBlock(level, box, length, x_axis, y_axis, 382, 'GlisteringMelon',0)	#10
  length = CentreBlock(level, box, length, x_axis, y_axis, 297, 'Bread',0)		#11
  length = CentreBlock(level, box, length, x_axis, y_axis, 319, 'RawPorkchop',0)	#12
  length = CentreBlock(level, box, length, x_axis, y_axis, 320, 'CookedPorkchop',0)	#13
  length = CentreBlock(level, box, length, x_axis, y_axis, 322, 'GoldenApple',0)	#14
  length = CentreBlock(level, box, length, x_axis, y_axis, 338, 'Sugarcane',0)		#15
  length = CentreBlock(level, box, length, x_axis, y_axis, 393, 'BakedPotato',0)	#16
  length = CentreBlock(level, box, length, x_axis, y_axis, 394, 'PoisonousPotato',0)	#17
  length = CentreBlock(level, box, length, x_axis, y_axis, 396, 'GoldenCarrot',0)	#18
  length = CentreBlock(level, box, length, x_axis, y_axis, 400, 'Pumpkin Pie',0)	#19
  length = CentreBlock(level, box, length, x_axis, y_axis, 334, 'Leather',0)		#20
  (length, x_axis) = CentreRight(level, box, length, x_axis, y_axis);

  # Row 5 (Building)
  length = 0
  length = CentreLeft (level, box, length, x_axis, y_axis,   1, 'Stone', 0)		#1
  length = CentreBlock(level, box, length, x_axis, y_axis,   3, 'Dirt', 0)	        #2
  length = CentreBlock(level, box, length, x_axis, y_axis,   4, 'Cobblestone',0)	#3
  length = CentreBlock(level, box, length, x_axis, y_axis,  17, 'OakWood',0)		#4
  length = CentreBlock(level, box, length, x_axis, y_axis,  17, 'SpruceWood',1)		#5
  length = CentreBlock(level, box, length, x_axis, y_axis,  17, 'BirchWood',2)		#6
  length = CentreBlock(level, box, length, x_axis, y_axis,  17, 'JungleWood',3)		#7
  length = CentreBlock(level, box, length, x_axis, y_axis,  12, 'Sand',0)		#8
  length = CentreBlock(level, box, length, x_axis, y_axis,  13, 'Gravel',0)		#9
  length = CentreBlock(level, box, length, x_axis, y_axis,  24, 'Sandstone',0)   	#10
  length = CentreBlock(level, box, length, x_axis, y_axis,  24, 'ChiseledSandstone',1)	#11
  length = CentreBlock(level, box, length, x_axis, y_axis,  24, 'SmoothSandstone',2)	#12
  length = CentreBlock(level, box, length, x_axis, y_axis,  87, 'Netherrack',0)		#13
  length = CentreBlock(level, box, length, x_axis, y_axis,  88, 'SoulSand',0)	        #14
  length = CentreBlock(level, box, length, x_axis, y_axis,  89, 'Glowstone',0)		#15
  length = CentreBlock(level, box, length, x_axis, y_axis, 101, 'IronBars',0)		#16
  length = CentreBlock(level, box, length, x_axis, y_axis, 336, 'ClayBrick',0)		#17
  length = CentreBlock(level, box, length, x_axis, y_axis, 337, 'ClayBalls',0)		#18
  length = CentreBlock(level, box, length, x_axis, y_axis, 405, 'NetherBrick',0)	#19
  length = CentreBlock(level, box, length, x_axis, y_axis, 45,  'Brick',0)		#20
  (length, x_axis) = CentreRight(level, box, length, x_axis, y_axis);

  # Row 6 (Others)
  length = 0
  length = CentreLeft (level, box, length, x_axis, y_axis, 106, 'Vines', 0)		#1
  length = CentreBlock(level, box, length, x_axis, y_axis, 110, 'Mycelium', 0)	        #2
  length = CentreBlock(level, box, length, x_axis, y_axis, 111, 'LilyPad',0)		#3
  length = CentreBlock(level, box, length, x_axis, y_axis,  50, 'Torch',0)		#4
  length = CentreBlock(level, box, length, x_axis, y_axis,  49, 'Obsidian',0)		#5
  length = CentreBlock(level, box, length, x_axis, y_axis,  48, 'MossyCobblestone',0)	#6
  length = CentreBlock(level, box, length, x_axis, y_axis,  65, 'Ladder',0)		#7
  length = CentreBlock(level, box, length, x_axis, y_axis, 287, 'String',0)		#8
  length = CentreBlock(level, box, length, x_axis, y_axis, 288, 'Feather',0)		#9
  length = CentreBlock(level, box, length, x_axis, y_axis, 289, 'Sulphur',0)    	#10
  length = CentreBlock(level, box, length, x_axis, y_axis, 323, 'Sign',1)		#11
  length = CentreBlock(level, box, length, x_axis, y_axis, 321, 'Painting',2)		#12
  length = CentreBlock(level, box, length, x_axis, y_axis, 389, 'Frame',0)		#13
  length = CentreBlock(level, box, length, x_axis, y_axis, 339, 'Paper',0)	        #14
  length = CentreBlock(level, box, length, x_axis, y_axis, 340, 'Book',0)		#15
  length = CentreBlock(level, box, length, x_axis, y_axis, 155, 'ChiseledQuartz',1)	#16
  length = CentreBlock(level, box, length, x_axis, y_axis, 155, 'PillarQuartz',2)	#17
  length = CentreBlock(level, box, length, x_axis, y_axis, 352, 'Bone',0)		#18
  length = CentreBlock(level, box, length, x_axis, y_axis,  38, 'Rose',0)       	#19
  length = CentreBlock(level, box, length, x_axis, y_axis,  37, 'Dandelion',0)		#20
  (length, x_axis) = CentreRight(level, box, length, x_axis, y_axis);

  # Row 7 (Redstone)
  length = 0
  length = CentreLeft (level, box, length, x_axis, y_axis,  76, 'RedstoneTorch', 0)	#1
  length = CentreBlock(level, box, length, x_axis, y_axis,  77, 'StoneButton', 0)	#2
  length = CentreBlock(level, box, length, x_axis, y_axis, 143, 'WoodButton',0)		#3
  length = CentreBlock(level, box, length, x_axis, y_axis,  69, 'Lever',0)		#4
  length = CentreBlock(level, box, length, x_axis, y_axis, 154, 'Hopper',0)		#5
  length = CentreBlock(level, box, length, x_axis, y_axis, 158, 'Dropper',0)		#6
  length = CentreBlock(level, box, length, x_axis, y_axis,  23, 'Dispenser',0)		#7
  length = CentreBlock(level, box, length, x_axis, y_axis,  29, 'StickyPiston',0)	#8
  length = CentreBlock(level, box, length, x_axis, y_axis,  33, 'Piston',0)		#9
  length = CentreBlock(level, box, length, x_axis, y_axis,  27, 'PoweredRail',0)   	#10
  length = CentreBlock(level, box, length, x_axis, y_axis,  28, 'DetectorRail',0)	#11
  length = CentreBlock(level, box, length, x_axis, y_axis, 157, 'ActivatorRail',0)	#12
  length = CentreBlock(level, box, length, x_axis, y_axis,  66, 'Rails',0)		#13
  length = CentreBlock(level, box, length, x_axis, y_axis,  70, 'StonePressurePlate',0) #14
  length = CentreBlock(level, box, length, x_axis, y_axis,  72, 'WoodPressurePlate',0)	#15
  length = CentreBlock(level, box, length, x_axis, y_axis, 123, 'RedstoneLamp',0)	#16
  length = CentreBlock(level, box, length, x_axis, y_axis, 131, 'TripwireHook',0)	#17
  length = CentreBlock(level, box, length, x_axis, y_axis, 356, 'Repeater',0)		#18
  length = CentreBlock(level, box, length, x_axis, y_axis, 404, 'Comparator',0)		#19
  length = CentreBlock(level, box, length, x_axis, y_axis,  46, 'TNT',0)		#20
  (length, x_axis) = CentreRight(level, box, length, x_axis, y_axis);

  # Row 8 (Clay,Other)
  length = 0
  length = CentreLeft (level, box, length, x_axis, y_axis,  39, 'BrownMushroom', 0)	#1
  length = CentreBlock(level, box, length, x_axis, y_axis,  40, 'RedMushroom', 0)	#2
  length = CentreBlock(level, box, length, x_axis, y_axis,  47, 'Bookshelf',0)		#3
  length = CentreBlock(level, box, length, x_axis, y_axis, 172, 'HardenedClay',0)	#4
  length = CentreBlock(level, box, length, x_axis, y_axis, 159, 'WhiteStanedClay',0)	#5
  length = CentreBlock(level, box, length, x_axis, y_axis, 159, 'OrangeStanedClay',1)	#6
  length = CentreBlock(level, box, length, x_axis, y_axis, 159, 'MagentaStanedClay',2)	#7
  length = CentreBlock(level, box, length, x_axis, y_axis, 159, 'LightBlueStanedClay',3)#8
  length = CentreBlock(level, box, length, x_axis, y_axis, 159, 'YellowStanedClay',4)	#9
  length = CentreBlock(level, box, length, x_axis, y_axis, 159, 'LimeStanedClay',5)   	#10
  length = CentreBlock(level, box, length, x_axis, y_axis, 159, 'PinkStanedClay',6)	#11
  length = CentreBlock(level, box, length, x_axis, y_axis, 159, 'GrayStanedClay',7)	#12
  length = CentreBlock(level, box, length, x_axis, y_axis, 159, 'LightGrayStainedClay',8)#13
  length = CentreBlock(level, box, length, x_axis, y_axis, 159, 'CyanStanedClay',9)     #14
  length = CentreBlock(level, box, length, x_axis, y_axis, 159, 'PurpleStainedClay',10)	#15
  length = CentreBlock(level, box, length, x_axis, y_axis, 159, 'BlueStainedClay',11)	#16
  length = CentreBlock(level, box, length, x_axis, y_axis, 159, 'BrownStainedClay',12)	#17
  length = CentreBlock(level, box, length, x_axis, y_axis, 159, 'GreenStainedClay',13)	#18
  length = CentreBlock(level, box, length, x_axis, y_axis, 159, 'RedStainedClay',14)	#19
  length = CentreBlock(level, box, length, x_axis, y_axis, 159, 'BlackStainedClay',15)	#20
  (length, x_axis) = CentreRight(level, box, length, x_axis, y_axis);

  # Row 9 (Clay,Other)
  length = 0
  length = CentreLeft (level, box, length, x_axis, y_axis, 368, 'EnderPearl', 0)	#1
  length = CentreBlock(level, box, length, x_axis, y_axis, 369, 'BlazeRod', 0)		#2
  length = CentreBlock(level, box, length, x_axis, y_axis, 370, 'GhastTear',0)		#3
  length = CentreBlock(level, box, length, x_axis, y_axis, 371, 'GoldNugget',0)		#4
  length = CentreBlock(level, box, length, x_axis, y_axis, 372, 'NetherWartSeeds',0)	#5
  length = CentreBlock(level, box, length, x_axis, y_axis, 374, 'GlassBottle',0)	#6
  length = CentreBlock(level, box, length, x_axis, y_axis, 381, 'EyeOfEnder',0)		#7
  length = CentreBlock(level, box, length, x_axis, y_axis, 351, 'InkSack',0)		#8
  length = CentreBlock(level, box, length, x_axis, y_axis,   6, 'OakSapling',0)		#9
  length = CentreBlock(level, box, length, x_axis, y_axis,   6, 'SpruceSapling',1)	#10
  length = CentreBlock(level, box, length, x_axis, y_axis,   6, 'BirchSapling',2)	#11
  length = CentreBlock(level, box, length, x_axis, y_axis,   6, 'JungleSapling',3)	#12
  length = CentreBlock(level, box, length, x_axis, y_axis,   5, 'OakWoodPlank',0)	#13
  length = CentreBlock(level, box, length, x_axis, y_axis,   5, 'SpruceWoodPlank',1)	#14
  length = CentreBlock(level, box, length, x_axis, y_axis,   5, 'BirchWoodPlank',2)	#15
  length = CentreBlock(level, box, length, x_axis, y_axis,   5, 'JungleWoodPlank',3)	#16
  length = CentreBlock(level, box, length, x_axis, y_axis,  98, 'StoneBrick',0)		#17
  length = CentreBlock(level, box, length, x_axis, y_axis,  98, 'MossyStoneBrick',1)	#18
  length = CentreBlock(level, box, length, x_axis, y_axis,  98, 'ChiseledStoneBrick',3)	#19
  length = CentreBlock(level, box, length, x_axis, y_axis, 153, 'NetherQuartzOre',0)    #20
  (length, x_axis) = CentreRight(level, box, length, x_axis, y_axis);

  # Row 10 (Future Block)
  length = 0
  length = CentreLeft (level, box, length, x_axis, y_axis,   7, 'Open',0)	#1
  length = CentreBlock(level, box, length, x_axis, y_axis,   7, 'Open',0)	#2
  length = CentreBlock(level, box, length, x_axis, y_axis,   7, 'Open',0)	#3
  length = CentreBlock(level, box, length, x_axis, y_axis,   7, 'Open',0)	#4
  length = CentreBlock(level, box, length, x_axis, y_axis,   7, 'Open',0)	#5
  length = CentreBlock(level, box, length, x_axis, y_axis,   7, 'Open',0)	#6
  length = CentreBlock(level, box, length, x_axis, y_axis,   7, 'Open',0)	#7
  length = CentreBlock(level, box, length, x_axis, y_axis,   7, 'Open',0)	#8
  length = CentreBlock(level, box, length, x_axis, y_axis,   7, 'Open',0)	#9
  length = CentreBlock(level, box, length, x_axis, y_axis,   7, 'Open',0)	#10
  length = CentreBlock(level, box, length, x_axis, y_axis,   7, 'Open',0)	#11
  length = CentreBlock(level, box, length, x_axis, y_axis,   7, 'Open',0)	#12
  length = CentreBlock(level, box, length, x_axis, y_axis,   7, 'Open',0)	#13
  length = CentreBlock(level, box, length, x_axis, y_axis,   7, 'Open',0)	#14
  length = CentreBlock(level, box, length, x_axis, y_axis,   7, 'Open',0)	#15
  length = CentreBlock(level, box, length, x_axis, y_axis,   7, 'Open',0)	#16
  length = CentreBlock(level, box, length, x_axis, y_axis,   7, 'Open',0)	#17
  length = CentreBlock(level, box, length, x_axis, y_axis,   7, 'Open',0)	#18
  length = CentreBlock(level, box, length, x_axis, y_axis,   7, 'Open',0)	#19
  length = CentreBlock(level, box, length, x_axis, y_axis,   7, 'Open',0)	#20
  (length, x_axis) = CentreRight(level, box, length, x_axis, y_axis);

  # Front Blocks
  fl = mclevel.fromFile(IS_Path+"ItemSorter-FL.schematic")
  updateTP(fl, options)
  schematic_fl = fl.extractSchematic(fl.bounds)
  level.copyBlocksFrom(schematic_fl, schematic_fl.bounds, box.origin+(x_axis,y_axis,length), create=True);
  length = length + fl.Length

  fc = mclevel.fromFile(IS_Path+"ItemSorter-FC.schematic")
  schematic_fc = fc.extractSchematic(fc.bounds)
  for x in range(0, TotalCenter-1):
     level.copyBlocksFrom(schematic_fc, schematic_fc.bounds, box.origin+(x_axis,y_axis,length), create=True);
     length = length + fc.Length
     
  fr = mclevel.fromFile(IS_Path+"ItemSorter-FR.schematic")
  schematic_fr = fr.extractSchematic(fr.bounds)
  level.copyBlocksFrom(schematic_fr, schematic_fr.bounds, box.origin+(x_axis,y_axis,length), create=True);



