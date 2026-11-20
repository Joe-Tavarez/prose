## Repository overview (file tree and README, at the starting commit)
386 tracked files, 223 .cs files, 13 .csproj files.

### Project files
- `benchmarks/RestSharp.Benchmarks/RestSharp.Benchmarks.csproj`
- `gen/SourceGenerator/SourceGenerator.csproj`
- `src/RestSharp.Serializers.CsvHelper/RestSharp.Serializers.CsvHelper.csproj`
- `src/RestSharp.Serializers.NewtonsoftJson/RestSharp.Serializers.NewtonsoftJson.csproj`
- `src/RestSharp.Serializers.Xml/RestSharp.Serializers.Xml.csproj`
- `src/RestSharp/RestSharp.csproj`
- `test/RestSharp.InteractiveTests/RestSharp.InteractiveTests.csproj`
- `test/RestSharp.Tests.Integrated/RestSharp.Tests.Integrated.csproj`
- `test/RestSharp.Tests.Serializers.Csv/RestSharp.Tests.Serializers.Csv.csproj`
- `test/RestSharp.Tests.Serializers.Json/RestSharp.Tests.Serializers.Json.csproj`
- `test/RestSharp.Tests.Serializers.Xml/RestSharp.Tests.Serializers.Xml.csproj`
- `test/RestSharp.Tests.Shared/RestSharp.Tests.Shared.csproj`
- `test/RestSharp.Tests/RestSharp.Tests.csproj`

### Directories (files; .cs files), most relevant first
- `src/RestSharp/Parameters/` (12; 12 .cs)
- `test/` (144; 0 .cs)
- `src/` (123; 0 .cs)
- `docs/` (76; 0 .cs)
- `.github/` (12; 0 .cs)
- `benchmarks/` (6; 0 .cs)
- `gen/` (5; 0 .cs)
- `.idea/` (4; 0 .cs)
- `"test/` (2; 0 .cs)
- `.devcontainer/` (2; 0 .cs)
- `props/` (1; 0 .cs)
- `src/RestSharp/` (104; 19 .cs)
- `test/RestSharp.Tests/` (45; 18 .cs)
- `test/RestSharp.Tests.Serializers.Xml/` (42; 4 .cs)
- `test/RestSharp.Tests.Integrated/` (35; 23 .cs)
- `docs/versioned_docs/` (26; 0 .cs)
- `docs/docs/` (15; 0 .cs)
- `docs/static/` (10; 0 .cs)
- `src/RestSharp.Serializers.Xml/` (9; 7 .cs)
- `docs/src/` (8; 0 .cs)
- `test/RestSharp.Tests.Shared/` (8; 0 .cs)
- `benchmarks/RestSharp.Benchmarks/` (6; 1 .cs)
- `docs/.idea/` (6; 0 .cs)
- `test/RestSharp.Tests.Serializers.Json/` (6; 1 .cs)
- `gen/SourceGenerator/` (5; 3 .cs)
- `src/RestSharp.Serializers.NewtonsoftJson/` (5; 3 .cs)
- `.github/workflows/` (4; 0 .cs)
- `src/RestSharp.Serializers.CsvHelper/` (4; 2 .cs)
- `test/RestSharp.InteractiveTests/` (4; 3 .cs)
- `.github/ISSUE_TEMPLATE/` (3; 0 .cs)
- `test/RestSharp.Tests.Serializers.Csv/` (3; 2 .cs)
- `"test/RestSharp.Tests.Integrated/` (2; 0 .cs)
- `docs/versioned_sidebars/` (2; 0 .cs)
- `test/RestSharp.Tests.Serializers.Xml/SampleClasses/` (22; 22 .cs)
- `test/RestSharp.Tests/SampleData/` (18; 0 .cs)
- `src/RestSharp/Request/` (17; 17 .cs)
- `src/RestSharp/Serializers/` (17; 17 .cs)
- `docs/versioned_docs/version-v111/` (15; 0 .cs)
- `src/RestSharp/Authenticators/` (15; 15 .cs)
- `test/RestSharp.Tests.Serializers.Xml/SampleData/` (15; 0 .cs)
- `docs/versioned_docs/version-v110/` (11; 0 .cs)
- `docs/static/img/` (9; 0 .cs)
- `src/RestSharp/Extensions/` (9; 9 .cs)
- `docs/docs/usage/` (7; 0 .cs)
- `test/RestSharp.Tests/Auth/` (7; 7 .cs)
- `docs/docs/advanced/` (6; 0 .cs)
- `docs/src/pages/` (5; 0 .cs)
- `src/RestSharp/Response/` (4; 4 .cs)
- `test/RestSharp.Tests.Shared/Fixtures/` (4; 4 .cs)
- `src/RestSharp/Polyfills/` (3; 3 .cs)
- `test/RestSharp.Tests.Integrated/Fixtures/` (3; 3 .cs)
- `test/RestSharp.Tests.Serializers.Json/NewtonsoftJson/` (3; 3 .cs)
- `test/RestSharp.Tests.Shared/Extensions/` (3; 3 .cs)
- `"test/RestSharp.Tests.Integrated/Assets/` (2; 0 .cs)
- `benchmarks/RestSharp.Benchmarks/Requests/` (2; 2 .cs)
- `benchmarks/RestSharp.Benchmarks/Serializers/` (2; 2 .cs)
- `docs/src/components/` (2; 0 .cs)
- `src/RestSharp/Interceptors/` (2; 2 .cs)
- `src/RestSharp/Options/` (2; 2 .cs)
- `src/RestSharp/Properties/` (2; 2 .cs)
- `test/RestSharp.Tests.Integrated/Assets/` (2; 0 .cs)
- `test/RestSharp.Tests.Integrated/Authentication/` (2; 2 .cs)
- `test/RestSharp.Tests.Integrated/Interceptor/` (2; 2 .cs)
- `test/RestSharp.Tests.Integrated/Server/` (2; 2 .cs)
- `docs/src/css/` (1; 0 .cs)
- `gen/SourceGenerator/Properties/` (1; 0 .cs)
- `test/RestSharp.Tests.Serializers.Json/SystemTextJson/` (1; 1 .cs)
- `test/RestSharp.Tests/Fixtures/` (1; 1 .cs)

