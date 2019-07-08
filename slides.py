import expyriment as ex
import os
from os.path import join

from main import exp

class memstim(ex.stimuli.Canvas):
    def __init__(self, objects):
        ex.stimuli.Canvas.__init__(self, ex.control.defaults.window_size, colour=(0,0,0))

        self.objects = objects
        self.span = len(objects)
        # self.preload()
        self.wait = 500

    def createStim(self):
        for obj in self.objects:
            stim_ = ex.stimuli.Rectangle((50,50), position=obj['position'], colour=obj['colour'])
            stim_.plot(self)

        ex.stimuli.TextLine(f"{str(self.span)}:{self.id}:{hex(id(self))}").plot(self)
        if ex.control.defaults.open_gl > 0:
            self.save(join(os.getcwd(), 'stimuli', f"stimulus_{self.span}_{self.id}_{hex(id(self))}.png"))

    def run(self,**argx):
        self.present()
        exp.clock.wait(self.wait)
        # x,y  = exp.keyboard.wait(ex.misc.constants.K_SPACE)

    def __repr__(self):
        return f"span={self.span}: id={self.id}:{hex(id(self))}"

###
class fixation(ex.stimuli.FixCross):
    '''
        display fixation
        @wait: time of presentation
    '''
    def __init__(self):
        ex.stimuli.FixCross.__init__(self)
        # self.preload()
        self.wait = 800

    def __repr__(self):
        return f"fixation: id={self.id}"


    def run(self, **argx):
        self.present()
        exp.clock.wait(self.wait)

class blank(ex.stimuli.BlankScreen):
    def __init__(self):
        ex.stimuli.BlankScreen.__init__(self)
        # self.preload()
        self.wait = 1000

    def __repr__(self):
        return f"blank: id={self.id}"

    def run(self, **argx):
        self.present()
        exp.clock.wait(self.wait)

class test_stim(ex.stimuli.Canvas):
    def __init__(self, obj):
        ex.stimuli.Canvas.__init__(self, ex.control.defaults.window_size, colour=(0, 0, 0))
        self.stim = ex.stimuli.Rectangle((50,50),**obj['test']).plot(self)

        # self.preload()
        self.wait = 2000
        self.response_keys = {ex.misc.constants.K_d:'D',
                         ex.misc.constants.K_s:'S'}
        self.cr = obj['cr']
        self.acc = None

        self.response_key = None
        self.response_rt = None

    def __repr__(self):
        return f"test: id={self.id}"

    def run(self,log):
        self.present()
        self.response_key, self.response_rt = exp.keyboard.wait(self.response_keys)
        self.acc = self.response_keys[self.response_key] == self.cr
        log.append( { 'cr': self.cr, 'id': self.id, 'resp': self.response_keys[self.response_key], 'rt': self.response_rt, 'acc':self.acc})

class feedback(ex.stimuli.Canvas):
    def __init__(self, obj):
        ex.stimuli.Canvas.__init__(self, ex.control.defaults.window_size, colour=(0, 0, 0))
        self.ok = ex.stimuli.TextLine('OK', text_colour=(0,255,0), text_size=20)
        self.err = ex.stimuli.TextLine('ERROR', text_colour=(255,0,0), text_size=20)

        self.wait = 1000
        self.source = obj

    def __repr__(self):
        return f"feedback: id={self.id}"

    def run(self, **args):
        if self.source.acc:
            self.ok.present()
        else:
            self.err.present()

        # self.present()
        exp.clock.wait(self.wait)
