from detection.detection_engine import DetectionEngine

class DetectIEX(DetectionEngine):

  def __init__(self,weight):
      super().__init__(weight)
      self.name="detect_iex"

  def run_detection(self,source_context):
      #Detect the iex/Invoke-Expression string
      try:
          target = ["iex", "invoke-expression"]
          self.result = False
          for t in target:
              self.result = source_context.concat_strings.lower().find(t) != -1 or self.get_result()
          self.score = self.result * self.weight
      except Exception as e:
        print("{0}:{1}".format(self.name,e))
        self.result = 0
        self.score = 0
        self.error = str(e)

