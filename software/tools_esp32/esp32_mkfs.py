# https://forum.micropython.org/viewtopic.php?t=3102
import os
import flashbdev
os.VfsFat.mkfs(flashbdev.bdev)

print('Done')
