from datetime import date, datetime

class EventDisplayStrategy:
    def filter(self, events):
        raise NotImplementedError("implement filter method")

    def _parse_date(self, date_str):
        if not date_str: 
            return None
        try:
            return datetime.fromisoformat(date_str.replace('Z', '+00:00')).date()
        except:
            return None

class UpcomingEventStrategy(EventDisplayStrategy): 
    def filter(self, events):
        today = date.today()
        filtered = []       
        for e in events:
            event_date = self._parse_date(e.raw_end)
            if event_date and event_date >= today:
                filtered.append(e)
        return filtered

class PastEventStrategy(EventDisplayStrategy):
    def filter(self, events):
        today = date.today()
        filtered = []       
        for e in events:
            event_date = self._parse_date(e.raw_end)
            if event_date and event_date < today:
                filtered.append(e)
        return filtered