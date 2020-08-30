import QtQuick 2.5
import QtQuick.Controls 2.5
import QtQuick.Controls 1.4
import QtQuick.Controls.Styles 1.4
import QtQuick.Layouts 1.12
import QtQuick.Dialogs 1.1

ApplicationWindow {
    id: window
    visible: true
    title: "FotoSort"

    function updateImage(){
        var filepath = ui.getCurrentImage()
        image.source = filepath
        window.title = "FotoSort " + filepath + ' ' + ui.getCurrentImageTimestamp()
    }

    function selectAll(){
        combobox.selectAll();
    }

    function setUndoEnabled(enabled){
        undoMenuItem.enabled = enabled;
        return enabled;
    }

    function setUndoText(text){
        undoMenuItem.text = text;
    }

    function openTargetsDialog(permanentLocationsText, temporaryLocationsText){
        permanentLocations.text = permanentLocationsText;
        temporaryLocations.text = temporaryLocationsText;
        targetsDialog.open();
        permanentLocations.forceActiveFocus();
    }

    function applyTargetsDialog(){
        ui.applyTargetsDialog(permanentLocations.text, temporaryLocations.text);
    }

    function openAddTempTargetDialog(prefillText){
        newTempLocation.text = prefillText;
        addTempTargetDialog.open();
        newTempLocation.forceActiveFocus();
    }

    function applyAddTempTargetDialog(){
        ui.applyAddTempTargetDialog(newTempLocation.text);
    }

    function openSettingsDialog(tempOutputPrefixText, copyPicturesChecked){
        tempOutputPrefix.text = tempOutputPrefixText;
        copyPictures.checked = copyPicturesChecked;
        settingsDialog.open();
    }

    function applySettingsDialog(){
        ui.applySettingsDialog(tempOutputPrefix.text, copyPictures.checked);
    }

    function focusCombobox(){
        combobox.forceActiveFocus();
    }

    function showStatus(text, color){
        statusText.text = text;
        statusText.color = color;
    }

    function showError(message){
        errorDialog.text = message;
        errorDialog.open();
    }

    MessageDialog {
    id: errorDialog
        title: "An error occured"
        text: "(No info available)"
        standardButtons: StandardButton.Ok
        icon: StandardIcon.Critical
        onAccepted: focusCombobox();
    }

    FileDialog {
        id: folderDialog
        selectFolder: true
        title: "Select a directory with photos to move"
        folder: shortcuts.home
        onAccepted: ui.setLocation(folderDialog.folder)
        onRejected: focusCombobox();
    }

    Dialog {
        id: targetsDialog
        title: "Edit target locations"
        standardButtons: Dialog.Save | Dialog.Cancel
        modal: true
        x: (parent.width - width) / 2
        y: (parent.height - height) / 2
        onAccepted: applyTargetsDialog()
        onRejected: focusCombobox();

        ColumnLayout {
            anchors.fill: parent

            Label {
                text: "Permanent target locations:"
            }
            TextArea {
                id: permanentLocations
                Layout.fillWidth: true
            }
            Label {
                text: "Temporary target locations (forgotten when the application is closed):"
            }
            TextArea {
                id: temporaryLocations
                Layout.fillWidth: true
            }
        }
    }

    Dialog {
        id: addTempTargetDialog
        title: "Add temporary target location"
        standardButtons: Dialog.Save | Dialog.Cancel
        modal: true
        x: (parent.width - width) / 2
        y: (parent.height - height) / 2
        onAccepted: applyAddTempTargetDialog()
        onRejected: focusCombobox();

        Column {
            anchors.fill: parent
            
            TextField {
                id: newTempLocation
                width: parent.width
                style: TextFieldStyle {
                    textColor: "black"
                    background: Rectangle {
                        radius: 2
                        implicitWidth: 100
                        implicitHeight: 24
                        border.color: "#333"
                        border.width: 1
                    }
                }
                Keys.onPressed: {
                    if (event.key == Qt.Key_Return || event.key == Qt.Key_Enter) {
                        addTempTargetDialog.accept()
                        event.accepted = true;
                    }
                }
            }
        }
    }

    Dialog {
        id: settingsDialog
        title: "Fotosort settings"
        standardButtons: Dialog.Save | Dialog.Cancel
        modal: true
        x: (parent.width - width) / 2
        y: (parent.height - height) / 2
        onAccepted: applySettingsDialog()
        onRejected: focusCombobox();

        GridLayout {
            anchors.fill: parent
            columns: 2

            Text { text: "Path to pictures folder:  "}

            TextField {
                id: tempOutputPrefix
                width: parent.width
                style: TextFieldStyle {
                    textColor: "black"
                    background: Rectangle {
                        radius: 2
                        implicitWidth: 100
                        implicitHeight: 24
                        border.color: "#333"
                        border.width: 1
                    }
                }
            }

            Text { text: "Copy pictures? (otherwise moved):  "}

            CheckBox { id: copyPictures }

            Button { text: "Edit traget locations"; onClicked: ui.openTargetsDialog() }
        }
    }

    menuBar: MenuBar {
        Menu {
            title: "Fotosort"
            MenuItem { text: "Open folder"; shortcut: "Ctrl+O"; onTriggered: folderDialog.open() }
            MenuItem { text: "Manage settings"; shortcut: "Ctrl+,"; onTriggered: ui.openSettingsDialog() }
            MenuItem { text: "Manage target locations"; shortcut: "Ctrl+Shift+T"; onTriggered: ui.openTargetsDialog() }
            MenuItem { text: "Add temporary target location"; shortcut: "Ctrl+T"; onTriggered: ui.openAddTempTargetDialog() }
            MenuItem { text: "Quit"; shortcut: "Ctrl+Q"; onTriggered: Qt.quit() }
        }
        Menu {
            title: "Navigate"
            MenuItem { text: "First"; shortcut: "Ctrl+Shift+Tab"; onTriggered: ui.first() }
            MenuItem { text: "Prev"; shortcut: "Shift+Tab"; onTriggered: ui.prev() }
            MenuItem { text: "Next"; shortcut: "Tab"; onTriggered: ui.next() }
            MenuItem { text: "Last"; shortcut: "Ctrl+Tab"; onTriggered: ui.last() }
        }
        Menu {
            title: "Actions"
            MenuItem { text: "Undo"; shortcut: "Ctrl+Z"; onTriggered: { ui.undo(); ui.reload(); } id: undoMenuItem; enabled: false }
            MenuItem { text: "Trash"; shortcut: "Ctrl+D"; onTriggered: { ui.trashCurrentFile(); ui.reload(); } }
        }
    }

    ColumnLayout {
        anchors.fill: parent

        Image {
            id: image
            source: ui.getCurrentImage()
            fillMode: Image.PreserveAspectFit
            clip: true
            autoTransform: true
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.maximumHeight: sourceSize.height
            Layout.maximumWidth: sourceSize.width
            Layout.alignment: Qt.AlignCenter
        }

        RowLayout{
            Layout.fillWidth: true
            Layout.margins: 5

            ComboBox {
                id: combobox
                model: output_dirs
                editable: true
                focus: true;
                Keys.onPressed: {
                    if (event.key == Qt.Key_Return || event.key == Qt.Key_Enter) {
                        if (suggestionText.text !== ""){
                            ui.moveOrCopyCurrentFile(suggestionText.text);
                            ui.reload(); 
                            selectAll();
                            event.accepted = true;
                        }
                    }
                    if(event.modifiers & Qt.ControlModifier && event.key == Qt.Key_Z){
                        ui.undo();
                        ui.reload();
                        event.accepted = true;
                    }
                }
                onEditTextChanged: {
                    suggestionText.text = ui.autocomplete(combobox.editText)
                }
            }

            Label {
                id: suggestionText
                text: "Type left for autocompletion"
            }

            Item {  // Spacer
                Layout.fillWidth: true
            }

            Label {
                id: statusText
                text: ""
            }
        }
    }
}