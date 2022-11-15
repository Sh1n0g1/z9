def detect_iex(src):
  #Detect the iex/Invoke-Expression string
  target = ["iex", "invoke-expression"]
  for t in target:
    if src.lower().find(t) != -1:
      return True
  return False
