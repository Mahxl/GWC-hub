from models.event import Event, TechnicalWorkshop, SocialEvent, Conference, ProfessionalNetwork
from datetime import datetime

class EventFactory:
    @staticmethod
    def format_date(date_str):
        if not date_str:
            return ""
        try:
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return dt.strftime('%m/%d/%Y at %I:%M %p')
        except:
            return date_str

    @staticmethod
    def createEvent(eventType, name, startTime, endTime, description, perks,
                    flyer_img, location, topic=None, level=None, theme=None,
                    speaker=None, industry=None, id=None, volunteers=None):

        raw_start = startTime
        raw_end = endTime

        display_start = EventFactory.format_date(startTime)
        display_end = EventFactory.format_date(endTime)

        if eventType == "TechnicalWorkshop":
            obj = TechnicalWorkshop(name, display_start, display_end, description, location, topic, level, perks, flyer_img, id=id)
        elif eventType == "SocialEvent":
            obj = SocialEvent(name, display_start, display_end, description, location, theme, perks, flyer_img, id=id)
        elif eventType == "Conference":
            obj = Conference(name, display_start, display_end, description, location, perks, flyer_img, volunteers, id=id)
        elif eventType in ["ProfessionalNetwork", "Professional and Network"]:
            obj = ProfessionalNetwork(name, display_start, display_end, description, location, industry, perks, flyer_img, speaker, id=id)
        else:
            obj = Event(name, display_start, display_end, description, location, perks, flyer_img, eventType, id=id)

        obj.raw_end = raw_end
        obj.raw_start = raw_start
        return obj