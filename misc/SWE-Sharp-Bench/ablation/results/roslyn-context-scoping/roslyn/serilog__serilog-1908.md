## Repository map (from Roslyn, at the starting commit; declarations only)
Solution `Serilog.sln`, .NET SDK 7.0.102, 5 C# projects (3 test). Projects are listed most relevant to the issue first.

### Projects
- **Serilog** (`src/Serilog/Serilog.csproj`; net5.0, net6.0, net7.0, netstandard2.0, netstandard2.1) → no project refs; 51 public types; ns Serilog.Core, Serilog.Events, Serilog.Configuration
- Serilog.Tests (`test/Serilog.Tests/Serilog.Tests.csproj`; net5.0, net6.0, net7.0, netcoreapp3.1) — tests Serilog, TestDummies
- Serilog.PerformanceTests (`test/Serilog.PerformanceTests/Serilog.PerformanceTests.csproj`; net7.0) — tests Serilog
- **TestDummies** (`test/TestDummies/TestDummies.csproj`; net462, netstandard2.0, netstandard2.1) → Serilog; 12 public types; ns TestDummies, TestDummies.Console.Themes, TestDummies.Console
- Serilog.ApprovalTests (`test/Serilog.ApprovalTests/Serilog.ApprovalTests.csproj`; net7.0) — tests Serilog

### Key public types (members abbreviated)
- Serilog: `class LoggingLevelSwitch` (src/Serilog/Core/LoggingLevelSwitch.cs)
  LoggingLevelSwitch(LogEventLevel initialMinimumLevel); LogEventLevel MinimumLevel { get; set; }
- TestDummies: `class DummyThreadIdEnricher : ILogEventEnricher` (test/TestDummies/DummyThreadIdEnricher.cs)
  void Enrich(LogEvent logEvent, ILogEventPropertyFactory propertyFactory)
- Serilog: `enum LogEventLevel` (src/Serilog/Events/LogEventLevel.cs)
  Verbose; Debug; Information; Warning; Error; Fatal
- TestDummies: `abstract class ConsoleTheme` (test/TestDummies/Console/Themes/ConsoleTheme.cs)
  static ConsoleTheme None { get; }
- Serilog: `class LoggerConfiguration` (src/Serilog/LoggerConfiguration.cs)
  LoggerConfiguration(); LoggerSinkConfiguration WriteTo { get; internal set; }; LoggerAuditSinkConfiguration AuditTo { get; }; LoggerMinimumLevelConfiguration MinimumLevel { get; }; LoggerEnrichmentConfiguration Enrich { get; internal set; }; LoggerFilterConfiguration Filter { get; }; LoggerDestructuringConfiguration Destructure { get; }; LoggerSettingsConfiguration ReadFrom { get; }; … +1
- TestDummies: `static class DummyLoggerConfigurationExtensions` (test/TestDummies/DummyLoggerConfigurationExtensions.cs)
  static LoggerConfiguration WithDummyThreadId(this LoggerEnrichmentConfiguration enrich); static LoggerConfiguration DummyRollingFile(this LoggerSinkConfiguration loggerSinkConfiguration, string pathFormat, LogEventLevel restrictedToMinimumLevel, string outputTemplate, IFormatProvider formatProvider); static LoggerConfiguration DummyRollingFile(this LoggerSinkConfiguration loggerSinkConfiguration, ITextFormatter formatter, string pathFormat, LogEventLevel restrictedToMinimumLevel); static LoggerConfiguration DummyRollingFile(this LoggerAuditSinkConfiguration loggerSinkConfiguration, LogEventLevel restrictedToMinimumLevel); static LoggerConfiguration DummyWithLevelSwitch(this LoggerSinkConfiguration loggerSinkConfiguration, LogEventLevel restrictedToMinimumLevel, LoggingLevelSwitch controlLevelSwitch); static LoggerConfiguration DummyConsole(this LoggerSinkConfiguration loggerSinkConfiguration, LogEventLevel restrictedToMinimumLevel, ConsoleTheme theme); static LoggerConfiguration Dummy(this LoggerSinkConfiguration loggerSinkConfiguration, Action<LoggerSinkConfiguration> wrappedSinkAction); static LoggerConfiguration DummyWrap(this LoggerSinkConfiguration loggerSinkConfiguration, Action<LoggerSinkConfiguration> wrappedSinkAction, LogEventLevel logEventLevel, LoggingLevelSwitch levelSwitch); … +1
- Serilog: `class LoggerMinimumLevelConfiguration` (src/Serilog/Configuration/LoggerMinimumLevelConfiguration.cs)
  LoggerConfiguration Is(LogEventLevel minimumLevel); LoggerConfiguration ControlledBy(LoggingLevelSwitch levelSwitch); LoggerConfiguration Verbose(); LoggerConfiguration Debug(); LoggerConfiguration Information(); LoggerConfiguration Warning(); LoggerConfiguration Error(); LoggerConfiguration Fatal(); … +2
