from expyriment.design.randomize import make_multiplied_shuffled_list as shuffle, rand_element
properties_ ={
	'colors':{
		"Red"		:	(255,0,0),
		"Blue"		:	(0,0,255),
		"Yellow"	:	(255,255,0),
		"Magenta" 	:	(255,0,255),
		"Cyan" 		:	(0,255,255),
		"Green"		:	(0,128,0),
		"Lime"		:	(0,255,0),
		"Purple"	:	(128,0,128),
		"White"		:	(255,255,255),
	},

    'size' :(50,50),
    'positions':[
        (-65,0),(65,0),(0,65),(0, -65), (65,65), (-65,-65)
    ],

    'response': ['S','D']
}

factors_ = {
    'set_size':[2,4,6]
}


def create_stimuli(n):

    pos_ = shuffle(properties_['positions'], n)
    pos_xy_ = pos_[0:n]


    col_ = shuffle(properties_['colors'], n)[0:n]
    col_rgb = [properties_['colors'][c] for c in col_]

    resp_ = rand_element(properties_['response'])

    mem_ = [z for z in zip(pos_xy_,col_rgb)]

    if resp_=='S':
        test_ = rand_element(mem_)
    else:
        color_bank_ = [v for c,v in properties_['colors'].items() if c not in col_]
        test_pos = rand_element(pos_xy_)
        test_col = rand_element(color_bank_)
        test_ = (test_pos, test_col)

    stim = {
        'set': [ {'position':m[0], 'colour':m[1]} for m in mem_ ],
        'cr': resp_,
        'test': {'position':test_[0], 'colour':test_[1]},
    }
    return stim


if __name__=='__main__':
    stimulus_ = create_stimuli(2)
    print(stimulus_)