from models.event import Event, TechnicalWorkshop, SocialEvent, Conference, ProfessionalNetwork
class EventFactory:
    def createEvent(self, eventType, name, startTime, endTime, description, perks, flyer_img, location,topic=None, level=None, theme=None, keynote_speaker=None, industry_focus=None):
        if eventType == "TechnicalWorkshop":
            return TechnicalWorkshop(name, startTime, endTime, description, location, topic, level, perks, flyer_img)
        elif eventType == "SocialEvent":
            return SocialEvent(name, startTime, endTime, description, location, theme, perks, flyer_img)
        elif eventType == "Conference":
            return Conference(name, startTime, endTime, description, location, keynote_speaker, perks, flyer_img)
        elif eventType == "Professional and Network":
            return ProfessionalNetwork(name, startTime, endTime, description, location, industry_focus, perks, flyer_img)
        else:
            raise ValueError("Invalid event type")