- TestDummies: `class DummyWithLevelSwitchSink : ILogEventSink` (test/TestDummies/DummyWithLevelSwitchSink.cs)
  DummyWithLevelSwitchSink(LoggingLevelSwitch loggingControlLevelSwitch); static LoggingLevelSwitch ControlLevelSwitch; static List<LogEvent> Emitted; void Emit(LogEvent logEvent)
- Serilog: `interface ILogger` (src/Serilog/ILogger.cs)
  ILogger ForContext(ILogEventEnricher enricher); ILogger ForContext(IEnumerable<ILogEventEnricher> enrichers); ILogger ForContext(string propertyName, object value, bool destructureObjects); ILogger ForContext<TSource>(); ILogger ForContext(Type source); void Write(LogEvent logEvent); void Write(LogEventLevel level, string messageTemplate); void Write<T>(LogEventLevel level, string messageTemplate, T propertyValue); … +71
- TestDummies: `class DummyWrappingSink : ILogEventSink` (test/TestDummies/DummyWrappingSink.cs)
  static List<LogEvent> Emitted { get; }; DummyWrappingSink(ILogEventSink sink); void Emit(LogEvent logEvent); static void Reset()
- Serilog: `static class Log` (src/Serilog/Log.cs)
  static ILogger Logger { get; set; }; static void CloseAndFlush(); static ValueTask CloseAndFlushAsync(); static ILogger ForContext(ILogEventEnricher enricher); static ILogger ForContext(ILogEventEnricher[] enrichers); static ILogger ForContext(string propertyName, object value, bool destructureObjects); static ILogger ForContext<TSource>(); static ILogger ForContext(Type source); … +74
- TestDummies: `class DummyConsoleSink : ILogEventSink` (test/TestDummies/Console/DummyConsoleSink.cs)
  DummyConsoleSink(ConsoleTheme theme); static ConsoleTheme Theme; void Emit(LogEvent logEvent)
- Serilog: `class Logger : ILogger, ILogEventSink, IDisposable` (src/Serilog/Core/Logger.cs)
  ILogger ForContext(ILogEventEnricher enricher); ILogger ForContext(IEnumerable<ILogEventEnricher> enrichers); ILogger ForContext(string propertyName, object value, bool destructureObjects); ILogger ForContext(Type source); ILogger ForContext<TSource>(); void Write(LogEventLevel level, string messageTemplate); void Write<T>(LogEventLevel level, string messageTemplate, T propertyValue); void Write<T0, T1>(LogEventLevel level, string messageTemplate, T0 propertyValue0, T1 propertyValue1); … +74
- TestDummies: `class DummyRollingFileAuditSink : ILogEventSink` (test/TestDummies/DummyRollingFileAuditSink.cs)
  static List<LogEvent> Emitted { get; }; void Emit(LogEvent logEvent); static void Reset()
- Serilog: `static class SelfLog` (src/Serilog/Debugging/SelfLog.cs)
  static void Enable(TextWriter output); static void Enable(Action<string> output); static void Disable(); static void WriteLine(string format, object arg0, object arg1, object arg2)
- TestDummies: `class DummyRollingFileSink : ILogEventSink` (test/TestDummies/DummyRollingFileSink.cs)
  static List<LogEvent> Emitted { get; }; void Emit(LogEvent logEvent); static void Reset()
- Serilog: `static class LogContext` (src/Serilog/Context/LogContext.cs)
  static IDisposable PushProperty(string name, object value, bool destructureObjects); static IDisposable Push(ILogEventEnricher enricher); static IDisposable Push(params ILogEventEnricher[] enrichers); static ILogEventEnricher Clone(); static IDisposable Suspend(); static void Reset()
- TestDummies: `class DummyHardCodedStringDestructuringPolicy : IDestructuringPolicy` (test/TestDummies/DummyHardCodedStringDestructuringPolicy.cs)
  DummyHardCodedStringDestructuringPolicy(string hardCodedString); bool TryDestructure(object value, ILogEventPropertyValueFactory propertyValueFactory, out LogEventPropertyValue result)
- Serilog: `class LoggerEnrichmentConfiguration` (src/Serilog/Configuration/LoggerEnrichmentConfiguration.cs)
  LoggerConfiguration With(params ILogEventEnricher[] enrichers); LoggerConfiguration With<TEnricher>(); LoggerConfiguration WithProperty(string name, object value, bool destructureObjects); LoggerConfiguration FromLogContext(); LoggerConfiguration When(Func<LogEvent, bool> condition, Action<LoggerEnrichmentConfiguration> configureEnricher); LoggerConfiguration AtLevel(LogEventLevel enrichFromLevel, Action<LoggerEnrichmentConfiguration> configureEnricher); LoggerConfiguration AtLevel(LoggingLevelSwitch levelSwitch, Action<LoggerEnrichmentConfiguration> configureEnricher); static LoggerConfiguration Wrap(LoggerEnrichmentConfiguration loggerEnrichmentConfiguration, Func<ILogEventEnricher, ILogEventEnricher> wrapEnricher, Action<LoggerEnrichmentConfiguration> configureWrappedEnricher)
