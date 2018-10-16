import pyautogui
import subprocess

import time
import csv

# remove this after done developing
#pyautogui.PAUSE = 1

# https://medium.com/@tracy_blog/pyautogui-and-retina-displays-2d5c37a5aa5e
IS_RETINA_DISPLAY = True #subprocess.call("system_profiler SPDisplaysDataType | grep 'retina'", shell= True) == 0


# while True:
# 	x, y = pyautogui.position()
# 	positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
# 	print(positionStr)

# returns [-1,-1] if can't find image
def findImage(png_name):
	button = pyautogui.locateCenterOnScreen(png_name)
	if button == None:
		print("Button {0} not found".format(png_name))
		return [-1,-1]
	x = button[0]
	y = button[1]
	if IS_RETINA_DISPLAY:
		x = x / 2
		y = y / 2
	return [x, y]

def clickImage(png_name):
	x, y = findImage(png_name)
	if x == -1:
		return False
	pyautogui.click((x, y))
	return True

def moveRightBeats(n):
	for i in range(n):
		pyautogui.press('right')

def moveLeftBeats(n):
	for i in range(n):
		pyautogui.press('left')

def moveRightOneLocator():
	return clickImage('gui-keys/right-locator.png')

def moveLeftOneLocator():
	return clickImage('gui-keys/left-locator.png')

def rightClickAboveCursor():
	PIX_UP = 20
	x, y = findImage('gui-keys/cursor2.png')
	if x == -1:
		x, y = findImage('gui-keys/cursor-alt.png')
		if x == -1:
			return False
	pyautogui.rightClick((x, y - PIX_UP))
	return True

def addLocator(locatorName):
	PIX_DOWN = 45
	PIX_RIGHT = 15
	PIX_UP_TO_RESET = 10

	name = str(locatorName)

	rightClickAboveCursor()
	pyautogui.moveRel(PIX_RIGHT, PIX_DOWN)
	pyautogui.click()
	pyautogui.typewrite(name)
	pyautogui.press('enter')

	# click back in measure to escape 
	pyautogui.moveRel(-PIX_RIGHT, -PIX_UP_TO_RESET)
	pyautogui.click()

# e.g. '6/4' -> newMeterTop = 6, newMeterBot = 4
# POTENTIAL BUG:
# if there's already a time signature there, it will delete it without making new one.
def addTimeSigChange(newTimeSigTop, newTimeSigBot):
	PIX_DOWN = 5
	PIX_RIGHT = 15
	PIX_DOWN_TO_RESET = 30

	top = str(newTimeSigTop)
	bot = str(newTimeSigBot)

	rightClickAboveCursor()
	pyautogui.moveRel(PIX_RIGHT, PIX_DOWN)
	pyautogui.click()
	pyautogui.typewrite([top, '/', bot, 'enter'])

	# click back in measure to escape 
	pyautogui.moveRel(-PIX_RIGHT, PIX_DOWN_TO_RESET)
	pyautogui.click()

# def addTempoChange(newTempoBPM):
# 	PIX_UP = 86

# 	tempo = str(newTempoBPM)
# 	x, y = findImage('gui-keys/cursor-tempo.png')
# 	if x == -1:
# 		return False
# 	pyautogui.moveTo((x, y - PIX_UP))
# 	pyautogui.click()
# 	#print("click")
# 	#time.sleep(0.2)
# 	#pyautogui.click()
# 	#print("click")
# 	pyautogui.doubleClick((x, y - PIX_UP), interval=.25)
# 	pyautogui.dragRel(0, -10, 1, button='left')
# 	return True

def moveToStart():
	# button turns grey at first locator
	while moveLeftOneLocator() == True:
		continue

# highlights n beats (quarter notes) to the right of current cursor
def highlightBeats(n):
	pyautogui.keyDown('shift')
	#print("n", n)
	for i in range(n):
		pyautogui.press('right')
	pyautogui.keyUp('shift')

def escapeHighlight():
	pyautogui.press('esc')

