import time

class Timer:
    def __init__(self):
        self.lasttick = 0.0
        self.tickcount = -1
        self.lastticktime = 0.0

    def tick(self, destfps = 0):
        """Tick a timer. If the destfps was given then application will not run
        faster then destfps frames per second"""
        self.lastticktime = time.time() - self.lasttick
        self.lasttick = time.time()
        if destfps:
            ftime = 1.0 / destfps
            if self.lastticktime < ftime:time.sleep(ftime - self.lasttick)
        self.tickcount += 1
        if self.tickcount >= 65000:self.tickcount = 0

    def tickpassed(self, count):
        """Return True every count tick"""
        count = int(count)
        if count == 0:return False # Avoid division by zero
        if self.tickcount % count == 0:return True
        else:return False

    def timepassed(self, timepassed):
        if time.time() - self.lasttick > timepassed / 1000.0:
            self.tick()
            return True
        else:return False

    def reset(self):
        """reset timer"""
        self.lasttick = 0.0
        self.tickcount = 0
