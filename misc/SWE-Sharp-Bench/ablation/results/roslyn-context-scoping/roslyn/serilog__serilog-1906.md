## Repository map (from Roslyn, at the starting commit; declarations only)
Solution `Serilog.sln`, .NET SDK 7.0.102, 5 C# projects (3 test). Projects are listed most relevant to the issue first.

### Projects
- **Serilog** (`src/Serilog/Serilog.csproj`; net5.0, net6.0, net7.0, netstandard2.0, netstandard2.1) → no project refs; 51 public types; ns Serilog.Core, Serilog.Events, Serilog.Configuration
- Serilog.Tests (`test/Serilog.Tests/Serilog.Tests.csproj`; net5.0, net6.0, net7.0, netcoreapp3.1) — tests Serilog, TestDummies
- Serilog.PerformanceTests (`test/Serilog.PerformanceTests/Serilog.PerformanceTests.csproj`; net7.0) — tests Serilog
- **TestDummies** (`test/TestDummies/TestDummies.csproj`; net462, netstandard2.0, netstandard2.1) → Serilog; 12 public types; ns TestDummies, TestDummies.Console.Themes, TestDummies.Console
- Serilog.ApprovalTests (`test/Serilog.ApprovalTests/Serilog.ApprovalTests.csproj`; net7.0) — tests Serilog

### Key public types (members abbreviated)
- Serilog: `class Logger : ILogger, ILogEventSink, IDisposable` (src/Serilog/Core/Logger.cs)
  ILogger ForContext(ILogEventEnricher enricher); ILogger ForContext(IEnumerable<ILogEventEnricher> enrichers); ILogger ForContext(string propertyName, object value, bool destructureObjects); ILogger ForContext(Type source); ILogger ForContext<TSource>(); void Write(LogEventLevel level, string messageTemplate); void Write<T>(LogEventLevel level, string messageTemplate, T propertyValue); void Write<T0, T1>(LogEventLevel level, string messageTemplate, T0 propertyValue0, T1 propertyValue1); … +74
- TestDummies: `static class DummyLoggerConfigurationExtensions` (test/TestDummies/DummyLoggerConfigurationExtensions.cs)
  static LoggerConfiguration WithDummyThreadId(this LoggerEnrichmentConfiguration enrich); static LoggerConfiguration DummyRollingFile(this LoggerSinkConfiguration loggerSinkConfiguration, string pathFormat, LogEventLevel restrictedToMinimumLevel, string outputTemplate, IFormatProvider formatProvider); static LoggerConfiguration DummyRollingFile(this LoggerSinkConfiguration loggerSinkConfiguration, ITextFormatter formatter, string pathFormat, LogEventLevel restrictedToMinimumLevel); static LoggerConfiguration DummyRollingFile(this LoggerAuditSinkConfiguration loggerSinkConfiguration, LogEventLevel restrictedToMinimumLevel); static LoggerConfiguration DummyWithLevelSwitch(this LoggerSinkConfiguration loggerSinkConfiguration, LogEventLevel restrictedToMinimumLevel, LoggingLevelSwitch controlLevelSwitch); static LoggerConfiguration DummyConsole(this LoggerSinkConfiguration loggerSinkConfiguration, LogEventLevel restrictedToMinimumLevel, ConsoleTheme theme); static LoggerConfiguration Dummy(this LoggerSinkConfiguration loggerSinkConfiguration, Action<LoggerSinkConfiguration> wrappedSinkAction); static LoggerConfiguration DummyWrap(this LoggerSinkConfiguration loggerSinkConfiguration, Action<LoggerSinkConfiguration> wrappedSinkAction, LogEventLevel logEventLevel, LoggingLevelSwitch levelSwitch); … +1
- Serilog: `interface ILogger` (src/Serilog/ILogger.cs)
  ILogger ForContext(ILogEventEnricher enricher); ILogger ForContext(IEnumerable<ILogEventEnricher> enrichers); ILogger ForContext(string propertyName, object value, bool destructureObjects); ILogger ForContext<TSource>(); ILogger ForContext(Type source); void Write(LogEvent logEvent); void Write(LogEventLevel level, string messageTemplate); void Write<T>(LogEventLevel level, string messageTemplate, T propertyValue); … +71
