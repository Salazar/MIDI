# name=LK MK3 2.0 By Myke

import ui 	# The script will use UI functions 
import midi	# The script will use MIDI functions.  
import transport
import playlist
import mixer
import patterns
import arrangement
import device
import general
import launchMapPages
import channels

# or in hex 0x6E. 110 is 6E in hex, but for scripting you need to proceed it by 0x so it's 0x6E. For the next variable lets use Hex
# or 111 in decimal.

''' 

FOR FPT Controls, use transport.globalTransport(midi.FPT_FuncName, 1)

'''

### TRANSPORT BUTTONS ON THE RIGHT OF THE KEYBOARD
Record = 117
Play = 115
Stop = 105
ToggleLoop = 104
Up = UndoUp = 106
Down = UndoDown = 107
Left = TabLeft = 103
Right = TabRight = 102 

### VERTICAL PAD PAIR FROM LEFT TO RIGHT
"""
Playlist(F5)   C-Rack(F6)	P-Roll(F7)	 Mixer(F9)   PtrnUp    Overdub   SnapUp    BPM    [ToggleLoop]
CRack-Up	   CRack-Down   Mute         Solo        PtrnDown  LoopRec   SnapDown  Metro  [STOP]

Shift Up = Undo
Shift Down = Redo

Shift left = Prev Window
Shift Right = Next Window
"""

Playlist = 1
ChannelRack = 2
PianoRoll = 3
Mixer = 4

Previous = 9
Next = 10
Mute = 11
Solo = 12

PatternUp = 5
PatternDown = 13
Overdub = 6
LoopRecord = 14

SnapUp = 7
SnapDown = 15
TapTempo = 8
Metro = 16

### KNOBS

KNOB1 = 21
KNOB2 = 22
KNOB3 = 23
KNOB4 = 24
KNOB5 = 25
KNOB6 = 26
KNOB7 = 27
KNOB8 = 28


Knobs = [
	21,
	22,
	23,
	24,
	25,
	26,
	27,
	28,
]

VAL_MIN = 1
VAL_MAX = 127

ON = 1
OFF = 0

#  1st byte - midiID (function), is it Note or Control Change data?  
#  2nd byte - data1 - Data associated with the MIDI event. Normally this is the value to use.
#  3rd byte - data2 - Data associated with the MIDI event. Normally ignore this value.


