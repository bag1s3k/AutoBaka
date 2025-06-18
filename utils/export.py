from config.logging_conf import setup_logging

setup_logging()

def export_results(subjects, path):
    with open(path, "w") as file:
        for subject, marks in subjects.items():
            file.write(f"{subject:30} {marks[-1]["avg"]}\n")