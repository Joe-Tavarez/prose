## Repository map (from Roslyn, at the starting commit; declarations only)
Solution `Polly.sln`, .NET SDK 7.0.403, 13 C# projects (5 test). Projects are listed most relevant to the issue first.

### Projects
- Polly.Specs (`test/Polly.Specs/Polly.Specs.csproj`; net6.0, net7.0) — tests Polly, Polly.Core, Polly.TestUtils
- **Polly.Core** (`src/Polly.Core/Polly.Core.csproj`; net462, net472, net6.0, net7.0, netstandard2.0) → no project refs; 71 public types; ns Polly, Polly.CircuitBreaker, Polly.Utils
- **Polly** (`src/Polly/Polly.csproj`; net462, net472, net6.0, net7.0, netstandard2.0) → Polly.Core; 131 public types; ns Polly, Polly.Caching, Polly.CircuitBreaker
- **Polly.Core.Benchmarks** (`bench/Polly.Core.Benchmarks/Polly.Core.Benchmarks.csproj`; net7.0) → Polly, Polly.Core, Polly.Extensions, Polly.RateLimiting; 19 public types; ns Polly.Core.Benchmarks, Polly.Core.Benchmarks.Utils, (global)
- **Polly.TestUtils** (`test/Polly.TestUtils/Polly.TestUtils.csproj`; net6.0, net7.0) → Polly.Core; 10 public types; ns Polly.TestUtils
- **Polly.Benchmarks** (`bench/Polly.Benchmarks/Polly.Benchmarks.csproj`; net6.0, net7.0) → Polly, Polly.Core; 9 public types; ns Polly.Benchmarks, (global)
- **Polly.Extensions** (`src/Polly.Extensions/Polly.Extensions.csproj`; net462, net472, net6.0, net7.0, netstandard2.0) → Polly.Core; 7 public types; ns System.Diagnostics.CodeAnalysis, Polly.Telemetry, Polly
- **Polly.RateLimiting** (`src/Polly.RateLimiting/Polly.RateLimiting.csproj`; net462, net472, net6.0, net7.0, netstandard2.0) → Polly.Core; 5 public types; ns System.Diagnostics.CodeAnalysis, Polly.RateLimiting, Polly.Utils
- **Polly.Testing** (`src/Polly.Testing/Polly.Testing.csproj`; netstandard2.0) → Polly.Core; 3 public types; ns Polly.Testing
- Polly.Core.Tests (`test/Polly.Core.Tests/Polly.Core.Tests.csproj`; net6.0, net7.0) — tests Polly.Core, Polly.TestUtils, Polly.Testing
- Polly.Extensions.Tests (`test/Polly.Extensions.Tests/Polly.Extensions.Tests.csproj`; net6.0, net7.0) — tests Polly.Core, Polly.Extensions, Polly.RateLimiting, Polly.TestUtils
- Polly.RateLimiting.Tests (`test/Polly.RateLimiting.Tests/Polly.RateLimiting.Tests.csproj`; net6.0, net7.0) — tests Polly.Core, Polly.RateLimiting, Polly.TestUtils, Polly.Testing
- Polly.Testing.Tests (`test/Polly.Testing.Tests/Polly.Testing.Tests.csproj`; net6.0, net7.0) — tests Polly.Core, Polly.Extensions, Polly.RateLimiting, Polly.Testing

### Key public types (members abbreviated)
- Polly.Core: `class CircuitBreakerManualControl` (src/Polly.Core/CircuitBreaker/CircuitBreakerManualControl.cs)
  CircuitBreakerManualControl(); CircuitBreakerManualControl(bool isIsolated); Task IsolateAsync(CancellationToken cancellationToken); Task CloseAsync(CancellationToken cancellationToken)
- Polly: `abstract class Policy : PolicyBase, ISyncPolicy` (src/Polly/Bulkhead/AsyncBulkheadSyntax.cs)
  static AsyncBulkheadPolicy BulkheadAsync(int maxParallelization); static AsyncBulkheadPolicy BulkheadAsync(int maxParallelization, Func<Context, Task> onBulkheadRejectedAsync); static AsyncBulkheadPolicy BulkheadAsync(int maxParallelization, int maxQueuingActions); static AsyncBulkheadPolicy BulkheadAsync(int maxParallelization, int maxQueuingActions, Func<Context, Task> onBulkheadRejectedAsync); … +248
- Polly.Core.Benchmarks: `class MultipleStrategiesBenchmark` (bench/Polly.Core.Benchmarks/MultipleStrategiesBenchmark.cs)
  void Setup(); void Cleanup(); ValueTask ExecuteStrategyPipeline_Generic_V7(); ValueTask ExecuteStrategyPipeline_Generic_V8(); … +3
- Polly.TestUtils: `static class TestUtilities` (test/Polly.TestUtils/TestUtilities.cs)
  static Task AssertWithTimeoutAsync(Func<Task> assertion); static Task AssertWithTimeoutAsync(Action assertion); static Task AssertWithTimeoutAsync(Func<Task> assertion, TimeSpan timeout); static ResilienceStrategyTelemetry CreateResilienceTelemetry(TelemetryListener listener, ResilienceTelemetrySource source); … +6
