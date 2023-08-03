# pyright: strict

import os
import re
from typing import Any, List, cast

def find_handler(handler_map: dict[str, Any], content: str, ):
    for pattern, handler in handler_map.items():
        if re.match(pattern, content, flags=re.IGNORECASE):
            return handler
    
    return None


def _is_empty(input: Any):
    if input:
        if type(input) == str and input.isspace():
            return True
        elif type(input) == list and len(cast(List[Any], input,)) == 0:
            return True
        else:
            return False
    
    return True


def default_if_empty(input:Any, default: Any):
    return input if not _is_empty(input) else default

def get_env_config(key: str, ini_fallback:(str|None)=None, section:str ='Default') -> (str|None):
    if key in os.environ:
        print("Using token from environment")
        return os.environ[key]
    else:
        if ini_fallback:
            import configparser
            config = configparser.ConfigParser()
            config.read(os.path.expanduser('~/.data/.private/app-secrets/telegram/tokens.ini'))
            return config.get(section, key)
        else:
            print("No ini_fallback provided")
            return None