## Repository overview (file tree and README, at the starting commit)
250 tracked files, 186 .cs files, 5 .csproj files.

### Project files
- `test/Serilog.PerformanceTests/Serilog.PerformanceTests.csproj`
- `src/Serilog/Serilog.csproj`
- `test/Serilog.ApprovalTests/Serilog.ApprovalTests.csproj`
- `test/Serilog.Tests/Serilog.Tests.csproj`
- `test/TestDummies/TestDummies.csproj`

### Directories (files; .cs files), most relevant first
- `test/Serilog.PerformanceTests/` (23; 13 .cs)
- `test/Serilog.PerformanceTests/Support/` (6; 6 .cs)
- `src/Serilog/Context/` (3; 3 .cs)
- `test/Serilog.PerformanceTests/MessageTemplateCacheBenchmark/` (2; 2 .cs)
- `test/Serilog.Tests/Context/` (1; 1 .cs)
- `src/` (99; 0 .cs)
- `test/` (94; 0 .cs)
- `results/` (30; 0 .cs)
- `.github/` (3; 0 .cs)
- `assets/` (3; 0 .cs)
- `src/Serilog/` (99; 6 .cs)
- `test/Serilog.Tests/` (52; 5 .cs)
- `test/TestDummies/` (16; 10 .cs)
- `results/netcoreapp2.0/` (11; 0 .cs)
- `results/net4.5.2/` (8; 0 .cs)
- `results/netcoreapp1.0/` (8; 0 .cs)
- `.github/ISSUE_TEMPLATE/` (3; 0 .cs)
- `test/Serilog.ApprovalTests/` (3; 1 .cs)
- `results/net46/` (1; 0 .cs)
- `results/netcoreapp1.1/` (1; 0 .cs)
- `results/netcoreapp3.1/` (1; 0 .cs)
- `src/Serilog/Core/` (30; 30 .cs)
- `test/Serilog.Tests/Support/` (18; 18 .cs)
- `src/Serilog/Events/` (11; 11 .cs)
- `test/Serilog.Tests/Core/` (11; 11 .cs)
- `src/Serilog/Configuration/` (8; 8 .cs)
- `src/Serilog/Formatting/` (7; 7 .cs)
- `src/Serilog/Parsing/` (7; 7 .cs)
- `src/Serilog/Policies/` (7; 7 .cs)
- `src/Serilog/Capturing/` (5; 5 .cs)
- `test/TestDummies/Console/` (5; 5 .cs)
- `src/Serilog/Rendering/` (4; 4 .cs)
- `src/Serilog/Settings/` (4; 4 .cs)
- `test/Serilog.Tests/Formatting/` (3; 3 .cs)
- `test/Serilog.Tests/Settings/` (3; 3 .cs)
- `results/net4.5.2/MessageTemplateCache/` (2; 0 .cs)
- `results/netcoreapp1.0/MessageTemplateCache/` (2; 0 .cs)
- `src/Serilog/Data/` (2; 2 .cs)
- `src/Serilog/Debugging/` (2; 2 .cs)
- `test/Serilog.Tests/Capturing/` (2; 2 .cs)
- `test/Serilog.Tests/Events/` (2; 2 .cs)
- `src/Serilog/Filters/` (1; 1 .cs)
- `src/Serilog/Properties/` (1; 1 .cs)
- `test/Serilog.Tests/Data/` (1; 1 .cs)
- `test/Serilog.Tests/Debugging/` (1; 1 .cs)
- `test/Serilog.Tests/Filters/` (1; 1 .cs)
- `test/Serilog.Tests/Parsing/` (1; 1 .cs)
- `test/Serilog.Tests/Properties/` (1; 1 .cs)
- `test/Serilog.Tests/Rendering/` (1; 1 .cs)

