# finder-py
finder-py contains an implementation for **Desktop Search Application**. 

If you have seen macos `spotlight` or `microsoft powertools run` this is just a template to help you create similar applications in python and pyside6.

The Frontend on PySide6 and has the necessary functionality implimented to complete app.

It has a demo function `populate_list` that basically gathers all files and folders from current folder and shows it

![ss preivew](/images/ss-preview-file-finder.png)

## Features
- Widgets:
    - 🪟 AppListWidget
        - Custom ListWidget has support for selecting items using arrow keys, and some helpful functions
    - 📃ListItem
        - Custom item widget for QListWidgetItem It is a QFrame that holds all the content can be shown on each list item, all you have to do to add more items is to add widgets to *layout*  
    - 🔎 SearchInput
        - Custom QLinEdit that supports input debouncing
    - 📥 System tray support
        - has system tray functionality, for now default options are to show and quite the application 
    - ⌨️ Global Keyboard shortcut
        - Using the pynput module, it listens to `ctrl+space` (changeable) and executes `show` function on the main window so the app can be shown from any window without having to focus.


#### This is basically a template to get you started on making finder applications or whatever you want to, i posted this because after making the UI i didn't knew what to make `(*>﹏<*)′

