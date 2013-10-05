import sys
import unicodedata
import re
from pymclevel import mclevel
from pymclevel.schematic import MCSchematic
from pymclevel.box import BoundingBox

from pymclevel.nbt import TAG_Compound, TAG_Byte, TAG_List, TAG_Int_Array, TAG_Short, TAG_String, TAG_Int
from pymclevel.box import Vector

displayName = "001 Replace Sorter"

def perform(level, box, options):
  print box

  for (chunk, slices, point) in level.getChunkSlices(box):
     for t in chunk.TileEntities:
  	x = t["x"].value
	y = t["y"].value
	z = t["z"].value

        # replace the items in the hopper
        if t["id"].value == "Hopper":
          print t["id"]
          if "Items" in t:
            for item in t["Items"]:
                print "***" + t["id"].value + "***********************************************\n"
                print item
                if item["id"].value != 7:
                   item["id"] = TAG_Short(7)
                   item["Damage"] = TAG_Short(0)
                   print item

        # replace the items in the hopper
        if t["id"].value == "Chest":
          print t["id"]
          if "Items" in t:
            for item in t["Items"]:
                print "***" + t["id"].value + "***********************************************\n"
                print item
                if item["id"].value != 7:
                   item["id"] = TAG_Short(7)
                   item["Damage"] = TAG_Short(0)
                   print item



