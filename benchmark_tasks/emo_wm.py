from psychopy import visual, core, event
import pandas as pd
import random
import os

from taskpresenter import TaskPresenter


def format_array(tp, let_array):

    poses = [(-0.3, -0.2), (0.0, -0.2), (0.3, -0.2),
             (-0.3, 0.2), (0.0, 0.2), (0.3, 0.2)]

    let_array = [visual.TextStim(tp.win, text=letter, pos=poses[indx], height=0.4)
                 for indx, letter in enumerate(let_array)]
    return let_array


def run_trial(tp, trials, data, block):

    # If application is randomly selecting subset of trails,
    # rather than running through the trials directly.
    img_dir = "./trial_sheets/stims/oasis/images/"

    if tp.rand_select:
        trials = tp.select_trials(trials, block)
    if tp.marking:
        tp.send_mark("task_start")

    for i, trial in enumerate(trials.iterrows()):
        if trial[1]["block"] in block:

            # This will allow the 'prac' col to be removed from the trial sheets.
            if trial[1]["block"] == 0:
                prac = "Yes"
            else:
                prac = "No"

            display_array_time = trial[1]["display_array_time"]
            display_img_time = trial[1]["display_img_time"]
            let_array = trial[1]["display_array"].upper()
            let_stim_array = format_array(tp, let_array)

            # Draw Focus
            focus_time = int(trial[1]["focus_time"])
            tp.draw_focus(focus_time)

            # Show array
            for let_stim in let_stim_array:
                let_stim.draw()
            tp.win.flip()
            core.wait(display_array_time)

            # Show picture
            img_stim = f"{img_dir}{trial[1]['display_img']}"
            disp = visual.ImageStim(tp.win, image=img_stim)
            disp.draw()
            tp.win.flip()
            core.wait(display_img_time)

            # Display Prompt:
            for letter in [trial[1]["q_1"], trial[1]["q_2"], trial[1]["q_3"]]:
                if tp.marking:
                    tp.send_mark("trial_start")

                prompt_text = f"Was: {letter.upper()} \n in the array?"
                prompt = visual.TextStim(tp.win,
                                         text=prompt_text)
                prompt.draw()
                tp.win.flip()
                timer = core.Clock()
                while timer.getTime() < 3: # Should there be a variable disp_time?
                    # Enter a response of 'Right'
                    if event.getKeys(keyList="right"):
                        # True Positive Response.
                        if letter.upper() in let_array:
                            # should make this a method of TP.
                            if tp.marking:
                                tp.send_mark("resp_cor")
                            data.append([i + 1, timer.getTime() * 1000, "Correct",
                                        "True Positive", "True Postive",
                                        prac, trial[1]["block"]])
                            if trial[1]["block"] == 0:
                                tp.show_performance(True)
                            break
                        # False Positive Response.
                        else:
                            if tp.marking:
                                tp.send_mark("resp_incor")
                            data.append([i + 1, timer.getTime() * 1000, "Incorrect",
                                        "True Negative", "False Positive",
                                        prac, trial[1]["block"]])
                            if trial[1]["block"] == 0:
                                tp.show_performance(False)
                            break
                    # Enter a response of 'Left'
                    if event.getKeys(keyList="left"):
                        # True Negative Response
                        if letter.upper() not in let_array:
                            if tp.marking:
                                tp.send_mark("resp_cor")
                            data.append([i + 1, timer.getTime() * 1000, "Correct",
                                        "True Negative", "True Negative",
                                        prac, trial[1]["block"]])
                            if trial[1]["block"] == 0:
                                tp.show_performance(True)
                            break
                        # False Negative Response.
                        else:
                            if tp.marking:
                                tp.send_mark("resp_incor")
                            data.append([i + 1, timer.getTime() * 1000, "Incorrect",
                                        "True Positive", "False Negative",
                                        prac, trial[1]["block"]])
                            if trial[1]["block"] == 0:
                                tp.show_performance(False)
                            break

                if timer.getTime() > 3:
                    data.append([i + 1, 1, "Incorrect", "None", "Lapse",
                                prac, trial[1]["block"]])
                    if trial[1]["block"] == 0:
                        tp.show_performance(False)

                timer.reset()
    if tp.marking:
        tp.send_mark("task_end")
    return(data)

def main(tp=None, templated=False, **kwargs):
    """Runs the participant through the entire cognigive task.
        Args:
            None
        Returns:
            None
    """
    trials = pd.read_csv("./trial_sheets/emo_working_memory_trials.csv")
    data = []

    tp = TaskPresenter(task="ewm")
    tp.show_instructions()
    data = run_trial(tp, trials, data, block=[0])
    tp.give_break(prompt_num=1)
    data = run_trial(tp, trials, data, block=[1, 2])
    tp.give_break(prompt_num=2)
    data = run_trial(tp, trials, data, block=[3, 4])
    tp.give_break(prompt_num=3)
    tp.write_to_csv(data)

if __name__ == "__main__":
    if not os.path.exists("./data/emo_working_memory/"):
        os.makedirs("./data/emo_working_memory/")
    main()
