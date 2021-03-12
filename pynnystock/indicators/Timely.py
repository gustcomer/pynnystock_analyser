from datetime import time

class Timely:

    def __init__(self, intra):

        self.intra = intra

        self.times = dict.fromkeys(['0min','10min','20min','30min','40min','50min','1h','1h15','1h30','1h45','2h','3h','4h','5h','6h','6h30'])

        self.times['0min'] = self.intra._core[0]['open']
        self.times['6h30'] = self.intra._core[-1]['close']

        position = 0

        for b in self.intra._core[position:]:
            if b['time'].time() >= time(9,40):
                self.times['10min'] = b['high']
                position = self.intra._core.index(b)
                break

        for b in self.intra._core[position:]:
            if b['time'].time() >= time(9,50):
                self.times['20min'] = b['high']
                position = self.intra._core.index(b)
                break

        for b in self.intra._core[position:]:
            if b['time'].time() >= time(10,0):
                self.times['30min'] = b['high']
                position = self.intra._core.index(b)
                break

        for b in self.intra._core[position:]:
            if b['time'].time() >= time(10,10):
                self.times['40min'] = b['high']
                position = self.intra._core.index(b)
                break

        for b in self.intra._core[position:]:
            if b['time'].time() >= time(10,20):
                self.times['50min'] = b['high']
                position = self.intra._core.index(b)
                break

        for b in self.intra._core[position:]:
            if b['time'].time() >= time(10,30):
                self.times['1h'] = b['high']
                position = self.intra._core.index(b)
                break

        for b in self.intra._core[position:]:
            if b['time'].time() >= time(10,45):
                self.times['1h15'] = b['high']
                position = self.intra._core.index(b)
                break

        for b in self.intra._core[position:]:
            if b['time'].time() >= time(11,0):
                self.times['1h30'] = b['high']
                position = self.intra._core.index(b)
                break

        for b in self.intra._core[position:]:
            if b['time'].time() >= time(11,15):
                self.times['1h45'] = b['high']
                position = self.intra._core.index(b)
                break

        for b in self.intra._core[position:]:
            if b['time'].time() >= time(11,30):
                self.times['2h'] = b['high']
                position = self.intra._core.index(b)
                break

        for b in self.intra._core[position:]:
            if b['time'].time() >= time(12,30):
                self.times['3h'] = b['high']
                position = self.intra._core.index(b)
                break

        for b in self.intra._core[position:]:
            if b['time'].time() >= time(13,30):
                self.times['4h'] = b['high']
                position = self.intra._core.index(b)
                break

        for b in self.intra._core[position:]:
            if b['time'].time() >= time(14,30):
                self.times['5h'] = b['high']
                position = self.intra._core.index(b)
                break

        for b in self.intra._core[position:]:
            if b['time'].time() >= time(15,30):
                self.times['6h'] = b['high']
                position = self.intra._core.index(b)
                break