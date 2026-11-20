## Repository overview (file tree and README, at the starting commit)
815 tracked files, 671 .cs files, 19 .csproj files.

### Project files
- `src/Polly/Polly.csproj`
- `src/Polly.Testing/Polly.Testing.csproj`
- `test/Polly.Testing.Tests/Polly.Testing.Tests.csproj`
- `bench/Polly.Benchmarks/Polly.Benchmarks.csproj`
- `bench/Polly.Core.Benchmarks/Polly.Core.Benchmarks.csproj`
- `samples/GenericPipelines/GenericPipelines.csproj`
- `src/Polly.Core/Polly.Core.csproj`
- `src/Polly.Extensions/Polly.Extensions.csproj`
- `src/Polly.RateLimiting/Polly.RateLimiting.csproj`
- `test/Polly.Core.Tests/Polly.Core.Tests.csproj`
- `test/Polly.Extensions.Tests/Polly.Extensions.Tests.csproj`
- `test/Polly.RateLimiting.Tests/Polly.RateLimiting.Tests.csproj`
- `test/Polly.Specs/Polly.Specs.csproj`
- `test/Polly.TestUtils/Polly.TestUtils.csproj`
- `samples/DependencyInjection/DependencyInjection.csproj`
- `samples/Extensibility/Extensibility.csproj`
- `samples/Intro/Intro.csproj`
- `samples/Retries/Retries.csproj`
- `src/Snippets/Snippets.csproj`

### Directories (files; .cs files), most relevant first
- `src/Polly.Core/Utils/` (28; 28 .cs)
- `src/Polly.Core/CircuitBreaker/` (22; 22 .cs)
- `src/Polly/CircuitBreaker/` (22; 22 .cs)
- `test/Polly.Core.Tests/CircuitBreaker/` (17; 17 .cs)
- `test/Polly.Core.Tests/Utils/` (17; 17 .cs)
- `bench/Polly.Core.Benchmarks/Utils/` (11; 11 .cs)
- `test/Polly.Specs/CircuitBreaker/` (9; 9 .cs)
- `test/Polly.Extensions.Tests/Utils/` (1; 1 .cs)
- `test/Polly.TestUtils/` (13; 12 .cs)
- `src/Polly.Testing/` (7; 3 .cs)
- `test/Polly.Testing.Tests/` (2; 1 .cs)
- `src/Polly/` (176; 35 .cs)
- `src/Polly.Core/` (144; 33 .cs)
- `test/Polly.Specs/` (125; 10 .cs)
- `test/Polly.Core.Tests/` (106; 19 .cs)
- `bench/Polly.Core.Benchmarks/` (29; 17 .cs)
- `src/Polly.Extensions/` (17; 0 .cs)
- `test/Polly.Extensions.Tests/` (16; 3 .cs)
- `bench/Polly.Benchmarks/` (13; 12 .cs)
- `src/Polly.RateLimiting/` (12; 8 .cs)
- `test/Polly.RateLimiting.Tests/` (7; 6 .cs)
- `test/Polly.Specs/Helpers/` (34; 34 .cs)
- `src/Polly/Caching/` (29; 29 .cs)
- `test/Polly.Core.Tests/Hedging/` (15; 15 .cs)
- `test/Polly.Specs/Retry/` (15; 15 .cs)
- `src/Polly.Core/Hedging/` (14; 14 .cs)
- `test/Polly.Specs/Caching/` (14; 14 .cs)
- `src/Polly/RateLimit/` (13; 13 .cs)
- `src/Polly/Bulkhead/` (11; 11 .cs)
- `src/Polly/Timeout/` (11; 11 .cs)
- `src/Polly/Utilities/` (11; 11 .cs)
- `src/Polly.Core/Telemetry/` (10; 10 .cs)
- `src/Polly/Wrap/` (10; 10 .cs)
- `src/Polly.Core/Retry/` (9; 9 .cs)
- `src/Polly.Extensions/Telemetry/` (9; 9 .cs)
- `src/Polly/NoOp/` (9; 9 .cs)
- `src/Polly/Retry/` (9; 9 .cs)
- `test/Polly.Specs/RateLimit/` (9; 9 .cs)
- `src/Polly.Core/Fallback/` (8; 8 .cs)
- `src/Polly.Core/Timeout/` (8; 8 .cs)
- `test/Polly.Core.Tests/Retry/` (8; 8 .cs)
- `test/Polly.Specs/Bulkhead/` (8; 8 .cs)
- `src/Polly/Fallback/` (7; 7 .cs)
- `test/Polly.Core.Tests/Timeout/` (7; 7 .cs)
- `src/Polly.Core/Registry/` (6; 6 .cs)
- `test/Polly.Core.Tests/Telemetry/` (6; 6 .cs)
- `test/Polly.Core.Tests/Fallback/` (5; 5 .cs)
- `test/Polly.Core.Tests/Registry/` (5; 5 .cs)
- `test/Polly.Extensions.Tests/Issues/` (5; 5 .cs)
- `test/Polly.Specs/Timeout/` (5; 5 .cs)
- `test/Polly.Specs/Wrap/` (5; 5 .cs)
- `src/Polly/Registry/` (4; 4 .cs)
- `test/Polly.Core.Tests/Issues/` (4; 4 .cs)
- `test/Polly.Extensions.Tests/Telemetry/` (4; 4 .cs)
- `test/Polly.Specs/Custom/` (4; 4 .cs)
- `test/Polly.Specs/Fallback/` (4; 4 .cs)
- `test/Polly.Specs/NoOp/` (4; 4 .cs)
- `src/Polly.Extensions/DependencyInjection/` (3; 3 .cs)
- `test/Polly.Specs/Registry/` (3; 3 .cs)
- `test/Polly.Core.Tests/Helpers/` (2; 2 .cs)
- `src/Polly.Core/ToBeRemoved/` (1; 1 .cs)
- `src/Polly.Extensions/Registry/` (1; 1 .cs)
- `src/Polly/Properties/` (1; 1 .cs)
- `test/Polly.Extensions.Tests/DependencyInjection/` (1; 1 .cs)
- `test/Polly.Extensions.Tests/Registry/` (1; 1 .cs)
- `samples/GenericPipelines/` (2; 1 .cs)
- `src/Snippets/Testing/` (1; 1 .cs)
- `src/` (385; 0 .cs)
- `test/` (269; 0 .cs)
- `bench/` (59; 0 .cs)
- `docs/` (20; 0 .cs)
- `.github/` (16; 0 .cs)
- `samples/` (16; 0 .cs)
- `eng/` (12; 0 .cs)
- `logos/` (8; 0 .cs)
- `.vscode/` (4; 0 .cs)
- `.config/` (1; 0 .cs)
- `src/Snippets/` (20; 0 .cs)
- `bench/BenchmarkDotNet.Artifacts/` (15; 0 .cs)
- `.github/workflows/` (10; 0 .cs)
- `src/LegacySupport/` (9; 9 .cs)
- `docs/strategies/` (6; 0 .cs)
- `eng/analyzers/` (5; 0 .cs)
- `.github/ISSUE_TEMPLATE/` (3; 0 .cs)
- `samples/Retries/` (3; 2 .cs)
- `samples/DependencyInjection/` (2; 1 .cs)
- `samples/Extensibility/` (2; 1 .cs)
- `samples/Intro/` (2; 1 .cs)
- `docs/v7/` (1; 0 .cs)

