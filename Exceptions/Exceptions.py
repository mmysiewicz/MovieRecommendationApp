
class ImageLoadException(Exception):
    def __init__(self, message, title=None, path=None):
        self.message = message
        self.title = title
        self.path = path
        super().__init__(f"{message}, Dotyczy filmu: {title}, Ścieżka: {path}")