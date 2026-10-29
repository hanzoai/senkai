"""Send application observations and candidate actions to an enabled alpha API."""
import argparse,json,time,uuid
from sekai_cookbook import Worlds
parser=argparse.ArgumentParser();parser.add_argument('--recipe',default='maintenance');parser.add_argument('--domain',default='simulation',choices=['simulation','business','drone']);args=parser.parse_args()
client=Worlds();world=client.create(args.domain);entity=args.recipe.replace('-','_')
client.event(world['id'],dict(event_id='event_'+uuid.uuid4().hex,entity_id=entity,timestamp=time.time(),modality='telemetry',features=[.1,.2,0.,0.]))
print(json.dumps(client.belief(world['id'],entity),indent=2))
# Candidate commands and goals are client inputs, not model parameters. Nothing executes.
print(json.dumps(client.plan(world['id'],dict(entity_id=entity,target=[0.,0.,0.,0.],candidates=[dict(id='hold',actions=[[0.,0.]],cost=0.),dict(id='adjust',actions=[[.1,0.]],cost=.1)])),indent=2))
