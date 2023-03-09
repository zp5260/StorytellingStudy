from psychopy import prefs
from psychopy import sound
from psychopy import visual, core, event, gui
import os.path
from psychopy.hardware import keyboard



## force quit (anytime): Strg + q|Q  ##
def f_quit():
    try:
        win.close()
    except:
        pass
    Quit = gui.Dlg(title="!!!forced quit!!!")
    Quit.addText('\nexperiment manually cancelled!\n')
    Quit.show()
    core.quit()


class InstructionPresenter:
    def __init__(self, win):
        self.win = win
        self.texts = texts

    def present_text(self, which, *args):
        text = self.texts[which].format(*args)
        instruction = visual.TextStim(self.win, name='instr' + which, font='Arial', alignHoriz='center', alignVert='center', height=1, wrapWidth=30, color='black', text=text)
        instruction.draw()
        self.win.flip()
        event.waitKeys(keyList=['space'])


def trials(triallist, phase, block):
    phase = phase
    block = block
    ntrials = len(triallist)
    trialpath = soundpath + block+'\\'
    n = 1

    for trial in triallist:
        text = f'{block} {n} of {ntrials} {phase} repetitions will now be played:'+'\n'+f'Please reproduce the {block} AFTER the BEEP TONE.'+'\n'+f'Press the "B/b" key to start the {block}.'+'\n'+f'{"8 taps with spacebar" if block== "tempo" else ""}'+'\n\n'+'After the reproducing is done, press the "ENTER" key to continue.'
        instruction = visual.TextStim(win, font='Arial', alignHoriz='center', alignVert='center', height=1, wrapWidth=30, color='black', text=text)
        instruction.draw()
        win.flip()
        event.waitKeys(keyList=['b'])
        beats = sound.Sound(trialpath + trial)
        beats.play()
        core.wait(beats.getDuration() + 0) # intervall before beep: 0
        go = True
        kb.clearEvents(eventType='keyboard') # to clear key buffer
        kb.start()
        beep.play()
        while go:
            core.wait(0.5)
            keys = kb.getKeys(['space', 'return'], waitRelease=False, clear=False)

            if 'return' in keys:                
                if (keys[0].name == 'space') & (len(keys) > 2+1): # extra 1 for the last return
                    go=False
                    kb.stop()
                else:
                    instruction.text="Not valid inputs: please tap again after the BEEP TONE!"
                    instruction.draw()
                    win.flip()
                    core.wait(1.5) 
                    instruction.text=text
                    instruction.draw()
                    win.flip()
                    kb.clearEvents(eventType='keyboard')
                    beep.play()
        win.flip()                        
        begintime = keys[0].rt
        for i, key in enumerate(keys):
            if key.duration is not None:
                duration = round(1000 *key.duration)
            else:
                duration = "NA"
            log_file.write('; '.join(
                subject_data +
                [str(block), str(phase), str(n), str(trial), str(i+1), str(round(1000 *(key.rt - begintime))), str(duration),str(key.name)]) + "\n")
        n += 1
        core.wait(1)


oriprefs=prefs.hardware['audioLib']
prefs.hardware['audioLib']=['pyo']
prefs.hardware['audioLib']=oriprefs

tempo_testing=["TE_MS2_tapping.wav", "TE_E1_tapping.wav", "TE_CS2_tapping.wav", "TE_ES1_tapping.wav", "TE_C1_tapping.wav", "TE_ES3_tapping.wav","TE_C3_tapping.wav", "TE_E2_tapping.wav", "TE_MS3_tapping.wav", "TE_M1_tapping.wav", "TE_CS3_tapping.wav", "TE_M2_tapping.wav", "TE_CS1_tapping.wav", "TE_ES2_tapping.wav", "TE_M3_tapping.wav", "TE_C2_tapping.wav", "TE_MS1_tapping.wav","TE_E3_tapping.wav",]
rhythm_testing=[ "R_E1_tapping.wav", "R_ES1_tapping.wav", "R_M1_tapping.wav", "R_MS2_tapping.wav", "R_ES2_tapping.wav", "R_C2_tapping.wav", "R_MS3_tapping.wav", "R_CS1_tapping.wav", "R_E2_tapping.wav", "R_ES3_tapping.wav", "R_C1_tapping.wav", "R_M2_tapping.wav",  "R_MS1_tapping.wav","R_M3_tapping.wav", "R_CS2_tapping.wav", "R_CS3_tapping.wav", "R_E3_tapping.wav","R_C3_tapping.wav",]
tempo_training = ["TE_exampleI_129bpm_tapping.wav", "TE_exampleII_116bpm_tapping.wav", "TE_exampleIII_121bpm_tapping.wav", ]
rhythm_training = ["R_exampleI_520260520260520130130520_tapping.wav", "R_exampleII_260520650130520260260260520_tapping.wav", "R_exampleIII_520650650520130390130520_tapping.wav", ]

