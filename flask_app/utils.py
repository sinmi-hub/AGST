# Tnis is simply a utility file.


from datetime import datetime

# returns the current date and time in string format. Simply get the current date and time, convert to string, and then cut out the nanoseconds. Lowest unit of time return in str representation is seconds
def curr_datetime_str() -> str:
    return datetime.now().strftime("(%A), %B %d, %Y at %H:%M:%S")

def curr_datetime()->datetime:
    return datetime.utcnow().replace(microsecond=0)
   
   
#============= TESTING ============================
# print(curr_datetime_str())
# print(curr_datetime())
# print(type(curr_datetime()))