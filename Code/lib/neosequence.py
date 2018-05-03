# The MIT License (MIT)
#
# Copyright (c) 2016 Damien P. George
# Copyright (c) 2017 Scott Shawcroft for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from digitalio import *
from random import randint
from neopixel import NeoPixel
from time import sleep
import board

__version__ = "1.0"
__repo__ = "https://github.com/SuperSayu/featherboa_display.git"

STRIP_PIN = board.D6
STRIP_BRIGHTNESS = 0.5
NUMBER_PIXELS = 8

BUTTON_PIN = board.D10
BUTTON_PULL = Pull.UP # Up: Button leads to ground

# Main loop:
# Run(Sequence_List)

# Where
# Sequence_List: [State_List,State_list,...]
#   State_List: [State,State,...]
#     State: [r,g,b, hold_time, step_count]

# Step count determines how many steps between the current color and this new color will be rendered.
# So for example if you are at [0,0,0] and go to [255,255,255,1,16] then it will render 16 steps between 0 and 255, then hold for 1s.
# Each step pauses for 1/20sec so you can see it properly.
# The total transition time is slightly longer since it loops through the pixels once more with the final value

strip = NeoPixel( STRIP_PIN, NUMBER_PIXELS, brightness = STRIP_BRIGHTNESS )
cache = [0] * NUMBER_PIXELS # persistent storage for pixel values during transitions

# Slide-in transition starting from low index (0)
def tsl( next ):
  for j in range( NUMBER_PIXELS - 1, 0, -1):
    cache[ j ] = cache[ j - 1 ]
  cache[ 0 ] = next
  strip[:] = cache
  sleep( 0.05 )
# Slide-in transition starting from high index
def tsh( next ):
  for j in range( 0, NUMBER_PIXELS - 1 ):
    cache[ j ] = cache[ j + 1 ]
  cache[ NUMBER_PIXELS - 1 ] = next
  strip[:] = cache
  sleep( 0.05 )
# fast transition that does not slide in - not used in the random set
def tfast( next ):
  for j in range( 0, NUMBER_PIXELS - 1 ):
    cache[j] = next
  strip[:] = cache
  sleep( 0.05 )
trans_funcs = [ tsl, tsh ]

# trans(): moves from one state to another.  Cur can also just be [r,g,b] which is all that is used.
def trans( cur, next ):
  s = next[4]
  tr = cur[0]
  tg = cur[1]
  tb = cur[2]
  dr = (next[0] - tr) / s
  dg = (next[1] - tg) / s
  db = (next[2] - tb) / s
  # For lack of proper direction we will just randomly pick left or right wipes for each transition
  tfunc = trans_funcs[ randint( 0, 1 ) ]
  for i in range( 1, s ):
    tr += dr
    tg += dg
    tb += db
    tfunc( [ int( tr ), int( tg ), int( tb )] )
  # The above fully animated the leading pixel.  The change must still propagate through the rest.
  # The below makes sure all pixels end up at the target value.
  temp = next[0:3]
  for i in range( 0, NUMBER_PIXELS - 1 ):
    tfunc( temp )
  sleep( next[3] )

# Writes to state.txt if we are booted in that mode, fail silently
def write_state( s ):
  try:
    with open( "state.txt", "w+" ) as f:
      f.write( str( s ) )
  except( OSError ):
    pass
  return s
# Read from state.txt with a sane default of 0
def read_state( ):
  try:
    return abs( int( next( open( "state.txt", "r" ) ) ) )
  except( OSError, ValueError ):
    return write_state(0)

def Run( seq_list ):
  # Prepare button for reading
  button = DigitalInOut( BUTTON_PIN )
  button.switch_to_input( BUTTON_PULL )
  # Figure out what light set we are using
  seq = read_state()
  if seq >= len( seq_list ):
    seq = 0
  step = 0
  trans( [0,0,0], seq_list[seq][step] )
  while True:
    old = seq_list[seq][step]
    step += 1
    if step == len( seq_list[seq] ):
      step = 0
    if not button.value:
      seq += 1
      if seq == len( seq_list ):
        seq = 0
      step = 0
      write_state( seq )
    trans( old, seq_list[seq][step] )