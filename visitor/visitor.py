from django.conf import settings


class Visitor(object):

    def __init__(self, request):
        self.request = request
        self.session = request.session
        # Makes an empty visitor if one does not exist then save it.
        self.data = self.session.get(settings.VISITOR_SESSION_ID, {})
        if self.data == {}:
            self.save()

    def get(self, key, option=None):
        return self.data.get(key, option)

    def add(self, key, value, update_function=None):
        if key not in self.data.keys():
            self.data[key] = value
        else:
            if update_function is None:
                return None
            self.data[key] = update_function(self.data[key], key, value)

        self.save()
        return None

    def save(self):
        # update the session visitor
        self.session[settings.VISITOR_SESSION_ID] = self.data
        # mark the session as "modified" to make sure it is saved
        self.session.modified = True

    def remove(self, key):
        """
        Remove data from the visitor.
        """
        if key in self.data:
            del self.data[key]
            self.save()

    def update(self, key, value):
        if key in self.data:
            self.data[key] = value
            self.save()

    def clear(self):
        # empty visitor
        self.session[settings.VISITOR_SESSION_ID] = {}
        self.session.modified = True
