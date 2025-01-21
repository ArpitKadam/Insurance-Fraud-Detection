import os
import os
import sys
import logging
from datetime import datetime

# Define the logging format
logging_str = "[%(asctime)s: %(levelname)s: %(module)s: %(message)s]"

# Define the directory where log files will be saved
log_dir = "logs"

# Create a unique log file name based on current timestamp
log_filepath = os.path.join(log_dir, f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.log")

# Create the log directory if it doesn't exist
os.makedirs(log_dir, exist_ok=True)

# Set up logging
logging.basicConfig(
    level=logging.INFO,  # This ensures INFO and ERROR are captured
    format=logging_str,
    handlers=[
        logging.FileHandler(log_filepath),  # Save logs to a file
        logging.StreamHandler(sys.stdout)    # Print logs to the console
    ]
)

# Get the logger instance
logger = logging.getLogger("InsuranceFraudDetectionLogger")


