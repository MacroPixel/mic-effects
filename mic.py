import sounddevice as sd
import soundfile as sf
import winsound
import numpy as np
import random
import subprocess
import time
from localdata import localdata
import traceback

listen = True
filtered = True
effect = 0
running = True

sounds = []
IN_DEVICES = [ 'Krisp Microphone (Krisp)', 'Microphone (Razer Seiren Mini)' ] # Filtered, non-filtered
OUT_DEVICES = [ 'Realtek HD Audio 2nd output (Re', 'CABLE Input (VB-Audio Virtual C' ] # Playback, external

ahk = subprocess.Popen( [ "C:/Program Files/AutoHotkey/AutoHotkey.exe", localdata[ 'mic_dir' ] + "remap.ahk" ] )

def log( string ):

  print( string )

def get_device( name ):

  for i, device in enumerate( sd.query_devices() ):
    if device[ 'name' ] == name:
      return i

def f_effect0():
  global effect, filtered
  effect = 0
  filtered = True
  print( '[!] Switched to default mic' )

def f_effect1():
  global effect, filtered
  effect = 1
  filtered = True
  print( '[!] Switched to loud mic' )

def f_effect2():
  global effect, filtered
  effect = 0
  filtered = False
  print( '[!] Switched to unfiltered mic' )

def f_effectExtreme():
  global effect, filtered
  effect = 99
  filtered = False
  print( '[!] Switched to extreme mic' )
  ping( pingtype = 'extreme' )

def f_effect9():
  global effect
  effect = 9
  print( '[!] Switched to muted mic' )

def f_listen():
  global listen
  listen = not listen
  if listen:
    print( '[***] Listening turned on' )
  else:
    print( '[**] Listening turned off' )

def f_exit():
  global running
  running = False

def ping( pingtype = 'quit' ):

  if pingtype in [ 'extreme', 'quit' ]:
    winsound.PlaySound( localdata[ 'mic_dir' ] + 'ping2.wav', winsound.SND_FILENAME )

def load_sounds():

  for sound in open( 'sound_list.txt' ).read().split( '\n' ):
    sounds.append( sound )

def set_sound( index, new_name ):

  sounds[ index ] = new_name
  file = open( 'sound_list.txt', 'w' )
  file.write( '\n'.join( sounds ) )
  file.close()

def playsound( index ):

  try:
    data, fs = sf.read( 'soundboard/' + sounds[ index ], dtype = 'float32' )
    sd.play( data, fs, device = get_device( out_device ) )
    log( f'[#] Played sound { sounds[ index ] }' )
  except IndexError:
    print( f'No sound in memory for index { index }' )
  except FileNotFoundError:
    print( 'File could not be found' )

def mod_sound( indata, outdata, frames, time, status ):

  global effect

  for x in range( indata.shape[0] ):
    for y in range( indata.shape[1] ):
      if effect == 99: indata[ x, y ] = min( indata[ x, y ], 0.1 ** 20 ) * 15
  if effect == 1: indata *= 4
  if effect == 9: indata *= 0
  outdata[:] = indata

def read_keyboard_data():

  f = open( localdata[ 'mic_dir' ] + 'data.txt' ).read()
  if f == '':
    time.sleep( 0.1 )
  else:
    open( localdata[ 'mic_dir' ] + 'data.txt', 'w' ).write( '' )
  return f

def use_mic():

  global running, in_device, out_device

  while running:

    in_device = IN_DEVICES[ 0 if filtered else 1 ]
    out_device = OUT_DEVICES[ 0 if listen else 1 ]

    with sd.Stream( callback = mod_sound, device = ( get_device( in_device ), get_device( out_device ) ) ):

      while True:

        f = read_keyboard_data()
        if f in [ 'enter_normal', 'sub', '9_sb' ]:
          sd.stop()
          log( '[#] Stopped playback' )
        if f == '0_normal': f_effect0()
        elif f == '1_normal': f_effect1()
        elif f == '2_normal': f_effect2()
        elif f == 'add_normal': f_effectExtreme()
        elif f == '9_normal': f_effect9()
        elif f == 'sub': f_exit()
        elif f == 'enter_normal': f_listen()
        elif f == 'div_normal':

          try:
            sound_index, sound_name = input( 'Enter "[index] : [new_name]" ' ).split( ' : ' )
            set_sound( int( sound_index ), sound_name )
          except ( ValueError, IndexError ):
            print( traceback.format_exc() )
            print( 'Incorrect input' )

        elif f == '0_sb': playsound( 0 )
        elif f == '1_sb': playsound( 1 )
        elif f == '2_sb': playsound( 2 )
        elif f == '3_sb': playsound( 3 )
        if f in [ 'enter_normal', 'sub' ] or in_device != IN_DEVICES[ 0 if filtered else 1 ]:
          break


try:

  load_sounds()
  use_mic()

except Exception:

  print( traceback.format_exc() )
  ping()
  input( 'Press any key to close' )

else:

  log( 'Closing program...' )
  ping()

ahk.kill()