- Polly.Benchmarks: `class Retry` (bench/Polly.Benchmarks/Retry.cs)
  void Retry_Synchronous_Succeeds(); Task Retry_Asynchronous_Succeeds(); Task Retry_Asynchronous_Succeeds_With_CancellationToken(); int Retry_Synchronous_With_Result_Succeeds(); … +4
- Polly.Extensions: `abstract class MeteringEnricher` (src/Polly.Extensions/Telemetry/MeteringEnricher.cs)
  abstract void Enrich<TResult, TArgs>(in EnrichmentContext<TResult, TArgs> context)
- Polly.RateLimiting: `class RateLimiterRejectedException : ExecutionRejectedException` (src/Polly.RateLimiting/RateLimiterRejectedException.cs)
  RateLimiterRejectedException(); RateLimiterRejectedException(TimeSpan retryAfter); RateLimiterRejectedException(string message); RateLimiterRejectedException(string message, TimeSpan retryAfter); … +4
- Polly.Testing: `class ResiliencePipelineDescriptor` (src/Polly.Testing/ResiliencePipelineDescriptor.cs)
  IReadOnlyList<ResilienceStrategyDescriptor> Strategies { get; }; ResilienceStrategyDescriptor FirstStrategy { get; }; bool IsReloadable { get; }
- Polly.Core: `abstract class ResilienceStrategy` (src/Polly.Core/ResilienceStrategy.cs)
  protected abstract ValueTask<Outcome<TResult>> ExecuteCore<TResult, TState>(Func<ResilienceContext, TState, ValueTask<Outcome<TResult>>> callback, ResilienceContext context, TState state)
- Polly: `abstract class AsyncPolicy : PolicyBase, IAsyncPolicy` (src/Polly/AsyncPolicy.ContextAndKeys.cs)
  AsyncPolicy WithPolicyKey(string policyKey); protected AsyncPolicy(PolicyBuilder policyBuilder); Task ExecuteAsync(Func<Task> action); Task ExecuteAsync(Func<Context, Task> action, IDictionary<string, object> contextData); … +38
- Polly.Core.Benchmarks: `class ResiliencePipelineBenchmark` (bench/Polly.Core.Benchmarks/ResiliencePipelineBenchmark.cs)
  ValueTask ExecuteOutcomeAsync(); ValueTask ExecuteAsync_ResilienceContextAndState(); ValueTask ExecuteAsync_CancellationToken(); ValueTask ExecuteAsync_GenericStrategy_CancellationToken(); … +3
- Polly.TestUtils: `static class OutcomeExtensions` (test/Polly.TestUtils/OutcomeExtensions.cs)
  static ValueTask<bool> ResultPredicateAsync<TResult>(this Outcome<object> outcome, TResult result); static ValueTask<bool> ResultPredicateAsync<TResult>(this Outcome<object> outcome, Predicate<TResult> predicate); static bool ResultPredicate<TResult>(this Outcome<object> outcome, TResult result); static bool ResultPredicate<TResult>(this Outcome<object> outcome, Predicate<TResult> predicate); … +4
- Polly.Benchmarks: `class Timeout` (bench/Polly.Benchmarks/Timeout.cs)
  void Timeout_Synchronous_Succeeds(); Task Timeout_Asynchronous_Succeeds(); Task Timeout_Asynchronous_Succeeds_With_CancellationToken(); int Timeout_Synchronous_With_Result_Succeeds(); … +3
- Polly.Extensions: `static class PollyServiceCollectionExtensions` (src/Polly.Extensions/DependencyInjection/PollyServiceCollectionExtensions.cs)
  static IServiceCollection AddResiliencePipeline<TKey, TResult>(this IServiceCollection services, TKey key, Action<ResiliencePipelineBuilder<TResult>> configure); static IServiceCollection AddResiliencePipeline<TKey, TResult>(this IServiceCollection services, TKey key, Action<ResiliencePipelineBuilder<TResult>, AddResiliencePipelineContext<TKey>> configure); static IServiceCollection AddResiliencePipeline<TKey>(this IServiceCollection services, TKey key, Action<ResiliencePipelineBuilder> configure); static IServiceCollection AddResiliencePipeline<TKey>(this IServiceCollection services, TKey key, Action<ResiliencePipelineBuilder, AddResiliencePipelineContext<TKey>> configure); … +2
- Polly.RateLimiting: `static class RateLimiterResiliencePipelineBuilderExtensions` (src/Polly.RateLimiting/RateLimiterResiliencePipelineBuilderExtensions.cs)
  static TBuilder AddConcurrencyLimiter<TBuilder>(this TBuilder builder, int permitLimit, int queueLimit); static TBuilder AddConcurrencyLimiter<TBuilder>(this TBuilder builder, ConcurrencyLimiterOptions options); static TBuilder AddRateLimiter<TBuilder>(this TBuilder builder, RateLimiter limiter); static TBuilder AddRateLimiter<TBuilder>(this TBuilder builder, RateLimiterStrategyOptions options)
