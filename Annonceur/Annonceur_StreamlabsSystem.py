import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

import os
import codecs
import json
import time
import collections

ScriptName = "Annonceur"
Website = "https://github.com/DomiBot/ScriptChatBot"
Description = "Annonce de bienvenue pour Streamlabs Chatbot"
Creator = "Domi"
Version = "1.0.0"

CustomSettingsFile = os.path.join(os.path.dirname(__file__), "customSettings.json")
isEnabled = True
AddMessage = ""
DeleteMessage = 0
SendMessages = True
SafeQuestion = False
DeleteViewer = ""

class Settings(object):
	""" Load in saved settings file if available else set default values. """
	def __init__(self, CustomSettingsFile=None):
		try:
			with codecs.open(CustomSettingsFile, encoding="utf-8-sig", mode="r") as f:
				self.__dict__ = json.load(f, encoding="utf-8")
		except:
			self.messages = ["Welcome to the community {viewer}!"]
			self.viewers = {}

	def Reload(self, jsondata):
		""" Reload settings from AnkhBot user interface by given json data. """
		self.__dict__ = json.loads(jsondata, encoding="utf-8")
		return

	def Save(self, CustomSettingsFile):
		""" Save settings contained within to .json and .js settings files. """
		with codecs.open(CustomSettingsFile, encoding="utf-8-sig", mode="w+") as f:
			json.dump(self.__dict__, f, encoding="utf-8", ensure_ascii=False, indent=4, sort_keys=True)
		#Parent.Log(ScriptName, "The settings file could not be saved!")
		return

def Init():
	global ScriptSettings
	
	ScriptSettings = Settings(CustomSettingsFile)
	return

def ReloadSettings(jsondata):
	global ScriptSettings, AddMessage, DeleteMessage, SendMessages, SafeQuestion, ViewerToDelete

	UISettings = Settings(CustomSettingsFile)
	UISettings.Reload(jsondata)
	AddMessage = UISettings.AddMessage
	DeleteMessage = UISettings.DeleteMessage
	SendMessages = UISettings.SendMessages
	SafeQuestion = UISettings.SafeQuestion
	ViewerToDelete = UISettings.ViewerToDelete
	
	if AddMessage.replace(" ", "") != "" and AddMessage not in ScriptSettings.messages:
		ScriptSettings.messages.append(AddMessage)
		Parent.Log(ScriptName, "Succsessfully added the message: {0}".format(AddMessage))
		ScriptSettings.Save(CustomSettingsFile)
	if DeleteMessage != 0:
		if DeleteMessage <= len(ScriptSettings.messages):
			Parent.Log(ScriptName, "Succsessfully removed the message: {0}".format(ScriptSettings.messages[DeleteMessage - 1]))
			del ScriptSettings.messages[DeleteMessage - 1]
			ScriptSettings.Save(CustomSettingsFile)
		else:
			Parent.Log(ScriptName, 	"There is no message with the ID {0}!".format(DeleteMessage))
	return

def Unload():
	ScriptSettings.Save(CustomSettingsFile)
	return

def ScriptToggled(state):
	global ScriptSettings, isEnabled

	if not state:
		ScriptSettings.Save(CustomSettingsFile)
		isEnabled = False
	else:
		isEnabled = True
	return

def Execute():

	return

def GetKeyByIndex(dictionary, index):
	counter = 0
	for key, value in dictionary.iteritems():
		if counter == index:
			return key
		counter += 1
	return
		
def Tick():
	global ScriptSettings, isEnabled, SendMessages;
	
	if isEnabled:
		viewers = Parent.GetViewerList()
		
		for viewer in viewers:
			try:
				if not viewer in ScriptSettings.viewers:
					if SendMessages:
						for message in ScriptSettings.messages:
							Parent.SendStreamMessage(message.replace("{viewer}", Parent.GetDisplayName(viewer)))
					ScriptSettings.viewers[viewer] = time.strftime("%Y/%m/%d")
					Parent.Log(time.strftime("%H:%M"), viewer + " has joined your stream for the first time!")
			except:
				ScriptSettings.viewers = {}
	return

def DeleteViewers():
	global ScriptSettings, SafeQuestion

	if SafeQuestion:
		ScriptSettings.viewers = {}
		Parent.Log(ScriptName, "Deleted all viewers!")
	else:
		Parent.Log(ScriptName, "Please check the checkbox first and press the \"Save Settings\" button before you press the \"Delete ALL Viewers\" button! - Viewers have not been removed!")
	return
	
def ShowViewers():
	global ScriptSettings
	
	if len(ScriptSettings.viewers) == 0:
		Parent.Log(ScriptName, "Your viewer list is empty!")
	else:
		Parent.Log("Join date", "Your {0} viewers:".format(len(ScriptSettings.viewers)))
		ordered = collections.OrderedDict(sorted(ScriptSettings.viewers.items()))
		for viewer, time in ordered.iteritems():
			Parent.Log(time, viewer)
	return

def DeleteViewer():
	global ScriptSettings, ViewerToDelete
	
	if ViewerToDelete.replace(" ", "") != "":
		if ViewerToDelete in ScriptSettings.viewers:
			del ScriptSettings.viewers[ViewerToDelete]
			Parent.Log(ScriptName, "Viewer {0} successfully removed from the list!".format(ViewerToDelete))
			ViewerToDelete = ""
		else:
			Parent.Log(ScriptName, "The list dosen't contains a viewer called {0}".format(ViewerToDelete))
	else:
		Parent.Log(ScriptName, "The textfield was empty! Please ensure that you press the \"Save Settings\" button before you press the \"Delete Viewer\" button!")
	return
	
def ShowMessages():
	global ScriptSettings
	
	try:
		if len(ScriptSettings.messages) == 0:
			Parent.Log(ScriptName, "You don't have any welcome messages!")
		else:
			Parent.Log("Message ID", "{0} Welcome Message(s): ".format(len(ScriptSettings.messages)))
			counter = 1
			
			for message in ScriptSettings.messages:
				Parent.Log(str(counter), message)
				counter += 1
	except:
		ScriptSettings.messages = []
	return