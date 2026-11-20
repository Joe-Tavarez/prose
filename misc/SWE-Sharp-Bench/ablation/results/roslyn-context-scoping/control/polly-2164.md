## Repository overview (file tree and README, at the starting commit)
1006 tracked files, 785 .cs files, 21 .csproj files.

### Project files
- `bench/Polly.Benchmarks/Polly.Benchmarks.csproj`
- `bench/Polly.Core.Benchmarks/Polly.Core.Benchmarks.csproj`
- `samples/Retries/Retries.csproj`
- `src/Polly.Core/Polly.Core.csproj`
- `src/Polly.Extensions/Polly.Extensions.csproj`
- `src/Polly.RateLimiting/Polly.RateLimiting.csproj`
- `src/Polly.Testing/Polly.Testing.csproj`
- `src/Polly/Polly.csproj`
- `test/Polly.AotTest/Polly.AotTest.csproj`
- `test/Polly.Core.Tests/Polly.Core.Tests.csproj`
- `test/Polly.Extensions.Tests/Polly.Extensions.Tests.csproj`
- `test/Polly.RateLimiting.Tests/Polly.RateLimiting.Tests.csproj`
- `test/Polly.Specs/Polly.Specs.csproj`
- `test/Polly.TestUtils/Polly.TestUtils.csproj`
- `test/Polly.Testing.Tests/Polly.Testing.Tests.csproj`
- `samples/Chaos/Chaos.csproj`
- `samples/DependencyInjection/DependencyInjection.csproj`
- `samples/Extensibility/Extensibility.csproj`
- `samples/GenericPipelines/GenericPipelines.csproj`
- `samples/Intro/Intro.csproj`
- `src/Snippets/Snippets.csproj`

