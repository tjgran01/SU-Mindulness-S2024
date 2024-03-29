from psychopy import visual, core, event
import pandas as pd
import os

from taskpresenter import TaskPresenter

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

    if tp.rand_select:
        trials = tp.select_trials(trials, block)

    tp.send_mark("task_start")

    for i, trial in enumerate(trials.iterrows()):
        if trial[1]["block"] in block:
            if trial[1]["block"] == 0:
                prac_trial = "Yes"
            else:
                prac_trial = "No"
            # focus period
            focus_time = int(trial[1]["focus_time"])
            tp.draw_focus(focus_time)

            # if participant goes to early.
            if event.getKeys(keyList="space"):
                tp.send_mark("too_early")
                data.append([i + 1, -1, "Incorrect",
                            trial[1]["display_item"], prac_trial, trial[1]["block"]])
                if trial[1]["block"] == 0:
                    tp.show_performance(False, too_early=True)
                continue

            # stim displayed
            if trial[1]["display_item"] == "Go":
                stim = visual.Rect(tp.win, width=.5, height=.5, fillColor=[191 / 255, 23 / 255, 37 / 255],
                                   lineColor=[204 / 255, 57 / 255, 69 / 255])
            elif trial[1]["display_item"] == "No":
                stim = visual.Circle(tp.win, radius=0.5, edges=32, fillColor=[23 / 255, 37 / 255, 191 / 255],
                                     lineColor=[23 / 255, 37 / 255, 191 / 255])
            stim.draw()
            tp.win.flip()
            timer = core.Clock()
            tp.send_mark("trial_start")
            while timer.getTime() < 2:

                if event.getKeys(keyList="space"):
                    if trial[1]["display_item"] == "Go":
                        tp.send_mark("resp_cor")
                        data.append([i + 1, timer.getTime() * 1000, "Correct",
                                    trial[1]["display_item"], prac_trial, trial[1]["block"]])
                        if trial[1]["block"] == 0:
                            tp.show_performance(True)
                        break
                    elif trial[1]["display_item"] == "No":
                        tp.send_mark("resp_incor")
                        data.append([i + 1, timer.getTime() * 1000, "Incorrect",
                                    trial[1]["display_item"], prac_trial, trial[1]["block"]])
                        if trial[1]["block"] == 0:
                            tp.show_performance(False)
                        break
                    print(trial[1]["display_item"])

            if timer.getTime() >= 2 and trial[1]["display_item"] == "Go":
                tp.send_mark("resp_incor")
                data.append([i + 1, 1, "Incorrect",
                            trial[1]["display_item"], prac_trial, trial[1]["block"]])
                if trial[1]["block"] == 0:
                    tp.show_performance(False)
            if timer.getTime() >= 2 and trial[1]["display_item"] == "No":
                tp.send_mark("resp_cor")
                data.append([i + 1, 0, "Correct",
                            trial[1]["display_item"], prac_trial, trial[1]["block"]])
                if trial[1]["block"] == 0:
                    tp.show_performance(True)
            timer.reset()

    tp.send_mark("task_end")
    return data


def main(tp=None, templated=False, **kwargs):
    """Runs the participant through the entire cognigive task.
        Args:
            None
        Returns:
            None
    """

    trials = pd.read_csv("./trial_sheets/go_no_go_trials.csv")
    gng_data = []

    tp = TaskPresenter(task="gng")
    tp.show_instructions()
    gng_data = run_trial(tp, trials, gng_data, block=[0])
    tp.give_break(prompt_num=1)
    gng_data = run_trial(tp, trials, gng_data, block=[1, 2])
    tp.give_break(prompt_num=2)
    gng_data = run_trial(tp, trials, gng_data, block=[3, 4])
    tp.give_break(prompt_num=3)
    tp.write_to_csv(gng_data)



if __name__ == "__main__":
    if not os.path.exists("./data/go_no_go/"):
        os.makedirs("./data/go_no_go/")
    main()
