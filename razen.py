from kivy.app import App
from kivy.lang import Builder
from kivy.base import runTouchApp
from kivy.core.audio import SoundLoader
from kivy.properties import ListProperty
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition

import sys
import time
import random
import threading

sound_path = 'gong.mp3'

clamp  = lambda val, minv, maxv: max(min(val, maxv), minv)
sample = lambda mu, sigma, lo, hi: int(clamp(abs(random.gauss(mu, sigma)), lo, hi))

class Timer(threading.Thread):
    def __init__(self, sec=5, screenmgr=None):
        self.killed = False
        self.finished = False
        self.time = int(sec)
        self.screenmgr = screenmgr
        threading.Thread.__init__(self)

    def run(self):
        global sound_path
        print("Take a few deep breaths")
        for i in reversed(range(8)):
            print(i)
            time.sleep(1)
        print("Start of practice!")
        SoundLoader.load(sound_path).play()

        current_time = time.monotonic()
        end_time = current_time + self.time

        while current_time < end_time:
            time.sleep(1)
            togo = end_time - current_time
            current_time = time.monotonic()
            print("Time to go:", togo)

        # End practice - 2x for effect
        print("End of practice!")
        SoundLoader.load(sound_path).play()
        time.sleep(5)
        SoundLoader.load(sound_path).play()

        self.finished = True
        # self.screenmgr.new_exit_screen()

    def start(self): 
        self.__run_backup = self.run 
        self.run = self.__run       
        threading.Thread.start(self) 

    def __run(self):
        sys.settrace(self.globaltrace) 
        self.__run_backup() 
        self.run = self.__run_backup 

    def globaltrace(self, frame, event, arg): 
        if event == 'call': 
            return self.localtrace 
        else: 
            return None

    def localtrace(self, frame, event, arg): 
        if self.killed: 
            if event == 'line': 
                raise SystemExit() 
        return self.localtrace 

    def kill(self):
        self.killed = True

    def update_time(self, sec):
        self.time = int(sec)

TIMER = Timer()

class FirstScreen(Screen):
    pass

class SecondScreen(Screen):
    def update_values(self): # Seconds
        self.std  = float(self.ids.std.text or 300)
        self.lo   = float(self.ids.min.text or 180)
        self.hi   = float(self.ids.max.text or 900)
        self.mean = float(self.ids.mean.text or (abs(self.hi - self.lo) / 2))
        self.params = {
            'std': self.std,
            'mean': self.mean,
            'lo': self.lo,
            'hi': self.hi
        }
        print(self.params)

    def restore_defaults(self):
        self.std  = 300.
        self.lo   = 180.
        self.hi   = 900.
        self.mean = abs(self.hi - self.lo) / 2
        self.params = {
            'std': self.std,
            'mean': self.mean,
            'lo': self.lo,
            'hi': self.hi
        }
        print(self.params)

class RazenTimer(Screen):
    colour = ListProperty([1., 0., 0., 1.])

class ExitScreen(Screen):
    label = Label()

class MyScreenManager(ScreenManager):
    def stop_timer(self):
        global TIMER
        TIMER.kill()

    def time_convert(self, sec):
        mins = sec // 60
        sec = sec % 60
        hours = mins // 60
        mins = mins % 60
        return "{0}:{1}:{2}".format(int(hours),int(mins),sec)

    def new_colour_screen(self):
        global TIMER
        TIMER.killed = True

        self.get_screen('settings').restore_defaults()

        name = 'RazenTimer'
        s = RazenTimer(name=name,
                       colour=[random.random() for _ in range(3)] + [1])
        self.add_widget(s)
        self.current = name

        screen = self.get_screen('settings')
        v = {
            'std': screen.std,
            'mean': screen.mean,
            'lo': screen.lo,
            'hi': screen.hi
        }
        self.params = v

        meditation_time = sample(v['mean'], v['std'], v['lo'], v['hi'])
        TIMER = Timer(meditation_time)
        TIMER.start()
        s.label = Label()

        # End practice screen
        # new_thread = threading.Thread(target=self.new_exit_screen)
        # new_thread.start()
        # while TIMER.finished is False:
        #     time.sleep(0.1)
        # self.new_exit_screen()

    # TODO: Should really be using Kivy's clock for this. Refactor.
    # TODO: how to change labels and text dynamically on widgets?

    def new_exit_screen(self):
        s = ExitScreen()
        s.label = Label()
        self.add_widget(s)
        self.current = 'ExitScreen'

root_widget = Builder.load_string('''
#:import FadeTransition kivy.uix.screenmanager.FadeTransition
MyScreenManager:
    transition: FadeTransition()
    FirstScreen:
    SecondScreen:
<FirstScreen>:
    name: 'main'
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Razen (Random Zen) Meditation App'
            font_size: 30
        Image:
            source: 'razen_logo.jpg'
            allow_stretch: True
            keep_ratio: True
        BoxLayout:
            Button:
                text: 'Start Razen'
                font_size: 30
                on_release: app.root.new_colour_screen()
            Button:
                text: 'Settings'
                font_size: 30
                on_release: app.root.current = 'settings'
<SecondScreen>:
    name: 'settings'
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Settings'
            font_size: 30
        BoxLayout:
            Button:
                text: 'min time (seconds)'
            TextInput:
                id: min
        BoxLayout:
            Button:
                text: 'max time (seconds)'
            TextInput:
                id: max
        BoxLayout:
            Button:
                text: 'mean (seconds)'
            TextInput:
                id: mean
        BoxLayout:
            Button:
                text: 'standard deviation (seconds)'
            TextInput:
                id: std
        Image:
            source: 'razen_logo.jpg'
            allow_stretch: True
            keep_ratio: True
        BoxLayout:
            Button:
                text: 'Start Razen'
                font_size: 20
                on_release: app.root.new_colour_screen()
            Button:
                text: 'Update Values'
                font_size: 20
                on_release: app.root.get_screen('settings').update_values()
            Button:
                text: 'Restore Defaults'
                font_size: 20
                on_release: app.root.get_screen('settings').restore_defaults()
            Button:
                text: 'Back'
                font_size: 20
                on_release: app.root.current = 'main'
<RazenTimer>:
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Params: {}, {}, {}, {}'.format(*app.root.get_screen('settings').params.items())
            font_size: 16
        Widget:
            canvas:
                Color:
                    rgba: root.colour
                Ellipse:
                    pos: self.pos
                    size: self.size

        BoxLayout:
            Button:
                text: 'Stop Razen'
                font_size: 30
                on_release: app.root.stop_timer()
            Button:
                text: 'Reroll Razen'
                font_size: 30
                on_release: app.root.new_colour_screen()
            Button:
                text: 'Back'
                font_size: 30
                on_release: app.root.current = 'main'
<ExitScreen>:
    name: 'ExitScreen'
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Congratulations! Razen practice has ended.'
            font_size: 30
        Image:
            source: 'razen_logo.jpg'
            allow_stretch: True
            keep_ratio: True
        BoxLayout:
            Button:
                text: 'Back'
                font_size: 30
                on_release: app.root.current = 'main'
            Button:
                text: 'Reroll Razen'
                font_size: 30
                on_release: app.root.new_colour_screen()

''')

class ScreenManagerApp(App):
    def build(self):
        return root_widget
 
if __name__ == "__main__":
    ScreenManagerApp().run()

