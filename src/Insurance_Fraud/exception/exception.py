import sys
sys.path.append('C:\\Users\\Arpit Kadam\\Desktop\\Insurance-Fraud-Detection\\src')
from Insurance_Fraud.logger.logger import logger

class NetworkSecurityException(Exception):
    def __init__(self, error_message: str, error_details: sys):
        super().__init__(error_message)
        self.error_message = error_message
        self.error_details = error_details
        _, _, exc_tb = error_details.exc_info()     
        self.lineno = exc_tb.tb_lineno
        self.filename = exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return (
            f"Error occurred in file: {self.filename} at line number: {self.lineno} "
            f"with error message: {self.error_message}"
        )

##testing
'''if __name__ == "__main__":
    try:
        a = 1/0
    except Exception as e:
        logger.info("Divide by zero")
        raise NetworkSecurityException(e, sys)
        '''