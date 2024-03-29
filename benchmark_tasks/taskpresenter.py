from psychopy import visual, core, event
import pandas as pd
import numpy as np
import gc

from tools.lsl_wrapper import LSLSEventStreamer

class TaskPresenter():
    def __init__(self, task_list=["rt"], block_list=["0"], focus="+",
                 fullscr=False, marking=False, templated=False,
                 rand_select=True, n_trials=20, rest_time=25, **kwargs):

        self.audio_tasks = ["anb"]
        self.k_words = kwargs
        self.rest_time = rest_time
        self.marking = self.mark_string_to_bool(marking)
        self.task_list = task_list
        self.rand_select = rand_select
        self.n_trials = n_trials

        if fullscr:
            self.win = visual.Window(size=[1920, 1080], monitor="testMonitor",
                                    fullscr=True, screen=1)
        else:
            self.win = visual.Window(monitor="testMonitor")
        self.focus = visual.TextStim(self.win, text=focus)

        if kwargs["sub_id"] and kwargs["session_num"]:
            self.sub_id = kwargs["sub_id"]
            self.session_num = kwargs["session_num"]

        self.lsl_logger = LSLSEventStreamer(str(self.sub_id))

        if templated:
            for indx, task in enumerate(self.task_list):
                self.task = task
                self.block = block_list[indx]
                print(f"Task: {self.task}, Block: {self.block}")
                self.export_dir = self.get_export_dir_string()
                self.prompts = self.load_prompts()
                self.run_task()
                gc.collect()
            if self.marking:
                self.markserver.data_transfer("KILL")
        else:
            raise FileNotFoundError("No template file found")
            self.sub_id, self.session_num = self.get_session_information()

# Setting Optional Parameters.--------------------------------------------------

    def check_for_kwarg(self, kwarg):

        if k_word in self.k_words:
            return True
        return False