# 6/8 = 3 quarters
# 3/4 = 3 quarters
# 2/2 = 4 quarters

def measuresToBeats(numMeasures, timeSigTop, timeSigBot):
	return numMeasures * timeSigTop * int(4 / timeSigBot)

def highlightMeasures(n, timeSigTop, timeSigBot):
	numBeats = measuresToBeats(n, timeSigTop, timeSigBot)
	highlightBeats(numBeats)

def moveRightMeasures(n, timeSigTop, timeSigBot):
	numBeats = measuresToBeats(n, timeSigTop, timeSigBot)
	moveRightBeats(numBeats)

def copy():
	pyautogui.hotkey('command', 'c')

def paste():
	pyautogui.hotkey('command', 'v')

# note duplicate n times makes n+1 total instances
def duplicate(n):
	for i in range(n):
		pyautogui.hotkey('command', 'd')

# combines highlighted clips into single clip
def consolidate():
	pyautogui.hotkey('command', 'j')

# renames the highlighted clip
# make sure newName is a unicode string
def rename(newName):
	#name = #str(newName, 'utf-8')#u'1.1 Click, 150BPM'#str(newName)
	#print(name)
	if 'm' in newName:
		print("warning: m in newName being replaced with M") # because lowercase m opens a menu
		newName = newName.replace(u'm', u'M')
	if '-' in newName:
		print("warning: - in newName being replaced with _") # because lowercase m opens a menu
		newName = newName.replace(u'-', u'_')

	pyautogui.hotkey('command', 'r')
	keys = [c for c in newName]
	for k in keys:
		pyautogui.press(k)
		time.sleep(.1)
	pyautogui.press('enter')
	#print(keys)
	#pyautogui.typewrite(keys)
	#pyautogui.press('enter')


# creates n instances of whatevers in the clipboard
def pasteN(n):
	paste()
	duplicate(n-1)

# cursor must be at the beginning of the track, and
# beginning of track must be in view
def rightClickTrackName():
	PIX_DOWN = 5
	PIX_RIGHT = 5
	x, y = findImage('gui-keys/cursor-alt.png') # because most likely has a locator
	if x == -1:
		x, y = findImage('gui-keys/cursor.png')
		if x == -1:
			return False
	pyautogui.rightClick((x + PIX_RIGHT, y + PIX_DOWN))
	return True

def moveClipToSessionView():
	PIX_DOWN = 230
	PIX_RIGHT = 10
	rightClickTrackName()
	pyautogui.moveRel(PIX_RIGHT, PIX_DOWN)
	time.sleep(1)
	pyautogui.click()

def metronomePosition(timeSigTop, timeSigBot):
	if timeSigTop == 6 and timeSigBot == 4:
		return 0
	elif timeSigTop == 4 and timeSigBot == 4:
		return 6
	elif timeSigTop == 2 and timeSigBot == 4:
		return 10
	elif timeSigTop == 2 and timeSigBot == 2:
		return 12
	else:
		print("No metronome for time signature " + str(timeSigTop) + "/" + str(timeSigBot))
		raise Exception

def renameSessionViewScene(songNum, songTitle, measuresDescription, isVamp, tempo, isFirstSceneOfSong, globalSceneNum):
	vampStr = ""
	if isVamp:
		vampStr = " VAMP"
	titleStr = ""
	if isFirstSceneOfSong:
		titleStr = u'{} {} '.format(songNum, songTitle)
	name = u'{}{}{}; {} BPM'.format(titleStr, measuresDescription, vampStr, tempo)

	#pyautogui.press("up")
	pyautogui.press("right")
	#slotsToMoveDown = 1
	#if globalSceneNum == 1:
	#	slotsToMoveDown == 2 # move down extra for the first one
	#for i in range(slotsToMoveDown):
	pyautogui.press("down")
	rename(name)

def toggleSessionArrangementView():
	#clickImage('gui-keys/session-view.png')
	pyautogui.press('tab')

#def switchToArrangementView():
	#clickImage('gui-keys/arrangement-view.png')