### Directories (files; .cs files), most relevant first
- `test/Polly.Specs/Retry/` (15; 15 .cs)
- `src/Polly.Core/Retry/` (9; 9 .cs)
- `src/Polly/Retry/` (9; 9 .cs)
- `test/Polly.Core.Tests/Retry/` (8; 8 .cs)
- `src/Polly.Core/` (179; 33 .cs)
- `src/Polly/` (176; 35 .cs)
- `test/Polly.Core.Tests/` (147; 19 .cs)
- `test/Polly.Specs/` (126; 10 .cs)
- `bench/Polly.Core.Benchmarks/` (31; 19 .cs)
- `src/Polly.Extensions/` (19; 0 .cs)
- `test/Polly.Extensions.Tests/` (18; 3 .cs)
- `bench/Polly.Benchmarks/` (13; 12 .cs)
- `test/Polly.TestUtils/` (13; 12 .cs)
- `src/Polly.RateLimiting/` (12; 8 .cs)
- `src/Polly.Testing/` (7; 3 .cs)
- `test/Polly.RateLimiting.Tests/` (7; 6 .cs)
- `samples/Retries/` (3; 2 .cs)
- `test/Polly.AotTest/` (2; 1 .cs)
- `test/Polly.Testing.Tests/` (2; 1 .cs)
- `test/Polly.Core.Tests/Simmy/` (38; 38 .cs)
- `src/Polly.Core/Simmy/` (34; 34 .cs)
- `test/Polly.Specs/Helpers/` (34; 34 .cs)
- `src/Polly.Core/Utils/` (30; 30 .cs)
- `src/Polly/Caching/` (29; 29 .cs)
- `src/Polly.Core/CircuitBreaker/` (23; 23 .cs)
- `src/Polly/CircuitBreaker/` (22; 22 .cs)
- `test/Polly.Core.Tests/Utils/` (19; 19 .cs)
- `test/Polly.Core.Tests/CircuitBreaker/` (18; 18 .cs)
- `test/Polly.Core.Tests/Hedging/` (15; 15 .cs)
- `test/Polly.Specs/Caching/` (14; 14 .cs)
- `src/Polly.Core/Hedging/` (13; 13 .cs)
- `src/Polly/RateLimit/` (13; 13 .cs)
- `bench/Polly.Core.Benchmarks/Utils/` (11; 11 .cs)
- `src/Polly/Bulkhead/` (11; 11 .cs)
- `src/Polly/Timeout/` (11; 11 .cs)
- `src/Polly/Utilities/` (11; 11 .cs)
- `src/Polly.Core/Telemetry/` (10; 10 .cs)
- `src/Polly.Extensions/Telemetry/` (10; 10 .cs)
- `src/Polly/Wrap/` (10; 10 .cs)
- `src/Polly/NoOp/` (9; 9 .cs)
- `test/Polly.Specs/CircuitBreaker/` (9; 9 .cs)
- `test/Polly.Specs/RateLimit/` (9; 9 .cs)
- `src/Polly.Core/Fallback/` (8; 8 .cs)
- `src/Polly.Core/Timeout/` (8; 8 .cs)
- `test/Polly.Specs/Bulkhead/` (8; 8 .cs)
- `src/Polly/Fallback/` (7; 7 .cs)
- `test/Polly.Core.Tests/Timeout/` (7; 7 .cs)
- `test/Polly.Extensions.Tests/Issues/` (7; 7 .cs)
- `src/Polly.Core/Registry/` (6; 6 .cs)
- `test/Polly.Core.Tests/Telemetry/` (6; 6 .cs)
- `test/Polly.Core.Tests/Fallback/` (5; 5 .cs)
- `test/Polly.Core.Tests/Issues/` (5; 5 .cs)
- `test/Polly.Core.Tests/Registry/` (5; 5 .cs)
- `test/Polly.Specs/Timeout/` (5; 5 .cs)
- `test/Polly.Specs/Wrap/` (5; 5 .cs)
- `src/Polly.Extensions/DependencyInjection/` (4; 4 .cs)
- `src/Polly/Registry/` (4; 4 .cs)
- `test/Polly.Extensions.Tests/Telemetry/` (4; 4 .cs)
- `test/Polly.Specs/Custom/` (4; 4 .cs)
- `test/Polly.Specs/Fallback/` (4; 4 .cs)
- `test/Polly.Specs/NoOp/` (4; 4 .cs)
- `test/Polly.Specs/Registry/` (3; 3 .cs)
- `src/Polly.Extensions/Registry/` (1; 1 .cs)
- `src/Polly/Properties/` (1; 1 .cs)
- `test/Polly.Core.Tests/Helpers/` (1; 1 .cs)
- `test/Polly.Extensions.Tests/DependencyInjection/` (1; 1 .cs)
- `test/Polly.Extensions.Tests/Registry/` (1; 1 .cs)
- `test/Polly.Extensions.Tests/Utils/` (1; 1 .cs)
- `test/Polly.Specs/Utilities/` (1; 1 .cs)
- `src/` (438; 0 .cs)
- `test/` (316; 0 .cs)
- `docs/` (67; 0 .cs)
- `bench/` (63; 0 .cs)
- `samples/` (39; 0 .cs)
- `.github/` (25; 0 .cs)
- `eng/` (17; 0 .cs)
- `logos/` (9; 0 .cs)
- `.vscode/` (4; 0 .cs)
- `.config/` (1; 0 .cs)
- `src/Snippets/` (36; 0 .cs)
- `docs/media/` (21; 0 .cs)
- `bench/BenchmarkDotNet.Artifacts/` (17; 0 .cs)
- `.github/workflows/` (14; 0 .cs)
- `samples/Extensibility/` (11; 1 .cs)
- `samples/Chaos/` (10; 5 .cs)
- `src/LegacySupport/` (9; 9 .cs)

