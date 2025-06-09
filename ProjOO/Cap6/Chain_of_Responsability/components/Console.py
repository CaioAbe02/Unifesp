class Console:
  def __init__(self):
    self.text: str = ""

  def getText(self) -> str:
    return self.text

  def setText(self):
    print("Digite o texto")
    self.text = input()