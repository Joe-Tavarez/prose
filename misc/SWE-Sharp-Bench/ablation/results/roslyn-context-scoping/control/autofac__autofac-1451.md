## Repository overview (file tree and README, at the starting commit)
674 tracked files, 578 .cs files, 10 .csproj files.

### Project files
- `bench/Autofac.BenchmarkProfiling/Autofac.BenchmarkProfiling.csproj`
- `bench/Autofac.Benchmarks/Autofac.Benchmarks.csproj`
- `codegen/Autofac.CodeGen/Autofac.CodeGen.csproj`
- `src/Autofac/Autofac.csproj`
- `test/Autofac.Specification.Test/Autofac.Specification.Test.csproj`
- `test/Autofac.Test.CodeGen/Autofac.Test.CodeGen.csproj`
- `test/Autofac.Test.Compilation/Autofac.Test.Compilation.csproj`
- `test/Autofac.Test.Scenarios.LoadContext/Autofac.Test.Scenarios.LoadContext.csproj`
- `test/Autofac.Test.Scenarios.ScannedAssembly/Autofac.Test.Scenarios.ScannedAssembly.csproj`
- `test/Autofac.Test/Autofac.Test.csproj`

### Directories (files; .cs files), most relevant first
- `build/` (8; 0 .cs)
- `src/Autofac/Builder/` (22; 20 .cs)
- `test/Autofac.Test/Builder/` (6; 6 .cs)
- `test/Autofac.Specification.Test/Registration/` (20; 20 .cs)
- `src/` (309; 0 .cs)
- `test/` (290; 0 .cs)
- `bench/` (43; 0 .cs)
- `codegen/` (4; 0 .cs)
- `.vscode/` (3; 0 .cs)
- `.github/` (1; 0 .cs)
- `src/Autofac/` (309; 32 .cs)
- `test/Autofac.Test/` (142; 13 .cs)
- `test/Autofac.Specification.Test/` (83; 3 .cs)
- `test/Autofac.Test.Scenarios.ScannedAssembly/` (41; 33 .cs)
- `bench/Autofac.Benchmarks/` (40; 15 .cs)
- `test/Autofac.Test.CodeGen/` (8; 1 .cs)
- `test/Autofac.Test.Compilation/` (6; 5 .cs)
- `test/Shims/` (5; 0 .cs)
- `codegen/Autofac.CodeGen/` (4; 1 .cs)
- `test/Autofac.Test.Scenarios.LoadContext/` (4; 3 .cs)
- `bench/Autofac.BenchmarkProfiling/` (3; 1 .cs)
- `src/Autofac/Core/` (152; 128 .cs)
- `src/Autofac/Features/` (62; 47 .cs)
- `test/Autofac.Test/Features/` (43; 43 .cs)
- `test/Autofac.Test/Core/` (37; 37 .cs)
- `test/Autofac.Specification.Test/Features/` (27; 27 .cs)
- `test/Autofac.Test/Scenarios/` (26; 26 .cs)
- `bench/Autofac.Benchmarks/Decorators/` (23; 23 .cs)
- `src/Autofac/Util/` (21; 18 .cs)
- `test/Autofac.Specification.Test/Resolution/` (17; 17 .cs)
- `src/Autofac/Diagnostics/` (13; 12 .cs)
- `test/Autofac.Test/Util/` (12; 12 .cs)
- `test/Autofac.Specification.Test/Lifetime/` (11; 11 .cs)
- `test/Autofac.Test.Scenarios.ScannedAssembly/MetadataAttributeScanningScenario/` (6; 6 .cs)
- `test/Shims/required/` (5; 3 .cs)
- `test/Autofac.Test.CodeGen/Snapshots/` (3; 2 .cs)
- `test/Autofac.Test/Diagnostics/` (3; 3 .cs)
- `test/Autofac.Specification.Test/Diagnostics/` (2; 2 .cs)
- `test/Autofac.Specification.Test/Util/` (2; 2 .cs)
- `test/Autofac.Test.CodeGen/Helpers/` (2; 2 .cs)
- `bench/Autofac.BenchmarkProfiling/Properties/` (1; 0 .cs)
- `codegen/Autofac.CodeGen/Properties/` (1; 1 .cs)
- `src/Autofac/Properties/` (1; 1 .cs)
- `test/Autofac.Test.Scenarios.ScannedAssembly/Properties/` (1; 1 .cs)
- `test/Autofac.Test/Concurrency/` (1; 1 .cs)

