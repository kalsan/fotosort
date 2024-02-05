from PySide6.QtWidgets import QApplication, QErrorMessage
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QUrl, QObject, Signal, Slot, QStringListModel
import os

from . import imgutils


class UI(QObject):
    imageChangedSignal = Signal()

    def __init__(self, conf, controller):
        super().__init__()

        self.currentImage = None
        self.controller = controller
        self.conf = conf
        self.temp_output_dirs = []
        self.output_dirs = self.conf.perm_output_dirs.copy()

        self.app = QApplication([])
        self.engine = QQmlApplicationEngine()
        self.context = self.engine.rootContext()
        self.context.setContextProperty("ui", self)
        self._refreshOutputDirs()
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.engine.load(QUrl.fromLocalFile(os.path.join(dir_path, "qml/main.qml")))
        self.root = self.engine.rootObjects()[0]
        self.imageChangedSignal.connect(self.root.updateImage)

        self.setCurrentImage(self.controller.current())
        self.root.selectAll()

    def run(self):
        self.app.exec_()

    @Slot(result=str)
    def getVersion(self):
        with open(os.path.join(os.path.dirname(__file__), 'VERSION')) as f:
            v = self.version = f.read()
        return v

    def excepthook(self, cls, exception, traceback):
        self.root.showStatus("An error occured.", "red")
        self.root.showError("An error occured:\n\n{}".format(exception))

    @Slot(str, result=str)
    def autocomplete(self, searchtext):
        if len(searchtext) == 0:
            return ""
        for item in self.output_dirs:
            if searchtext in item:
                return item
        for item in self.output_dirs:  # Fallback to lowercase search
            if searchtext.lower() in item.lower():
                return item
        return ""

    @Slot(result=str)
    def getCurrentImage(self):
        return self.currentImage or "../images/noimage.png"

    @Slot(result=int)
    def getCurrentImageRotation(self):
        return imgutils.get_orientation(self.currentImage)

    @Slot(result=str)
    def getCurrentImageTimestamp(self):
        return imgutils.get_timestamp(self.currentImage)

    def setCurrentImage(self, new_image):
        self.currentImage = new_image
        self.imageChangedSignal.emit() # This loads the picture and displays it
        # Adjust undo button
        if self.root.setUndoEnabled(len(self.controller.history) > 0):
            self.root.setUndoText("Undo {}".format(self.controller.history[-1][0]))

    @Slot()
    def first(self):
        self.setCurrentImage(self.controller.first())
        self.root.showStatus("[<-", "black")

    @Slot()
    def prev(self):
        self.setCurrentImage(self.controller.prev())
        self.root.showStatus("<-", "black")

    @Slot()
    def next(self):
        self.setCurrentImage(self.controller.next())
        self.root.showStatus("->", "black")

    @Slot()
    def last(self):
        self.setCurrentImage(self.controller.last())
        self.root.showStatus("->]", "black")

    @Slot()
    def reload(self):
        self.setCurrentImage(self.controller.current())

    @Slot(str)
    def moveOrCopyCurrentFile(self, targetdir):
        if self.conf.copy_pictures:
            self.controller.copyCurrentFile(targetdir)
            self.controller.next()
            self.root.showStatus("Image copied.", "darkgreen")
        else:
            self.controller.moveCurrentFile(targetdir)
            self.root.showStatus("Image moved.", "darkgreen")

        # In case of success, make this target dir the first in the list
        picked_index = self.output_dirs.index(targetdir)
        del self.output_dirs[picked_index]
        self.output_dirs.insert(0, targetdir)
        self._refreshOutputDirs()

    @Slot()
    def trashCurrentFile(self):
        self.controller.trashCurrentFile()
        self.root.showStatus("Image moved to trash.", "brown")

    @Slot()
    def undo(self):
        self.controller.undo()
        self.root.showStatus("Undo completed.", "purple")

    @Slot(str)
    def setLocation(self, location):
        self.controller.setLocation(location)
        self.reload()
        self.root.showStatus("Folder loaded.", "blue")

    @Slot()
    def openTargetsDialog(self):
        self.root.openTargetsDialog("\n".join(self.conf.perm_output_dirs), "\n".join(self.temp_output_dirs))

    @Slot(str, str)
    def applyTargetsDialog(self, perm_output_dirs, temp_output_dirs):
        self.conf.perm_output_dirs = list(filter(None, [a.strip() for a in perm_output_dirs.split("\n")]))
        self.temp_output_dirs = list(filter(None, [a.strip() for a in temp_output_dirs.split("\n")]))
        self._refreshOutputDirs()
        self.root.focusCombobox()
        self.root.showStatus("Targets updated.", "blue")

    @Slot()
    def openAddTempTargetDialog(self):
        ts = imgutils.get_timestamp(self.controller.current())
        if ts:
            ts = self.conf.temp_output_prefix + ts[:10] + ' '
        self.root.openAddTempTargetDialog(ts)

    @Slot(str)
    def applyAddTempTargetDialog(self, newTarget):
        self.temp_output_dirs.insert(0, newTarget)
        self.controller.ensure_dir_exists(newTarget)
        self._refreshOutputDirs()
        self.root.focusCombobox()
        self.root.showStatus("Target added.", "blue")

    @Slot()
    def openSettingsDialog(self):
        self.root.openSettingsDialog(self.conf.temp_output_prefix, bool(self.conf.copy_pictures))

    @Slot(str, bool)
    def applySettingsDialog(self, temp_output_prefix, copy_pictures):
        self.conf.temp_output_prefix = temp_output_prefix
        if not self.conf.temp_output_prefix.endswith('/'):
            self.conf.temp_output_prefix += '/'
        self.conf.copy_pictures = copy_pictures
        self.root.focusCombobox()
        self.root.showStatus("Settings applied.", "blue")

    def _refreshOutputDirs(self):
        self.output_dirs = self.temp_output_dirs + self.conf.perm_output_dirs
        self.context.setContextProperty("output_dirs", self.output_dirs)
