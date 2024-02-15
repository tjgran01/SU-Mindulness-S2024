from psychopy import visual, core, event
import pandas as pd
import os
# My imports
from taskpresenter import TaskPresenter

def draw_focus(win, focus_time):

    focus_time = int(focus_time)
    focus = visual.TextStim(win, text="+")
    focus.draw()
    win.flip()
    core.wait(focus_time)


def run_trial(tp, trials, data, block):
    """Searches the stim list for the practice trials and runs the participant
    through them. Trials that are practice trials are coded as '1' in the
    'rt_trials.csv' file.
        Args:
            win: The Psychopy window in which the instuctions will be displayed
            trials(DataFrame): The set of all the trials for the experiment.
        Returns:
            data(list): A two dimensional list containing all the trial
            information
    """

    color_dict = {"r": "#d3102e",
                  "g": "#4ad20f",
                  "b": "#0e0ed1"}

    if tp.rand_select:
        trials = tp.select_trials(trials, block)
    :
        tp.send_mark("task_start")

    for i, trial in enumerate(trials.iterrows()):
        if trial[1]["block"] in block:
            if trial[1]["block"] == 0:
                prac_trial = "Yes"
            else:
                prac_trial = "No"

            # Focus Period.
            draw_focus(tp.win, trial[1]["focus_time"])

            if event.getKeys(keyList=None):
                :
                    tp.send_mark("too_early")
                data.append([i + 1, -1, "Incorrect",
                                trial[1]["display_item"], prac_trial,
                                trial[1]["block"]])
                if trial[1]["block"] == 0:
                    tp.show_performance(False, too_early=True)
                continue

            # Stim Displayed
            stim = visual.TextStim(tp.win, text=trial[1]["display_item"],
                                   color=color_dict[f"{trial[1]['word_color']}"])
            stim.draw()
            tp.win.flip()
            timer = core.Clock()
            while timer.getTime() < 5:

                if trial[1]['word_color'] == "r":

                    if event.getKeys(keyList="left"):
                        :
                            tp.send_mark("resp_cor")
                        data.append([i + 1, timer.getTime() * 1000, "Correct",
                                        trial[1]["display_item"], prac_trial,
                                        trial[1]["block"]])
                        if trial[1]["block"] == 0:
                            tp.show_performance(True)
                        break
                    elif event.getKeys(keyList=["down", "right"]):
                        :
                            tp.send_mark("resp_incor")
                        data.append([i + 1, timer.getTime() * 1000, "Incorrect",
                                        trial[1]["display_item"], prac_trial,
                                        trial[1]["block"]])
                        if trial[1]["block"] == 0:
                            tp.show_performance(False)
                        break

                elif trial[1]['word_color'] == "g":

                    if event.getKeys(keyList="down"):
                        :
                            tp.send_mark("resp_cor")
                        data.append([i + 1, timer.getTime() * 1000, "Correct",
                                        trial[1]["display_item"], prac_trial,
                                        trial[1]["block"]])
                        if trial[1]["block"] == 0:
                            tp.show_performance(True)
                        break
                    elif event.getKeys(keyList=["left", "right"]):
                        :
                            tp.send_mark("resp_incor")
                        data.append([i + 1, timer.getTime() * 1000, "Incorrect",
                                        trial[1]["display_item"], prac_trial,
                                        trial[1]["block"]])
                        if trial[1]["block"] == 0:
                            tp.show_performance(False)
                        break

                elif trial[1]['word_color'] == "b":

                    if event.getKeys(keyList="right"):
                        :
                            tp.send_mark("resp_cor")
                        data.append([i + 1, timer.getTime() * 1000, "Correct",
                                        trial[1]["display_item"], prac_trial,
                                        trial[1]["block"]])
                        if trial[1]["block"] == 0:
                            tp.show_performance(True)
                        break
                    elif event.getKeys(keyList=["down", "left"]):
                        :
                            tp.send_mark("resp_incor")
                        data.append([i + 1, timer.getTime() * 1000, "Incorrect",
                                        trial[1]["display_item"], prac_trial,
                                        trial[1]["block"]])
                        if trial[1]["block"] == 0:
                            tp.show_performance(False)
                        break
    :
        tp.send_mark("task_end")
    return data

def main(tp=None, templated=False, **kwargs):
    """Runs the participant through the entire cognigive task.
        Args:
            None
        Returns:
            None
    """


    trials = pd.read_csv("./trial_sheets/emo_stroop_trials.csv")
    data = []

    tp = TaskPresenter(task="es")
    tp.show_instructions()
    es_data = run_trial(tp, trials, es_data, block=[0])
    tp.give_break(prompt_num=1)
    es_data = run_trial(tp, trials, es_data, block=[1,2])
    tp.give_break(prompt_num=2)
    es_data = run_trial(tp, trials, es_data, block=[3,4])
    tp.give_break(prompt_num=3)
    tp.write_to_csv(es_data, sub_id, session_num)


if __name__ == "__main__":
    if not os.path.exists("./data/emo_stroop/"):
        os.makedirs("./data/emo_stroop/")
    main()