- TestDummies: `class DummyHardCodedStringDestructuringPolicy : IDestructuringPolicy` (test/TestDummies/DummyHardCodedStringDestructuringPolicy.cs)
  DummyHardCodedStringDestructuringPolicy(string hardCodedString); bool TryDestructure(object value, ILogEventPropertyValueFactory propertyValueFactory, out LogEventPropertyValue result)
- Serilog: `class LoggerSinkConfiguration` (src/Serilog/Configuration/LoggerSinkConfiguration.cs)
  LoggerConfiguration Sink(ILogEventSink logEventSink, LogEventLevel restrictedToMinimumLevel); LoggerConfiguration Sink(ILogEventSink logEventSink, LogEventLevel restrictedToMinimumLevel, LoggingLevelSwitch levelSwitch); LoggerConfiguration Sink<TSink>(LogEventLevel restrictedToMinimumLevel, LoggingLevelSwitch levelSwitch); LoggerConfiguration Logger(Action<LoggerConfiguration> configureLogger, LogEventLevel restrictedToMinimumLevel, LoggingLevelSwitch levelSwitch); LoggerConfiguration Logger(ILogger logger, LogEventLevel restrictedToMinimumLevel); LoggerConfiguration Logger(ILogger logger, bool attemptDispose, LogEventLevel restrictedToMinimumLevel, LoggingLevelSwitch levelSwitch); LoggerConfiguration Conditional(Func<LogEvent, bool> condition, Action<LoggerSinkConfiguration> configureSink); static LoggerConfiguration Wrap(LoggerSinkConfiguration loggerSinkConfiguration, Func<ILogEventSink, ILogEventSink> wrapSink, Action<LoggerSinkConfiguration> configureWrappedSink, LogEventLevel restrictedToMinimumLevel, LoggingLevelSwitch levelSwitch)
- TestDummies: `class DummyReduceVersionToMajorPolicy : IDestructuringPolicy` (test/TestDummies/DummyReduceVersionToMajorPolicy.cs)
  bool TryDestructure(object value, ILogEventPropertyValueFactory propertyValueFactory, out LogEventPropertyValue result)
- Serilog: `static class Log` (src/Serilog/Log.cs)
  static ILogger Logger { get; set; }; static void CloseAndFlush(); static ValueTask CloseAndFlushAsync(); static ILogger ForContext(ILogEventEnricher enricher); static ILogger ForContext(ILogEventEnricher[] enrichers); static ILogger ForContext(string propertyName, object value, bool destructureObjects); static ILogger ForContext<TSource>(); static ILogger ForContext(Type source); … +74
- TestDummies: `abstract class ConsoleTheme` (test/TestDummies/Console/Themes/ConsoleTheme.cs)
  static ConsoleTheme None { get; }
- Serilog: `class LoggerAuditSinkConfiguration` (src/Serilog/Configuration/LoggerAuditSinkConfiguration.cs)
  LoggerConfiguration Sink(ILogEventSink logEventSink, LogEventLevel restrictedToMinimumLevel, LoggingLevelSwitch levelSwitch); LoggerConfiguration Sink<TSink>(LogEventLevel restrictedToMinimumLevel, LoggingLevelSwitch levelSwitch); LoggerConfiguration Logger(Action<LoggerConfiguration> configureLogger, LogEventLevel restrictedToMinimumLevel, LoggingLevelSwitch levelSwitch); LoggerConfiguration Logger(ILogger logger, LogEventLevel restrictedToMinimumLevel)
- TestDummies: `class DummyWithLevelSwitchSink : ILogEventSink` (test/TestDummies/DummyWithLevelSwitchSink.cs)
  DummyWithLevelSwitchSink(LoggingLevelSwitch loggingControlLevelSwitch); static LoggingLevelSwitch ControlLevelSwitch; static List<LogEvent> Emitted; void Emit(LogEvent logEvent)
