#!/usr/bin/env python3

from gi.repository import Gtk
import os
import sys
import json
import requests
import threading
import webbrowser
from subprocess import call
from pprint import pprint

class aStatusIcon:
  appdir = os.getenv("HOME") + "/.jenkins_applet/"
  
  def __init__(self):
    self.statusicon = Gtk.StatusIcon()
    self.statusicon.set_from_file(self.appdir + "favicon.ico")
    self.statusicon.connect("popup-menu", self.right_click_event)

  def exit_app(self, widget):
    quit()

  def right_click_event(self, icon, button, time):
    responses = None
    self.menu = Gtk.Menu()

    quit = Gtk.ImageMenuItem()
    quit.set_label("Quit")
    quit.connect("activate", self.exit_app)

    separator = Gtk.SeparatorMenuItem()
    with open(self.appdir + "responses.json", 'r') as json_data:
      responses = json.load(json_data)

    for x in responses["responses"]:
      jobActionMenu = Gtk.Menu()
      
      img = Gtk.Image()
      img.set_from_file(x["imgpath"])
      job = Gtk.ImageMenuItem()
      job.set_label(x["name"])
      job.set_image(img)
      job.set_always_show_image(True)
      
      
      jopImg = Gtk.Image()
      jopImg.set_from_file(self.appdir + "open_in_browser.png")
      jobOpenPage = Gtk.ImageMenuItem()
      jobOpenPage.set_image(jopImg)
      jobOpenPage.set_label("Open Web Page")
      jobOpenPage.set_always_show_image(True)
      jobOpenPage.connect("activate", self.openurl, x)
      
      
      jbaImg = Gtk.Image()
      jbaImg.set_from_file(self.appdir + "build.png")
      jobBuildAction = Gtk.ImageMenuItem()
      jobBuildAction.set_image(jbaImg)
      jobBuildAction.set_label("Build Now")
      jobBuildAction.set_always_show_image(True)
      jobBuildAction.connect("activate", self.callbuildnow, x)
      
      jbcImg = Gtk.Image()
      jbcImg.set_from_file(self.appdir + "history.png")
      jobBuildConsole = Gtk.ImageMenuItem()
      jobBuildConsole.set_image(jbcImg)
      jobBuildConsole.set_label("Current Build Console")
      jobBuildConsole.set_always_show_image(True)
      jobBuildConsole.connect("activate", self.opencurrentbuildconsole, x)
      
      
      jobActionMenu.append(jobBuildAction)
      jobActionMenu.append(jobOpenPage)
      jobActionMenu.append(jobBuildConsole)
      
      job.set_submenu(jobActionMenu)
      self.menu.append(job)
    
    self.menu.append(separator)
    self.menu.append(quit)
    
    self.menu.show_all()
    self.menu.popup(None, None, None, Gtk.StatusIcon.position_menu, button, time)

  def opencurrentbuildconsole(self, widget, data):
    webbrowser.open_new(data["currentBuildUrl"] + "console")

  def openurl(self, widget, data):
    webbrowser.open_new(data["url"])

  def callbuildnow(self, widget, data):
    requests.post(data["url"] + "build")
    
aStatusIcon()
Gtk.main()