### README.md (start)
# Serilog
Serilog is a diagnostic logging library for .NET applications. It is easy to set up, has a clean API, and runs on all recent .NET platforms. While it's useful even in the simplest applications, Serilog's support for structured logging shines when instrumenting complex, distributed, and asynchronous applications and systems.
Like many other libraries for .NET, Serilog provides diagnostic logging to [files](https://github.com/serilog/serilog-sinks-file), the [console](https://github.com/serilog/serilog-sinks-console), and [many other outputs](https://github.com/serilog/serilog/wiki/Provided-Sinks).
```csharp
var log = new LoggerConfiguration()
    .WriteTo.Console()
    .WriteTo.File("log.txt")
    .CreateLogger();
log.Information("Hello, Serilog!");
```
Unlike other logging libraries, Serilog is built from the ground up to record _structured event data_.
```csharp
var position = new { Latitude = 25, Longitude = 134 };
var elapsedMs = 34;
log.Information("Processed {@Position} in {Elapsed} ms", position, elapsedMs);
```
Serilog uses [message templates](https://messagetemplates.org), a simple DSL that extends .NET format strings with _named_ as well as positional parameters. Instead of formatting events immediately into text, Serilog captures the values associated with each named parameter.
The example above records two properties, `Position` and `Elapsed`, in the log event. The `@` operator in front of `Position` tells Serilog to _serialize_ the object passed in, rather than convert it using `ToString()`. Serilog's deep and rich support for structured event data opens up a huge range of diagnostic possibilities not available when using traditional loggers.
Rendered into [JSON format](https://github.com/serilog/serilog-formatting-compact) for example, these properties appear alongside the timestamp, level, and message like:
```json
{"Position": {"Latitude": 25, "Longitude": 134}, "Elapsed": 34}
```
Back-ends that are capable of recording structured event data make log searches and analysis possible without log parsing or regular expressions.
Supporting structured data doesn't mean giving up text: when Serilog writes events to files or the console, the template and properties are rendered into friendly human-readable text just like a traditional logging library would produce:
```
09:14:22 [INF] Processed {"Latitude": 25, "Longitude": 134} in 34 ms.
```
> **Upgrading from Serilog 1.x?** Check out the [2.0 Upgrade Guide](https://github.com/serilog/serilog/wiki/2.x-Upgrade-Guide) and [Release Notes](https://github.com/serilog/serilog/blob/dev/CHANGES.md).
### Features
 * **Community-backed and actively developed**
 * Format-based logging API with familiar [levels](https://github.com/serilog/serilog/wiki/Configuration-Basics#minimum-level) like `Debug`, `Information`, `Warning`, `Error`, and so-on
 * Discoverable C# configuration syntax and optional [XML](https://github.com/serilog/serilog-settings-appsettings) or [JSON](https://github.com/serilog/serilog-settings-configuration) configuration support
 * Efficient when enabled, extremely low overhead when a logging level is switched off
 * Best-in-class .NET Core support, including [rich integration with ASP.NET Core](https://github.com/serilog/serilog-aspnetcore)
 * Support for a [comprehensive range of sinks](https://github.com/serilog/serilog/wiki/Provided-Sinks), including files, the console, on-premises and cloud-based log servers, databases, and message queues
 * Sophisticated [enrichment](https://github.com/serilog/serilog/wiki/Enrichment) of log events with contextual information, including scoped (`LogContext`) properties, thread and process identifiers, and domain-specific correlation ids such as `HttpRequestId`
 * Zero-shared-state `Logger` objects, with an optional global static `Log` class
 * Format-agnostic logging pipeline that can emit events in plain text, JSON, in-memory `LogEvent` objects (including [Rx pipelines](https://github.com/serilog/serilog-sinks-observable)) and other formats
### Getting started
Serilog is installed from NuGet. To view log events, one or more sinks need to be installed as well, here we'll use the pretty-printing console sink, and a rolling file set:
```
dotnet add package Serilog
dotnet add package Serilog.Sinks.Console
dotnet add package Serilog.Sinks.File
```
The simplest way to set up Serilog is using the static `Log` class. A `LoggerConfiguration` is used to create and assign the default logger.
```csharp
using Serilog;
public class Program
{
    public static void Main()
    {
        Log.Logger = new LoggerConfiguration()
            .MinimumLevel.Information()
            .WriteTo.Console()
            .WriteTo.File("log.txt",
                rollingInterval: RollingInterval.Day,
                rollOnFileSizeLimit: true)
            .CreateLogger();
        Log.Information("Hello, Serilog!");
        Log.CloseAndFlush();
    }
}
```
Find more, including a runnable example application, under the [Getting Started topic](https://github.com/serilog/serilog/wiki/Getting-Started) in the [documentation](https://github.com/serilog/serilog/wiki/).
### Getting help
To learn more about Serilog, check out the [documentation](https://github.com/serilog/serilog/wiki) - you'll find information there on the most common scenarios. If Serilog isn't working the way you expect, you may find the [troubleshooting guide](https://github.com/serilog/serilog/wiki/Debugging-and-Diagnostics) useful.
Serilog has an active and helpful community who are happy to help point you in the right direction or work through any issues you might encounter. You can get in touch via:
 * [Stack Overflow](http://stackoverflow.com/questions/tagged/serilog) &mdash; this is the best place to start if you have a question
 * [Gitter chat](https://gitter.im/serilog/serilog)
 * The [#serilog tag on Twitter](https://twitter.com/search?q=%23serilog)
 * [Serilog-related courses on Pluralsight](https://www.pluralsight.com/search/?q=serilog)
We welcome bug reports and suggestions through our [issue tracker](https://github.com/serilog/serilog/issues) here on GitHub.
### Contributing
Would you like to help make Serilog even better? We keep a list of issues that are approachable for newcomers under the [up-for-grabs](https://github.com/issues?utf8=✓&q=is%3Aopen+is%3Aissue+archived%3Afalse+user%3Aserilog+label%3Aup-for-grabs) label (accessible only when logged into GitHub). Before starting work on a pull request, we suggest commenting on, or raising, an issue on the issue tracker so that we can help and coordinate efforts.  For more details check out our [contributing guide](CONTRIBUTING.md).
When contributing please keep in mind our [Code of Conduct](CODE_OF_CONDUCT.md).
### Detailed build status
Branch  | AppVeyor
------------- | -------------
`dev` |
`main` |
_Serilog is copyright &copy; 2013-2020 Serilog Contributors - Provided under the [Apache License, Version 2.0](http://apache.org/licenses/LICENSE-2.0.html). Needle and thread logo a derivative of work by [Kenneth Appiah](http://www.kensets.com/)._