event.globalKeys.clear()
event.globalKeys.add(key='q', modifiers=['ctrl'], func=f_quit, name='force quit q')
event.globalKeys.add(key='q', modifiers=['ctrl', 'capslock'], func=f_quit, name='force quit Q')

texts = {
    "instruction": "Hello \nThank you for participating in our study! \n\nIn each passage you will hear a ritem or beat sequence. Afterwards, please repeat these sound units as precise as possible by tapping the space bar several times. \n\n <Please continue with pressing the space bar.>",
    'tempo_training': "You can now practice the beat task in practice trials before the actual trials begin.\n\nIf you still have questions, you can now turn to the experimenter. After the practice trial, there will be another opportunity to ask questions.\n\n<Start with spacebar>.",
    'rhythm_training': "You can now practice the ritem task in practice trials before the actual trials begin.\n\nIf you still have questions, you can now turn to the experimenter. After the practice trial, there will be another opportunity to ask questions.\n\n<Start with spacebar>.",
    'trained': "You have finished the practice runs.\nDo you have any questions?\n\nIf not, press the space bar to start the experiment.",
    'pause': "Great! You've just completed one of a total of two blocks! \nNow you can pause for a moment.\nIt will continue as soon as you press the spacebar.",
}

file_name = os.path.splitext(os.path.basename(os.path.abspath(__file__)))[0]
info = gui.Dlg(title=f'{file_name}')
info.addField('ID:')
info.addField('Starost:')
info.addField('Spol:', choices=["ženski", "moški", "nebinaren"])
info.show()
if info.OK == False:
    FQuit()
VPinfo = info.data
ID = VPinfo[0]
age = int(VPinfo[1])
sex = VPinfo[2]
header_subject = 'sbj; age; sex; '
subject_data = list(map(str, [ID, age, sex, ]))
header = header_subject + 'block; phase; trialnr; sound; press order; accumulated RT; press duration; key name\n'

win = visual.Window(monitor="TestMonitor", units="deg", color="grey", fullscr= True)
#False, size=(1700, 600))
instruction = InstructionPresenter(win)
beep = sound.Sound(value=500, secs=0.10, volume = 0.1)
kb = keyboard.Keyboard(waitForStart=True)

soundpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Stimuli\\")
data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logfiles')
file_path = os.path.join(data_path, f'VP {ID} {file_name}.csv')
if not os.path.exists(data_path):
    os.makedirs(data_path)
if os.path.exists(file_path):
    try:
        win.close()
    except:
        pass
    error = gui.Dlg(title="!!!Error!!!")
    error.addText("\nVP ID already exists!\n")
    error.show()
    core.quit()

with open(file_path, 'w', buffering=1, encoding='utf-8') as log_file:
    log_file.write(header)
    instruction.present_text('instruction')

    instruction.present_text('tempo_training')
    trials(tempo_training, 'practice', 'tempo')
    instruction.present_text('trained')
    trials(tempo_testing, 'testing', 'tempo')

    instruction.present_text('pause')

    instruction.present_text('rhythm_training')
    trials(rhythm_training, 'practice', 'ritem')
    instruction.present_text('trained')
    trials(rhythm_testing, 'testing', 'ritem')

win.close()
done = gui.Dlg(title="done :)")
done.addText('\nthx for participation!\n')
done.show()
core.quit()
