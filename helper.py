import datetime

def from_string_to_time(string):
    arr = str(string).split(':',2)
    print arr
    return datetime.time(int(arr[0]),int(arr[1]))
