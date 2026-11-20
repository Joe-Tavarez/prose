## Repository map (from Roslyn, at the starting commit; declarations only)
Solution `Serilog.sln`, .NET SDK 8.0.100, 5 C# projects (3 test). Projects are listed most relevant to the issue first.

### Projects
- **TestDummies** (`test/TestDummies/TestDummies.csproj`; net462, netstandard2.0) → Serilog; 12 public types; ns TestDummies, TestDummies.Console.Themes, TestDummies.Console
- **Serilog** (`src/Serilog/Serilog.csproj`; net6.0, net8.0, netstandard2.0) → no project refs; 54 public types; ns Serilog.Core, Serilog.Events, Serilog.Configuration
- Serilog.Tests (`test/Serilog.Tests/Serilog.Tests.csproj`; net6.0, net7.0, net8.0) — tests Serilog, TestDummies
- Serilog.PerformanceTests (`test/Serilog.PerformanceTests/Serilog.PerformanceTests.csproj`; net6.0, net8.0) — tests Serilog
- Serilog.ApprovalTests (`test/Serilog.ApprovalTests/Serilog.ApprovalTests.csproj`; net8.0) — tests Serilog

### Key public types (members abbreviated)
- TestDummies: `class DummyReduceVersionToMajorPolicy : IDestructuringPolicy` (test/TestDummies/DummyReduceVersionToMajorPolicy.cs)
  bool TryDestructure(object value, ILogEventPropertyValueFactory propertyValueFactory, out LogEventPropertyValue result)
- Serilog: `interface IDestructuringPolicy` (src/Serilog/Core/IDestructuringPolicy.cs)
  bool TryDestructure(object value, ILogEventPropertyValueFactory propertyValueFactory, out LogEventPropertyValue result)
- TestDummies: `class DummyHardCodedStringDestructuringPolicy : IDestructuringPolicy` (test/TestDummies/DummyHardCodedStringDestructuringPolicy.cs)
  DummyHardCodedStringDestructuringPolicy(string hardCodedString); bool TryDestructure(object value, ILogEventPropertyValueFactory propertyValueFactory, out LogEventPropertyValue result)
- Serilog: `interface ILogEventSink` (src/Serilog/Core/ILogEventSink.cs)
  void Emit(LogEvent logEvent)
- TestDummies: `abstract class ConsoleTheme` (test/TestDummies/Console/Themes/ConsoleTheme.cs)
  static ConsoleTheme None { get; }
- Serilog: `interface ILogger` (src/Serilog/ILogger.cs)
  ILogger ForContext(ILogEventEnricher enricher); ILogger ForContext(IEnumerable<ILogEventEnricher> enrichers); ILogger ForContext(string propertyName, object value, bool destructureObjects); ILogger ForContext<TSource>(); … +75
- TestDummies: `static class DummyLoggerConfigurationExtensions` (test/TestDummies/DummyLoggerConfigurationExtensions.cs)
  static LoggerConfiguration WithDummyThreadId(this LoggerEnrichmentConfiguration enrich); static LoggerConfiguration DummyRollingFile(this LoggerSinkConfiguration loggerSinkConfiguration, string pathFormat, LogEventLevel restrictedToMinimumLevel, string outputTemplate, IFormatProvider formatProvider); static LoggerConfiguration DummyRollingFile(this LoggerSinkConfiguration loggerSinkConfiguration, ITextFormatter formatter, string pathFormat, LogEventLevel restrictedToMinimumLevel); static LoggerConfiguration DummyRollingFile(this LoggerAuditSinkConfiguration loggerSinkConfiguration, LogEventLevel restrictedToMinimumLevel); … +5
- Serilog: `static class Log` (src/Serilog/Log.cs)
  static ILogger Logger { get; set; }; static void CloseAndFlush(); static ValueTask CloseAndFlushAsync(); static ILogger ForContext(ILogEventEnricher enricher); … +78
- TestDummies: `class DummyWithLevelSwitchSink : ILogEventSink` (test/TestDummies/DummyWithLevelSwitchSink.cs)
  DummyWithLevelSwitchSink(LoggingLevelSwitch loggingControlLevelSwitch); static LoggingLevelSwitch ControlLevelSwitch; static List<LogEvent> Emitted; void Emit(LogEvent logEvent)
- Serilog: `class Logger : ILogger, ILogEventSink, IDisposable` (src/Serilog/Core/Logger.cs)
  ILogger ForContext(ILogEventEnricher enricher); ILogger ForContext(IEnumerable<ILogEventEnricher> enrichers); ILogger ForContext(string propertyName, object value, bool destructureObjects); ILogger ForContext(Type source); … +78
- TestDummies: `class DummyWrappingSink : ILogEventSink` (test/TestDummies/DummyWrappingSink.cs)
  static List<LogEvent> Emitted { get; }; DummyWrappingSink(ILogEventSink sink); void Emit(LogEvent logEvent); static void Reset()
