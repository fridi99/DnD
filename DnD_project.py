"""as of yet unnamed project
This project uses the dnd api www.dnd5eapi.co to query game rules and statistics and compiles them into a card-like format for easy reference using tkinter
I will call this version 1.0 (10.08.2023)
a short description of a statblock, the main object of this project:
The stat block contains a numerical representation of the abilities and properties of a creature. These include physical abilities, skills and magical powers.
From that information most actions in the game can be reasonably represented through play.
Now there is no particular reason to do this in isolation, as all the rules are already present on the internet and accessible through the api. However, based on this tool, more programming adebt DMs
might be able to customize monsters automatically and add automatic encounter builders to their game.
"""

"""some thoughts on documentation (feel free to ignore)
as I hope to make this my first project to be released to a wider audience I want to attempt to produce meaningful documentation in the form of comments.
In the past my documentation was a very literal explanation of what my code does, which, in retrospect, does not make a lot of sense, as that information is a simple googlesearch away for most programmers
Instead I will attempt to relay my intent and approach with the code i create and comment large portions of code  with long comments rather than countless short comments.

"""

import tkinter as tk
import numpy as np
import random as rand
#import requests
import json
import http.client
attribute_strings = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"] #the basic abilities of a creature


def call_creature(creature_name):
    """the basic getter function of this project. Takes the creatures name into a http get request and calls the corresponding data. If the data can not be found it returns an error message."""
    req = http.client.HTTPConnection("www.dnd5eapi.co", 80, timeout=5)
    req.request("GET", "/api/monsters/"+creature_name+"/")
    response = req.getresponse()
    if response.status == 404:
        print("sorry, could not find that creature")
        return False
    data = json.load(response)
    creature = statblock(data)
    creature.draw_block()
    return True


