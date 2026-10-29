# Language clients

Set `HANZO_BASE_URL` to your enabled alpha `/v1` base (no trailing slash) and `HANZO_API_KEY` to its credential. Every example requests `sekai-1-alpha`. Defaults name the intended Hanzo API address but hosted Sekai activation is still pending.

| Language | Command from repository root | Local alpha check |
|---|---|---|
| Python | `python examples/python.py` | Passed |
| Python + Hanzo ML | `python examples/python_ml.py` | Passed with built wheel |
| Rust | `cargo run --manifest-path clients/rust/Cargo.toml` | Passed |
| Rust + Hanzo ML | `cargo run --manifest-path clients/rust/Cargo.toml -- ml` | Passed |
| JavaScript | `node clients/javascript.mjs` | Passed |
| TypeScript | `node --experimental-strip-types clients/typescript.ts` (Node 24+) | Passed |
| Go | `go run clients/go/main.go` | Passed |
| Java | `java clients/java/Sekai.java` (JDK 17+) | Passed |
| Kotlin | `kotlinc clients/kotlin/Sekai.kt -include-runtime -d /tmp/sekai.jar && java -jar /tmp/sekai.jar` | Toolchain unavailable; not run |
| C# | Copy `clients/csharp/Program.cs` into a .NET console project and `dotnet run` | Toolchain unavailable; not run |
| Ruby | `ruby clients/ruby.rb` | Passed |
| PHP | `php clients/php.php` | Passed |
| Swift | `swift clients/swift.swift` | Toolchain unavailable; not run |
| Dart | `dart clients/dart.dart` | Passed |
| Elixir | `elixir clients/elixir.exs` | Toolchain unavailable; not run |
| C | `cc clients/c/main.c -lcurl -o /tmp/sekai-c && /tmp/sekai-c` | Passed |
| C++ | `c++ clients/cpp/main.cpp -lcurl -o /tmp/sekai-cpp && /tmp/sekai-cpp` | Passed |
| curl | `sh clients/curl.sh` | Passed |

Local checks establish transport compatibility, not hosted availability, task accuracy, latency guarantees or domain qualification. Languages without installed toolchains are supplied as examples and need their own build checks.
