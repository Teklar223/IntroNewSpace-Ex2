from Src.Configuration import Configuration
import os, csv, time
from Src.Constants import c_is_player

class Logger():

    def __init__(self) -> None:
        timestr = time.strftime("%Y-%m-%d-%H-%M-%S")
        self.filename = f"log_{timestr}_.csv"

    def log_csv(self, config: Configuration, path: str = None, filename = None, active = True) -> None:
        if not active: 
            return
        
        # Get the current working directory if no path is provided
        if not path:
            path = os.path.join(os.getcwd(), "Logs")
            os.makedirs(path, exist_ok=True)

        # Define the filename for the log file
        
        if not filename:
            filename = self.filename

        # Create the full path for the log file
        log_path = os.path.join(path, filename)

        # Check if the log file already exists
        file_exists = os.path.isfile(log_path)

        # Specify the attributes to include in the log entry
        attributes = [key for (key,_) in config.__dict__.items()]
        attributes.remove(c_is_player)

        # Open the log file in append mode and write the log entry
        with open(log_path, "a", newline="") as log_file:
            writer = csv.DictWriter(log_file, fieldnames=attributes)

            # Write the header row if the file is newly created
            if not file_exists:
                writer.writeheader()

            # Extract the attribute values and write the log entry
            log_entry = {attr: getattr(config, attr) for attr in attributes}
            writer.writerow(log_entry)

        # Print the log entry for testing purposes
        print(log_entry)

    def read_csv(self, desired_attributes):
        parsed_data = []

        with open(self.file_path, "r", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            
            for row in reader:
                parsed_entry = {}
                
                for attr in desired_attributes:
                    if attr in reader.fieldnames:
                        parsed_entry[attr] = row[attr]
                
                parsed_data.append(parsed_entry)
        
        return parsed_data
