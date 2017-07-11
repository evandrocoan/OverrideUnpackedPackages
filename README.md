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


## License

All files in this repository are released under GNU General Public License v3.0
or the latest version available on http://www.gnu.org/licenses/gpl.html

1. The [LICENSE](LICENSE) file for the GPL v3.0 license
1. The website https://www.gnu.org/licenses/gpl-3.0.en.html

For more information.


