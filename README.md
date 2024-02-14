### Mindfulness Stims:

#### Current Tasks:

| Task  | Abbreviation | Task Description  | Cognitive Resource   |
|---|---|---|---|
|  Controlled Rest | __cr__  | Participant stares blankly at a '+' displayed in the center of the screen and wonders to themselves if the compensation money is worth it.  |  None (Control - Physiological) |
|  Reaction Time | __rt__  | Participant Responds as soon as stimulus is displayed to screen.  |  None (Control - Behavioral) |
| Go No Go  | __gng__  | Participant responds when they see "Go" stimulus, and does NOT respond when they see the "No Go" stimulus | Inhibitory Control  |
| Emotional Stoop  | __es__  | Participants respond to which color (Red, Blue, or Green) a word stimulus was presented in. The words vary in valance / arousal levels. | Emotional Response Inhibition  |
| N - Back | __nb__  | Participants are given an **n** value (1 - 3) and are showed a stream of letter slides on the screen. They are tasked with responding with as to whether or not the letter currently displayed was displayed **n** slides ago. | Working Memory |
| Audio N - Back | __anb__  | Participants are given an **n** value (1 - 3) and are presented a stream of letters via the computer's speakers. They are tasked with responding with as to whether or not the letter most recently spoken was spoken **n** presentations ago. | Working Memory |
| Emotional Working Memory (Delayed Recall) | __ewm__  | Participants are shown an array of letters (len of 3, 6 or 9) and are asked to memorize the letters that appear in the array. The array is then replaced with an image of varying valence and arousal level. After viewing the picture they are asked whether or not a given letter was present in the array. | Emotional Working Memory |

#### Getting Set Up.

__This has not currently fully implimented__

Because experiments (and life) are complicated there are a few scripts that can
help to generate many of the files that are needed in order to create a custom task battery. These tools, and their documentation, can be found in `./setuptools/`.

##### What You'll Need.

###### Experiment Template File.

This is the master file for the whole experiment. It is a look up table so that the rest
of the application knows what to draw from when presenting the tasks. Below is an example
of what a basic experiment template file would look like. For more detailed information see a
working example at: `./benchmark_tasks/templates/exper_temps/mindfulness.csv`. Or look over the
README in `./setuptools/`.

| Subject ID  | Session Number | Template Number |
|--|--|--|
|9999|1|1|
|9999|2|2|
|9998|1|3|
|9998|2|4|
|9997|1|1|
|9997|2|2|

As you can see in the example above each row indicates what template each individual session should pull from. Templates you say? What to you mean templates? Well, I'm glad you asked because the next section is ...

##### Running From A Template File:

Templates are a good way to customize an experiment. A template file is a `.csv` that
passes the application information about what task and what block to run next. They're pretty simple and look similar to the below:

| index | task_type | block |
|-------|-----------|-------|
|1      | cr (Controlled Rest)| 0 |
|2      | rt (Reaction Time)| 0 |
|3      | cr (Controlled Rest)| 0 |
|4      | gng (Go No Go)   | 0 |
|5      | cr | 0 |
|6      | rt | 1 |

And so on.

##### Okay, but where does this stuff go?

Right, okay. Lets assume you named your experiment 'sampleExperiment. Here's what you need.

1. An experiment template file named `sampleExperiment.csv`. This file will be located in `./benchmark_tasks/templates/exper_temps/`.

2. All of the individual templates for the experiment. Say you have four different orders of arranging the tasks, you would therefore need to create 4 templates. Create a directory in the `./benchmark_tasks/templates/` folder with the name of your experiment, e.g.: `sampleExperiment`. And place all of the template files within this folder. Name them like so: `{study_name}{template_number}.csv`. In our example that would be `sampleExperiment1.csv`, `sampleExperiment2`, and so on.


#### Running your template:

To run the template you'll need to run the `run_template.py` file (pretty decent name for it, I'd say). When you run the file, you'll want to pass the subject id, session number, and experiment template file name to the script (this is why we named everything the same darn thing earlier), so that it knows what to run. Do so like this in the command line:

`$ python run_template.py subject_id session_num experiment_template_name`

For our example:

`$ python run_template.py 9999 1 sampleExperiment.csv`


#### Current Methods of Running Tasks:

<strike>Tasks can be run individually</strike> by using an experiment template. Template files should be stored in `./benchmark_tasks/templates/`.

##### Running an Individual Task (Coming soon.):

To run the tasks separately - invoke them from a command line (**only tested in Mac OS and Ubuntu Linux as of 12/18/18**).

`source venv/bin/activate`
`cd benchmark_tasks`
`python rt.py` (run Reaction Time Task).

You will then have to enter a participant ID and session number. Participant IDs are 4 digits long. Session numbers are a single digit. (You're a sadist if you have someone come in for > 9 sessions and the IRB should have your head. The code reflects this sentiment).

Running a task in this way will run the participant through three blocks with two self paced brakes between the them. The first block is a practice block, and will inform the participant as to whether or not they are completing the task correctly.

## Altering Trial Sheets:

Trial sheets at this time should not be messed with (there's no legal penalty, however, no matter how many judges I speak with). I'm not sure **what** exactly I want to do with them. Currently, trial sheets all contain 5 blocks with 40 trials. The application randomly selects 20 of the 40 for each block. If you want to alter the number of trials then dig through the code and find the `n_trials` variable and change it. Change it to a number over 40 if you feel like crashing the application.

__Note: The randomization is not 'random'. The application randomly downsamples to the number of trials and then runs through the returned trials in order. Not a big fix, but something that I'll fix in the refactoring of the codebase. In the meantime I've got bigger fish to fry.__

### Troubleshooting Stuff.

There will be many issues I'm sure, but the ones I'm aware of will be posted below:

#### Why can't I just pip install the world?

I wish I could, but versioning and stuff. I don't know. I went to school for Philosophy.

##### Trouble installing psychopy on Ubuntu:

Most of the trouble I have run into is because Psychopy is trying to use an outdated version of wxPython. Refer to the documentation at: https://wiki.wxpython.org/How%20to%20install%20wxPython#Installing_wxPython-Phoenix_using_pip to figure out the exact issue you are having.

Once you've succsessfully installed wxPython - you should be able to easily `pip install psychopy`.
