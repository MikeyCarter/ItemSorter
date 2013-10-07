The problem:
============

When mining or farming you can build up a pile of items.  But you don't want to
spend a lot of time walking back to your house to sort them into chests.

The other problem is with all your sorted chests you don't want to have to walk
back to the house to pick up those items you need for building in a remote area.

Thus the Item Selector/Sorter was born.

The solution:
============

The Item Selector/Sorter, takes your various mining, and farming materials and
sorts them into bins.  Then using command blocks you can remotely select items
you want and it will dispense them to you.

Notes:
 - Originally I tried using a really compact sorter.  But then the selection
   part became a problem with cross talk.  Not to mention some items like wool
   would cause sorters beside to activate and empty their contents.
 - It's surrounded by bedrock so it can't be entered in adventure/survival mode
   unless by administrator.  * You may need to modify the TP command block
 - There should be enough light generated in the housing to stop MOB spawning,
   or so I hope.
 - The inside should be completely navigable in adventure/survival mode. You 
   might get lost though.
 - There is signs on each block/area explaining what it's doing.
 - There's a set of chests lining the back wall (File BL) for the items not 
   covered by the sorting system.  You could redirect it as the final hopper is
   right at the bedrock wall.
   11 double chests.  54 slots per double chests.  594 slots total.  Then the
   backup of hoppers transporting to the chests.
   
   Should been enough for overflow... sorting will stop working if you overflow
   past that.

Block Legend:

   Yellow Clay: Message system (Hopper empty/loading), Ladder
   Purple Clay: Selection System
   Red Clay...: Sorting System
   Grey Clay..: Hopper Clock (one at the beginning of each row to power 
                              selection system)

Delivery System and the Chunk Loading Problem:
==============================================

Initially I designed the system to use minecarts to pickup/deliver the items.
However, even though I've included the designs, I've abandoned all hope of using
minecarts.  When chunks are unloaded minecarts freeze and wait for a player to
enter the zone before resuming.   So if your sorting station is under the spawn
blocks and your selection system is 1000 blocks away.   There's going to be a few
100 unloaded chunks between you and the sorting/selection system.

The way around this is to create chunk loaders, by using pistons, or hopper clocks
between the corners to create a 5 by 5 loaded area around the carts.  500MB of ram
later... it's just not worth it.

Best way is to use hoppers and droppers.   Create a hopper and dropper tower from
the selection house to the item sorter.  Hoppers will partly load the chunks as
the items pass through them.  Solving the minecart problem.

Ref: Minecraft Piston Creation #29: Self Loading Minecart Track
     http://www.youtube.com/watch?v=wj2A1uzwj_4


Some Assembly Required!
=======================

I tried to make the Item Selector/Sorter modular so you could infinitely expand
it.  

The layout of the files:

+----+ +----+ +----+
| FL | | FC | | FR |
+----+ +----+ +----+

+----+ +----+ +----+
| CL | | CC | | CR |
+----+ +----+ +----+

+----+ +----+ +----+
| BL | | BC | | BR |
+----+ +----+ +----+

To make bigger:
===============

Expand by adding more xC columns in the middle, or Cx rows.

Example:

+----+ +----+ +----+ +----+
| FL | | FC | | FC | | FR |
+----+ +----+ +----+ +----+

+----+ +----+ +----+ +----+
| CL | | CC | | CC | | CR |
+----+ +----+ +----+ +----+

+----+ +----+ +----+ +----+
| CL | | CC | | CC | | CR |
+----+ +----+ +----+ +----+

+----+ +----+ +----+ +----+
| BL | | BC | | BC | | BR |
+----+ +----+ +----+ +----+


Manually setting up each module:
================================

Each module needs to be setup to accept items.  

  - Each module has 8 command blocks with a code item001.  This needs to be 
    replaced with the item tag (like Glass, or Dirt)
  - Replace bedrock items from selection hopper (place 18-1-1-1-1) with items to
    be selected (might not be 18 for things like eggs)
 
  * I used bedrock for any placeholder items since you wouldn't be sorting
    bedrock.
    
Automatically setting up the modules:
=====================================

I've included a MCEdit filter script ItemSorter.py which creates a 10 x 20 sorter 
If you wish to customize it, it should be pretty self explanatory.  Just modify
the bunch of CentreBlock and CentreLeft entries.

By default I have a role of 20 as "Open" for manually configuration on already 
placed sorters.

My suggestion is create this block in an empty world.  Then cut/paste as a file
to the world you want.  That way you can move it around in the import selection
process.

Files:
======

├── LICENSE
├── MCEdit-filters
│   ├── ItemSorter.py             # Sample script to create 20 x 10 sorter
│   └── ReplaceSorter.py          # Script to replace items in hopper
├── MCEdit-schematics
│   ├── ItemSorter-BL.schematic   # Modules Back Left
│   ├── ItemSorter-BC.schematic   # Modules Back Centre
│   ├── ItemSorter-BR.schematic   # Modules Back Right
│   ├── ItemSorter-CL.schematic   # Modules Centre Left
│   ├── ItemSorter-CC.schematic   # Modules Centre Centre
│   ├── ItemSorter-CR.schematic   # Modules Centre Right
│   ├── ItemSorter-FL.schematic   # Modules Front Left
│   ├── ItemSorter-FC.schematic   # Modules Front Centre
│   ├── ItemSorter-FR.schematic   # Modules Front Right
│   ├── ItemSorter-Exploded.schematic         # Exploded version of the modules above
│   ├── ItemSorter-SampleSorterTop.schematic  # Sample top for the 10 x 20 sorter
│   ├── Sample-Sorter-Hopper.schematic        # Sample 10 x 20 sorter (with hopper sub-station) - Used in 
│   ├── Sample-Sorter-Minecart.schematic      # Abandoned Minecart Design
│   ├── SelectionHouse-Hopper-Lrg.schematic   # Sample Selection House 20 x 3 deep selection
│   ├── SelectionHouse-Hopper-Sml.schematic   # Sample Selection House 20 x 1 deep selection
│   ├── SelectionHouse-Minecart-Lrg.schematic # Abandoned Minecart Design
│   ├── SelectionHouse-Minecart-Sml.schematic # Abandoned Minecart Design
│   ├── SubStation-Hopper.schematic           # Hopper based Selection Sub-Station
│   └── SubStation-Minecart.schematic         # Abandoned Minecart Design
└── Worlds
    ├── ItemSorter                            # Flat world with working system
    ├── Sample ItemSorter Hopper              # Sample world with hopper system
    └── Sample ItemSorter World               # Abandoned Minecart Design (should work but quarky)



TODO:
=====

1.  Need overflow clock on the sending stations. (Rail house and selection house)
2.  Replace world clock with pulse length extender?
3.  Hoppers into Station causes blocks arriving message to repeat for each item (item gap because of tower)
4.  Add command block custom name to sub-station.
5.  Need Light to say station is selected!
6.  Additional Stations
	- Castle Style.  (10 x 10 x 10 x 10 buttons with selection and minecart in centre)
	- Sand Castle/Temple?
7.  In Sample world add Check Points (activator and full/empty sensor)
8.  Villagers still got back in the circuit area.

