TODO:
=====

1.  Make teleport points in and out of command block.  Takes care of entering
    problem.  (may be have it trans port all players in r=xx where name=XXX?)

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
 - Originally I tried using a really compact sorter.  But then they selection
   part became a problem with cross talk.  Not to mention some items like wool
   would cause sorters beside to activate and empty their contents.
 - It's surrounded by bedrock so it can't be entered in adventure/survival mode
   unless accompanied by administrator
 - It's design was intended to place under the bottom layer of bed rock using 
   MCEdit.  That way it doesn't destroy the existing world too much.  You just
   need to use mine carts to transport items around
 - There should be enough light generated in the housing to stop MOB spawning,
   or so I hope.
 - The inside should be completely navigable in adventure/survival mode. You 
   might get lost though.
 - There is signs on each block/area explaining what it's doing.
 - There's a set of chests lining the back wall (file 010) for the items not 
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


Setting up each module:
=======================

Each module needs to be setup to accept items.  

  - There will be left over dirt in the hoppers/chests.  Remove it.
  - Each module has 8 command blocks with a code item001.  This needs to be 
    replaced with the item (like Glass, or Dirt)
  - Hit button on initialize command block.
  - Replace dirt items from selection hopper (place 18-1-1-1-1) with items to
    be selected (might not be 18 for things like eggs)