- TestDummies: `static class ConsoleThemes` (test/TestDummies/Console/Themes/ConsoleThemes.cs)
  static ConsoleTheme Theme1 { get; }
- Serilog: `static class Constants` (src/Serilog/Core/Constants.cs)
  const string SourceContextPropertyName
- TestDummies: `class DummyAnonymousUserFilter : ILogEventFilter` (test/TestDummies/DummyAnonymousUserFilter.cs)
  bool IsEnabled(LogEvent logEvent)
- Serilog: `static class LoggerExtensions` (src/Serilog/LoggerExtensions.cs)
  static ILogger ForContext<TValue>(this ILogger logger, LogEventLevel level, string propertyName, TValue value, bool destructureObjects)
- TestDummies: `class DummyReduceVersionToMajorPolicy : IDestructuringPolicy` (test/TestDummies/DummyReduceVersionToMajorPolicy.cs)
  bool TryDestructure(object value, ILogEventPropertyValueFactory propertyValueFactory, out LogEventPropertyValue result)
- Serilog: `interface ILogEventSink` (src/Serilog/Core/ILogEventSink.cs)
  void Emit(LogEvent logEvent)
- Serilog: `interface ILogEventEnricher` (src/Serilog/Core/ILogEventEnricher.cs)
  void Enrich(LogEvent logEvent, ILogEventPropertyFactory propertyFactory)
- Serilog: `interface IDestructuringPolicy` (src/Serilog/Core/IDestructuringPolicy.cs)
  bool TryDestructure(object value, ILogEventPropertyValueFactory propertyValueFactory, out LogEventPropertyValue result)
- Serilog: `abstract class LogEventPropertyValue : IFormattable` (src/Serilog/Events/LogEventPropertyValue.cs)
  abstract void Render(TextWriter output, string format, IFormatProvider formatProvider); override string ToString(); string ToString(string format, IFormatProvider formatProvider)
- Serilog: `abstract class LogEventPropertyValueVisitor<TState, TResult>` (src/Serilog/Data/LogEventPropertyValueVisitor.cs)
  protected virtual TResult Visit(TState state, LogEventPropertyValue value); protected abstract TResult VisitScalarValue(TState state, ScalarValue scalar); protected abstract TResult VisitSequenceValue(TState state, SequenceValue sequence); protected abstract TResult VisitStructureValue(TState state, StructureValue structure); … +2
- Serilog: `class PropertyToken : MessageTemplateToken` (src/Serilog/Parsing/PropertyToken.cs)
  PropertyToken(string propertyName, string rawText, string format, in Alignment? alignment, Destructuring destructuring); override int Length { get; }; override void Render(IReadOnlyDictionary<string, LogEventPropertyValue> properties, TextWriter output, IFormatProvider formatProvider); string PropertyName { get; }; … +8
- Serilog: `class JsonValueFormatter : LogEventPropertyValueVisitor<TextWriter, bool>` (src/Serilog/Formatting/Json/JsonValueFormatter.cs)
  JsonValueFormatter(string typeTagName); void Format(LogEventPropertyValue value, TextWriter output); protected override bool VisitScalarValue(TextWriter state, ScalarValue scalar); protected override bool VisitSequenceValue(TextWriter state, SequenceValue sequence); … +4
- Serilog: `class LogEvent` (src/Serilog/Events/LogEvent.cs)
  LogEvent(DateTimeOffset timestamp, LogEventLevel level, Exception exception, MessageTemplate messageTemplate, IEnumerable<LogEventProperty> properties); DateTimeOffset Timestamp { get; }; LogEventLevel Level { get; }; MessageTemplate MessageTemplate { get; }; … +7
- Serilog: `interface ILogEventPropertyValueFactory` (src/Serilog/Core/ILogEventPropertyValueFactory.cs)
  LogEventPropertyValue CreatePropertyValue(object value, bool destructureObjects)
- Serilog: `class LoggerDestructuringConfiguration` (src/Serilog/Configuration/LoggerDestructuringConfiguration.cs)
  LoggerConfiguration AsScalar(Type scalarType); LoggerConfiguration AsScalar<TScalar>(); LoggerConfiguration With(params IDestructuringPolicy[] destructuringPolicies); LoggerConfiguration With<TDestructuringPolicy>(); … +5
- Serilog: `abstract class LogEventPropertyValueRewriter<TState> : LogEventPropertyValueVisitor<TState, LogEventPropertyValue>` (src/Serilog/Data/LogEventPropertyValueRewriter.cs)
  protected override LogEventPropertyValue VisitScalarValue(TState state, ScalarValue scalar); protected override LogEventPropertyValue VisitSequenceValue(TState state, SequenceValue sequence); protected override LogEventPropertyValue VisitStructureValue(TState state, StructureValue structure); protected override LogEventPropertyValue VisitDictionaryValue(TState state, DictionaryValue dictionary); … +1
