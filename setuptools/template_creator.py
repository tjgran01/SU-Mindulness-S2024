import pandas as pd
import os

class TemplateCreator():
    def __init__(self, experiment_name="sampleExperiment", n_templates=4,
                 included_tasks=["rt", "cr"], practice_tasks=True,
                 rest_pattern="alternating"):

        self.experiment_name = experiment_name
        self.n_templates = n_templates
        self.included_tasks = included_tasks
        self.practice_task = practice_tasks
        self.rest_pattern = rest_pattern

        print("Hello")
