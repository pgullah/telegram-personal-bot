WHITELIST_IDS = ['50770706']

def AdminOnly(func):
    def wrapper(*args, **kwargs):
        chat_id = args[0].effective_chat.id
        if str(chat_id) in WHITELIST_IDS:
           return func(*args, **kwargs)
        else:
           print("{} is not entitled to access the resource: '{}' ".format(chat_id, func.__name__))
           return None

    return wrapper