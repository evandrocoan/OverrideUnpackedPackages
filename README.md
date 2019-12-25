# Sublime Unpacked Packages Override

To override Sublime Text unpacked packages every Sublime Text start. You can also call the command
`OverrideUnpackedPackages: Now` on the command palette.

To select the file to override,
just creates them on the folder `Packages/User/OverrideUnpackedPackages` following the packages file structure.
For example,
if you want to override the file:

1. `Packages/amxmodx/Main.sublime-menu`

You need to create the replacement file on the folder:

1. `Packages/User/OverrideUnpackedPackages/amxmodx/Main.sublime-menu`

Then run the command `OverrideUnpackedPackages Now` on the command palette or just restart Sublime
Text.


### Settings

To allow you override default menu as files `.sublime-menu`, you will need to rename the files you
put on the folder `OverrideUnpackedPackages` to `.sublime-menu.hide`. This way Sublime Text
will not double load your menus.

When the `OverrideUnpackedPackages` will perform the override, it will rename them back to their
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


## Installation

### By Package Control

1. Download & Install **`Sublime Text 3`** (https://www.sublimetext.com/3)
1. Go to the menu **`Tools -> Install Package Control`**, then,
   wait few seconds until the installation finishes up
1. Now,
   Go to the menu **`Preferences -> Package Control`**
1. Type **`Add Channel`** on the opened quick panel and press <kbd>Enter</kbd>
1. Then,
   input the following address and press <kbd>Enter</kbd>
   ```
   https://raw.githubusercontent.com/evandrocoan/StudioChannel/master/channel.json
   ```
1. Go to the menu **`Tools -> Command Palette...
   (Ctrl+Shift+P)`**
1. Type **`Preferences:
   Package Control Settings – User`** on the opened quick panel and press <kbd>Enter</kbd>
1. Then,
   find the following setting on your **`Package Control.sublime-settings`** file:
   ```js
       "channels":
       [
           "https://packagecontrol.io/channel_v3.json",
           "https://raw.githubusercontent.com/evandrocoan/StudioChannel/master/channel.json",
       ],
   ```
1. And,
   change it to the following, i.e.,
   put the **`https://raw.githubusercontent...`** line as first:
   ```js
       "channels":
       [
           "https://raw.githubusercontent.com/evandrocoan/StudioChannel/master/channel.json",
           "https://packagecontrol.io/channel_v3.json",
       ],
   ```
   * The **`https://raw.githubusercontent...`** line must to be added before the **`https://packagecontrol.io...`** one, otherwise,
     you will not install this forked version of the package,
     but the original available on the Package Control default channel **`https://packagecontrol.io...`**
1. Now,
   go to the menu **`Preferences -> Package Control`**
1. Type **`Install Package`** on the opened quick panel and press <kbd>Enter</kbd>
1. Then,
search for **`OverrideUnpackedPackages`** and press <kbd>Enter</kbd>

See also:

1. [ITE - Integrated Toolset Environment](https://github.com/evandrocoan/ITE)
1. [Package control docs](https://packagecontrol.io/docs/usage) for details.


## License

All files in this repository are released under GNU General Public License v3.0
or the latest version available on http://www.gnu.org/licenses/gpl.html

1. The [LICENSE](LICENSE) file for the GPL v3.0 license
1. The website https://www.gnu.org/licenses/gpl-3.0.en.html

For more information.


