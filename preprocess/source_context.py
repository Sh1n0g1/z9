from preprocess import remove_backtick
from preprocess import concat_strings

class SourceContext:
    def __init__(self):
        self.removed_backtick = ""
        self.source = ""
        self.concat_strings = ""
      
    def preprocess(self, source):
        self.removed_backtick = remove_backtick.remove_backtick(source)
        self.concat_strings = concat_strings.concat_strings(self.removed_backtick)
        self.source = source