class LKMK3():

	def OnInit(self):
		print("Launchkey Mini MK3")
		print("Script by Myke (Cadenzic Records)")


	def OnMidiMsg(self, event): 
		event.handled = False

		# FOR PRINTING DATA ON SCRIPT OUTPUT
		
		print("status: {}, port: {}, midiId: {}, data1: {}, data2: {}".format(event.status, event.port, event.midiId, event.data1, event.data2))

		# CONTROL CHANGE EVENT FOR BUTTONS OF MIDI
		if event.midiId == midi.MIDI_CONTROLCHANGE:
			if event.data2 > 0:

				if event.data1 == Play:
					print('Playback')
					transport.start()
					ui.setHintMsg("Play/Pause")
					event.handled = True
				elif event.data1 == Record:
					print('Record')
					transport.record()
					ui.setHintMsg("Record")
					event.handled = True
				elif event.data1 == Stop:
					print('Stop')
					transport.stop()
					ui.setHintMsg("Stop")
					event.handled = True
				elif event.data1 == ToggleLoop:
					print('Toggle Loop')
					transport.setLoopMode()
					ui.setHintMsg("Pattern/Song")
					event.handled = True

				elif event.data1 == Left:
					print('Previous Tab')
					transport.globalTransport(midi.FPT_WindowJog, -1)
					ui.setHintMsg("Previous Tab")
					event.handled = True
				elif event.data1 == Right:
					print('Next Tab')
					transport.globalTransport(midi.FPT_WindowJog, 1)
					ui.setHintMsg("Next Tab")
					event.handled = True
				
				elif event.data1 == Up:
					print('Undo Up')
					general.undoUp()
					ui.setHintMsg("Undo Up")
					event.handled = True
				elif event.data1 == Down:
					print('Undo Down/ReDo')
					general.restoreUndo()
					ui.setHintMsg("Undo Down/ReDo")
					event.handled = True
				
				elif event.data1 in Knobs:
					mixer.setTrackVolume(
						mixer.trackNumber() + Knobs.index(event.data1),
						event.data2 / 127
					)
					event.handled = True

		#MIDI NOTE ON/OFF FOR NOTE EVENTS
		elif event.midiId == midi.MIDI_NOTEON:
			if (event.pmeFlags & midi.PME_System !=0):

				if event.data1 == Playlist:
					print('Playlist')
					transport.globalTransport(midi.FPT_F5, 1)
					ui.setHintMsg("Playlist")
					event.handled = True
				elif event.data1 == ChannelRack:
					print('ChannelRack')
					transport.globalTransport(midi.FPT_F6, 1)
					ui.setHintMsg("ChannelRack")
					event.handled = True
				elif event.data1 == PianoRoll:
					print('PianoRoll')
					transport.globalTransport(midi.FPT_F7, 1)
					ui.setHintMsg("PianoRoll")
					event.handled = True
				elif event.data1 == Mixer:
					print('Mixer')
					transport.globalTransport(midi.FPT_F9, 1)
					ui.setHintMsg("Mixer")
					event.handled = True

				elif event.data1 == Previous:
					print('Previous')
					ui.previous()
					ui.setHintMsg("Previous")
					event.handled = True
				elif event.data1 == Next:
					print('Next')
					ui.next()
					ui.setHintMsg("Next")
					event.handled = True

				elif event.data1 == Mute:
					print('Mute')
					channels.muteChannel(channels.channelNumber())
					ui.setHintMsg("Mute")
					event.handled = True
				elif event.data1 == Solo:
					print('Solo')
					channels.soloChannel(channels.channelNumber())
					ui.setHintMsg("Solo")
					event.handled = True

				elif event.data1 == PatternUp:
					print('Pattern Up')
					transport.globalTransport(midi.FPT_PatternJog, -1)
					ui.setHintMsg("Pattern Up")
					event.handled = True
				elif event.data1 == PatternDown:
					print('Pattern Down')
					transport.globalTransport(midi.FPT_PatternJog, 1)
					ui.setHintMsg("Pattern Down")
					event.handled = True

				elif event.data1 == Overdub:
					print('Overdub')
					transport.globalTransport(midi.FPT_Overdub, 1)
					ui.setHintMsg("Overdub")
					event.handled = True
				elif event.data1 == LoopRecord:
					print('Loop Record')
					transport.globalTransport(midi.FPT_LoopRecord, 1)
					ui.setHintMsg("Loop Record")
					event.handled = True

				elif event.data1 == SnapUp:
					print('Snap -1')
					transport.globalTransport(midi.FPT_SnapMode, -1)
					ui.setHintMsg("Snap -1")
					event.handled = True
				elif event.data1 == SnapDown:
					print('Snap +1')
					transport.globalTransport(midi.FPT_SnapMode, 1)
					ui.setHintMsg("Snap +1")
					event.handled = True

				elif event.data1 == TapTempo:
					print('Tap Tempo')
					transport.globalTransport(midi.FPT_TapTempo, 1)
					ui.setHintMsg("Tap Tempo")
					event.handled = True
				elif event.data1 == Metro:
					print('Metronome')
					transport.globalTransport(midi.FPT_Metronome, 1)
					ui.setHintMsg("Metronome")
					event.handled = True


'''
# CODE FOR MIXER NAVIGATION yet to be checked

				elif event.data1 == PAD12:
					print('D')
					ui.showWindow(midi.widMixer)
					transport.globalTransport(midi.FPT_Left, 1)
					ui.setHintMsg("D")
					 
				elif event.data1 == PAD13:
					print('D')
					ui.showWindow(midi.widMixer)
					transport.globalTransport(midi.FPT_Right, 1)
					ui.setHintMsg("D")
					 
'''


lk = LKMK3()

def OnInit():
	lk.OnInit()

def OnMidiMsg(event):
	lk.OnMidiMsg(event)


# print("handled: {}, timestamp: {}, status: {}, data1: {}, data2: {}, port: {}, midiId: {}".format(event.handled, event.timestamp, event.status, event.data1, event.data2, event.port, event.midiId))

#Lighting SysEx
# device.midiOutSysex(bytes([240, 0, 32, 41, 2, 13, 3, 144, 105, 3, 247]))
