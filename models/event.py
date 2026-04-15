from datetime import datetime, date
import urllib.parse


class Event: 
    def __init__(self, name, startTime, endTime, description, location, perks, flyer_img, eventType, id=None): 
        self.id = id
        self.name = name 
        self.endTime = endTime
        self.startTime = startTime
        self.description = description
        self.location = location
        self.perks = perks
        self.flyer_img = flyer_img
        self.eventType = eventType
        self.raw_end = None
        self.raw_start = None
    
    def __getinfo__(self):
        return f"Event: {self.name}\nStarts: {self.startTime}\nEnds: {self.endTime}\nLocation: {self.location}\nDescription: {self.description}\nPerks: {', '.join(self.perks)}\nType: {self.eventType}"
    def get_calendar_link(self):
        start = self.raw_start.replace("-", "").replace(":", "").split("+")[0]
        end = self.raw_end.replace("-", "").replace(":", "").split("+")[0]
        
        base_url = "https://www.google.com/calendar/render?action=TEMPLATE"
        params = {
            "text": self.name,
            "dates": f"{start}/{end}",
            "details": self.description,
            "location": self.location,
            "sf": "true",
            "output": "xml"
        }
        return base_url + "&" + urllib.parse.urlencode(params)

class TechnicalWorkshop(Event):
    def __init__(self, name, startTime, endTime, description, location, topic, level, perks, flyer_img, id=None):
        super().__init__(name, startTime, endTime, description, location, perks, flyer_img, "Technical Workshop", id=id)
        self.topic = topic
        self.level = level

class SocialEvent(Event):
    def __init__(self, name, startTime, endTime, description, location, theme, perks, flyer_img, id=None):
        super().__init__(name, startTime, endTime, description, location, perks, flyer_img, "Social Event", id=id)
        self.theme = theme

class Conference(Event):
    def __init__(self, name, startTime, endTime, description, location, perks, flyer_img, volunteers, id=None):
        super().__init__(name, startTime, endTime, description, location, perks, flyer_img, "Conference", id=id)
        self.volunteers = volunteers

class ProfessionalNetwork(Event):
    def __init__(self, name, startTime, endTime, description, location, industry, perks, flyer_img, speaker, id=None):
        super().__init__(name, startTime, endTime, description, location, perks, flyer_img, "Professional and Network", id=id)
        self.industry = industry
        self.speaker = speaker


