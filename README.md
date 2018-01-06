# Sublime Unpacked Packages Override

To override Sublime Text unpacked packages every Sublime Text start. You can also call the command
`Override Unpacked Packages Now` on the command palette.

To select the file to override, just creates them on the folder `Packages/User/Override Unpacked
Packages` following the packages file structure. For example, if you want to override the file:

1. `Packages/amxmodx/Main.sublime-menu`

You need to create the replacement file on the folder:

1. `Packages/User/Override Unpacked Packages/amxmodx/Main.sublime-menu`

Then run the command `Override Unpacked Packages Now` on the command palette or just restart Sublime
Text.


### Settings

To allow you override default menu as files `.sublime-menu`, you will need to rename the files you
put on the folder `Override Unpacked Packages` to `.sublime-menu.hide`. This way Sublime Text
will not double load your menus.

When the `Override Unpacked Packages` will perform the override, it will rename them back to their
original names as the `.sublime-menu` mentioned just above.


## API

Other packages can import `OverrideUnpackedPackages` and add files to be copied and overridden.
This is a simple example:
```python
import os

try:
    from OverrideUnpackedPackages.override_unpacked_packages import add_folder_to_processing_queue

except ImportError as error:
    print( "Error: Could not import the package `OverrideUnpackedPackages`, please install the package. " + str( error ) )

    def add_folder_to_processing_queue(*args):
        print( "add_folder_to_processing_queue could not add the following arguments..." )

        for arg in args:
            print( str( arg ) )

PACKAGE_ROOT_DIRECTORY = os.path.dirname( os.path.realpath( __file__ ) )


def plugin_loaded() :
    add_files_to_copy_list()

def add_files_to_copy_list():
    add_folder_to_processing_queue( PACKAGE_ROOT_DIRECTORY, "amxmodx", 100 )
```

This some code also works when the package is inside a `.sublime-package` file. This is
automatically detected by `OverrideUnpackedPackages` when the `PACKAGE_ROOT_DIRECTORY` is set to the
folder `.sublime-package`. Therefore the file is unzipped, instead of just copied.


## License

All files in this repository are released under GNU General Public License v3.0
or the latest version available on http://www.gnu.org/licenses/gpl.html

1. The [LICENSE](LICENSE) file for the GPL v3.0 license
1. The website https://www.gnu.org/licenses/gpl-3.0.en.html

For more information.


