import clr
import sys
import json
import os
import ctypes
import codecs

ScriptName = "Annonceur"
Website = "http://www.github.com/DomiBot/ScriptChatBot"
Description = "Annonce de bienvenue pour Streamlabs ChatBot"
Creator = "Domi"
Version = "1.0.0"

configFile = "config.json"
settings = {}
volume = 0.1
command = "__WelcomeAnnouncer__"
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
			"words": "hey, hi, hello, salut, bonjour",
			"permission": "Everyone",
			"volume": 50.0,
			"useCooldown": True,
			"useCooldownMessages": False,
			"userCooldown": 1800,
			"onUserCooldown": "$user, la commande est sur cooldown pour $cd minutes!",
			"responseHello": "Salut ($user) Bienvenue!"
		}

	volume = settings["volume"] / 100.0
	sounds = os.listdir(soundspath)	

	words = settings["words"].replace(" ","").split(",")
	words = [k.lower() for k in words]

	return

def Execute(data):
	if data.IsChatMessage() and (data.GetParam(0).lower() in words) and Parent.HasPermission(data.User, settings["permission"], "") and ((settings["liveOnly"] and Parent.IsLive()) or (not settings["liveOnly"])):
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
			
			outputMessage = settings["responseHello"]

		outputMessage = outputMessage.replace("$user", username)

		Parent.SendStreamMessage(outputMessage)
	return

def ReloadSettings(jsonData):
	Init()

	return

def Tick():
	return
