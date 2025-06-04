from components.Console import Console
from components.CharCounter.SpaceCounter import SpaceCounter
from components.CharCounter.ACounter import ACounter

console = Console()
console.setText()
text = console.getText()

space_counter = SpaceCounter()
a_counter = ACounter()

space_counter.setNext(a_counter)

space_counter.countChar(text)
