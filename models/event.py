class Event: 
    def __init__(self, name, startTime, endTime, description, location,perks, flyer_img): 
        self.name = name 
        self.endTime = endTime
        self.startTime = startTime
        self.description = description
        self.location = location
        self.perks = perks
        self.flyer_img = flyer_img
    
    def __getinfo__(self):
        return f"Event: {self.name}\nStarts: {self.startTime}\nEnds: {self.endTime}\nLocation: {self.location}\nDescription: {self.description}\nPerks: {', '.join(self.perks)}"
    
        
 #concrete products: all the possible events       
class TechnicalWorkshop (Event):
    def __init__(self, name, startTime, endTime, description, location, topic, level, perks, flyer_img):
        super().__init__(name, startTime, endTime, description, location,perks, flyer_img)
        self.topic = topic
        self.level = level
        self.eventType = "Technical Workshop"

class SocialEvent (Event):
    def __init__(self, name, startTime, endTime, description, location, theme, perks, flyer_img):
        super().__init__(name, startTime, endTime, description, location,perks, flyer_img)
        self.theme = theme
        self.eventType = "Social Event"

class Conference (Event):
    def __init__(self, name, startTime, endTime, description, location, keynote_speaker, perks, flyer_img):
        super().__init__(name, startTime, endTime, description, location,perks, flyer_img)
        self.keynote_speaker = keynote_speaker
        self.volunteers = self.volunteers
        self.eventType = "Conference"

class ProfessionalNetwork (Event):
    def __init__(self, name, startTime, endTime, description, location, industry, perks, flyer_img):
        super().__init__(name, startTime, endTime, description, location,perks, flyer_img)
        self.industry = industry
        self.speakers = self.speakers
        self.eventType = "Professional and Network"
