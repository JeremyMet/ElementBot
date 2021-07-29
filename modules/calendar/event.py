from modules.calendar.event_type import event_type;

class event(object):

    def __init__(self, type, datetime, event_str):
        self.type = type;
        self.datetime = datetime;
        self.event_str = event_str;

    def __str__(self, separator = " @ "):
        ret = "\""+self.event_str+"\""+separator ;
        if self.datetime.minute < 10:
            time = str(self.datetime.hour)+":0"+str(self.datetime.minute);
        else:
            time = str(self.datetime.hour)+":"+str(self.datetime.minute);
        if self.type == event_type.T:
            ret += time ;
        elif self.type == event_type.DT:
            ret += str(self.datetime.day)+"T"+time;
        elif self.type == event_type.MDT:
            ret += str(self.datetime.month)+"-"+str(self.datetime.day)+"T"+time;
        elif self.type == event_type.YMDT:
            ret += str(self.datetime.year)+"-"+str(self.datetime.month)+"-"+str(self.datetime.day)+"T"+time;
        # return ret;
        return "\""+self.event_str+"\""+separator+str(self.datetime);
