class GQLContextViewer:
    def __init__(self):
        self.clients = { }

    def get_current(self, request):
        return { "request": request, "clients": self.clients }
 