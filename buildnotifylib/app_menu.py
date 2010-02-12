import os
import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from distance_of_time import DistanceOfTime
from dateutil.parser import parse
from preferences import PreferencesDialog

class AppMenu:
    def __init__(self, tray, widget, conf, build_icons):
        self.menu = QtGui.QMenu(widget)
        tray.setContextMenu(self.menu)
        self.conf = conf
        self.build_icons = build_icons

    def update(self, projects):
        self.menu.clear()
        for project in projects:
            self.create_menu_item(project.name, self.build_icons.for_status(project.get_build_status()), project.url, parse(project.lastBuildTime))
        self.create_default_menu_items()
            
    def create_default_menu_items(self):
#        self.menu.addAction(QtGui.QAction("About", self.menu, triggered=self.about_clicked))
        self.menu.addAction(QtGui.QAction("Preferences", self.menu, triggered=self.preferences_clicked))
        self.menu.addAction(QtGui.QAction("Exit", self.menu, triggered=self.exit))
        
    def about_clicked(self,widget):
#        self.about_dialog.create()
        pass

    def preferences_clicked(self, widget):
        self.preferences_dialog = PreferencesDialog(self.conf)
        self.preferences_dialog.exec_()
    
    def exit(self,widget):
        sys.exit()

    def create_menu_item(self, label, icon, url, lastBuildTime):
        action = self.menu.addAction(icon, label + ", " + DistanceOfTime(lastBuildTime).age() + " ago")
        receiver = lambda url=url: self.open_url(self, url)
        QtCore.QObject.connect(action, QtCore.SIGNAL('triggered()'), receiver)

    def open_url(self, something, url) :
        os.system(self.conf.browser + " " + url + " &")