### README.md (start)
> **Note**
>
> **Important Announcement: Architectural changes in v8**
>
> Major performance improvements are on the way! Please see our [blog post](https://www.thepollyproject.org/2023/03/03/we-want-your-feedback-introducing-polly-v8/) to learn more and provide feedback in the [related GitHub issue](https://github.com/App-vNext/Polly/issues/1048).
>
> :rotating_light::rotating_light: **Polly v8 feature-complete!** :rotating_light::rotating_light:
> - Polly v8 Beta 1 is now available on [NuGet.org](https://www.nuget.org/packages/Polly/8.0.0-beta.1).
> - The Beta 1 version is considered feature-complete and the public API surface is stable.
> - Explore the [v8 documentation](https://github.com/App-vNext/Polly/blob/main/README_V8.md).
# Polly
Polly is a .NET resilience and transient-fault-handling library that allows developers to express policies such as Retry, Circuit Breaker, Timeout, Bulkhead Isolation, Rate-limiting and Fallback in a fluent and thread-safe manner.
Polly targets .NET Standard 1.1 ([coverage](https://docs.microsoft.com/en-us/dotnet/standard/net-standard#net-implementation-support): .NET Core 1.0, Mono, Xamarin, UWP, WP8.1+) and .NET Standard 2.0+ ([coverage](https://docs.microsoft.com/en-us/dotnet/standard/net-standard#net-implementation-support): .NET Core 2.0+, .NET Core 3.0, and later Mono, Xamarin and UWP targets). The NuGet package also includes direct targets for .NET Framework 4.6.1 and 4.7.2.
For versions supporting earlier targets such as .NET4.0 and .NET3.5, see the [supported targets](https://github.com/App-vNext/Polly/wiki/Supported-targets) grid.
[](https://www.dotnetfoundation.org/)
We are a member of the [.NET Foundation](https://www.dotnetfoundation.org/about)!
**Keep up to date with new feature announcements, tips & tricks, and other news through [www.thepollyproject.org](https://www.thepollyproject.org)**
## NuGet Packages
### Polly v7
### Polly v8 Pre-releases
| **Package** | **Latest Version** |
|:--|:--|
| Polly |  |
| Polly.Core |  |
| Polly.Extensions |  |
| Polly.RateLimiting |  |
| Polly.Testing |  |
## Get Started
### Installing via the .NET SDK
```sh
dotnet add package Polly
```
### Supported targets
For details of supported compilation targets by version, see the [supported targets](https://github.com/App-vNext/Polly/wiki/Supported-targets) grid.
### Role of the readme and the wiki
This ReadMe aims to give a quick overview of all Polly features - including enough to get you started with any policy.  For deeper detail on any policy, and many other aspects of Polly, be sure also to check out the [wiki documentation](https://github.com/App-vNext/Polly/wiki).
## Release notes
* The [changelog](https://github.com/App-vNext/Polly/blob/main/CHANGELOG.md) describes changes by release.
* We tag Pull Requests and Issues with [milestones](https://github.com/App-vNext/Polly/milestones) which match to NuGet package release numbers.
* Breaking changes are called out in the wiki ([v7](https://github.com/App-vNext/Polly/wiki/Polly-v7-breaking-changes); [v6](https://github.com/App-vNext/Polly/wiki/Polly-v6-breaking-changes)) with simple notes on any necessary steps to upgrade.
## Resilience policies
Polly offers multiple resilience policies.
In addition to the detailed pages on each policy, an [introduction to the role of each policy in resilience engineering](https://github.com/App-vNext/Polly/wiki/Transient-fault-handling-and-proactive-resilience-engineering)  is also provided in the wiki.
|Policy| Premise | Aka| How does the policy mitigate?|
| ------------- | ------------- |:-------------: |------------- |
|**Retry** (policy family)([quickstart](#retry)&nbsp;;&nbsp;[deep](https://github.com/App-vNext/Polly/wiki/Retry))|Many faults are transient and may self-correct after a short delay.| "Maybe it's just a blip" |  Allows configuring automatic retries. |