- Serilog: `interface ILogEventEnricher` (src/Serilog/Core/ILogEventEnricher.cs)
  void Enrich(LogEvent logEvent, ILogEventPropertyFactory propertyFactory)
- TestDummies: `class DummyConsoleSink : ILogEventSink` (test/TestDummies/Console/DummyConsoleSink.cs)
  DummyConsoleSink(ConsoleTheme theme); static ConsoleTheme Theme; void Emit(LogEvent logEvent)
- Serilog: `class LogEvent` (src/Serilog/Events/LogEvent.cs)
  LogEvent(DateTimeOffset timestamp, LogEventLevel level, Exception exception, MessageTemplate messageTemplate, IEnumerable<LogEventProperty> properties); LogEvent(DateTimeOffset timestamp, LogEventLevel level, Exception exception, MessageTemplate messageTemplate, IEnumerable<LogEventProperty> properties, ActivityTraceId traceId, ActivitySpanId spanId); DateTimeOffset Timestamp { get; }; LogEventLevel Level { get; }; … +11
- TestDummies: `class DummyRollingFileAuditSink : ILogEventSink` (test/TestDummies/DummyRollingFileAuditSink.cs)
  static List<LogEvent> Emitted { get; }; void Emit(LogEvent logEvent); static void Reset()
- Serilog: `abstract class LogEventPropertyValue : IFormattable` (src/Serilog/Events/LogEventPropertyValue.cs)
  abstract void Render(TextWriter output, string format, IFormatProvider formatProvider); override string ToString(); string ToString(string format, IFormatProvider formatProvider)
- TestDummies: `class DummyRollingFileSink : ILogEventSink` (test/TestDummies/DummyRollingFileSink.cs)
  static List<LogEvent> Emitted { get; }; void Emit(LogEvent logEvent); static void Reset()
- Serilog: `abstract class LogEventPropertyValueVisitor<TState, TResult>` (src/Serilog/Data/LogEventPropertyValueVisitor.cs)
  protected virtual TResult Visit(TState state, LogEventPropertyValue value); protected abstract TResult VisitScalarValue(TState state, ScalarValue scalar); protected abstract TResult VisitSequenceValue(TState state, SequenceValue sequence); protected abstract TResult VisitStructureValue(TState state, StructureValue structure); … +2
- TestDummies: `static class ConsoleThemes` (test/TestDummies/Console/Themes/ConsoleThemes.cs)
  static ConsoleTheme Theme1 { get; }
- Serilog: `class LoggerSinkConfiguration` (src/Serilog/Configuration/LoggerSinkConfiguration.cs)
  LoggerConfiguration Sink(ILogEventSink logEventSink, LogEventLevel restrictedToMinimumLevel); LoggerConfiguration Sink(ILogEventSink logEventSink, LogEventLevel restrictedToMinimumLevel, LoggingLevelSwitch levelSwitch); LoggerConfiguration Sink<TSink>(LogEventLevel restrictedToMinimumLevel, LoggingLevelSwitch levelSwitch); LoggerConfiguration Sink(IBatchedLogEventSink batchedLogEventSink, BatchingOptions batchingOptions, LogEventLevel restrictedToMinimumLevel, LoggingLevelSwitch levelSwitch); … +8
- TestDummies: `class DummyAnonymousUserFilter : ILogEventFilter` (test/TestDummies/DummyAnonymousUserFilter.cs)
  bool IsEnabled(LogEvent logEvent)
- Serilog: `class PropertyToken : MessageTemplateToken` (src/Serilog/Parsing/PropertyToken.cs)
  PropertyToken(string propertyName, string rawText, string format, in Alignment? alignment, Destructuring destructuring); override int Length { get; }; override void Render(IReadOnlyDictionary<string, LogEventPropertyValue> properties, TextWriter output, IFormatProvider formatProvider); string PropertyName { get; }; … +8
- TestDummies: `class DummyThreadIdEnricher : ILogEventEnricher` (test/TestDummies/DummyThreadIdEnricher.cs)
  void Enrich(LogEvent logEvent, ILogEventPropertyFactory propertyFactory)
- Serilog: `class JsonValueFormatter : LogEventPropertyValueVisitor<TextWriter, bool>` (src/Serilog/Formatting/Json/JsonValueFormatter.cs)
  JsonValueFormatter(string typeTagName); void Format(LogEventPropertyValue value, TextWriter output); protected override bool VisitScalarValue(TextWriter state, ScalarValue scalar); protected override bool VisitSequenceValue(TextWriter state, SequenceValue sequence); … +4
- Serilog: `interface ILogEventPropertyValueFactory` (src/Serilog/Core/ILogEventPropertyValueFactory.cs)
  LogEventPropertyValue CreatePropertyValue(object value, bool destructureObjects)
