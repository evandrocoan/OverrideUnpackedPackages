
import os
import re

import shutil
import zipfile
import contextlib

import sublime
import sublime_plugin

from queue import Queue
from threading import Thread


PACKAGE_ROOT_DIRECTORY = os.path.dirname( os.path.realpath( __file__ ) )
PACKAGE_NAME = os.path.basename( PACKAGE_ROOT_DIRECTORY ).rsplit('.', 1)[0]

PACKAGES_PATH = ""
SETTINGS_FOLDER = ""

# A queue of folders to be copyied to the Packages folder overriding the existent files
g_working_queue = Queue()


# Import the debugger
from debug_tools import getLogger

# Debugger settings: 0 - disabled, 127 - enabled
log = getLogger( 127, __name__ )

# log( 2, "..." )
# log( 2, "..." )
# log( 2, "Debugging" )
# log( 2, "PACKAGE_ROOT_DIRECTORY: " + PACKAGE_ROOT_DIRECTORY )


def plugin_loaded():
    unpack_variables()

    if not os.path.exists( SETTINGS_FOLDER ):
        os.makedirs( SETTINGS_FOLDER )

    # Flush out the accumulated files
    sublime.set_timeout_async( start_overriding_files, 5000 )
    add_folder_to_processing_queue( SETTINGS_FOLDER, priority=1001 )


def unpack_variables():
    global PACKAGES_PATH
    global SETTINGS_FOLDER

    # We only can call `sublime` API, after the `plugin_loaded` forward
    PACKAGES_PATH   = sublime.packages_path()
    SETTINGS_FOLDER = os.path.join( PACKAGES_PATH, "User", PACKAGE_NAME )

    # log( 2, "PACKAGE_NAME:    " + str( PACKAGE_NAME ) )
    # log( 2, "PACKAGES_PATH:   " + str( PACKAGES_PATH ) )
    # log( 2, "SETTINGS_FOLDER: " + str( SETTINGS_FOLDER ) )

    # files = os.listdir( SETTINGS_FOLDER )
    # for file in files:
    #     log( 1, "file: " + str( file ) )


class OverrideUnpackedPackagesNowCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        start_overriding_files()


def add_folder_to_processing_queue(directory_path, folder_name="", priority=100):
    """
        Add a folder to the copied and override an unpacked package. It must be called on the 5
        first seconds after the `plugin_loaded()` forward has been called by Sublime Text.

        If this is called later, you need to import the non-blocking function
        `start_overriding_files()` function, and then call it when finished adding files to the
        queue.

        @param directory_path  a file full path like `C:\Sublime\Data\Packages\MyPackage`,
                               this also accepts path generated from inside a sublime-package like
                               `C:\Sublime\Data\Installed Packages\MyPackage.sublime-package`

        @param folder_name     the name of the folder to install/copy, which is inside the
                               `directory_path`

        @param priority        The priority 1 to 1000 should be used for files which are added by
                               packages, which want to run before the user overriding, i.e., do not
                               want to override user files in cases the user has also configured the
                               package to run.
    """
    g_working_queue.put( (priority, directory_path, folder_name) )


def start_overriding_files():
    """
        Creating Threads in python
        https://stackoverflow.com/questions/2905965/creating-threads-in-python
    """
    thread = Thread( target=_load_overrides )
    thread.start()


def _load_overrides():
    """
        Copy directory contents into a directory with python
        https://stackoverflow.com/questions/15034151/copy-directory-contents-into-a-directory-with-python
    """
    # log( 2, "( start_overriding_files ) thread started coping files." )

    while not g_working_queue.empty():
        queue_item     = g_working_queue.get()
        directory_path = queue_item[1]
        directory_name = queue_item[2]

        if ".sublime-package" in directory_path:
            copy_overrides_from_zipfile( directory_path, directory_name, PACKAGES_PATH )

        else:
            copy_overrides_from_folder( directory_path, directory_name, PACKAGES_PATH )


def get_zipfile_paths(directory_path):
    match = re.search( r"\.sublime-package", directory_path )

    zip_path   = ""
    zip_folder = ""

    if match:
        zip_path   = directory_path[:match.end(0)]
        zip_folder = directory_path[match.end(0)+1:]

    else:
        raise ValueError( "The path provided does not contains `.sublime-package`! directory_path: %s" % directory_path )

    return zip_path, zip_folder


def copy_overrides_from_zipfile(zip_path, zip_folder, destine_folder):
    """
        If the files already exists on the destine, they will be overridden.
    """
    # log( 2, "zip_path:       " + str( zip_path ) )
    # log( 2, "zip_folder:     " + str( zip_folder ) )
    # log( 2, "destine_folder: " + str( destine_folder ) )

    try:
        package_file = zipfile.ZipFile( zip_path )

    except zipfile.BadZipfile as error:
        log( 1, " The package file '%s is invalid! Error: %s" % ( zip_path, error ) )

    with contextlib.closing( package_file ):

        try:
            os.mkdir( destine_folder )

        except OSError as error:

            if os.path.isdir( destine_folder ):
                pass

            else:
                log( 1, "The directory '%s' could not be created! Error: %s" % ( destine_folder, error ) )
                return

        try:

            for file_path in package_file.namelist():
                # log( 2, "Trying to extract: " + str( file_path ) )

                if zip_folder in file_path:
                    destine_file = os.path.join( destine_folder, file_path )
                    # log( 2, "Unzipping... " + str( destine_file ) )

                    os.makedirs( destine_folder, exist_ok=True )
                    package_file.extract( file_path, destine_folder )

                    if destine_file.endswith(".hide"):
                        os.replace( destine_file, destine_file[0:-5] )

        except Exception as error:
            log( 1, "Error: `%s`" % error )
            log( 1, "The file extraction failed failed: `%s`" % zip_path )
            return

        # log( 2, "The file was successfully extracted: %s" % zip_path )


def copy_overrides_from_folder( root_source_folder, directory_name, root_destine_folder, move_files=False ):
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

    root_source_folder  = os.path.join( root_source_folder, directory_name )
    root_destine_folder = os.path.join( root_destine_folder, directory_name )

    for source_folder, directories, files in os.walk( root_source_folder ):
        destine_folder = source_folder.replace( root_source_folder, root_destine_folder)

        if not os.path.exists( destine_folder ):
            os.mkdir( destine_folder )

        for file in files:
            source_file  = os.path.join( source_folder, file )
            destine_file = os.path.join( destine_folder, file )

            if os.path.exists( destine_file ):
                os.remove( destine_file )

            # log( 2, ( "Moving" if move_files else "Coping" ), " file: ", source_file, " to ", destine_file )
            copy_file()

            if file.endswith(".hide"):
                os.replace( destine_file, destine_file[0:-5] )


