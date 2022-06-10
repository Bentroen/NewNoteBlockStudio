from pathlib import Path

from nbs.core.audio import AudioEngine
from nbs.core.data import default_instruments
from nbs.ui.actions import (
    Actions,
    ChangeInstrumentActionsManager,
    SetCurrentInstrumentActionsManager,
)
from nbs.ui.menus import MenuBar
from nbs.ui.toolbar import InstrumentToolBar, ToolBar
from nbs.ui.workspace import *
from nbs.ui.workspace.constants import appctxt  # TODO: move this somewhere else
from nbs.ui.workspace.layers import LayerArea
from nbs.ui.workspace.note_blocks import NoteBlockArea
from nbs.ui.workspace.piano import HorizontalAutoScrollArea, PianoWidget
from nbs.ui.workspace.time_bar import TimeBar
from nbs.ui.workspace.workspace import Workspace
from PyQt5 import QtCore, QtWidgets


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Minecraft Note Block Studio")
        self.setMinimumSize(854, 480)
        self.initAudio()
        self.initUI()
        self.initNoteBlocks()
        self.initPiano()
        self.initInstruments()

    def initAudio(self):
        self.audioEngine = AudioEngine(self)

    def initUI(self):
        self.menuBar = MenuBar()
        self.toolBar = ToolBar()
        self.instrumentBar = InstrumentToolBar()

        self.setMenuBar(self.menuBar)
        self.addToolBar(self.toolBar)
        self.addToolBar(self.instrumentBar)

        self.noteBlockArea = NoteBlockArea()
        self.layerArea = LayerArea()
        self.timeBar = TimeBar()
        self.piano = PianoWidget(keyCount=88, offset=9, validRange=(33, 57))
        self.pianoContainer = HorizontalAutoScrollArea()

        self.workspace = Workspace(self.noteBlockArea, self.layerArea, self.timeBar)
        self.centralArea = CentralArea(self.workspace, self.piano, self.pianoContainer)

        self.setCentralWidget(self.centralArea)

    def initNoteBlocks(self):
        # Selection
        self.noteBlockArea.blockCountChanged.connect(Actions.setBlockCount)
        self.noteBlockArea.selectionChanged.connect(Actions.setSelectionStatus)
        self.noteBlockArea.selectionChanged.connect(lambda: Actions.setClipboard(True))

        Actions.cutAction.triggered.connect(self.noteBlockArea.cutSelection)
        Actions.copyAction.triggered.connect(self.noteBlockArea.copySelection)
        Actions.pasteAction.triggered.connect(self.noteBlockArea.pasteSelection)

        # Playback
        Actions.playPauseAction.triggered.connect(
            lambda checked: self.noteBlockArea.view.playbackManager.setPlaying(checked)
        )
        Actions.stopAction.triggered.connect(
            self.noteBlockArea.view.playbackManager.stop
        )

        # Sounds
        self.noteBlockArea.blockAdded.connect(
            lambda: self.audioEngine.playSound(0, 0.5, 1.2, 0)
        )
        self.noteBlockArea.blockPlayed.connect(
            lambda: self.audioEngine.playSound(0, 0.5, 1.2, 0)
        )

    def initPiano(self):
        # Set active workspace key
        self.piano.activeKeyChanged.connect(self.noteBlockArea.setActiveKey)

        # Sounds
        self.piano.activeKeyChanged.connect(
            lambda key: self.audioEngine.playSound(15, 0.5, 2 ** ((key - 45) / 12), 0)
        )

    def initInstruments(self):
        for ins in default_instruments:
            sound_path = appctxt.get_resource(Path("sounds", ins.sound_path))
            self.audioEngine.loadSound(sound_path)

        self.setCurrentInstrumentActionsManager = SetCurrentInstrumentActionsManager()
        self.changeInstrumentActionsManager = ChangeInstrumentActionsManager()

        self.setCurrentInstrumentActionsManager.updateActions(default_instruments)
        self.setCurrentInstrumentActionsManager.instrumentChanged.connect(
            # TODO: connect this to future InstrumentManager object that will notify  widgets
            lambda id_: self.noteBlockArea.changeCurrentInstrument(
                default_instruments[id_]
            )
            # self.centralWidget().workspace.piano.setValidRange(ins)
        )

        self.instrumentBar.populateInstruments(default_instruments)

        self.changeInstrumentActionsManager.updateActions(default_instruments)

    #
    #
    #
    #
    #
    def drawToolBar(self):
        icons = {
            "new_song":         qta.icon('mdi.file-plus'),
            "open_song":        qta.icon('mdi.folder-open'),
            "save_song":        qta.icon('mdi.content-save'),
            "rewind":           qta.icon('mdi.rewind'),
            "fast_forward":     qta.icon('mdi.fast-forward'),
            "play":             qta.icon('mdi.play'),
            "pause":            qta.icon('mdi.pause'),
            "stop":             qta.icon('mdi.stop'),
            "record":           qta.icon('mdi.record'),
            "loop":             qta.icon('mdi.repeat'),
            "loop_off":         qta.icon('mdi.repeat-off'),
            "undo":             qta.icon('mdi.undo'),
            "redo":             qta.icon('mdi.redo'),
            "cut":              qta.icon('mdi.content-cut'),
            "copy":             qta.icon('mdi.content-copy'),
            "paste":            qta.icon('mdi.content-paste'),
            "delete":           qta.icon('mdi.delete'),
            "select_all":       qta.icon('mdi.select-all'),
            "song_instruments": qta.icon('mdi.piano'),
            "song_info":        qta.icon('mdi.information'),
            "song_properties":  qta.icon('mdi.label'),
            "song_stats":       qta.icon('mdi.file-document-edit'),
            "midi_devices":     qta.icon('mdi.usb'),
            "settings":         qta.icon('mdi.settings')
        }

        instrument_list = ["harp", "double_bass", "bass_drum", "snare_drum", "click", "guitar", "flute", "bell",
                           "chime", "xylophone", "iron_xylophone", "cow_bell", "didgeridoo", "bit", "banjo", "pling"]
        instrument_button_list = [nbs.ui.components.InstrumentButton(instrument) for instrument in instrument_list]
        for instrument in self.currentSong.custom_instruments:  # TODO: reset custom instruments on new song
            instrument_button_list.append(nbs.ui.components.InstrumentButton("custom"))  # TODO: put in custom name

        instrument_buttons = QtWidgets.QButtonGroup(self)
        instrument_buttons.setExclusive(True)
        for button in instrument_button_list:
            instrument_buttons.addButton(button)

    def drawStatusBar(self):
        pass

    @QtCore.pyqtSlot()
    def new_song(self):
        self.currentSong = nbs.core.data.Song()
        # TODO: save confirmation if editing unsaved work
        self.centralWidget().workspace.resetWorkspace()

    @QtCore.pyqtSlot()
    def load_song(self, filename=None):
        """Loads a .nbs file into the current session. passing a filename overrides opening the file dialog.
        loadFlag determines if the method is allowed to load the file and reset the workspace (needed in case the
        user presses cancel on the open file dialog)."""
        loadFlag = False

        if filename:
            loadFlag = True
        else:
            dialog = QtWidgets.QFileDialog(self)
            dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
            dialog.setWindowTitle("Open song")
            dialog.setLabelText(QtWidgets.QFileDialog.FileName, "Song name:")
            dialog.setNameFilter("Note Block Songs (*.nbs)")
            # dialog.restoreState()
            if dialog.exec():
                filename = dialog.selectedFiles()[0]
                # dialog.saveState()
                loadFlag = True

        if loadFlag:
            self.currentSong = nbs.core.data.Song(filename=filename)
            self.centralWidget().workspace.resetWorkspace()
            # TODO: load layers
            for note in self.currentSong.notes:
                self.centralWidget().workspace.noteBlockWidget.addBlock(note.tick, note.layer, note.key, note.instrument)
            # It's really weird to updateSceneSize() here, there has to be a better solution.
            self.centralWidget().workspace.noteBlockWidget.updateSceneSize()

        # TODO: The main window should only interact with the workspace (consisting of layer area + note block area),
        # not directly with the note block area. The workspace will do the talking between the layer and note block
        # areas, keeping them in sync, and also provide an interface for interacting with both at the same time.

    @QtCore.pyqtSlot()
    def save_song(self):
        """Save current file without bringing up the save dialog if it has a defined location on disk"""
        if not self.currentSong.location:
            self.song_save_as()
        else:
            self.currentSong.save()

    @QtCore.pyqtSlot()
    def song_save_as(self):
        dialog = QtWidgets.QFileDialog(self)
        dialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
        dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
        dialog.setWindowTitle("Save song")
        dialog.setLabelText(QtWidgets.QFileDialog.FileName, "Song name:")
        dialog.setNameFilter("Note Block Songs (*.nbs)")
        # dialog.restoreState()
        if dialog.exec():
            location = dialog.selectedFiles()[0]
            self.currentSong.save(location)
            # dialog.saveState()
