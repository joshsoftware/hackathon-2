class EventDBModel:
    def __init__(self, uuid, source, url, payload, status, result, user_agent, ad_blocker_active, plugin_installed):
        self.uuid = uuid
        self.source = source
        self.url = url
        self.payload = payload
        self.status = status
        self.result = result
        self.user_agent = user_agent
        self.ad_blocker_active = ad_blocker_active
        self.plugin_installed = plugin_installed

    def as_tuple(self):
        return (
            self.uuid, self.source, self.url, self.payload, self.status,
            self.result, self.user_agent, self.ad_blocker_active, self.plugin_installed
        )
