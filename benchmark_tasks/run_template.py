import pandas as pd
import sys
from sys import platform

from taskpresenter import TaskPresenter
from psychopy import gui


def get_dialogue_data(err="None"):

    first_dialogue = gui.Dlg(title="Mindfuless Experiment")
    first_dialogue.addField('Is this a practice session?', True)

    first_dialogue.addField('Is this a dev session?', False)

    practice = first_dialogue.show()
    
    if practice[0]:
        return ["1234", 1, "Control"]
    if practice[1]:
        return ["9876", 1, "Control"]

    myDlg = gui.Dlg(title="Mindfulness experiment")

    if err == "None":
        myDlg.addText(f'Error with previous entry (try again): {err}')

    myDlg.addText('Subject info')
    myDlg.addField('Participant ID:', '1234')

    myDlg.addText('Experiment Info')
    myDlg.addField('Session Number:', 0)
    myDlg.addField('Group:', choices=["Treatment", "Control"])
    ok_data = myDlg.show()  # show dialog and wait for OK or Cancel
    if myDlg.OK:  # or if ok_data is not None
        print(ok_data)
    else:
        print('user cancelled')
        sys.exit()

    return ok_data


def check_platform():

    if platform == "linux" or platform == "linux2":
        return "ln"
    elif platform == "darwin":
        return "osx"
    elif platform == "win32":
        print("Hello")
        return "win"


def check_cmd_line_session_info(sub_id, session_num):
    """Checks for validity of command line arguements passed to the
    program.
    Args:
        sub_id(str): the 4-digit subject id.
    Returns:
        None.
    Raises: 'ValueError'"""

    if len(sub_id) == 4 and sub_id.isdigit():
        if len(session_num) == 1 and session_num.isdigit():
            return True
        raise ValueError(f"session_num: {session_num} invalid."
                         " (1 - 9 are valid sessions.)")
        sys.exit()
    raise ValueError(f"Sub_ID: {sub_id} invalid. (9999 > Four Digits < 1000)")
    sys.exit()


def get_task_template(sub_id, session_num, exper_tmp_file_name):
    """Finds task template for session for all of the subjects in mindfulness study
    particiular study.
    Args:
        sub_id(str): The subject """

    f_path = f"./templates/exper_temps/{exper_tmp_file_name}"

    table = pd.read_csv(f_path)
    print(table)
    table = table[(table["subject_id"] == int(sub_id))
                  & (table["session_num"] == int(session_num))]
    print(table)
    try:
        return(int(table["template"]))
    except:
        raise ValueError(f"Session {session_num} not found for Subject: "
                         f"{sub_id}")
        sys.exit()


def main(sub_id, session_num, marking, exper_tmp_file_name="mindfulness.csv"):
    """Locates experiment and partcipant template file - feeds the list of
    tasks to be presented to a TaskPresenter() object.
    Args:
        sub_id(str): subject's participant ID number (four digits).
        session_num(str): subject's session number (one digit).
        marking(bool): whether or not the physiological data will be marked.
        exper_tmp_file_name(string): the name of the experiment template file.
    Returns:
        None
    """

    platform = check_platform()
    check_cmd_line_session_info(sub_id, session_num)
    temp_num = get_task_template(sub_id, session_num, exper_tmp_file_name)
    print(temp_num)

    try:
        ### Remove Zero When Done Testing
        template_file = pd.read_csv(f"./templates/{exper_tmp_file_name[:-4]}"
                                    f"/{exper_tmp_file_name[:-4]}{temp_num}.csv")
    except FileNotFoundError as e:
        print(e)
        print(f"Either the file ./templates/mndful_template{temp_num}.csv"
              " could not be located, or you did not enter the promper template"
              " number.")
        sys.exit()

    task_list = template_file["task"].tolist()
    block_list = template_file["block"].tolist()

    if platform == "ln" or "win":
        fullscreen = True
    else:
        fullscreen = False


    tp = TaskPresenter(task_list=task_list, block_list=block_list,
                       templated=True, sub_id=sub_id,
                       session_num=session_num, marking=marking,
                       fullscr=fullscreen)


if __name__ == "__main__":

    err = "None"
    while True:
        ok_data = get_dialogue_data(err=err)
        if ok_data:
            break

        
    main(ok_data[0], str(ok_data[1]), "no")