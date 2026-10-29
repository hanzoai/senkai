"""Create an alpha world via Hanzo's API. No model runs in this client."""
import json
from sekai_cookbook import Worlds
print(json.dumps(Worlds().create(), indent=2))
