"""Use public Hanzo ML tensors to prepare an event; all Sekai inference is remote."""
import json
import time
import uuid
import hanzo_ml as ml
from sekai_cookbook import Worlds

# Public, application-owned unit conversion, not a model encoder or latent state.
features = (ml.Tensor([10.0, 20.0, 0.0, 0.0])/100.0).values()
client = Worlds()
world = client.create()
result = client.event(world["id"], dict(event_id="event_"+uuid.uuid4().hex,
    entity_id="sensor_a", timestamp=time.time(), modality="telemetry", features=features))
print(json.dumps(result, indent=2))
