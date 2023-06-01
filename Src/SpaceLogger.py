from Src.Configuration import Configuration
import os
import csv

class Logger():

    def __init__(self) -> None:
        pass

    def log(self, config: Configuration, path: str = None,  filename: str= None) -> None:
        # Create a log entry based on the configuration object
        log_entry = [
            config.time,
            config.alt,
            config.fuel
            # Add more attributes here as needed
        ]

        # Get the current working directory if no path is provided
        if not path:
            path = os.getcwd()
        if not filename:
            filename = "game_log.csv"

        # Define the filename for the log file

        # Create the full path for the log file
        log_path = os.path.join(path, filename)

        # Check if the log file already exists
        file_exists = os.path.isfile(log_path)

        # Open the log file in append mode and write the log entry
        with open(log_path, "a", newline="") as log_file:
            writer = csv.writer(log_file)

            # Write the header row if the file is newly created
            if not file_exists:
                header = ["Time", "Altitude", "Fuel"]
                writer.writerow(header)

            # Write the log entry
            writer.writerow(log_entry)

        # Print the log entry for testing purposes
        print(log_entry)