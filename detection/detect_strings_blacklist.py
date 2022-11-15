import csv

def detect_strings_blacklist(src):
    bl = blacklist2()
    return bl.detect_strings(src)
            
class blacklist2:
    dic = {}

    def __init__(self):
        # read file
        with open('detection/blacklist.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                # make dictionary
                self.dic[row[0].strip().lower()] = row[1]
            
    def detect_strings(self, src):
    #extract the black listed strings
        words = []
        # すべて小文字にする
        src_small = src.lower()
        for word in self.dic.keys():
            if src_small.find(word) != -1:
                words.append({"keyword": word, "score": int(self.dic[word])})
        return words