- Serilog: `class LoggerConfiguration` (src/Serilog/LoggerConfiguration.cs)
  LoggerConfiguration(); LoggerSinkConfiguration WriteTo { get; internal set; }; LoggerAuditSinkConfiguration AuditTo { get; }; LoggerMinimumLevelConfiguration MinimumLevel { get; }; LoggerEnrichmentConfiguration Enrich { get; internal set; }; LoggerFilterConfiguration Filter { get; }; LoggerDestructuringConfiguration Destructure { get; }; LoggerSettingsConfiguration ReadFrom { get; }; … +1
- TestDummies: `class DummyWrappingSink : ILogEventSink` (test/TestDummies/DummyWrappingSink.cs)
  static List<LogEvent> Emitted { get; }; DummyWrappingSink(ILogEventSink sink); void Emit(LogEvent logEvent); static void Reset()
- Serilog: `class LoggerMinimumLevelConfiguration` (src/Serilog/Configuration/LoggerMinimumLevelConfiguration.cs)
  LoggerConfiguration Is(LogEventLevel minimumLevel); LoggerConfiguration ControlledBy(LoggingLevelSwitch levelSwitch); LoggerConfiguration Verbose(); LoggerConfiguration Debug(); LoggerConfiguration Information(); LoggerConfiguration Warning(); LoggerConfiguration Error(); LoggerConfiguration Fatal(); … +2
- TestDummies: `class DummyConsoleSink : ILogEventSink` (test/TestDummies/Console/DummyConsoleSink.cs)
  DummyConsoleSink(ConsoleTheme theme); static ConsoleTheme Theme; void Emit(LogEvent logEvent)
- Serilog: `class DictionaryValue : LogEventPropertyValue` (src/Serilog/Events/DictionaryValue.cs)
  DictionaryValue(IEnumerable<KeyValuePair<ScalarValue, LogEventPropertyValue>> elements); IReadOnlyDictionary<ScalarValue, LogEventPropertyValue> Elements { get; }; override void Render(TextWriter output, string format, IFormatProvider formatProvider)
- TestDummies: `class DummyRollingFileAuditSink : ILogEventSink` (test/TestDummies/DummyRollingFileAuditSink.cs)
  static List<LogEvent> Emitted { get; }; void Emit(LogEvent logEvent); static void Reset()
- Serilog: `enum Destructuring` (src/Serilog/Parsing/Destructuring.cs)
  Default; Stringify; Destructure
- TestDummies: `class DummyRollingFileSink : ILogEventSink` (test/TestDummies/DummyRollingFileSink.cs)
  static List<LogEvent> Emitted { get; }; void Emit(LogEvent logEvent); static void Reset()
- Serilog: `enum LogEventLevel` (src/Serilog/Events/LogEventLevel.cs)
  Verbose; Debug; Information; Warning; Error; Fatal
- TestDummies: `static class ConsoleThemes` (test/TestDummies/Console/Themes/ConsoleThemes.cs)
  static ConsoleTheme Theme1 { get; }
- Serilog: `class LoggerEnrichmentConfiguration` (src/Serilog/Configuration/LoggerEnrichmentConfiguration.cs)
  LoggerConfiguration With(params ILogEventEnricher[] enrichers); LoggerConfiguration With<TEnricher>(); LoggerConfiguration WithProperty(string name, object value, bool destructureObjects); LoggerConfiguration FromLogContext(); LoggerConfiguration When(Func<LogEvent, bool> condition, Action<LoggerEnrichmentConfiguration> configureEnricher); LoggerConfiguration AtLevel(LogEventLevel enrichFromLevel, Action<LoggerEnrichmentConfiguration> configureEnricher); LoggerConfiguration AtLevel(LoggingLevelSwitch levelSwitch, Action<LoggerEnrichmentConfiguration> configureEnricher); static LoggerConfiguration Wrap(LoggerEnrichmentConfiguration loggerEnrichmentConfiguration, Func<ILogEventEnricher, ILogEventEnricher> wrapEnricher, Action<LoggerEnrichmentConfiguration> configureWrappedEnricher)
