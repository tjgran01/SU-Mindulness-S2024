import csv

def generate_subj_ids(id_prefixes):

    ids = []
    for prfx in id_prefixes:
        ids.extend([f"{prfx}{x + 1}" if len(f"{prfx}{x + 1}") == 4 else f"{prfx}0{x + 1}" for x in range(99)])
    return ids

def main(id_prefixes=[10, 20]):
    
    subj_ids = generate_subj_ids(id_prefixes)

    sessions = ["1", "2"]
    templates = ["1", "2", "3", "4"]
    practice = ["0" for elm in subj_ids]
    ses = [sessions[i % len(sessions)] for i, elm in enumerate(subj_ids)]
    temp = [templates[i % len(templates)] for i, elm in enumerate(subj_ids)]

    with open ("out.csv", "w", newline='') as out_fp:
        writer = csv.writer(out_fp, delimiter=",")

        writer.writerow(["subject_id", "session_num", "template", "test"])

        for i, elm in enumerate(subj_ids):
            writer.writerow([elm, ses[i], temp[i], "0"])
        
    



if __name__ == "__main__":
    main()