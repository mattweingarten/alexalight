import datetime

def from_string_to_time(string):
    arr = str(string).split(':',2)
    print arr
    return datetime.time(int(arr[0]),int(arr[1]))


def day_of_week(string):
    string = str(string)
    if string == "Monday":
        return 1
    elif string == "Tuesday":
        return 2
    elif string == "Wednesday":
        return 3
    elif string == "Thursday":
        return 4
    elif string == "Friday":
        return 5
    elif string == "Saturday":
        return 6
    elif string == "Sunday":
        return 7
