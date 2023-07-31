class DetectionEngine:
    
    def __init__(self,weight):
        self.weight = weight
        self.result = None
        self.score = None
        self.error = False

    def run_detection(self):
        # 検知エンジンの実行
        # sourcecodeを入力として受け取り、検知結果を返す
        
        # 検知ロジックの実装
        # ...
        pass


    def get_result(self):
        return self.result
    
    def get_score(self):
        return self.score
    
    def get_error(self):
        return self.error

    def init(self):
      self.result = None
      self.score = None
      self.error = False