### README.md (start)
# RestSharp - Simple .NET REST Client
RestSharp is a lightweight HTTP API client library. It's a wrapper around `HttpClient`, not a full-fledged client on
its own.
What RestSharp adds to `HttpClient`:
- Default parameters of any kind, not just headers
- Add a parameter of any kind to requests, like query, URL segment, header, cookie, or body
- Multiple ways to add a request body, including JSON, XML, URL-encoded form data, multipart form data with and
  without files
- Built-in serialization and deserilization of JSON, XML, and CSV, as well as the ability to add custom serializers
- Rich support for authentication
## Compatibility note
RestSharp 107 was a major release that brings a lot of changes. We've removed a lot of legacy code and added new
features. Finally, RestSharp has moved to `HttpClient`. We also deprecated the following:
- SimpleJson in favour of `System.Text.Json.JsonSerialzer`
- `IRestRequest`, and `IRestResponse` in favour of implementing classes
- Everything `Http` and `IHttp` as those are just wrappers
- Client configuration moved to `RestClientOptions` to make the client thread-safe
- `IRestClient` interface surface substantially reduced
Most of the client and some of the request options are now in `RestClientOptions`.
Check [v107+ docs](https://restsharp.dev/v107) for more information.
## Packages
| Package                                | What it's for                                                                        |
|----------------------------------------|--------------------------------------------------------------------------------------|
| `RestSharp`                            | The core library, including `System.Text.Json` serializer and basical XML serializer |
| `RestSharp.Serializers.NewtonsoftJson` | Use `Newtonsoft.Json` as a JSON serializer                                           |
| `RestSharp.Serializers.Xml`            | Use custom RestSharp XML serializer for XML                                          |
| `RestSharp.Serializers.CsvHelper`      | Use `CsvHelper` as a CSV serializer                                                  |
## Code of Conduct
This project has adopted the code of conduct defined by the Contributor Covenant to clarify expected behavior in our community.
For more information see the [.NET Foundation Code of Conduct](https://dotnetfoundation.org/code-of-conduct).
**Users violated the aforementioned code of conduct will be blocked.**
## Support
RestSharp is an open-source project with a single maintainer. Do not expect your issue to be resolved unless it concerns a large group of RestSharp users.
The best way to resolve your issue is to fix it yourself. Fork the repository and submit a pull request.
You can also motivate the maintainer by sponsoring this project.
### Contribute
Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on the process for reporting issues and submitting pull requests.
### Get help
Read the docs: [Official Site][1]
Ask a question on StackOverflow with the tag `restsharp`.
Join RestSharp Discord server:
Find RestSharp on Twitter: [@RestSharp][2]
## Community
### .NET Foundation
This project is a part of the [.NET Foundation](https://dotnetfoundation.org).
### Code Contributors
This project exists thanks to all the people who contribute.
[](https://github.com/restsharp/RestSharp/graphs/contributors)
### Financial Contributors
Become a financial contributor and help us sustain our community. [Contribute](https://github.com/sponsors/restsharp)
## License
[Apache License 2.0](https://github.com/restsharp/RestSharp/blob/dev/LICENSE.txt)
  [1]: https://restsharp.dev
  [2]: https://twitter.com/RestSharp
  [3]: https://github.com/restsharp/RestSharp/issues
