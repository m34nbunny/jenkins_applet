#!/usr/bin/env python3

import os
import json
import sys
import requests
from subprocess import call
from pprint import pprint

class poller:
  appdir = os.getenv("HOME") + "/.jenkins_applet/"

  def __init__(self):
    self.poll_servers()

  def get_server_file_path(self):
    return self.appdir + "servers.json"

  def poll_servers(self):
    serverFilePath = self.get_server_file_path()
    hasdata = os.stat(serverFilePath).st_size != 0
    
    if hasdata:	
      with open(serverFilePath) as data_file:
        data = json.load(data_file)
    
        length = len(data["jobs"])
        self.tmpresponses = "{  \n   \"responses\" : [\n"
        count = 0
        for x in data["jobs"]:
          self.tmpresponses += self.poll_server(x, length, count)
          count = count + 1
    
        self.tmpresponses += "\n\t]\n}"
        self.responses = self.tmpresponses
    
        responsesFilePath = self.appdir + "responses.json"
        target = open(responsesFilePath, "w")
        target.write(self.responses)
        target.close()
    if hasdata == False:
      pprint("No servers defined in servers.json")
      
  def poll_server(self, item, length, count):
      currentBuildUrl = None
      jsontext = None
      friendly_text = None
      response_data = None
      status = None
      allBuilds = None
      imgpath = self.appdir
      try:
        url = item["job"] + "api/json"
        params = { "pretty" : "true", "tree" : "color,lastBuild[url]" }
        response = requests.get(url, params=params)
      except:
        print("${color DimGray}" + item["name"] + "${alignr}No Conn.")
        imgpath += "grey.png"
        friendly_text = "No Conn."
        currentBuildUrl = ""
        if (count + 1) == length:
          jsontext = "\t\t{ \"name\" : \"" + item["name"] + "\", \"status\" : \"Failure\", \"url\" : \"" + item["job"] + "\", \"imgpath\" : \"" + imgpath + "\", \"currentBuildUrl\" : \"" + currentBuildUrl + "\" } \n"
        else:
          jsontext = "\t\t{ \"name\" : \"" + item["name"] + "\", \"status\" : \"Failure\", \"url\" : \"" + item["job"] + "\", \"imgpath\" : \"" + imgpath + "\", \"currentBuildUrl\" : \"" + currentBuildUrl + "\" }, \n"
        return jsontext
		
      try:
        response_data = response.json()
      except:
        print("${color DimGray}" + item["name"] + "${alignr}No Conn.")
        imgpath += "grey.png"
        friendly_text = "No Conn."
        currentBuildUrl = ""
        if (count + 1) == length:
          jsontext = "\t\t{ \"name\" : \"" + item["name"] + "\", \"status\" : \"Failure\", \"url\" : \"" + item["job"] + "\", \"imgpath\" : \"" + imgpath + "\", \"currentBuildUrl\" : \"" + currentBuildUrl + "\" } \n"
        else:
          jsontext = "\t\t{ \"name\" : \"" + item["name"] + "\", \"status\" : \"Failure\", \"url\" : \"" + item["job"] + "\", \"imgpath\" : \"" + imgpath + "\", \"currentBuildUrl\" : \"" + currentBuildUrl + "\" }, \n"
        return jsontext
		
      try:
        status = response_data["color"]
        currentBuildUrl = response_data["lastBuild"]["url"]

        if status == "blue":
          friendly_text = "Success"
          imgpath += "green.png"
        elif status == "blue_anime":
          friendly_text = "Building"
          imgpath += "green_anime.gif"
        elif status == "notbuilt":
          friendly_text = "Not Built"
          imgpath += "notbuilt.png"
        elif status == "aborted":
          friendly_text = "Aborted"
          imgpath += "nobuilt.png"
        elif status == "notbuilt_anime":
          friendly_text = "First Build"
          imgpath += "nobuilt_anime.gif"
        elif status == "red":
          friendly_text = "Failure"
          imgpath += "red.png"
        elif status == "red_anime":
          friendly_text = "Building Failure"
          imgpath += "red_anime.gif"
        
        if friendly_text == "Success":
          print("${color green}" + item["name"] + "${alignr}" + friendly_text)
        elif friendly_text == "Aborted":
          print("${color DimGray}" + item["name"] + "${alignr}" + friendly_text)
        elif friendly_text == "Failure":
          print("${color red}" + item["name"] + "${alignr}" + friendly_text)
        elif friendly_text == "Building":
          print("${color lightblue}" + item["name"] + "${alignr}" + friendly_text)
        elif friendly_text == "Not Built":
          print("${color DimGray}" + item["name"] + "${alignr}" + friendly_text)
        elif friendly_text == "First Build":
          print("${color DimGray}" + item["name"] + "${alignr}" + friendly_text)
        elif friendly_text == "Building Failure":
          print("${color red}" + item["name"] + "${alignr}" + friendly_text)
      
        if (count + 1) == length:
          jsontext = "\t\t{ \"name\" : \"" + item["name"] + "\", \"status\" : \"" + friendly_text + "\", \"url\" : \"" + item["job"] + "\", \"imgpath\" : \"" + imgpath + "\", \"currentBuildUrl\" : \"" + currentBuildUrl + "\" } \n"
        else:
          jsontext = "\t\t{ \"name\" : \"" + item["name"] + "\", \"status\" : \"" + friendly_text + "\", \"url\" : \"" + item["job"] + "\", \"imgpath\" : \"" + imgpath + "\", \"currentBuildUrl\" : \"" + currentBuildUrl + "\" }, \n"
          
      except:
        imgpath += "red.png"
        if (count + 1) == length:
          jsontext = "\t\t{ \"name\" : \"" + item["name"] + "\", \"status\" : \"Failure\", \"url\" : \"" + item["job"] + "\", \"imgpath\" : \"" + imgpath + "\", \"currentBuildUrl\" : \"" + currentBuildUrl + "\" } \n"
        else:
          jsontext = "\t\t{ \"name\" : \"" + item["name"] + "\", \"status\" : \"Failure\", \"url\" : \"" + item["job"] + "\", \"imgpath\" : \"" + imgpath + "\", \"currentBuildUrl\" : \"" + currentBuildUrl + "\" }, \n"
          
      return jsontext

poller()
