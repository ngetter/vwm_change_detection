import expyriment as ex
from stimuli import create_stimuli

exp = ex.design.Experiment(name="Change Detection")
from slides import *

LANG = 'HE'

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
    ex.control.defaults.window_size = (1280, 720)
    ex.control.defaults.open_gl = 2

    ex.control.initialize(exp)


    # practice exp
    trials_p_ = [x for x in range(0, 4)]
    blocks_p_ = [1, 3]

    for val in blocks_p_:
        block_ = ex.design.Block(name = f'practice_{val}')
        block_.set_factor('span',val)
        block_.set_factor('phase','practice')

        exp.add_block(block_,1)


    # main exp
    trials_ = [x for x in range(0,4)]
    blocks_ = [1,3,6]

    for val in blocks_:
        block_ = ex.design.Block(name = f'main_{val}')
        block_.set_factor('span',val)
        block_.set_factor('phase','main')

        exp.add_block(block_,1)

    # start the experiment

    lg = logresp()
    ex.control.start()

    # instructions
    inst_ = instructions(join(os.getcwd(), 'instructions',LANG, 'Slide1.PNG'))
    inst_.run()

    inst_ = instructions(join(os.getcwd(), 'instructions', LANG, 'Slide2.PNG'))
    inst_.run()

    inst_ = instructions(join(os.getcwd(), 'instructions', LANG, 'Slide3.PNG'))
    inst_.run()

    print ("\nStart running PRACTICE ********")
    for block_ in [b for b in exp.blocks if b.factor_dict['phase'] == 'practice']:
        for trial_ in trials_:
            _seq = sequence(block_)
            print(f"running trial (prac):{_seq}")
            _seq.preload_stimuli()
            _seq.run()
            block_.add_trial(_seq)
        block_.save_design(f'{block_.name}_{block_.id}.csv')

    print ("\nStart running MAIN ********")
    for block_ in [b for b in exp.blocks if b.factor_dict['phase'] == 'main']:
        for trial_ in trials_:
            lg.append({'span': block_.get_factor('span')})
            _seq = sequence(block_)
            _seq.log = lg
            print(f"running trial:{_seq}")
            _seq.preload_stimuli()
            _seq.run()
            block_.add_trial(_seq)
            lg.add_log()
        block_.save_design(f'{block_.name}_{block_.id}.csv')
        inst_ = instructions(join(os.getcwd(), 'instructions', LANG, f"{block_.name}.png"))
        inst_.run()

    inst_ = instructions(join(os.getcwd(), 'instructions', LANG, 'end.png'))
    inst_.run()

    ex.control.end()
    exp.save_design('design.csv')