# Instruction and Prompt Display Methods ---------------------------------------


    def run_task(self):

        data = []

        if self.task == "cr":
            from controlled_rest import run_trial as task_logic
            self.show_instructions()
            task_logic(self, rest_time=self.rest_time)
            self.show_instructions(exit_instruct=True)
            return
        elif self.task == "rt":
            from rt import run_trial as task_logic
            trials = pd.read_csv("./trial_sheets/rt_trials.csv")
        elif self.task == "gng":
            from go_no_go import run_trial as task_logic
            trials = pd.read_csv("./trial_sheets/go_no_go_trials.csv")
        elif self.task == "es":
            from stroop import run_trial as task_logic
            trials = pd.read_csv("./trial_sheets/es_trials.csv")
        elif self.task == "nb" or self.task == "anb":
            from n_back import run_trial as task_logic
            trials = pd.read_csv("./trial_sheets/n_back_trials.csv")
        elif self.task == "ewm":
            from emo_wm import run_trial as task_logic
            trials = pd.read_csv("./trial_sheets/ewm_trials.csv")

        # task_logic(tp=self, templated=True, block=self.block)
        if self.block == 0:
            self.show_instructions(practice=True)
        else:
            self.show_instructions(practice=False)
        if self.task in self.audio_tasks:
            data = task_logic(self, trials, data, block=[self.block], aud=True)
        else:
            data = task_logic(self, trials, data, block=[self.block])
        self.show_instructions(exit_instruct=True)
        self.write_to_csv(data)



    def load_prompts(self):
        """Loads the instructions that are displayed to the participant depending
           on what cognitive task they are completing.
           Args:
                self.task(str): string value code for each task.
           Returns:
                self.prompts(dict): Set of instructions for the cognitive task.
        """

        prompt_dict = "rt"

        if self.task == "rt":
            from prompts import rt
            return rt
        elif self.task == "gng":
            from prompts import gng
            return gng
        elif self.task == "es":
            from prompts import es
            return es
        elif self.task == "nb":
            from prompts import nb
            return nb
        elif self.task == "anb":
            from prompts import anb
            return anb
        elif self.task == "ewm":
            from prompts import ewm
            return ewm
        elif self.task == "cr":
            from prompts import cr
            return cr
        else:
            pass


    def show_instructions(self, practice=True, exit_instruct=False):
        """Shows the participant the instructions that they will need in order to
           complete the cognitive task.
           Args:
                win: The Psychopy window in which the instuctions will be displayed
           Returns:
                None
        """
        if not practice:
            instructions = self.prompts["instructions"]
            del instructions[-2]
            del instructions[-2]
        elif exit_instruct:
            instructions = self.prompts["exit_instructions"]
        else:
            instructions = self.prompts["instructions"]

        for prompt in instructions:
                self.send_mark("insruction_page_turn")
                main_text = visual.TextStim(self.win, text=prompt)
                sub_text = visual.TextStim(self.win, text="Press any key to continue",
                                           pos=(0.0, -0.8))
                sub_text.setColor((175, 72, 72), 'rgb255')
                main_text.draw()
                sub_text.draw()
                self.win.flip()
                while not event.getKeys(keyList=None):
                    pass


    def display_n(self, n):

        prompt = (f"For this set of trails you will be performing a {n}-Back. "
                  f"Press the RIGHT arrow key if the current letter displayed "
                  f"matches the letter displayed {n} letter(s) ago.")
        main_text = visual.TextStim(self.win, text=prompt)
        sub_text = visual.TextStim(self.win, text="Press any key to continue",
                                   pos=(0.0, -0.8))
        sub_text.setColor((175, 72, 72), 'rgb255')
        main_text.draw()
        sub_text.draw()
        self.win.flip()
        while not event.getKeys(keyList=None):
            pass



    def get_session_information(self):
        """Displays prompts for experimenter to input information about the
           data collection session to the command prompt.
           Args:
                None
           Returns:
                session_id(int): The session id number.
                sub_id(int of len 4): The four digit participant ID.
           """

        while True:
            print("Before beginning, please enter a participant ID: ")
            sub_id = input("> ")
            if len(sub_id) == 4 and sub_id.isdigit():
                break
            else:
                print("That is not a valid subject ID...")
        while True:
            print("Please enter the session number as in interger: ")
            session_num = input("> ")
            if len(session_num) == 1 and session_num.isdigit():
                break
            else:
                print("That is not a valid session number...")

        return (sub_id, session_num)


    def show_performance(self, entry, too_early=False):
        """Provides the participant feedback during practice trials.
           Args:
                entry(bool): True if participant responded correctly.
                too_early(bool): True is participant responded before stim was
                presented.
           Returns:
                None
        """

        if entry:
            message = visual.TextStim(self.win, text="Correct")
            message.draw()
            self.win.flip()
            core.wait(1)
        elif too_early:
            message = visual.TextStim(self.win, text="Incorrect - Too Early")
            message.draw()
            self.win.flip()
            core.wait(1)
        else:
            message = visual.TextStim(self.win, text="Incorrect")
            message.draw()
            self.win.flip()
            core.wait(1)


    def log_response(self, resp_cor, resp_type, q_type, data):
        """Handles Response Logic when the participant responds to a trial."""
        pass


    def give_break(self, prompt_num="1"):
        """Displays text to the participant informing them that they are currently
           experiencing a self-paced break.
           Args:
                prompt_num(int): The nth break (i.e. break 1, 2 or 3).
           Returns:
                None"""

        for prompt in self.prompts[f"break_{prompt_num}"]:
            while not event.getKeys(keyList=None):
                message = visual.TextStim(self.win, text=prompt)
                m2 = visual.TextStim(self.win, text="Press any key to continue",
                                           pos=(0.0, -0.8))
                m2.setColor((175, 72, 72), 'rgb255')
                message.draw()
                m2.draw()
                self.win.flip()


    def draw_focus(self, focus_time):
        """Draws a focus / fixation point to the screen before a trial begins.
           Args:
                focus_time(float): Amount of time, in seconds, a focus should
                be displayed for.
           Returns:
                None.
        """

        self.focus.draw()
        self.win.flip()
        core.wait(focus_time)

