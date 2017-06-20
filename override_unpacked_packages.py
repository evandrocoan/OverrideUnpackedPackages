
import os
import shutil

import sublime
import sublime_plugin

from threading import Thread


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
        Creating Threads in python
        https://stackoverflow.com/questions/2905965/creating-threads-in-python
    """
    thread = Thread( target=_load_overrides )
    thread.start()

    # If we join the thread, we would hang Sublime Text until the copy if finished
    # thread.join()
    # print( "( load_overrides ) thread finished coping files." )


def _load_overrides():
    """
        Copy directory contents into a directory with python
        https://stackoverflow.com/questions/15034151/copy-directory-contents-into-a-directory-with-python
    """
    # files = os.listdir( SETTINGS_FOLDER )
    # for file in files:
    #     print( "file: " + str( file ) )
    copy_overrides( SETTINGS_FOLDER, PACKAGES_PATH )


def copy_overrides( root_source_folder, root_destine_folder, move_files=False ):
    """
        Python How To Copy Or Move Folders Recursively
        http://techs.studyhorror.com/python-copy-move-sub-folders-recursively-i-92

        Python script recursively rename all files in folder and subfolders
        https://stackoverflow.com/questions/41861238/python-script-recursively-rename-all-files-in-folder-and-subfolders

        Force Overwrite in Os.Rename
        https://stackoverflow.com/questions/8107352/force-overwrite-in-os-rename
    """
    # Call this if operation only one time, instead of calling the for every file.
    if move_files:
        def copy_file():
            shutil.move( source_file, destine_folder )
    else:
        def copy_file():
            shutil.copy( source_file, destine_folder )

    for source_folder, directories, files in os.walk( root_source_folder ):
        destine_folder = source_folder.replace( root_source_folder, root_destine_folder)

        if not os.path.exists( destine_folder ):
            os.mkdir( destine_folder )

        for file in files:
            source_file  = os.path.join( source_folder, file )
            destine_file = os.path.join( destine_folder, file )

            if os.path.exists( destine_file ):
                os.remove( destine_file )

            # print( ( "Moving" if move_files else "Coping" ), "file:", source_file, "to", destine_file )
            copy_file()

            if file.endswith(".hide"):
                os.replace( destine_file, destine_file[0:-5] )


