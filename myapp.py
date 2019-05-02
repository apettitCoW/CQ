from kivy.config import Config
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
import load_spreadsheet

class FooScreen(Screen):
    pass

class SharedData:
    """
    A class designed to hold data that needs to be access by multiple app
    screens.
    """
    def __init__(self):
        """
        Initialize the SharedData class by creating an attribute called json.
        """
        self.json = None


class FileSelectorPopup(FloatLayout):
    """
    A class that creates a popup screen containing a FileChooser.
    """
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class IntroductionScreen(Screen):
    """
    A welcome screen for a new user. Gives an introductory message and prompts
    the user to upload a spreadsheet from their instructor.
    """
    loadfile = ObjectProperty(None)

    def dismiss_popup(self):
        """
        Close popup.
        :return: None
        """
        self._popup.dismiss()

    def show_load(self):
        """
        Create popup window that displays FileChooser widget, allowing a user
        to select and load a spreadsheet.
        :return: None
        """
        content = FileSelectorPopup(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, selection):
        """
        Get the json representation of an excel file when given that file's
        path. Exit popup window and transition to the next screen.
        :param selection: An array containing one element: the path of an excel
         file
        :return: None
        """
        json_actions = load_spreadsheet.get_actions(selection[0])
        App.get_running_app().shared_data.json = json_actions

        print(App.get_running_app().shared_data.json)

        self.dismiss_popup()


class CQApp(App):
    """
    The overall app class.
    """
    # attribute for sharing data across screens
    shared_data = SharedData()


if __name__ == '__main__':
    Config.set('graphics', 'resizable', 0)
    Window.size = (350, 650)
    CQApp().run()

