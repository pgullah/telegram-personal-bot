
import re

def find_handler(handler_map: dict[str, any], content, ):
    for pattern, handler in handler_map.items():
        if re.match(pattern, content, flags=re.IGNORECASE):
            return handler
    
    return None




def _is_empty(input):
    if input:
        if type(input) == str and input.isspace():
            return True
        elif type(input) == list and len(input) == 0:
            return True
        else:
            return False
    
    return True


def default_if_empty(input, default):
    return input if not _is_empty(input) else default