### README.md (start)
Autofac is an [IoC container](http://martinfowler.com/articles/injection.html) for Microsoft .NET. It manages the dependencies between classes so that **applications stay easy to change as they grow** in size and complexity. This is achieved by treating regular .NET classes as *[components](https://autofac.readthedocs.io/en/latest/glossary.html)*.
## Get Packages
You can get Autofac by [grabbing the latest NuGet package](https://www.nuget.org/packages/Autofac/). There are several [application integration and extended functionality packages to choose from](https://www.nuget.org/profiles/Autofac). If you're feeling adventurous, [continuous integration builds are on MyGet](https://www.myget.org/gallery/autofac).
[Release notes are available on GitHub](https://github.com/autofac/Autofac/releases).
## Get Help
**Need help with Autofac?** We have [a documentation site](https://autofac.readthedocs.io/) as well as [API documentation](https://autofac.org/apidoc/). We're ready to answer your questions on [Stack Overflow](https://stackoverflow.com/questions/tagged/autofac) or check out the [discussion forum](https://groups.google.com/forum/#forum/autofac).
## Get Started
Our [Getting Started](https://autofac.readthedocs.io/en/latest/getting-started/index.html) tutorial walks you through integrating Autofac with a simple application and gives you some starting points for learning more.
Super-duper quick start:
[Register components with a `ContainerBuilder`](https://autofac.readthedocs.io/en/latest/register/registration.html) and then build the component container.
```csharp
var builder = new ContainerBuilder();
builder.Register(c => new TaskController(c.Resolve()));
builder.RegisterType();
builder.RegisterInstance(new TaskController());
builder.RegisterAssemblyTypes(controllerAssembly);
var container = builder.Build();
```
[Resolve services from a lifetime scope](https://autofac.readthedocs.io/en/latest/resolve/index.html) - either the container or a nested scope:
```csharp
var taskController = container.Resolve();
```
There is a growing number of [application integration libraries](https://autofac.readthedocs.io/en/latest/integration/index.html) that make using Autofac with your application a snap. Support for several popular frameworks is also available through the "Extras" packages.
**[Intrigued? Check out our Getting Started walkthrough!](https://autofac.readthedocs.io/en/latest/getting-started/index.html)**
## Project
Autofac is licensed under the MIT license, so you can comfortably use it in commercial applications (we still love [contributions](https://autofac.readthedocs.io/en/latest/contributors.html) though).
**File issues in the repo with the associated feature/code.**
- [Autofac](https://github.com/autofac/Autofac) - Core dependency resolution and common functions (this repo).
- [Autofac.AspNetCore.Multitenant](https://github.com/autofac/Autofac.AspNetCore.Multitenant) - Multitenant DI support for ASP.NET Core applications.
- [Autofac.Configuration](https://github.com/autofac/Autofac.Configuration) - JSON/XML file-based configuration support.
- [Autofac.Diagnostics.DotGraph](https://github.com/autofac/Autofac.Diagnostics.DotGraph) - Diagnostics support to enable DOT graph visualization of resolve requests.
- [Autofac.Extensions.DependencyInjection](https://github.com/autofac/Autofac.Extensions.DependencyInjection) - .NET Core integration for Autofac.
- [Autofac.Extras.AggregateService](https://github.com/autofac/Autofac.Extras.AggregateService) - Dynamic aggregate service implementation generation.
- [Autofac.Extras.AttributeMetadata](https://github.com/autofac/Autofac.Extras.AttributeMetadata) - Metadata scanning/filtering through attributes.
- [Autofac.Extras.CommonServiceLocator](https://github.com/autofac/Autofac.Extras.CommonServiceLocator) - Common Service Locator implementation backed by Autofac.
- [Autofac.Extras.DynamicProxy](https://github.com/autofac/Autofac.Extras.DynamicProxy) - Decorators and interceptors.
- [Autofac.Extras.FakeItEasy](https://github.com/autofac/Autofac.Extras.FakeItEasy) - FakeItEasy mocking framework integration.
- [Autofac.Extras.Moq](https://github.com/autofac/Autofac.Extras.Moq) - Moq mocking framework integration.
- [Autofac.Mef](https://github.com/autofac/Autofac.Mef) - MEF catalog integration.
- [Autofac.Multitenant](https://github.com/autofac/Autofac.Multitenant) - Multitenant dependency resolution support.
- [Autofac.Multitenant.Wcf](https://github.com/autofac/Autofac.Multitenant.Wcf) - Multitenant WCF service hosting.
- [Autofac.Mvc](https://github.com/autofac/Autofac.Mvc) - ASP.NET MVC integration.
- [Autofac.Mvc.Owin](https://github.com/autofac/Autofac.Mvc.Owin) - OWIN support for ASP.NET MVC.
- [Autofac.Owin](https://github.com/autofac/Autofac.Owin) - Core OWIN support - shared middleware for request lifetime integration.
- [Autofac.Pooling](https://github.com/autofac/Autofac.Pooling) - Support for pooled instance lifetime scopes.
- [Autofac.ServiceFabric](https://github.com/autofac/Autofac.ServiceFabric) - Application integration for Service Fabric services.
- [Autofac.SignalR](https://github.com/autofac/Autofac.SignalR) - Application integration for SignalR.
- [Autofac.Wcf](https://github.com/autofac/Autofac.Wcf) - WCF service hosting.
- [Autofac.Web](https://github.com/autofac/Autofac.Web) - ASP.NET web forms integration.
- [Autofac.WebApi](https://github.com/autofac/Autofac.WebApi) - Application integration for Web API.
- [Autofac.WebApi.Owin](https://github.com/autofac/Autofac.WebApi.Owin) - OWIN support for Web API.
## Sponsors
Autofac is supported by AWS. Thanks for your contribution!
## Contributing / Pull Requests
Refer to the [Contributor Guide](https://github.com/autofac/.github/blob/master/CONTRIBUTING.md) for setting up and building Autofac source.
You can also open this repository right now [in VS Code](https://open.vscode.dev/autofac/Autofac).
