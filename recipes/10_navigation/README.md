# Navigation — alpha API sketch

```sh
python examples/workflow.py --recipe navigation
```

This sends example observations, a goal, and two candidate action sequences to the API. All belief updates and planning run on the server. The numbers are illustrative client inputs; this is not a domain-qualified model or benchmark. Requires an enabled alpha deployment. No action is executed.

For business/drone domains, planning is blocked by the alpha service. `--domain business` or `--domain drone` demonstrates that refusal, not operational support.
