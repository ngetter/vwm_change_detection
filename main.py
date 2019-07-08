import expyriment as ex
from stimuli import create_stimuli

exp = ex.design.Experiment(name="Change Detection")
from slides import *


class logresp:
    def __init__(self):
        self._log = []

    def append(self, other):
        self._log.append(other)

    def add_log(self):
        rec = {}
        for it_ in self._log:
            rec = {**rec, **it_}
        exp.data.add([v for v in rec.values()])
        self._log.clear()

class sequence(ex.design.Trial):
    def __init__(self, block):
        ex.design.Trial.__init__(self)

        self.log: logresp
        self.log = None
        # associated block
        self.block = block

        # load random trial
        span_ = block.get_factor('span')
        stim_ = create_stimuli(span_)
        self.set_factor('cr',stim_['cr'])


        # fixation (500 ms)
        fix_ = fixation()
        self.add_stimulus(fix_)

        # memstim (500 ms)
        mem_ = memstim(stim_['set'])
        mem_.createStim()
        self.add_stimulus(mem_)
        print(mem_)

        # blank screen (1000 ms)
        blank_ = blank()
        self.add_stimulus(blank_)

        # test (2000ms or response)
        test_ = test_stim(stim_)
        self.add_stimulus(test_)

        # feedbak
        feed_ =  feedback(test_)
        self.add_stimulus(feed_)

    def __str__(self):
        return hex(id(self))


    def run(self):
        print(f"running trial:{self}")
        for stim_ in self.stimuli:
            print (stim_)
            stim_.run(log=self.log)

if __name__ == '__main__':
    ex.control.set_develop_mode(True)
    ex.control.defaults.open_gl = 1

    ex.control.initialize(exp)

    trials_ = [x for x in range(0,4)]
    blocks_ = [1,3,6]
    # prepere

    for val in blocks_:
        block_ = ex.design.Block(name = val)
        block_.set_factor('span',val)
        exp.add_block(block_,1)

    # start the experiment
    lg = logresp()
    ex.control.start()

    # instructions
    inst_ = instructions(join(os.getcwd(), 'instructions','instructions', 'Slide1.PNG'))
    inst_.run()

    print ("\nstart running blocks x trials")
    for block_ in exp.blocks:
        for trial_ in trials_:
            lg.append({'span': block_.get_factor('span')})
            _seq = sequence(block_)
            _seq.log = lg
            print(f"running trial:{_seq}")
            _seq.preload_stimuli()
            _seq.run()
            block_.add_trial(_seq)
            lg.add_log()

    ex.control.end()