- Serilog: `class LoggerDestructuringConfiguration` (src/Serilog/Configuration/LoggerDestructuringConfiguration.cs)
  LoggerConfiguration AsScalar(Type scalarType); LoggerConfiguration AsScalar<TScalar>(); LoggerConfiguration With(params IDestructuringPolicy[] destructuringPolicies); LoggerConfiguration With<TDestructuringPolicy>(); … +6
- Serilog: `class LoggerMinimumLevelConfiguration` (src/Serilog/Configuration/LoggerMinimumLevelConfiguration.cs)
  LoggerConfiguration Is(LogEventLevel minimumLevel); LoggerConfiguration ControlledBy(LoggingLevelSwitch levelSwitch); LoggerConfiguration Verbose(); LoggerConfiguration Debug(); … +6
- Serilog: `class LoggerConfiguration` (src/Serilog/LoggerConfiguration.cs)
  LoggerConfiguration(); LoggerSinkConfiguration WriteTo { get; internal set; }; LoggerAuditSinkConfiguration AuditTo { get; }; LoggerMinimumLevelConfiguration MinimumLevel { get; }; … +5
- Serilog: `static class OutputProperties` (src/Serilog/Formatting/Display/OutputProperties.cs)
  const string MessagePropertyName; const string TimestampPropertyName; const string UtcTimestampPropertyName; const string LevelPropertyName; … +5
- Serilog: `interface IBatchedLogEventSink` (src/Serilog/Core/IBatchedLogEventSink.cs)
  Task EmitBatchAsync(IReadOnlyCollection<LogEvent> batch); Task OnEmptyBatchAsync()
- Serilog: `abstract class LogEventPropertyValueRewriter<TState> : LogEventPropertyValueVisitor<TState, LogEventPropertyValue>` (src/Serilog/Data/LogEventPropertyValueRewriter.cs)
  protected override LogEventPropertyValue VisitScalarValue(TState state, ScalarValue scalar); protected override LogEventPropertyValue VisitSequenceValue(TState state, SequenceValue sequence); protected override LogEventPropertyValue VisitStructureValue(TState state, StructureValue structure); protected override LogEventPropertyValue VisitDictionaryValue(TState state, DictionaryValue dictionary); … +1
- Serilog: `class LoggerEnrichmentConfiguration` (src/Serilog/Configuration/LoggerEnrichmentConfiguration.cs)
  LoggerConfiguration With(params ILogEventEnricher[] enrichers); LoggerConfiguration With<TEnricher>(); LoggerConfiguration WithProperty(string name, object value, bool destructureObjects); LoggerConfiguration FromLogContext(); … +4
- Serilog: `class MessageTemplate` (src/Serilog/Events/MessageTemplate.cs)
  static MessageTemplate Empty { get; }; MessageTemplate(IEnumerable<MessageTemplateToken> tokens); MessageTemplate(string text, IEnumerable<MessageTemplateToken> tokens); string Text { get; }; … +4
- Serilog: `abstract class MessageTemplateToken` (src/Serilog/Parsing/MessageTemplateToken.cs)
  abstract int Length { get; }; abstract void Render(IReadOnlyDictionary<string, LogEventPropertyValue> properties, TextWriter output, IFormatProvider formatProvider)
- Serilog: `interface ILogEventFilter` (src/Serilog/Core/ILogEventFilter.cs)
  bool IsEnabled(LogEvent logEvent)
- Serilog: `interface ILogEventPropertyFactory` (src/Serilog/Core/ILogEventPropertyFactory.cs)
  LogEventProperty CreateProperty(string name, object value, bool destructureObjects)
- Serilog: `interface ITextFormatter` (src/Serilog/Formatting/ITextFormatter.cs)
  void Format(LogEvent logEvent, TextWriter output)
- Serilog: `class TextToken : MessageTemplateToken` (src/Serilog/Parsing/TextToken.cs)
  TextToken(string text); override int Length { get; }; override void Render(IReadOnlyDictionary<string, LogEventPropertyValue> properties, TextWriter output, IFormatProvider formatProvider); override bool Equals(object obj); … +3
- Serilog: `static class LogContext` (src/Serilog/Context/LogContext.cs)
  static IDisposable PushProperty(string name, object value, bool destructureObjects); static IDisposable Push(ILogEventEnricher enricher); static IDisposable Push(params ILogEventEnricher[] enrichers); static ILogEventEnricher Clone(); … +2
- Serilog: `enum LogEventLevel` (src/Serilog/Events/LogEventLevel.cs)
  Verbose; Debug; Information; Warning; … +2
- Serilog: `class ScalarValue : LogEventPropertyValue` (src/Serilog/Events/ScalarValue.cs)
  static ScalarValue Null { get; }; ScalarValue(object value); object Value { get; }; override void Render(TextWriter output, string format, IFormatProvider formatProvider); … +2