# Data Entry and File Naming Methods -------------------------------------------

    def get_export_dir_string(self):

        """Returns the string value used for the data directory where the
        participant's data file is to be stored.
           Args:
                None.
           Returns:
                data_dir(str): The name of the data directory.
        """

        dir_strs = {"rt": "reaction_time", "gng": "go_no_go",
                    "es": "emo_stroop", "nb": "n_back", 
                    "ewm": "emotional_working_memory",
                    "cr": "controlled_rest"}
        
        return dir_strs[self.task]


    def write_to_csv(self, data, **kwargs):
        """Takes the data from all of the trails and writes it out to a .csv file
            Args:
                data(list): A two dimensional list containing all the trial
                information
            Returns:
                None
        """

        if self.task == "rt":
            data_frame = {"Trial": [d[0] for d in data],
                          "Reaction_Time": [d[1] for d in data],
                          "Performance": [d[2] for d in data],
                          "Practice": [d[3] for d in data],
                          "Block": [d[4] for d in data],
                         }
            df = pd.DataFrame(data=data_frame)
        elif self.task == "gng":
            data_frame = {"Trial": [d[0] for d in data],
                          "Reaction_Time": [d[1] for d in data],
                          "Performance": [d[2] for d in data],
                          "Condition": [d[3] for d in data],
                          "Practice": [d[4] for d in data],
                          "Block": [d[5] for d in data],
                         }
            df = pd.DataFrame(data=data_frame)
        elif self.task == "nb" or self.task == "anb":
            data_frame = {"Trial": [d[0] for d in data],
                          "Reaction_Time": [d[1] for d in data],
                          "Performance": [d[2] for d in data],
                          "Correct Response": [d[3] for d in data],
                          "Participant Response": [d[4] for d in data],
                          "Practice": [d[5] for d in data],
                          "Block": [d[6] for d in data],
                         }
            df = pd.DataFrame(data=data_frame)
        elif self.task == "ewm":
            data_frame = {"Trial": [d[0] for d in data],
                          "Reaction_Time": [d[1] for d in data],
                          "Performance": [d[2] for d in data],
                          "Correct Response": [d[3] for d in data],
                          "Participant Response": [d[4] for d in data],
                          "Practice": [d[5] for d in data],
                          "Block": [d[6] for d in data],
                         }
            df = pd.DataFrame(data=data_frame)
        elif self.task == "es":
            data_frame = {"Trial": [d[0] for d in data],
                          "Reaction_Time": [d[1] for d in data],
                          "Performance": [d[2] for d in data],
                          "Display Item": [d[3] for d in data],
                          "Practice": [d[4] for d in data],
                          "Block": [d[5] for d in data],
                         }
            df = pd.DataFrame(data=data_frame)
        else:
            print("Task not supported.")

        df.to_csv(f"./data/{self.export_dir}/{self.sub_id}_{self.task}_s"
                  f"{self.session_num}_blk{self.block}.csv",
                  index=False)

# Marking Methods --------------------------------------------------------------

    def mark_string_to_bool(self, marking):
        """Converts an incoming mark string to a Bool.
        Args:
            marking(str): The mark string sent when object is created.
        Returns:
            Bool.
        """
        if marking.lower() in ["t", "true", "1", "yes", "y"]:
            return True
        return False


    def send_mark(self, mark_type):

        mark_dict = {"task_start": "BLOCK_START",
                     "trial_start": "STIM_DISPLAYED",
                     "resp_cor": "CORRECT_RESPONSE",
                     "resp_incor": "INCORRECT_RESPONSE",
                     "too_early": "TOO_EARLY",
                     "task_end": "BLOCK_END",
                     "rest_start": "REST_START",
                     "rest_end": "REST_END",
                     "insruction_page_turn": "PAGE_TURN"}
        
        print("Marking")
        self.lsl_logger.send_event(mark_dict[mark_type], self.task)

        

# Trial Selection / Modulation Methods -----------------------------------------

    def select_trials(self, trials, block, n_trials=20):

        trials = trials[trials["block"].isin(block)].reset_index()
        selected = np.random.choice(trials.index.values, n_trials)
        sampled_trials = trials.iloc[selected]
        return sampled_trials
