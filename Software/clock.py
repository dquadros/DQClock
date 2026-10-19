'''
This class implements the alarm clock logic
'''

import time

MAX_SEC_ALARM = 90
INTERVAL_SEC_ALARM = 5

# utility routines
def min_from_hhmm(hhmm):
    '''Convert hh:mm in minutes after midnight'''
    return int(hhmm[0:2])*60 + int(hhmm[3:5])

def min_from_localtime(lt):
    '''Convert localtime in minutes after midnight'''
    return lt[3]*60 + lt[4]

class CLOCK:

    def _set_next_alarm(self, now):
        '''
        Finds what is the next alarm
        Sets alarm_type, alarm_time and alarm_sound
        '''
        min_now = min_from_localtime(now)
        min_wake = self.min_wake
        if self.snooze_on:
            min_wake += int(self.cfg['snooze'])
        if (min_now < min_wake) or (min_now >= self.min_sleep):
            print (f'Wake at {min_wake}')
            self.alarm_type = 'wake'
            self.alarm_time = min_wake
            self.alarm_sound = int(self.cfg['wake_sound'])
        else:
            print (f'Sleep at {self.min_sleep}')
            self.alarm_type = 'sleep'
            self.alarm_time = self.min_sleep
            self.alarm_sound = int(self.cfg['sleep_sound'])
        print (f"Next alarm: {self.alarm_time//60:02d}:{self.alarm_time%60:02d}")

    def dayOk(now):
        '''Checks if alarm should sound today'''
        if self.cfg['weekend']:
            return True
        return now[6] < 5  # 0 = Monday, 5 = Saturday, 6 = Sunday

    def __init__(self, cfg_clock, now):
        self.cfg = cfg_clock
        self.min_wake = min_from_hhmm(self.cfg['wake_time'])
        self.min_sleep = min_from_hhmm(self.cfg['sleep_time'])
        self.alarm_on = False
        self.alarm_stop = 0
        self.alarm_repeat = 0
        self.snooze_on = False
        self._set_next_alarm(now)
        
    def isAlarmOn(self):
        '''Returns True if alarm is On'''
        return self.alarm_on

    def checkAlarm(self, now):
        '''
        Check for alarm start/stop
        Return operation ('play', 'stop', 'nop') and sound (if op is 'play')
        '''
        if self.alarm_on:
            if time.time() >= self.alarm_stop:
                # time-out alarm
                self.alarm_on = False
                self.snooze_on = False
                self._set_next_alarm(now)
                return 'stop', 0
            elif time.time() >= self.alarm_repeat:
                # repeat alarm_sound
                self.alarm_repeat = time.time() + INTERVAL_SEC_ALARM
                return 'play', self.alarm_sound
        elif min_from_localtime(now) == self.alarm_time:
            if _dayOk(now):
                # start alarm
                self.alarm_on = True
                self.alarm_stop = time.time() + MAX_SEC_ALARM
                self.alarm_repeat = time.time() + INTERVAL_SEC_ALARM
                return 'play', self.alarm_sound
            else:
                self._set_next_alarm(now)
        return 'nop', 0
    
    def endAlarm(self, now):
        '''Ends the curent alarm'''
        self.alarm_on = False
        self.snooze_on = False
        self._set_next_alarm(now)
        
    def snooze(self, now):
        '''Snooze the curent alarm'''
        self.snooze_on = True
        self._set_next_alarm(now)
    