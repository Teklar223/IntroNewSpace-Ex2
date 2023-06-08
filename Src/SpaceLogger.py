from Src.Configuration import Configuration
import os, csv, time
from Src.Constants import c_is_player

class Logger():

    def __init__(self) -> None:
        timestr = time.strftime("%Y-%m-%d-%H-%M-%S")
        self.filename = f"log_{timestr}_.csv"

    def log_csv(self, configs: list, path: str = None, filename = None, active = True, full_path=None) -> None:
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

        if full_path is not None:
            log_path = full_path

        # Check if the log file already exists
        file_exists = os.path.isfile(log_path)

        # Specify the attributes to include in the log entry
        attributes = [key for (key,_) in configs[0].__dict__.items()]
        attributes.remove(c_is_player)

        # Open the log file in append mode and write the log entry
        with open(log_path, "a", newline="") as log_file:
            writer = csv.DictWriter(log_file, fieldnames=attributes)

            # Write the header row if the file is newly created
            if not file_exists:
                writer.writeheader()

            # Extract the attribute values and write the log entry
            for config in configs:
                log_entry = {attr: getattr(config, attr) for attr in attributes}
                writer.writerow(log_entry)

        # Print the log entry for testing purposes
        # print(log_entry)

    def read_csv(self, filename, desired_attributes):
        '''
            returns a list of dictionaries containing the desired attributes, order is dictated by the lines of the csv file
        '''
        parsed_data = []

        with open(filename, "r", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            
            for row in reader:
                parsed_entry = {}
                
                for attr in desired_attributes:
                    if attr in reader.fieldnames:
                        parsed_entry[attr] = row[attr]
                
                parsed_data.append(parsed_entry)
        
        return parsed_data
