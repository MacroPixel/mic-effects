import sounddevice as sd
import winsound
import numpy as np
import random
import asyncio
import pygame
import keyboard
import subprocess

listen = False
effect = 0
running = True

listen = True
effect = 0

ahk = subprocess.Popen( [ "C:\Program Files\AutoHotkey\AutoHotkey.exe", "remap.ahk" ] )

def ping():
	winsound.PlaySound( 'ping.wav', winsound.SND_FILENAME )

def mod_sound( indata, outdata, frames, time, status ):

	global effect

	for x in range( indata.shape[0] ):
		for y in range( indata.shape[1] ):
			if effect == 1: indata[ x, y ] = min( indata[ x, y ], 0.1 ** 20 ) * 15
	if effect == 2: indata *= 5
	outdata[:] = indata

def wait_for_input():

	global effect, listen, running

	while True:
		if keyboard.is_pressed( 'f22' ):
			listen = not listen
			while keyboard.is_pressed( 'f22' ): pass
			break
		if keyboard.is_pressed( 'f23' ):
			effect = ( effect + 1 ) % 3
			if effect == 0: ping()
			while keyboard.is_pressed( 'f23' ): pass
			break
		if keyboard.is_pressed( 'f24' ):
			running = False
			while keyboard.is_pressed( 'f24' ): pass
			break

def use_mic():

	global running

	while running:
		with sd.Stream( callback = mod_sound, device = ( 1, 6 if listen else 10 ) ):
			wait_for_input()

use_mic()

ahk.kill()