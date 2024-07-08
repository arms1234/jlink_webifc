#Helper function which checkes if exists the key  returns 
#the value of key othervise returns empty character.

def get_value(var,key,val):
    if var.has_key(key):
        return var[key][val]
    else:
        return ''

