import clr
import sys
import json
import os
import ctypes
import codecs

ScriptName = "Notification"
Website = "http://www.github.com/Domi/ScriptChatBot"
Description = "Notification Streamlabs ChatBot"
Creator = "Domi"
Version = "1.0.0"

configFile = "config.json"
settings = {}
volume = 0.1
soundspath = ""
sounds = []
words = []

def ScriptToggled(state):
	return

def Init():
	global sounds, soundspath, volume, words, settings

	path = os.path.dirname(__file__)
	soundspath = path + "\\sounds"

	try:
		with codecs.open(os.path.join(path, configFile), encoding='utf-8-sig', mode='r') as file:
			settings = json.load(file, encoding='utf-8-sig')
	except:
		settings = {
			"liveOnly": True,
			"permission": "Everyone",
			"volume": 50.0,
			"useCooldown": True,
			"useCooldownMessages": False,
			"userCooldown": 1800,
			"onUserCooldown": "$user, $command is still on user cooldown for $cd minutes!",
			
		}

	volume = settings["volume"] / 1000.0
	sounds = os.listdir(soundspath)	



	return

def Execute(data):
	if data.IsChatMessage() and Parent.HasPermission(data.User, settings["permission"], "") and ((settings["liveOnly"] and Parent.IsLive()) or (not settings["liveOnly"])):
		outputMessage = ""
		userId = data.User			
		username = data.UserName

		if settings["useCooldown"] and (Parent.IsOnUserCooldown(ScriptName, command, userId)):
			if settings["useCooldownMessages"]:
				cdi = Parent.GetUserCooldownDuration(ScriptName, command, userId)
				cd = str(cdi / 60) + ":" + str(cdi % 60).zfill(2) 
				outputMessage = settings["onUserCooldown"]
				outputMessage = outputMessage.replace("$cd", cd)
			else:
				outputMessage = ""
		else:
			sound = sounds[Parent.GetRandom(0, len(sounds))]

			soundpath = soundspath + "\\" + sound
			if Parent.PlaySound(soundpath, volume): 
				if settings["useCooldown"]:
					Parent.AddUserCooldown(ScriptName, command, userId, settings["userCooldown"])
					
		outputMessage = outputMessage.replace("$user", username)
		
		Parent.SendStreamMessage(outputMessage)
	return

def ReloadSettings(jsonData):
	Init()

	return

def Tick():
	return
