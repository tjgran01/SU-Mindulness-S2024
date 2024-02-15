from pylsl import StreamInfo, StreamOutlet
import time


class LSLSEventStreamer(object):
    def __init__(self, participant_id):
        self.log_delim = "\t"
        self.log_dir = "./data/event_logs/"
        self.out_file = f"{participant_id}_EVENT_LOG.txt"
        self.info = StreamInfo('MindfulnessExperimentalMarks', 'Markers', 1, 0, 'string', str(participant_id))
        self.out = StreamOutlet(self.info)

        self.log_headers = ["timestamp", "event_type", "event_data", "\n"]
        self.create_log()


    def create_log(self):

        with open (f"{self.log_dir}{self.out_file}", "w") as out_f:
            out_f.write(f"{self.log_delim}".join(self.log_headers))
            out_f.write(f"{self.log_delim}".join([str(time.time()), "SYSTEM", "LSL Streamer / Logger Initalized.", "\n"]))


    def log_event(self, etype, taskname):

        event_dict = {"BLOCK_START": f"Task block {taskname} has begun.",
                      "STIM_DISPLAYED": "Stimulus was displayed to the participant.",
                      "CORRECT_RESPONSE": "Participant responded correctly to the stimulus.",
                      "INCORRECT_RESPONSE": "Participant responded incorrectly to the stimulus",
                      "TOO_EARLY": "Participant responded before stimulus was displayed.",
                      "BLOCK_END": f"Task block {taskname} has completed.",
                      "REST_START": "A controlled rest has begun.",
                      "REST_END": "A controlled rest has finished.",
                      "PAGE_TURN": "Participant turned an instruction page."}

        with open (f"{self.log_dir}{self.out_file}", "a") as out_f:
            out_f.write(f"{self.log_delim}".join([str(time.time()), etype, event_dict[etype], "\n"]))
            

    def send_event(self, etype, taskname):
        
        self.out.push_sample([etype])
        self.log_event(etype, taskname)


if __name__ == "__main__":
    streamer = LSLSEventStreamer(1234)
    while True:
        time.sleep(1)
        streamer.send_event("STIM", "controlled_rest")
