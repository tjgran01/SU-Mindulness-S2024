from psychopy import visual, core, event
import pandas as pd
import os
# My imports
from taskpresenter import TaskPresenter

def run_trial(tp, trials, rt_data, block):
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

            if block == 0:
                prac = "Yes"
            else:
                prac = "No"

            focus_time = int(trial[1]["focus_time"])
            tp.draw_focus(focus_time)

            # Too Early
            if event.getKeys(keyList="space"):
                rt_data.append([i + 1, -1, "Incorrect", prac, trial[1]["block"]])
                if trial[1]["block"] == 0:
                    tp.send_mark("too_early")
                    tp.show_performance(False, too_early=True)
                continue
                tp.send_mark("trial_start")

            # Draw Stim
            stim = visual.TextStim(tp.win, text="X")
            stim.draw()
            tp.win.flip()
            timer = core.Clock()

            # Wait for response.
            while timer.getTime() < 5:
                if event.getKeys(keyList="space"):
                    tp.send_mark("resp_cor")
                    rt_data.append([i + 1, timer.getTime() * 1000, "Correct",
                                    prac, trial[1]["block"]])
                    if trial[1]["block"] == 0:
                        tp.show_performance(True)
                    break
            if timer.getTime() >= 5:
                tp.send_mark("resp_incor")
                rt_data.append([i + 1, 1, "Incorrect", prac, trial[1]["block"]])
                if trial[1]["block"] == 0:
                        tp.show_performance(False)
            timer.reset()

        tp.send_mark("task_end")
    return rt_data


def main(tp=None, templated=False, **kwargs):
    """Runs the participant through the entire cognigive task.
        Args:
            None
        Returns:
            None
    """

    trials = pd.read_csv("./trial_sheets/rt_trials.csv")
    data = []

    # Running the trial file in order.
    tp = TaskPresenter(task="rt")
    tp.show_instructions()
    rt_data = run_trial(tp, trials, rt_data, block=[0])
    tp.give_break(prompt_num="1")
    rt_data = run_trial(tp, trials, rt_data, block=[1])
    tp.give_break(prompt_num="2")
    rt_data = run_trial(tp, trials, rt_data, block=[3])
    tp.give_break(prompt_num="3")
    tp.write_to_csv(rt_data)


if __name__ == "__main__":
    if not os.path.exists("./data/reaction_time/"):
        os.makedirs("./data/reaction_time/")
    main()
