from fb import facebook
import threading

class AsyncWallPost(threading.Thread):
    def __init__(self, token, message, attachment):
        self.token = token
        self.message = message
        self.attachment = attachment
        threading.Thread.__init__(self)
    def run(self):
        try:
            graph = facebook.GraphAPI(self.token)
            graph.put_wall_post(self.message, self.attachment)
        except:
            return None
