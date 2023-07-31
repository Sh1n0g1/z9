from detection.detection_engine import DetectionEngine
import re

class DetectSign(DetectionEngine):
    def __init__(self, weight):
        super().__init__(weight)
        self.name="detect_sign"

    def run_detection(self,source_context):
        try:
            sign_num = len(re.findall(r'[^\s0-9a-zA-z]|`', source_context.source))
            src_len = len(source_context.source)
            ret_val = sign_num / src_len

            if src_len < 100:
                self.result = 0
            elif ret_val < 0.3:
                self.result = 0
            else:
                self.result = ret_val
            self.score = self.result * self.weight

        except Exception as e:
            print("{0}:{1}".format(self.name,e))
            self.result = 0
            self.score = 0
            self.error = str(e)
            
