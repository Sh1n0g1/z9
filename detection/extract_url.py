from detection.detection_engine import DetectionEngine
import re

class ExtractURL(DetectionEngine):
    def __init__(self, weight):
        super().__init__(weight)
        self.name = "url_result"

    def run_detection(self,source_context):
        try:
            urls = re.findall(r"https?://[\w!?/+\-_~;.,&#$%()[\]]+", source_context.removed_backtick)
            self.result = urls
            self.score = len(urls) * self.weight

        except Exception as e:
            print("{0}:{1}".format(self.name,e))
            self.result = []
            self.score = 0
            self.error = str(e)
