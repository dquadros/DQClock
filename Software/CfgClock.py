import json
import os

CFG_FILE = "cfg_clock.json"

class CfgClock:
    
    def save(self):
        '''Save current configuration'''
        with open(CFG_FILE, "w") as f:
            json.dump(self.cfg, f)
            f.close()
    
    def load(self):
        '''Read current configuration'''
        try:
            os.stat(CFG_FILE)
            with open(CFG_FILE) as f:
                self.cfg = json.load(f)
        except OSError:
            # file does not exist, create with defaults
            self.cfg = {
                'weekend': False,
                'wake_time': '06:15',
                'wake_sound': '1',
                'snooze': '5',
                'sleep_time': '19:50',
                'sleep_sound': '6',
                'night_color': '2',
                'night_bright': '5'
                }
            self.save()

    def __init__(self):
        self.load()
        
    def __getitem__(self, key):
        return self.cfg[key]

    def __setitem__(self, key, value):
        self.cfg[key] = value

cfg_clock = CfgClock()