wraplen = 400
class statblock:
    """statblocks are saved as classes. For the simple creation of statblocks this is not the most straightforward approach, but in the future I hope for a developer
    to be able to change certain properties of a creature, so each creature is assigned a class object.
    I am somewhat confused here between C++ and Python, as I would like to initialize my class with optional variables. However that is not a thing and the second init just overwrites the first.
    consider it a reminder for later when I will attempt to code optional class definitions"""
    def __init__(self):
        self.attributes = [10,10,10,10,10,10]
        self.name = ""
    def __init__(self, file):
        """The init function takes data in the form of a JSON file and sets class variables to the received values. Unfortunatley the data is not very uniform so there is no space for reasonable iteration."""
        self.atributes = [file["strength"], file["dexterity"], file["constitution"], file["intelligence"], file["wisdom"], file["charisma"]]
        self.name = file["name"]
        self.type = file['type']
        self.size = file['size']
        self.alignment = file['alignment']
        self.AC = file['armor_class'][0]['value']
        self.HP = file['hit_points']
        self.skills = file['proficiencies']
        self.properties = file['special_abilities']
        self.movement = file['speed']
        self.vulnerabilities = file['damage_vulnerabilities']
        self.resistances = file['damage_resistances']
        self.immunities = file['damage_immunities']
        self.senses = file['senses']
        self.languages = file['languages']
        self.actions = file['actions']
        self.cr = file['challenge_rating']


    def draw_block(self):
        """This function creates a visual representation of the statblock using tkinter. It creates a window containing a grid where the creatures properties are listed
        in what I consider to be a sensible structure, based on the official statblocks used in D&D.
        The function is admittantly somewhat ugly, as i found no better way to list the properties than by creating a distinct line of code for each."""
        rownr = 0
        window = tk.Tk()
        txt = self.size + " " + self.type + " (" + self.alignment + ")   " + "CR: " + str(self.cr)
        window.title(self.name)
        firstline = []
        lab_name = tk.Label(window, text = self.name, font=('Times', 24))
        lab_name.grid(column = 0,row=rownr, columnspan = 6)
        rownr+=1
        lab_type = tk.Label(window, text = txt, font = ('Times', 12),bg = "#ffe6b3")
        lab_type.grid(column = 0, row = rownr, columnspan = 6)
        rownr += 1
        lab_ac = tk.Label(window, text = "AC: " + str(self.AC), font = ('Times', 15))
        lab_ac.grid(column = 0, row = rownr, columnspan = 3)
        lab_HP = tk.Label(window, text = "HP: " + str(self.HP), font = ('Times', 15))
        lab_HP.grid(column = 3, row = rownr, columnspan = 3)
        rownr += 1
        txt1 = ""
        for i in self.movement:
            txt1 += i
            txt1 += ": "
            if type(self.movement[i]) == str:
                txt1 += str(self.movement[i])
            txt1 += " "
        lab_speed = tk.Label(window, text = txt1, padx = 5).grid(column = 0, row = rownr, columnspan = 6, sticky = "W")
        rownr += 1
        for ite, i in enumerate(attribute_strings):
            firstline.append([tk.Label(window, text=i),tk.Label(window, text=self.atributes[ite])])
            firstline[ite][0].grid(column=ite, row=rownr)
            firstline[ite][1].grid(column=ite, row=rownr+1)
        rownr += 2
        txt2 = ""
        txt2_5 = "Saving throws: "
        txt3 = ""
        for i in self.skills:
            if(i['proficiency']['name'].find("Saving") != -1):
                txt2_5 += i['proficiency']['name'][-3:] + ": "
                txt2_5 += str(i['value']) + " "
            if(i['proficiency']['name'].find("Skill") != -1):
                txt2 += i['proficiency']['name'][6:] + ": " + str(i['value']) + ";"
        if(len(txt2_5) > 15):
            lab_save = tk.Label(window, text=txt2_5).grid(column=0, row=rownr, columnspan=6, sticky="W", pady=10)
            rownr += 1
        if(len(txt2)>0):
            lab_skills = tk.Label(window, text = "Skills: " + txt2).grid(column = 0, row = rownr, columnspan = 6, sticky = "W", pady = 2)
            rownr += 1
        txt_vul = "Damage Vulnerabilities: "
        for i in self.vulnerabilities:
            txt_vul += i
            txt_vul += ", "
        txt_vul += "\n"
        if (len(self.vulnerabilities) > 0):
            lab_vul = tk.Label(window, text=txt_vul, wraplength=wraplen, justify='left').grid(column=0, row=rownr, columnspan=6, sticky="W", pady=2, padx=5)
            rownr += 1
        txt_imm = "Damage Immunities: "
        for i in self.immunities:
            txt_imm += i
            txt_imm += ", "
        txt_imm += "\n"
        if(len(self.immunities) > 0):
            lab_immunity = tk.Label(window, text=txt_imm, wraplength = wraplen, justify = 'left').grid(column=0, row=rownr, columnspan=6, sticky="W", pady=2, padx=5)
            rownr += 1
        txt_res = "Damage Resistances: "
        for i in self.resistances:
            txt_res += i
            txt_res += ", "
        txt_res += "\n"
        if(len(self.resistances) > 0):
            lab_res = tk.Label(window, text=txt_res, wraplength = wraplen, justify = 'left').grid(column=0, row=rownr, columnspan=6, sticky="W", pady=5, padx=5)
            rownr += 1
        txt_sens = "Senses: "
        for i in self.senses:
            txt_sens += i.replace("_", " ")
            txt_sens += ": "
            txt_sens += str(self.senses[i])
            txt_sens += "; "
        lab_sens = tk.Label(window, text=txt_sens, wraplength=wraplen, justify='left').grid(column=0, row=rownr, columnspan=6, sticky="W", padx=5)
        rownr+=1
        txt_lang = "Languages: "
        if(len(self.languages) > 0):
            lab_lang = tk.Label(window, text=txt_lang + self.languages, wraplength=wraplen, justify='left').grid(column=0, row=rownr, columnspan=6, sticky="W", pady=5, padx=5)
        rownr +=1
        for i in self.properties:
            txt3 += i['name']
            txt3 += ": "
            txt3 += str(i['desc'])
            txt3 += "\n"
        lab_props = tk.Label(window, text=txt3, wraplength = wraplen, justify = 'left').grid(column=0, row=rownr, columnspan=6, sticky="W", pady = 5, padx = 5)
        rownr += 1
        lab_act = tk.Label(window, text= "ACTIONS", wraplength = wraplen, justify = 'left', font = ('Times', 16, 'bold')).grid(column=0, row=rownr, columnspan = 6, sticky="W", pady = 5, padx = 5)
        rownr += 1
        txt_act = ""
        for i in self.actions:
            txt_act += i['name']
            txt_act += ": "
            txt_act += i['desc']
            txt_act += "\n"
            txt_act += "\n"
        lab_acts = tk.Label(window, text=txt_act, wraplength=wraplen, justify='left', font=("Times", 10)).grid(column=0, row=rownr, columnspan=6, sticky="W", pady=5, padx=5)
        window.mainloop()

while True:
    """The basic structure of the program, simply querying the user for the creature name and calling it from the api using the function described above."""
    name = input("Creature name (type \"quit\" to quit): ").replace(" ", "-")
    if name == "quit":
        break
    call_creature(name)