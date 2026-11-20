## Repository overview (file tree and README, at the starting commit)
254 tracked files, 151 .cs files, 10 .csproj files.

### Project files
- `src/RestSharp/RestSharp.csproj`
- `benchmarks/RestSharp.Benchmarks/RestSharp.Benchmarks.csproj`
- `src/RestSharp.Serializers.NewtonsoftJson/RestSharp.Serializers.NewtonsoftJson.csproj`
- `src/RestSharp.Serializers.Xml/RestSharp.Serializers.Xml.csproj`
- `test/RestSharp.IntegrationTests/RestSharp.IntegrationTests.csproj`
- `test/RestSharp.InteractiveTests/RestSharp.InteractiveTests.csproj`
- `test/RestSharp.Serializers.Json.Tests/RestSharp.Serializers.Json.Tests.csproj`
- `test/RestSharp.Serializers.Xml.Tests/RestSharp.Serializers.Xml.Tests.csproj`
- `test/RestSharp.Tests.Shared/RestSharp.Tests.Shared.csproj`
- `test/RestSharp.Tests/RestSharp.Tests.csproj`

### Directories (files; .cs files), most relevant first
- `src/RestSharp/Request/` (10; 10 .cs)
- `src/RestSharp/` (65; 10 .cs)
- `test/RestSharp.Serializers.Xml.Tests/` (42; 4 .cs)
- `test/RestSharp.Tests/` (32; 13 .cs)
- `test/RestSharp.IntegrationTests/` (25; 15 .cs)
- `test/RestSharp.Tests.Shared/` (11; 0 .cs)
- `src/RestSharp.Serializers.Xml/` (8; 7 .cs)
- `benchmarks/RestSharp.Benchmarks/` (4; 1 .cs)
- `src/RestSharp.Serializers.NewtonsoftJson/` (4; 3 .cs)
- `test/RestSharp.Serializers.Json.Tests/` (4; 3 .cs)
- `test/RestSharp.InteractiveTests/` (3; 2 .cs)
- `test/RestSharp.Serializers.Xml.Tests/SampleClasses/` (22; 22 .cs)
- `test/RestSharp.Tests/SampleData/` (18; 0 .cs)
- `src/RestSharp/Serializers/` (16; 16 .cs)
- `src/RestSharp/Authenticators/` (15; 15 .cs)
- `test/RestSharp.Serializers.Xml.Tests/SampleData/` (15; 0 .cs)
- `test/RestSharp.Tests.Shared/Fixtures/` (8; 8 .cs)
- `src/RestSharp/Extensions/` (6; 6 .cs)
- `test/RestSharp.IntegrationTests/Fixtures/` (4; 4 .cs)
- `src/RestSharp/Parameters/` (3; 3 .cs)
- `benchmarks/RestSharp.Benchmarks/Serializers/` (2; 2 .cs)
- `src/RestSharp/Response/` (2; 2 .cs)
- `test/RestSharp.IntegrationTests/Assets/` (2; 0 .cs)
- `test/RestSharp.Tests.Shared/Extensions/` (2; 2 .cs)
- `src/RestSharp/Properties/` (1; 1 .cs)
- `test/RestSharp.IntegrationTests/Authentication/` (1; 1 .cs)
- `test/RestSharp.IntegrationTests/Models/` (1; 1 .cs)
- `test/` (118; 0 .cs)
- `src/` (78; 0 .cs)
- `docs/` (24; 0 .cs)
- `.github/` (9; 0 .cs)
- `.idea/` (4; 0 .cs)
- `benchmarks/` (4; 0 .cs)
- `.devcontainer/` (2; 0 .cs)
- `props/` (1; 0 .cs)
- `docs/CI-CD_DOCUMENTATION/` (9; 0 .cs)
- `docs/.idea/` (7; 0 .cs)
- `.github/workflows/` (3; 0 .cs)
- `docs/.vuepress/` (2; 0 .cs)
- `docs/support/` (1; 0 .cs)
- `docs/v107/` (1; 0 .cs)
- `docs/.idea/codeStyles/` (1; 0 .cs)
- `docs/.idea/dictionaries/` (1; 0 .cs)
- `docs/.vuepress/public/` (1; 0 .cs)

### README.md (start)
# RestSharp - Simple .NET REST Client
## RestSharp vNext
Finally, RestSharp has moved to `HttpClient`. We also deprecated the following:
- All sync calls in favour of async calls
- SimpleJson in favour of `System.Text.Json.JsonSerialzer`
- `IRestClient`, `IRestRequest`, and `IRestResponse` in favour of implementing classes
- Everything `Http` and `IHttp` as those are just wrappers
Most of the client and some of the request options are now in `RestClientOptions`.
Check [v107 docs](https://restsharp.dev/v107) for more information.
### Build
| | |
|-|-|
| dev |  |
### Nuget
| | |
|-|-|
| downloads |  |
| stable |  |
| preview |  |
### Support
RestSharp is an open-source project with a single maintainer. Do not expect your issue to be resolved unless it concerns a large group of RestSharp users.
The best way to resolve your issue is to fix it yourself. Fork the repository and submit a pull request.
You can also motivate the maintainer by sponsoring this project.
### Get help
Read the docs: [Official Site][1]
Find RestSharp on Twitter: [@RestSharp][2]
## Contributors
### Code Contributors
This project exists thanks to all the people who contribute. [[Contribute](CONTRIBUTING.md)].
### Financial Contributors
Become a financial contributor and help us sustain our community. [[Contribute](https://opencollective.com/RestSharp/contribute)]
#### Individuals
#### Organizations
Support this project with your organization. Your logo will show up here with a link to your website. [[Contribute](https://opencollective.com/RestSharp/contribute)]
### License: Apache License 2.0
  [1]: https://restsharp.dev
  [2]: https://twitter.com/RestSharp