### README.md (start)
# Polly
Polly is a .NET resilience and transient-fault-handling library that allows developers to express resilience strategies such as Retry, Circuit Breaker, Hedging, Timeout, Rate Limiter and Fallback in a fluent and thread-safe manner.
[](https://www.dotnetfoundation.org/)
We are a member of the [.NET Foundation](https://www.dotnetfoundation.org/about)!
**Keep up to date with new feature announcements, tips & tricks, and other news through [www.thepollyproject.org](https://www.thepollyproject.org)**
> [!IMPORTANT]
> This documentation describes the new Polly v8 API. If you are using the v7 API, please refer to the [previous version](https://github.com/App-vNext/Polly/tree/7.2.4) of the documentation.
## NuGet Packages
| **Package** | **Latest Version** | **About** |
|:--|:--|:--|
| `Polly.Core` |  | The core abstractions and [built-in strategies](https://www.pollydocs.org/strategies/index). |
| `Polly.Extensions` |  | [Telemetry](https://www.pollydocs.org/advanced/telemetry) and [dependency injection](https://www.pollydocs.org/advanced/dependency-injection) support. |
| `Polly.RateLimiting` |  | Integration with [`System.Threading.RateLimiting`](https://www.nuget.org/packages/System.Threading.RateLimiting) APIs. |
| `Polly.Testing` |  | [Testing support](https://www.pollydocs.org/advanced/testing) for Polly libraries. |
| `Polly` |  | This package contains the legacy API exposed by versions of the Polly library before version 8. |
## Documentation
This README aims to give a quick overview of some Polly features - including enough to get you started with any resilience strategy. For deeper detail on any resilience strategy, and many other aspects of Polly, be sure also to check out [pollydocs.org][polly-docs].
## Quick start
To use Polly, you must provide a callback and execute it using [**resilience pipeline**](https://www.pollydocs.org/pipelines). A resilience pipeline is a combination of one or more [**resilience strategies**](https://www.pollydocs.org/strategies) such as retry, timeout, and rate limiter. Polly uses **builders** to integrate these strategies into a pipeline.
To get started, first add the [Polly.Core](https://www.nuget.org/packages/Polly.Core/) package to your project by running the following command:
```sh
dotnet add package Polly.Core
```
You can create a `ResiliencePipeline` using the `ResiliencePipelineBuilder` class as shown below:
```cs
// Create an instance of builder that exposes various extensions for adding resilience strategies
ResiliencePipeline pipeline = new ResiliencePipelineBuilder()
    .AddRetry(new RetryStrategyOptions()) // Add retry using the default options
    .AddTimeout(TimeSpan.FromSeconds(10)) // Add 10 seconds timeout
    .Build(); // Builds the resilience pipeline
// Execute the pipeline asynchronously
await pipeline.ExecuteAsync(static async token => { /* Your custom logic goes here */ }, cancellationToken);
```
### Dependency injection
If you prefer to define resilience pipelines using [`IServiceCollection`](https://learn.microsoft.com/dotnet/api/microsoft.extensions.dependencyinjection.iservicecollection), you'll need to install the [Polly.Extensions](https://www.nuget.org/packages/Polly.Extensions/) package:
```sh
dotnet add package Polly.Extensions
```
You can then define your resilience pipeline using the `AddResiliencePipeline(...)` extension method as shown:
```cs
var services = new ServiceCollection();
// Define a resilience pipeline with the name "my-pipeline"
services.AddResiliencePipeline("my-pipeline", builder =>
{
    builder
        .AddRetry(new RetryStrategyOptions())
        .AddTimeout(TimeSpan.FromSeconds(10));
});
// Build the service provider
var serviceProvider = services.BuildServiceProvider();
// Retrieve a ResiliencePipelineProvider that dynamically creates and caches the resilience pipelines
var pipelineProvider = serviceProvider.GetRequiredService>();
// Retrieve your resilience pipeline using the name it was registered with
ResiliencePipeline pipeline = pipelineProvider.GetPipeline("my-pipeline");
// Alternatively, you can use keyed services to retrieve the resilience pipeline
pipeline = serviceProvider.GetRequiredKeyedService("my-pipeline");
// Execute the pipeline
await pipeline.ExecuteAsync(static async token =>
{
    // Your custom logic goes here
});
```
## Resilience strategies
Polly provides a variety of resilience strategies. Alongside the comprehensive guides for each strategy, the wiki also includes an [overview of the role each strategy plays in resilience engineering](https://github.com/App-vNext/Polly/wiki/Transient-fault-handling-and-proactive-resilience-engineering).
Polly categorizes resilience strategies into two main groups:
### Reactive