def configScene(nBeats, isVamp):
	PIX_DOWN = 25
	PIX_RIGHT = 80
	PIX_RIGHT_2 = 20
	PIX_DOWN_2 = 20

	# find "None" section of groove
	x, y = findImage('gui-keys/none.png')
	if x == -1:
		raise Exception
	print(x, y)

	# enter length through beats only. Zero measures
	pyautogui.moveTo(x, y)
	pyautogui.moveRel(PIX_RIGHT, PIX_DOWN)
	pyautogui.click()
	pyautogui.typewrite(['0', 'enter'])

	# beats
	pyautogui.moveRel(PIX_RIGHT_2, 0)
	pyautogui.click()
	pyautogui.typewrite(str(nBeats))
	pyautogui.press(['enter'])

	# 16ths? I think
	pyautogui.moveRel(PIX_RIGHT_2, 0)
	pyautogui.click()
	pyautogui.typewrite(['0', 'enter'])

	# select follow action
	pyautogui.moveRel(-2 * PIX_RIGHT_2, PIX_DOWN_2)
	pyautogui.click()
	pixDownToFollowAction = 30
	if isVamp:
		pixDownToFollowAction = 40
	pyautogui.moveRel(0, pixDownToFollowAction)
	pyautogui.click()

def addSubScene(tempo, numMeasures, timeSigTop, timeSigBot, globalSceneNum, beatsInSceneSoFar):
	addTimeSigChange(timeSigTop, timeSigBot)
	moveToStart()
	moveRightBeats(metronomePosition(timeSigTop, timeSigBot))
	# move to correct metronome
	highlightBeats(measuresToBeats(1, timeSigTop, timeSigBot))
	copy()
	escapeHighlight()
	for i in range(globalSceneNum):
		moveRightOneLocator() # n locators
	moveRightBeats(beatsInSceneSoFar)
	pasteN(numMeasures)
	escapeHighlight()
	moveRightBeats(measuresToBeats(1, timeSigTop, timeSigBot))


#def addScene(tempo, subScenes, songNum, songSceneNum, globalSceneNum, measuresDescription, songTitle):
def addScene(scene, song, songSceneNum, globalSceneNum):
	#assert len(numMeasuresList) == len(timeSigTopList) == len(timeSigBotList)

	addLocator("{}.{}".format(song.num, songSceneNum))

	beatsInSceneSoFar = 0
	for subScene in scene.subScenes:
		numMeasures = subScene.numMeasures
		assert numMeasures > 0
		timeSigTop = subScene.timeSigTop
		timeSigBot = subScene.timeSigBot
		addSubScene(scene.tempo, numMeasures, timeSigTop, timeSigBot, globalSceneNum, beatsInSceneSoFar)
		beatsInSceneSoFar += measuresToBeats(numMeasures, timeSigTop, timeSigBot)
	# for i in range((len(numMeasuresList))):1.1

	# 	numMeasures = numMeasuresList[i]
	# 	assert numMeasures > 0
	# 	timeSigTop = timeSigTopList[i]
	# 	timeSigBot = timeSigBotList[i]
	# 	addSubScene(tempo, numMeasures, timeSigTop, timeSigBot, globalSceneNum, beatsInSceneSoFar)
	# 	beatsInSceneSoFar += measuresToBeats(numMeasures, timeSigTop, timeSigBot)

	moveLeftOneLocator()
	highlightBeats(beatsInSceneSoFar)
	#highlightMeasures(numMeasures, timeSigTop, timeSigBot)
	consolidate()
	escapeHighlight()
	#highlightBeats(1)
	rename(u'Click {}.{}, {} BPM, {}'.format(song.num, songSceneNum, scene.tempo, scene.measuresDescription))
	time.sleep(2)
	escapeHighlight()
	moveClipToSessionView()
	escapeHighlight()
	toggleSessionArrangementView()
	renameSessionViewScene(song.num, song.title, scene.measuresDescription, scene.isVamp, scene.tempo, songSceneNum == 1, globalSceneNum)
	pyautogui.press('left')
	configScene(beatsInSceneSoFar, scene.isVamp)
	toggleSessionArrangementView()
	#moveRightMeasures(numMeasures, timeSigTop, timeSigBot)
	moveRightBeats(beatsInSceneSoFar)
	moveRightBeats(measuresToBeats(1, timeSigTop, timeSigBot)) # leave 1 measure and gap/

