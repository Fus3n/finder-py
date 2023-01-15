import os
import sys

from pynput import keyboard
from PySide6.QtCore import QMetaObject
from PySide6.QtGui import (QAction, QFont, QFontDatabase, QIcon, QKeyEvent,
                           QPixmap, Qt)
from PySide6.QtWidgets import (QApplication, QFrame, QMainWindow, QMenu,
                               QSystemTrayIcon, QVBoxLayout)

from AppListWidget import AppListWidget
from ListItem import ListItem
from SearchInput import SearcInput

# CONSTANTS
INPUT_BOX_STYLE = """
background: #282A3A; 
font-size: 21px; 
border-radius: 5px;
color: #D8D8D8;
padding: 13px 13px;
"""
# reusable function for frame style
def get_frame_style(bgcolor):
    return f"""
    background-color: {bgcolor}; 
    border-radius: 8px;
    """


class MainWindow(QMainWindow):
    
    def __init__(self, ):
        super().__init__(None)
        # Window Flags
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlag(self.windowFlags() | Qt.WindowStaysOnTopHint)

        # Load global Style sheets        
        with open("./style.qss", "r") as style:
            self.setStyleSheet(style.read())

        # Set main frame and layout       
        self.frame = QFrame()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.frame.setLayout(layout)

        # Setup frame and layout for search input (QLineEdit)        
        self.top_frame = QFrame()
        self.top_frame.setMinimumWidth(650)
        self.top_frame.setMaximumHeight(80)
        self.top_layout = QVBoxLayout()
        self.top_frame.setLayout(self.top_layout)
        self.top_frame.setStyleSheet(get_frame_style("#232323"))
        

        # Setup frame and layout for list      
        self.bottom_frame = QFrame()
        self.bottom_frame.setStyleSheet(get_frame_style("#282A3A"))
        self.bottom_layout = QVBoxLayout()
        self.bottom_frame.setLayout(self.bottom_layout)

        # Setup custom list view
        self.list_view = AppListWidget()
        

        # Setup input
        self.input_box = SearcInput(self.list_view, dobounce_delay=200) # delay in milliseconds
        self.input_box.debounce_timeout.connect(self.populate_list)
        self.input_box.setFocus()

        # load default list items 
        self.populate_list()

        
        # Setup search bar layout and list layout
        self.top_layout.addWidget(self.input_box)
        self.bottom_layout.addWidget(self.list_view)
        layout.addWidget(self.top_frame) 
        layout.addWidget(self.bottom_frame)

        # Load Fonts
        self.setup_font()

        # set central widgethdwdadwawdawd
        self.setCentralWidget(self.frame)
        # move to center of screen with offset
        self.moveToCenter(yoffset=-250)

    def showEvent(self, event) -> None:
        self.input_box.setFocus(Qt.FocusReason.ActiveWindowFocusReason)
        self.input_box.selectAll()
        return super().showEvent(event)

    def populate_list(self):
        """demo / filling out list with all the files and folders from the computers Download Folder"""
        list_dir = os.listdir("./")
        list_dir.sort()
        if self.input_box.text():
            res = [i for i in list_dir if self.input_box.text().lower() in i.lower()]
        else:
            res = list_dir
        self.list_view.clear()
        for idx, i in enumerate(res):
            is_file = os.path.isfile("./" + i)
            list_item = ListItem(self.list_view, i, QPixmap("./file-icon.png" if is_file else "./folder-icon.png"), idx)
            self.list_view.add_list_item(list_item, self.list_item_clicked)
            if idx == 0:
                list_item.set_selected(True)

        self.input_box.timer.stop()

    def list_item_clicked(self, item: ListItem):
        # select the item that was clicked
        print(item.text)
        print(item.icon_pixmap)

        # If you want to select the clicked item you need to manually do this by doing
        item.select_item()
    
    def setup_font(self):
        roboto_regular = QFontDatabase.addApplicationFont("./fonts/Roboto-Regular.ttf")
        roboto_bold = QFontDatabase.addApplicationFont("./fonts/Roboto-Medium.ttf")
        roboto_regular = QFontDatabase.applicationFontFamilies(roboto_regular)[0]
        roboto_bold = QFontDatabase.applicationFontFamilies(roboto_bold)[0]
        # Create a QFont object with the loaded font
        font = QFont(roboto_regular)
        font.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 1)
        font2 = QFont(roboto_bold)
        # font2.setBold(True)

        # Apply the font to the main window
        self.setFont(font)
        self.input_box.setFont(font)
        self.list_view.setFont(font2)

    def moveToCenter(self, yoffset=-250, xoffset=None):
        # not much going on here, just getting the screens resolution and getting its center
        qtRectangle = self.frameGeometry()
        centerPoint = QApplication.primaryScreen().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        cn = qtRectangle.center()
        cn.setY(cn.y() + yoffset)
        if not xoffset:
            xoffset = -self.width()//2
        cn.setX(cn.x() + xoffset)
        qtRectangle.moveCenter(cn)
        self.move(qtRectangle.center())

    def keyPressEvent(self, ev: QKeyEvent) -> None:
        if ev.key() == Qt.Key.Key_Escape:
            self.hide()
            
        return super().keyPressEvent(ev)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    window = MainWindow()
    # keyboard shortcut (Ctrl+Space) to trigger
    window.show()


    # Key combinations to trigger the app, can have multiple
    COMBINATIONS = [
        {keyboard.Key.ctrl_l, keyboard.Key.space},
    ]

    current = set()
    def on_press(key):
        if any([key in COMBO for COMBO in COMBINATIONS]):
            current.add(key)
        if any(all(k in current for k in COMBO) for COMBO in COMBINATIONS):
            # we are using MetaObject to invoke method as this keyboard listener is running on a different thread
            QMetaObject.invokeMethod(window, "show")

    def on_release(key):
        if any([key in COMBO for COMBO in COMBINATIONS]):
            current.remove(key)

    # start keyboard listener, that listens to shortcut to trigger the app (currently Ctrl+Space)
    listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release)
    listener.start()

    # SYSTEM TRAY, you can show and quit window using system tray 
    tray_icon = QSystemTrayIcon()
    tray_icon.setIcon(QIcon("./software.png")) # set an icon for the tray icon
    tray_icon.setVisible(True)

    tray_menu = QMenu()
    show_action = QAction("Show", tray_menu)
    show_action.triggered.connect(window.show)
    tray_menu.addAction(show_action)
    quit_action = QAction("Quit", tray_menu)
    quit_action.triggered.connect(app.quit)
    tray_menu.addAction(quit_action)
    tray_icon.setContextMenu(tray_menu)

    print("Started")
    sys.exit(app.exec())


