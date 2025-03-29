import sys
import logging

def create_error_message(error: Exception, error_detail:sys) -> str:
    """
    Basically this function is going to extract the error message from the exception object, and the loc where 
    the error has occurred.
    
    :param error: The exception that occurred.  
    :param error_detail: The sys module to access traceback details.
    :return: A formatted error message string.
    
    """
    
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number_of_error = exc_tb.tb_lineno
    error_message = f"Error has taken place in the python script: [{file_name}] at line number : [{line_number_of_error}]: str{error}"

    logging.error(error_message)
    return error_message


class MyException(Exception):
    def __init__(self, error_message: str, error_deatils: sys):
        
        """
        Basically this function is going to extract the error message from the exception object, and the loc where 
        the error has occurred.
        
        :param error_message: The error message.
        :param error_detail: The sys module to access traceback details.
        """
        
        super().__init__(error_message)
        self.error_message = create_error_message(error_message, error_deatils)
        
    def __str__(self) -> str:
        return self.error_message