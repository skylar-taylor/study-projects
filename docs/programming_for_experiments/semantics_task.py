from psychopy import visual, core, gui
from datetime import datetime
import random
from psychopy.hardware import keyboard

# create keyboard
kb = keyboard.Keyboard()

# terminate function
def terminate():
    win.close()
    f.close()
    print("Experiment terminated by user.")
    core.quit()

# escape function
def check_for_escape(win):
    escape = kb.getKeys(['escape'], waitRelease=False)
    if escape:
        terminate()

# dictionary for experiment details
exp_data = {}
exp_data['expname'] = 'Semantics Experiment'

# string for date in year/month/day hour/minute
exp_data['expdate'] = datetime.now().strftime('%Y%m%d_%H%M')

# blank string for participant ID
exp_data['participantid'] = ''

# dialogue box
dlg = gui.DlgFromDict(exp_data,
					  title='Input data',
					  fixed=['expname', 'expdate'],
                      order=['expname', 'expdate', 'participantid'])

# quit if okay is not pressed
if not dlg.OK:
    print("User cancelled the experiment")
    f.close()
    core.quit()

# create a fullscreen window with a grey background
win = visual.Window([1024, 768], fullscr=True,
                    allowGUI=True, units="pix", color=(0, 0, 0))

# read in the stimuli data
with open('trials.csv', 'r') as f:
    # read in header
    header = f.readline().strip().split(',')
    # read in data
    data = [line.strip().split(',') for line in f.readlines()]

# create file to store experiment results
filename = f'Par_{exp_data["participantid"]}_{exp_data["expdate"]}'
f = open(filename, 'w')
f.write('Condition,Target,Word1,Word2,Word3,Answer,Correct Answer,RT,IsCorrect,Time\n')

# blocks
condition = ['high', 'low', 'colour', 'size', 'texture', 'shape'] 
random.shuffle(condition)
# create dictionary with condition as key
data_dict = {x: [row for row in data if row[0] == x] for x in condition} 

# brief
brief = visual.TextStim(win, '', pos=(0,0), height=50, wrapWidth = 1000)
brief.setText('Welcome to our experiment.\n\n You will see a target word and three choices.\n\n Choose the word closest to the meaning or to a specific feature of the target word as fast as possible.\n\n Left Answer: Keypress “1”. Middle Answer: Keypress “2”. Right Answer: Keypress "3”.\n\n Press “space” to start or “escape” at any time to quit.')
brief.draw()
win.flip()
# wait for space or escape
keys = kb.waitKeys(keyList=['space', 'escape'])
start_time = core.getTime()
if 'escape' in keys:
    terminate()

#fixation cross
fixation = visual.TextStim(win, '+', height=60)
fixation.draw()
win.flip()
core.wait(5)
check_for_escape(win)

# text stimuli
target = visual.TextStim(win, '', pos=(0,200), height=60)
block = visual.TextStim(win, '', pos=(0,50), height=40)
word1 = visual.TextStim(win, '', pos=(-400,-100), height=60)
word2 = visual.TextStim(win, '', pos=(400,-100), height=60)
word3 = visual.TextStim(win, '', pos=(0,-100), height=60)

# set brief time to 5 seconds
brief_time = 5

# run each block
for x in data_dict.keys():
    # randomise trials
    condition_data = data_dict[x]
    random.shuffle(condition_data)
    
    # set similarity word for brief
    if x == "high" or x == "low":
        similarity = "meaning"
    else:
        similarity = x
    
    # block instructions
    brief.setText(f'The experiment is about to begin. \n\n In the next block choose the word that has a similar {similarity}.\n\n Get READY!')
    brief.draw()
    win.flip()
    core.wait(brief_time)
    check_for_escape(win)
    
    # run trials
    for row in condition_data:
        # set stimuli
        target.setText(f'{row[1]}')
        block.setText(f'{similarity}')
        word1.setText(f'{row[2]}')
        word2.setText(f'{row[3]}')
        word3.setText(f'{row[4]}')
        # draw stimuli
        target.draw()
        block.draw()
        word1.draw()
        word2.draw()
        word3.draw()
        win.flip()
        # set start time
        trial_time = core.getTime()
        kb.clock.reset()
        # wait for response or 10 seconds
        stim_keys = kb.waitKeys(keyList=['1', '2', '3', 'escape'], maxWait=10)
        # record response
        if stim_keys:
            if 'escape' in stim_keys:
                terminate()
            else:
                for key in stim_keys:
                    answer = key.name
                    rt = key.rt
                    if answer == row[5]:
                        iscorrect = 1
                    else:
                        iscorrect = 0
                    time = trial_time - start_time
        else:
            answer = ''
            rt = 'NA'
            iscorrect = 0
            time = trial_time - start_time
        
        # write to file
        f.write(f'{row[0]},{row[1]},{row[2]},{row[3]},{row[4]},{answer},{row[5]},{rt},{iscorrect},{time}\n')
        
        # fixation cross
        fixation.draw()
        win.flip()
        core.wait(random.uniform(0.5, 2.5))
    
    # randomise time for break and brief messages
    if x != condition[5]:
        brief_time = random.uniform(3.75, 6.25)
        brief.setText('Take a short break, but please pay attention to the screen. \n\n The experiment is going to start again in a few seconds.')
        brief.draw()
        win.flip()
        core.wait(brief_time)
        check_for_escape(win)

# end of experiment message
end = visual.TextStim(win, 'Thank you for taking part in this study. \n\n Your response has been recorded. \n\n The experiment will now close.', pos=(0,0), height=50, wrapWidth = 1000)
end.draw()
win.flip()
core.wait(5)


f.close()
win.close()
core.quit()