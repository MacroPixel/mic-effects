import sounddevice as sd
import winsound
import numpy as np
import random
import asyncio
import pygame
import keyboard
import subprocess
import time
from localdata import localdata

listen = True
effect = 0
running = True

ahk = subprocess.Popen( [ "C:/Program Files/AutoHotkey/AutoHotkey.exe", localdata[ 'mic_dir' ] + "remap.ahk" ] )

def f_effect0():
	global effect
	effect = 0

def f_effect1():
	global effect
	effect = 1

def f_effect2():
	global effect
	effect = 2

def f_listen():
	global listen
	listen = not listen

def f_exit():
	global running
	running = False

def ping():
	winsound.PlaySound( localdata[ 'mic_dir' ] + 'ping.wav', winsound.SND_FILENAME )

def mod_sound( indata, outdata, frames, time, status ):

	global effect

	for x in range( indata.shape[0] ):
		for y in range( indata.shape[1] ):
			if effect == 1: indata[ x, y ] = min( indata[ x, y ], 0.1 ** 20 ) * 15
	if effect == 2: indata *= 4
	outdata[:] = indata

def wait_for_input():

	while True:
		f = open( 'data.txt' ).read()
		if f == '': time.sleep( 0.1 )
		elif f == '0': f_effect0()
		elif f == '1': f_effect1()
		elif f == '2': f_effect2()
		elif f == '-': f_exit()
		elif f == 'ENTER': f_listen()
		if f != '':
			open( 'data.txt', 'w' ).write( '' )
			break

def use_mic():

	global running

	while running:
		with sd.Stream( callback = mod_sound, device = ( 1, 6 if listen else 10 ) ):
			wait_for_input()

def a():
	print( 'a' )

use_mic()

ahk.kill()
