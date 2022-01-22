

payload = """
nwdiag {
  External_Network [shape = cloud];
  External_Network -- Management;
  network Management {
      address = "10.1.10/24"

      sw01 [address = "10.1.10.54"];
      sw02 [address = "10.1.10.55"];
  }
}
"""
from nwdiag.command import NwdiagApp
import nwdiag

print(dir(nwdiag))
print(dir(nwdiag.builder))

from nwdiag import parser, builder, drawer

tree = parser.parse_string(payload)
diagram = builder.ScreenNodeBuilder.build(tree)
draw = drawer.DiagramDraw('PNG', diagram, filename="foo.png")
draw.draw()
draw.save()

