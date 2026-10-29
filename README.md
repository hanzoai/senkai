# Sekai-1 Alpha — API Cookbook

API-only examples for Hanzo's proprietary Sekai model. **Alpha only.** Model implementation, training, checkpoints, datasets and detailed evaluations are maintained privately. This repository contains clients, application-owned input preparation and forwarding gateways.

**Hosted availability:** activation of Sekai at `api.hanzo.ai/v1/worlds` has not been completed. A GET response there currently describes Hanzo World, a different product; the model-creation POST was checked and returned 405. Use an explicitly enabled alpha deployment. These examples do not imply a hosted launch.

## Python

```sh
git clone https://github.com/hanzoai/senkai.git
cd senkai
python -m pip install -e .
export HANZO_API_KEY=YOUR_KEY
export HANZO_BASE_URL=https://YOUR_ENABLED_ALPHA_HOST/v1
python examples/python.py
python examples/workflow.py --recipe maintenance
```

The model name is **`sekai-1-alpha`**. Credentials and tenant isolation are enforced by the serving deployment; clients do not mint tenant identity headers. Calls can create stored worlds and incur costs on your configured deployment.

## Python and Rust Hanzo ML

- [Python Hanzo ML example](examples/python_ml.py): use `hanzo_ml.Tensor` for application-owned unit conversion, then submit an event to the API.
- [Rust Hanzo ML client](clients/rust/src/main.rs): the same preparation with the published `hanzo-ml` crate; every model operation remains remote.

```sh
cargo run --manifest-path clients/rust/Cargo.toml -- ml
```

Python binding packaging is fixed in [hanzoai/ml PR #23](https://github.com/hanzoai/ml/pull/23). A wheel was built and tested; PyPI publication has not been confirmed. Until released, build that public source branch:

```sh
git clone --branch codex/python-hanzo-ml https://github.com/hanzoai/ml.git hanzo-ml-source
python -m pip install maturin
RUSTFLAGS="-C target-cpu=native" maturin build --manifest-path hanzo-ml-source/hanzo-ml-pyo3/Cargo.toml --out wheels
python -m pip install wheels/hanzo_ml-*.whl
python examples/python_ml.py
```

## Language clients

[Language commands and validation coverage](docs/languages.md) cover Python, Rust, JavaScript, TypeScript, Go, Java, Kotlin, C#, Ruby, PHP, Swift, Dart, Elixir, C, C++, and curl. The snippets use standard HTTP rather than claiming unverified generated SDK methods exist.

The twelve [recipe directories](recipes/) show API input/output workflows. They are application sketches, not domain-qualified models or published performance claims. No example performs external actuation or business writes. Alpha planning is restricted to simulation; business/drone planning is refused by the current service.

## Serving without shipping the model

[Python gateway](serving/python_gateway.py):

```sh
export HANZO_BASE_URL=https://YOUR_ENABLED_ALPHA_HOST/v1
export HANZO_API_KEY=SERVER_SIDE_UPSTREAM_KEY
export GATEWAY_API_KEY=YOUR_GATEWAY_CLIENT_KEY
python serving/python_gateway.py
```

[Rust gateway](clients/rust/src/main.rs): `cargo run --manifest-path clients/rust/Cargo.toml -- serve`. Python listens on loopback port 8050; Rust on 8051. Both forward to your private deployment and contain no model. Use a managed authenticated TLS edge for remote access. These are examples, not the hosted Sekai model service.

## Research SDK

```sh
python -m pip install 'hanzo-research>=0.3.0'
python examples/research.py
cargo run --manifest-path clients/rust/Cargo.toml -- research
```

Both use the real Hanzo Research SDK to record private API measurements. The Python example retains every attempted request and failure. Research uses `HANZO_API_KEY` or the Hanzo CLI credential; `RESEARCH_API_KEY` optionally separates Research from a local alpha test credential. Python accepts `RESEARCH_ORG` for SDK-validated organization switching. The pinned Rust SDK requires a credential scoped to its target organization; an admin token alone does not select Hanzo. Python cloud recording was verified; Rust cloud recording requires that scoped credential.

Canonical routes are **`/v1/research/{benchmarks,runs,experiments,artifacts}`** and the singular **`/v1/benchmark/...`** arena, not `/v1/benchmarks`. The arena is a separate claims/read surface, not an executor. No public grants or leaderboard claims are made by these examples.

## Tests

```sh
python -m unittest discover -s tests -v
```

CI uses a clearly labelled HTTP mock to check request shape/authentication. It does not run Sekai or publish benchmark results. Private integration checks additionally exercised available clients against a local alpha service.
