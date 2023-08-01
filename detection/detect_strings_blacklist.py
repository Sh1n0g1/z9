from detection.detection_engine import DetectionEngine
import csv


class DetectStringsBlacklist(DetectionEngine):
    def __init__(self,weight):
        super().__init__(weight)
        self.name = "detect_strings_blacklist"

        self.blacklist = Blacklist2()

    def run_detection(self, source_context):
        try:
            words = self.blacklist.detect_strings(source_context.concat_strings)
            self.result = words
            self.score = 0
            for word in words:
                self.score += word["score"] * self.weight
        except Exception as e:
            print("{0}:{1}".format(self.name,e))
            self.result = []
            self.score = 0
            self.error = str(e)
        
 

class Blacklist2:
    def __init__(self):
        self.dic = {}
        self.load_blacklist()

    def load_blacklist(self):
        with open('detection/blacklist.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                self.dic[row[0].strip().lower()] = row[1]

    def detect_strings(self, src):
        #extract the black listed strings
        words = []
        src_small = src.lower()
        for word in self.dic.keys():
            if src_small.find(word) != -1:
                words.append({"keyword": word, "score": int(self.dic[word])})
        return words