def createClickTrack(songs):
	END_OF_METRONOME_BEATS = 16
	moveToStart()
	moveRightBeats(END_OF_METRONOME_BEATS + 4)

	globalSceneNum = 0
	for song in songs:
		for i, scene in enumerate(song.scenes):
			tempo = scene.tempo
			songNum = song.num
			sceneNum = i + 1
			globalSceneNum += 1
			#songTitle = song.title##############
			#isVamp = scene.isVamp###############
			#addScene(tempo, scene.subScenes, songNum, sceneNum, globalSceneNum, scene.measuresDescription, songTitle)
			addScene(scene, song, sceneNum, globalSceneNum)
			



	# numScenes = 2
	# for i in range(numScenes):
	# 	tempo = 164
	# 	numMeasures = 8
	# 	timeSigTop = 6
	# 	timeSigBot = 4
	# 	#startBeat = 14
	# 	songNum = 1
	# 	sceneNum = 1
	# 	addScene(tempo, [numMeasures, 3], [timeSigTop, 4], [timeSigBot, 4], songNum, sceneNum, i + 1)
	# 	sceneNum += 1
	# 	if newSong:
	# 		songNum += 1
	# 		sceneNum = 1

class Song:
	def __init__(self):
		self.title = None
		self.scenes = []

class Scene:
	def __init__(self):
		self.num = None
		self.measuresDescription = None
		self.subScenes = []
		self.isVamp = False
		self.empo = None

class SubScene:
	def __init__(self):
		self.numMeasures = None
		self.timeSigTop = None
		self.timeSigBot = None

def readCSV(filename):
	SONG_COL = 0
	SCENE_COL = 1
	MEASURES_COL = 2
	DURATION_COL = 3
	METER_COL = 4
	TEMPO_COL = 5
	IS_A_VAMP_COL = 6
	with open(filename) as csvFile:
		csvReader = csv.reader(csvFile, delimiter=',')
		headers = next(csvReader)
		songs = []
		for row in csvReader:
			songTitle = row[SONG_COL]
			sceneNum = row[SCENE_COL]
			measuresDescription = row[MEASURES_COL]
			duration = row[DURATION_COL]
			meter = row[METER_COL]
			tempo = row[TEMPO_COL]
			isVamp = row[IS_A_VAMP_COL]
			if songTitle != "":
				song = Song()
				song.num = songTitle.split(' ')[0]
				song.title = ' '.join(songTitle.split(' ')[1:])
				songs.append(song)
			if sceneNum != "":
				scene = Scene()
				scene.num = int(sceneNum)
				scene.measuresDescription = measuresDescription
				scene.tempo = tempo
				if str.lower(isVamp) in ["y", "yes", "t", "true", "1"]:
					scene.isVamp = True
				song.scenes.append(scene)
			subScene = SubScene()
			subScene.numMeasures = int(duration)
			subScene.timeSigTop = int(meter.split('/')[0])
			subScene.timeSigBot = int(meter.split('/')[1])
			scene.subScenes.append(subScene)
		return songs

#subprocess.Popen(['open', 'Template/Click.als'])
#time.sleep(4) # wait for ableton to open

#pyautogui.typewrite(['enter']) # to accept free trail warning
time.sleep(1)

songs = readCSV('Click Tracking-Table 1.csv')
createClickTrack(songs)

#switchToSessionView()
#renameSessionViewScene(1, "I Hope I Get It", "m37-39", False, 150, True, 3)
#switchToArrangementView()
#switchToSessionView()
#configScene(10, True)

#29.0 588.5

#110 613








