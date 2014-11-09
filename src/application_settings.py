from PyQt5.QtCore import QSettings


class SettingData(object):

    def __init__(self, name, value, write_to_disk=False):

        self._name = name
        self._value = value
        self._writeToDisk = write_to_disk

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def write_to_disk(self):
        return self._writeToDisk

    @write_to_disk.setter
    def write_to_disk(self, value):
        self._writeToDisk = value


class ApplicationSettings(object):

    def __init__(self):

        self._settings = {}
        self._settingsClient = None

        QSettings.setPath(QSettings.IniFormat, QSettings.UserScope, "settings")
        QSettings.setDefaultFormat(QSettings.IniFormat)

    @property
    def settings_map(self):
        return self._settings

    def load_settings(self):

        self._settingsClient = QSettings()

        # SettingData: (Name, Value, WriteToDisk)
        self._settings["last_folder_path"] = SettingData("last_folder_path",
                                                         self._settingsClient.value
                                                         ("last_folder_path", None))

    def write_settings(self):

        for _, setting in self._settings.items():

            if setting.write_to_disk and setting.value is not None:

                self._settingsClient.setValue(setting.name, setting.value)