- TestDummies: `class DummyAnonymousUserFilter : ILogEventFilter` (test/TestDummies/DummyAnonymousUserFilter.cs)
  bool IsEnabled(LogEvent logEvent)
- Serilog: `class LoggerDestructuringConfiguration` (src/Serilog/Configuration/LoggerDestructuringConfiguration.cs)
  LoggerConfiguration AsScalar(Type scalarType); LoggerConfiguration AsScalar<TScalar>(); LoggerConfiguration With(params IDestructuringPolicy[] destructuringPolicies); LoggerConfiguration With<TDestructuringPolicy>(); LoggerConfiguration ByTransforming<TValue>(Func<TValue, object> transformation); LoggerConfiguration ByTransformingWhere<TValue>(Func<Type, bool> predicate, Func<TValue, object> transformation); LoggerConfiguration ToMaximumDepth(int maximumDestructuringDepth); LoggerConfiguration ToMaximumStringLength(int maximumStringLength); … +1
- TestDummies: `class DummyThreadIdEnricher : ILogEventEnricher` (test/TestDummies/DummyThreadIdEnricher.cs)
  void Enrich(LogEvent logEvent, ILogEventPropertyFactory propertyFactory)
- Serilog: `interface ILoggerSettings` (src/Serilog/Configuration/ILoggerSettings.cs)
  void Configure(LoggerConfiguration loggerConfiguration)
- Serilog: `class LoggerFilterConfiguration` (src/Serilog/Configuration/LoggerFilterConfiguration.cs)
  LoggerConfiguration With(params ILogEventFilter[] filters); LoggerConfiguration With<TFilter>(); LoggerConfiguration ByExcluding(Func<LogEvent, bool> exclusionPredicate); LoggerConfiguration ByIncludingOnly(Func<LogEvent, bool> inclusionPredicate)
- Serilog: `class LoggerSettingsConfiguration` (src/Serilog/Configuration/LoggerSettingsConfiguration.cs)
  LoggerConfiguration Settings(ILoggerSettings settings); LoggerConfiguration KeyValuePairs(IEnumerable<KeyValuePair<string, string>> settings)
- Serilog: `static class LoggerExtensions` (src/Serilog/LoggerExtensions.cs)
  static ILogger ForContext<TValue>(this ILogger logger, LogEventLevel level, string propertyName, TValue value, bool destructureObjects)
- Serilog: `abstract class LogEventPropertyValueVisitor<TState, TResult>` (src/Serilog/Data/LogEventPropertyValueVisitor.cs)
  protected virtual TResult Visit(TState state, LogEventPropertyValue value); protected abstract TResult VisitScalarValue(TState state, ScalarValue scalar); protected abstract TResult VisitSequenceValue(TState state, SequenceValue sequence); protected abstract TResult VisitStructureValue(TState state, StructureValue structure); protected abstract TResult VisitDictionaryValue(TState state, DictionaryValue dictionary); protected virtual TResult VisitUnsupportedValue(TState state, LogEventPropertyValue value)
- Serilog: `abstract class LogEventPropertyValueRewriter<TState> : LogEventPropertyValueVisitor<TState, LogEventPropertyValue>` (src/Serilog/Data/LogEventPropertyValueRewriter.cs)
  protected override LogEventPropertyValue VisitScalarValue(TState state, ScalarValue scalar); protected override LogEventPropertyValue VisitSequenceValue(TState state, SequenceValue sequence); protected override LogEventPropertyValue VisitStructureValue(TState state, StructureValue structure); protected override LogEventPropertyValue VisitDictionaryValue(TState state, DictionaryValue dictionary); protected override LogEventPropertyValue VisitUnsupportedValue(TState state, LogEventPropertyValue value)
- Serilog: `static class OutputProperties` (src/Serilog/Formatting/Display/OutputProperties.cs)
  const string MessagePropertyName; const string TimestampPropertyName; const string LevelPropertyName; const string NewLinePropertyName; const string ExceptionPropertyName; const string PropertiesPropertyName