- Polly.Testing: `static class ResiliencePipelineExtensions` (src/Polly.Testing/ResiliencePipelineExtensions.cs)
  static ResiliencePipelineDescriptor GetPipelineDescriptor<TResult>(this ResiliencePipeline<TResult> pipeline); static ResiliencePipelineDescriptor GetPipelineDescriptor(this ResiliencePipeline pipeline)
- Polly.Core: `abstract class ResilienceStrategyOptions` (src/Polly.Core/ResilienceStrategyOptions.cs)
  string Name { get; set; }
- Polly: `abstract class AsyncPolicy<TResult> : PolicyBase<TResult>, IAsyncPolicy<TResult>` (src/Polly/AsyncPolicy.ContextAndKeys.cs)
  AsyncPolicy<TResult> WithPolicyKey(string policyKey); protected abstract Task<TResult> ImplementationAsync(Func<Context, CancellationToken, Task<TResult>> action, Context context, CancellationToken cancellationToken, bool continueOnCapturedContext); protected AsyncPolicy(PolicyBuilder<TResult> policyBuilder); Task<TResult> ExecuteAsync(Func<Task<TResult>> action); … +19
- Polly.Core.Benchmarks: `class HedgingBenchmark` (bench/Polly.Core.Benchmarks/HedgingBenchmark.cs)
  void Setup(); ValueTask Hedging_Primary(); ValueTask Hedging_Secondary(); ValueTask Hedging_Primary_AsyncWork(); … +1
- Polly.TestUtils: `class FakeLogger : ILogger` (test/Polly.TestUtils/FakeLogger.cs)
  bool Enabled { get; set; }; IEnumerable<LogRecord> GetRecords(); IEnumerable<LogRecord> GetRecords(EventId eventId); IDisposable BeginScope<TState>(TState state); … +2
- Polly.Benchmarks: `class Bulkhead` (bench/Polly.Benchmarks/Bulkhead.cs)
  void Bulkhead_Synchronous(); Task Bulkhead_Asynchronous(); Task Bulkhead_Asynchronous_With_CancellationToken(); int Bulkhead_Synchronous_With_Result(); … +2
- Polly.Extensions: `class AddResiliencePipelineContext<TKey>` (src/Polly.Extensions/DependencyInjection/AddResiliencePipelineContext.cs)
  TKey PipelineKey { get; }; IServiceProvider ServiceProvider { get; }; void EnableReloads<TOptions>(string name); TOptions GetOptions<TOptions>(string name); … +1
- Polly.RateLimiting: `class RateLimiterStrategyOptions : ResilienceStrategyOptions` (src/Polly.RateLimiting/RateLimiterStrategyOptions.cs)
  RateLimiterStrategyOptions(); ConcurrencyLimiterOptions DefaultRateLimiterOptions { get; set; }; Func<OnRateLimiterRejectedArguments, ValueTask> OnRejected { get; set; }; Func<RateLimiterArguments, ValueTask<RateLimitLease>> RateLimiter { get; set; }
- Polly.Testing: `class ResilienceStrategyDescriptor` (src/Polly.Testing/ResilienceStrategyDescriptor.cs)
  ResilienceStrategyOptions Options { get; }; object StrategyInstance { get; }
- Polly.Core: `abstract class ExecutionRejectedException : Exception` (src/Polly.Core/ExecutionRejectedException.cs)
  protected ExecutionRejectedException(); protected ExecutionRejectedException(string message); protected ExecutionRejectedException(string message, Exception inner); protected ExecutionRejectedException(SerializationInfo info, StreamingContext context)
- Polly: `abstract class Policy<TResult> : PolicyBase<TResult>, ISyncPolicy<TResult>` (src/Polly/Policy.ContextAndKeys.cs)
  Policy<TResult> WithPolicyKey(string policyKey); static PolicyBuilder<TResult> Handle<TException>(); static PolicyBuilder<TResult> Handle<TException>(Func<TException, bool> exceptionPredicate); static PolicyBuilder<TResult> HandleInner<TException>(); … +19
- Polly.Core.Benchmarks: `class TelemetryBenchmark` (bench/Polly.Core.Benchmarks/TelemetryBenchmark.cs)
  void Prepare(); void Cleanup(); bool Telemetry { get; set; }; bool Enrichment { get; set; }; … +1
- Polly.TestUtils: `record LogRecord : IEquatable<LogRecord>` (test/Polly.TestUtils/LogRecord.cs)
  LogRecord(LogLevel LogLevel, EventId EventId, string Message, Exception Exception, object State); LogLevel LogLevel { get; init; }; EventId EventId { get; init; }; string Message { get; init; }; … +2
- Polly.Benchmarks: `class Cache` (bench/Polly.Benchmarks/Cache.cs)
  Task GlobalSetup(); object Cache_Synchronous_Hit(); Task<object> Cache_Asynchronous_Hit(); object Cache_Synchronous_Miss(); … +1
