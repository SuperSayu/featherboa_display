import digitalio
import board
import storage
 
switch = digitalio.DigitalInOut(board.D10)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP
 
storage.remount("/", not switch.value)