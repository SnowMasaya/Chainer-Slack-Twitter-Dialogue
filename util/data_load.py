#!/usr/bin/env python
#-*- coding:utf-8 -*-
import json

f = open("list", "r")
player_1 = open("player_1.txt", "w")
player_2 = open("player_2.txt ", "w")
count = 0

for line in f.readlines():
    f = open(line.rstrip())
    data = json.load(f)
    for i in range(len(data["turns"])):
        if i % 2 == 1:
            player_1.write(data["turns"][i]["utterance"] + "\n")
        else:
            if i == 0:
                print("pass")
            else: 
                player_2.write(data["turns"][i]["utterance"] + "\n")
