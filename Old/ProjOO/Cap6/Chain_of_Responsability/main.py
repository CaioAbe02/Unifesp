from components.Console import Console
from components.CharCounter.SpaceCounter import SpaceCounter
from components.CharCounter.ACounter import ACounter
from components.CharCounter.DotCounter import DotCounter
from components.CharCounterHandler import CharCounterHandler

console = Console()
console.setText()
text = console.getText()

handler = CharCounterHandler()

space_counter = SpaceCounter(handler)
a_counter = ACounter(handler)
dot_counter = DotCounter(handler)

space_counter.setNext(a_counter)
a_counter.setNext(dot_counter)
space_counter.countChar(text)

handler.printResults()
