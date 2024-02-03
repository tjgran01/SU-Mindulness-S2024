import pandas as pd
from numpy import random
import os
import string

class TrialSheetCreator():
    def __init__(self, tasks=["es"], num_blocks=5, num_trials=40,
                 exper_name="", focus_range=(20, 50):
        self.tasks = tasks
        self.num_blocks = num_blocks
        self.num_trials = num_trials
        self.exper_name = exper_name
        self.focus_min = focus_range[0]
        self.focus_max = focus_range[1]

        if self.exper_name == "":
            self.exper_name = "mindfulness"

        for task in self.tasks:
            self.block_num_list = self.make_block_num_list()
            self.focus_times = self.gen_focus_times()
            if task == "ewm":
                self.mk_ewm_trials()
            elif task == "es":
                self.mk_es_trials()

    def mk_ewm_trials(self):

        imgs = self.select_ewm_images()
        let_arrays = self.make_let_arrays()
        let_questions = self.make_let_questions(let_arrays)
        self.mk_ewm_sheet(self.block_num_list, self.focus_times, let_arrays, imgs,
                          let_questions)


    def mk_es_trials(self):

        display_items = self.gen_es_word_list()
        word_colors = self.gen_word_colors()
        self.mk_es_sheet(self.block_num_list, self.focus_times, display_items,
                        word_colors)

    def mk_rt_trials(self):

        display_items = ["X" for x in range(self.num_blocks * self.num_trials)]
        self.mk_rt_sheet(self.block_num_list, self.focus_times, display_items)


## Emo Working Mem Specific ----------------------------------------------------

    def select_ewm_images(self):

        img_dir = ("../benchmark_tasks/trial_sheets/stims/oasis/images/")
        selected_imgs = pd.read_csv(f"./resources/selected_imgs_mnd.csv").pic_name.tolist()
        selected_imgs = [f"{img}.jpg" for img in selected_imgs]

        if self.exper_name == "mindfulness":
            img_list = [img for img in os.listdir(img_dir) if img in selected_imgs]
        else:
            img_list = os.listdir(img_dir)

        trial_imgs = []
        for n in range(self.num_blocks):
            block_imgs = []
            for x in range(self.num_trials):
                sel_img = random.choice(img_list, replace=False)
                block_imgs.append(sel_img)
            trial_imgs.append(block_imgs)

        trial_imgs = [item for sublist in trial_imgs for item in sublist]
        return trial_imgs


    def make_let_arrays(self):

        letters = list(string.ascii_lowercase)

        let_arrays = []
        for trial in range(0, (self.num_blocks * self.num_trials)):
            let_array = [random.choice(letters, replace=False) for x in range(6)]
            let_array = "".join(let_array)
            let_arrays.append(let_array)
        return let_arrays


    def make_let_questions(self, let_arrays):

        letters = list(string.ascii_lowercase)
        options = ["all_in", "all_out", "one_in", "two_in"]

        let_questions_list = []
        for array in let_arrays:

            array = list(array)
            anti_array = [let for let in letters if let not in array]
            pick = random.choice(options)

            if pick == "all_in":
                let_questions = [random.choice(array, replace=False) for x in range(3)]
            elif pick == "all_out":
                let_questions = [random.choice(anti_array, replace=False) for x in range(3)]
            elif pick == "one_in":
                let_questions = [random.choice(anti_array, replace=False) for x in range(2)]
                let_questions.append(random.choice(array, replace=False))
                random.shuffle(let_questions)
            elif pick == "two_in":
                let_questions = [random.choice(array, replace=False) for x in range(2)]
                let_questions.append(random.choice(anti_array, replace=False))
                random.shuffle(let_questions)

            let_questions_list.append(let_questions)

        return let_questions_list


    def mk_ewm_sheet(self, block_num_list, focus_times, let_arrays, imgs,
                      let_questions):

        trial_sheet_dir = "../benchmark_tasks/trial_sheets/"
        f_name = "ewm_trials.csv"

        data_frame = {"block": block_num_list,
                      "focus_time": focus_times,
                      "display_img_time": [(random.randint(40, 60) / 10) for x in focus_times],
                      "display_array_time": [(random.randint(40, 80) / 10) for x in focus_times],
                      "display_array": let_arrays,
                      "display_img": imgs,
                      "q_1": [i[0] for i in let_questions],
                      "q_2": [i[1] for i in let_questions],
                      "q_3": [i[2] for i in let_questions],
                     }

        df = pd.DataFrame(data=data_frame)
        df.to_csv(f"{trial_sheet_dir}{f_name}", index=False)

## Emo Stroop Specific ---------------------------------------------------------

    def gen_word_colors(self):

        cols = ["r", "g", "b"]

        col_list = [random.choice(cols) for x in range(self.num_blocks * self.num_trials)]
        return col_list


    def gen_es_word_list(self):

        words = ['Break', 'Shoe', 'Medevac', 'Filthy', 'Concrete', 'Millionaire',
                 'Reset', 'Prod', 'Fields', 'Bodybags', 'Friendship', 'Ambush',
                 'Push', 'Shoot', 'Mix', 'Happy', 'Sniper', 'Sunk', 'Love',
                 'Tuck', 'Punch', 'Sequence', 'Button', 'Firefight', 'Olive',
                 'Cut', 'IED', 'Germs', 'Dirty', 'Patience', 'Number',
                 'Looking', 'Hatred', 'Input', 'Similar', 'Pleasant',
                 'Loyal', 'Dishes', 'Brush', 'Calm']

        trial_wrds = []
        for n in range(self.num_blocks):
            block_wrds = []
            for x in range(self.num_trials):
                sel_wrd = random.choice(words, replace=False)
                block_wrds.append(sel_wrd)
            trial_wrds.append(block_wrds)

        # Flatten List
        trial_wrds = [item for sublist in trial_wrds for item in sublist]
        return trial_wrds


    def mk_es_sheet(self, block_num_list, focus_times, display_items,
                    word_colors):

        trial_sheet_dir = "../benchmark_tasks/trial_sheets/"
        f_name = "es_trials.csv"

        data_frame = {"block": block_num_list,
                      "focus_time": focus_times,
                      "display_item": display_items,
                      "word_color": word_colors,
                     }

        df = pd.DataFrame(data=data_frame)
        df.to_csv(f"{trial_sheet_dir}{f_name}", index=False)

## Rt specific -----------------------------------------------------------------

    def mk_rt_sheet(self):
        pass

## Non Specific ----------------------------------------------------------------

    def make_block_num_list(self):

        block_list = []
        for x in range(self.num_blocks):
            for z in range(self.num_trials):
                block_list.append(x)

        return block_list


    def gen_focus_times(self):

        focus_times = random.randint(self.focus_min, self.focus_max, size=(self.num_blocks * self.num_trials))
        focus_times = [(ftime / 10) for ftime in focus_times]
        return focus_times








tsc = TrialSheetCreator()
