
import os

import sublime
import sublime_plugin

from distutils.dir_util import copy_tree


PACKAGE_NAME = "Override Unpacked Packages"
PACKAGES_PATH = sublime.packages_path()
SETTINGS_FOLDER = os.path.join( PACKAGES_PATH, "User", PACKAGE_NAME )


def plugin_loaded():
    # print( "PACKAGE_NAME:    " + str( PACKAGE_NAME ) )
    # print( "PACKAGES_PATH:   " + str( PACKAGES_PATH ) )
    # print( "SETTINGS_FOLDER: " + str( SETTINGS_FOLDER ) )

    if not os.path.exists( SETTINGS_FOLDER ):
        os.makedirs( SETTINGS_FOLDER )

    load_overrides()


class OverrideUnpackedPackagesNowCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        load_overrides()


def load_overrides():
    """
        Copy directory contents into a directory with python
        https://stackoverflow.com/questions/15034151/copy-directory-contents-into-a-directory-with-python
    """
    files = os.listdir( SETTINGS_FOLDER )

    # for file in files:
    #     print( "file: " + str( file ) )

    copy_tree( SETTINGS_FOLDER, PACKAGES_PATH )



