## Repository map (from Roslyn, at the starting commit; declarations only)
Solution `src/Spectre.Console.sln`, .NET SDK 8.0.204, 7 C# projects (2 test). Projects are listed most relevant to the issue first.

### Projects
- **Spectre.Console.Cli** (`src/Spectre.Console.Cli/Spectre.Console.Cli.csproj`; net6.0, net7.0, net8.0, netstandard2.0) → Spectre.Console; 60 public types; ns Spectre.Console.Cli, Spectre.Console.Cli.Help, System.Diagnostics.CodeAnalysis
- Spectre.Console.Cli.Tests (`test/Spectre.Console.Cli.Tests/Spectre.Console.Cli.Tests.csproj`; net6.0, net7.0, net8.0) — tests Spectre.Console, Spectre.Console.Cli, Spectre.Console.Testing
- **Spectre.Console.Testing** (`src/Spectre.Console.Testing/Spectre.Console.Testing.csproj`; net6.0, net7.0, net8.0) → Spectre.Console, Spectre.Console.Cli; 14 public types; ns Spectre.Console.Testing, Spectre.Console
- **Spectre.Console** (`src/Spectre.Console/Spectre.Console.csproj`; net6.0, net7.0, net8.0, netstandard2.0) → no project refs; 214 public types; ns Spectre.Console, Spectre.Console.Rendering, Spectre.Console.Enrichment
- Spectre.Console.Tests (`test/Spectre.Console.Tests/Spectre.Console.Tests.csproj`; net6.0, net7.0, net8.0) — tests Spectre.Console, Spectre.Console.Cli, Spectre.Console.Json, Spectre.Console.Testing
- **Spectre.Console.Json** (`src/Spectre.Console.Json/Spectre.Console.Json.csproj`; net6.0, net7.0, net8.0, netstandard2.0) → Spectre.Console; 10 public types; ns Spectre.Console.Json, Spectre.Console.Json.Syntax, Spectre.Console
- **Spectre.Console.ImageSharp** (`src/Spectre.Console.ImageSharp/Spectre.Console.ImageSharp.csproj`; net6.0, net7.0, net8.0) → Spectre.Console; 2 public types; ns Spectre.Console

### Key public types (members abbreviated)
- Spectre.Console.Cli: `class CommandApp<TDefaultCommand> : ICommandApp` (src/Spectre.Console.Cli/CommandAppOfT.cs)
  CommandApp(ITypeRegistrar registrar); void Configure(Action<IConfigurator> configuration); int Run(IEnumerable<string> args); Task<int> RunAsync(IEnumerable<string> args); CommandApp<TDefaultCommand> WithDescription(string description); CommandApp<TDefaultCommand> WithData(object data)
- Spectre.Console.Testing: `class CommandAppTester` (src/Spectre.Console.Testing/Cli/CommandAppTester.cs)
  CommandAppTester(ITypeRegistrar registrar); ITypeRegistrar Registrar { get; set; }; void SetDefaultCommand<T>(string description, object data); void Configure(Action<IConfigurator> action); CommandAppFailure RunAndCatch<T>(params string[] args); CommandAppResult Run(params string[] args); Task<CommandAppResult> RunAsync(params string[] args)
- Spectre.Console: `static class AnsiConsole` (src/Spectre.Console/AnsiConsole.cs)
  static IAnsiConsole Console { get; set; }; static IAnsiConsoleCursor Cursor { get; }; static Profile Profile { get; }; static IAnsiConsole Create(AnsiConsoleSettings settings); static void Clear(); static void WriteException(Exception exception, ExceptionFormats format); static void WriteException(Exception exception, ExceptionSettings settings); static LiveDisplay Live(IRenderable target); … +76
- Spectre.Console.Json: `class JsonText : JustInTimeRenderable` (src/Spectre.Console.Json/JsonText.cs)
  Style BracesStyle { get; set; }; Style BracketsStyle { get; set; }; Style MemberStyle { get; set; }; Style ColonStyle { get; set; }; Style CommaStyle { get; set; }; Style StringStyle { get; set; }; Style NumberStyle { get; set; }; Style BooleanStyle { get; set; }; … +4
- Spectre.Console.ImageSharp: `class CanvasImage : Renderable` (src/Spectre.Console.ImageSharp/CanvasImage.cs)
  int Width { get; }; int Height { get; }; int? MaxWidth { get; set; }; int PixelWidth { get; set; }; … +6
- Spectre.Console.Cli: `interface IConfigurator<TSettings>` (src/Spectre.Console.Cli/IConfiguratorOfT.cs)
  void SetDescription(string description); void AddExample(params string[] args); void SetDefaultCommand<TDefaultCommand>(); void HideBranch(); ICommandConfigurator AddCommand<TCommand>(string name); ICommandConfigurator AddDelegate<TDerivedSettings>(string name, Func<CommandContext, TDerivedSettings, int> func); ICommandConfigurator AddAsyncDelegate<TDerivedSettings>(string name, Func<CommandContext, TDerivedSettings, Task<int>> func); IBranchConfigurator AddBranch<TDerivedSettings>(string name, Action<IConfigurator<TDerivedSettings>> action)
- Spectre.Console.Testing: `class CommandAppResult` (src/Spectre.Console.Testing/Cli/CommandAppResult.cs)
  int ExitCode { get; }; string Output { get; }; CommandContext Context { get; }; CommandSettings Settings { get; }
- Spectre.Console: `class AnsiConsoleOutput : IAnsiConsoleOutput` (src/Spectre.Console/AnsiConsoleOutput.cs)
  TextWriter Writer { get; }; bool IsTerminal { get; }; int Width { get; }; int Height { get; }; AnsiConsoleOutput(TextWriter writer); void SetEncoding(Encoding encoding)
- Spectre.Console.Json: `abstract class JsonSyntax` (src/Spectre.Console.Json/Syntax/JsonSyntax.cs)
- Spectre.Console.ImageSharp: `static class CanvasImageExtensions` (src/Spectre.Console.ImageSharp/CanvasImageExtensions.cs)
  static CanvasImage MaxWidth(this CanvasImage image, int? maxWidth); static CanvasImage NoMaxWidth(this CanvasImage image); static CanvasImage PixelWidth(this CanvasImage image, int width); static CanvasImage Mutate(this CanvasImage image, Action<IImageProcessingContext> action); … +3
- Spectre.Console.Cli: `interface ICommandInfo : ICommandContainer` (src/Spectre.Console.Cli/Help/ICommandInfo.cs)
  string Name { get; }; string Description { get; }; bool IsBranch { get; }; bool IsDefaultCommand { get; }; bool IsHidden { get; }; IReadOnlyList<ICommandParameter> Parameters { get; }; ICommandInfo Parent { get; }
- Spectre.Console.Testing: `class CallbackCommandInterceptor : ICommandInterceptor` (src/Spectre.Console.Testing/Cli/CallbackCommandInterceptor.cs)
  CallbackCommandInterceptor(Action<CommandContext, CommandSettings> callback); void Intercept(CommandContext context, CommandSettings settings)
- Spectre.Console: `interface IAnsiConsoleOutput` (src/Spectre.Console/IAnsiConsoleOutput.cs)
  TextWriter Writer { get; }; bool IsTerminal { get; }; int Width { get; }; int Height { get; }; void SetEncoding(Encoding encoding)
- Spectre.Console.Json: `static class JsonTextExtensions` (src/Spectre.Console.Json/JsonTextExtensions.cs)
  static JsonText BracesStyle(this JsonText text, Style style); static JsonText BracketStyle(this JsonText text, Style style); static JsonText MemberStyle(this JsonText text, Style style); static JsonText ColonStyle(this JsonText text, Style style); … +14
- Spectre.Console.Cli: `interface ICommandContainer` (src/Spectre.Console.Cli/Help/ICommandContainer.cs)
  IReadOnlyList<string[]> Examples { get; }; IReadOnlyList<ICommandInfo> Commands { get; }; ICommandInfo DefaultCommand { get; }
- Spectre.Console.Testing: `class CommandAppFailure` (src/Spectre.Console.Testing/Cli/CommandAppFailure.cs)
  Exception Exception { get; }; string Output { get; }
- Spectre.Console: `static class RecorderExtensions` (src/Spectre.Console/Extensions/RecorderExtensions.cs)
  static string ExportText(this Recorder recorder); static string ExportHtml(this Recorder recorder)
- Spectre.Console.Json: `interface IJsonParser` (src/Spectre.Console.Json/IJsonParser.cs)
  JsonSyntax Parse(string json)
- Spectre.Console.Cli: `class UsageStyle` (src/Spectre.Console.Cli/Help/HelpProviderStyles.cs)
  Style Header { get; set; }; Style CurrentCommand { get; set; }; Style Command { get; set; }; Style Options { get; set; }; Style RequiredArgument { get; set; }; Style OptionalArgument { get; set; }
- Spectre.Console.Testing: `class TestConsole : IAnsiConsole, IDisposable` (src/Spectre.Console.Testing/TestConsole.cs)
  Profile Profile { get; }; IExclusivityMode ExclusivityMode { get; }; TestConsoleInput Input { get; }; RenderPipeline Pipeline { get; }; IAnsiConsoleCursor Cursor { get; }; string Output { get; }; IReadOnlyList<string> Lines { get; }; bool EmitAnsiSequences { get; set; }; … +4
- Spectre.Console: `class Calendar : JustInTimeRenderable, IHasCulture, IHasTableBorder` (src/Spectre.Console/Widgets/Calendar.cs)
  int Year { get; set; }; int Month { get; set; }; int Day { get; set; }; TableBorder Border { get; set; }; bool UseSafeBorder { get; set; }; Style BorderStyle { get; set; }; CultureInfo Culture { get; set; }; Style HighlightStyle { get; set; }; … +8
- Spectre.Console.Json: `class JsonMember : JsonSyntax` (src/Spectre.Console.Json/Syntax/JsonMember.cs)
  string Name { get; }; JsonSyntax Value { get; }; JsonMember(string name, JsonSyntax value)
- Spectre.Console.Cli: `class CommandApp : ICommandApp` (src/Spectre.Console.Cli/CommandApp.cs)
  CommandApp(ITypeRegistrar registrar); void Configure(Action<IConfigurator> configuration); DefaultCommandConfigurator SetDefaultCommand<TCommand>(); int Run(IEnumerable<string> args); Task<int> RunAsync(IEnumerable<string> args)
- Spectre.Console.Testing: `class FakeTypeRegistrar : ITypeRegistrar` (src/Spectre.Console.Testing/FakeTypeRegistrar.cs)
  Dictionary<Type, List<Type>> Registrations { get; }; Dictionary<Type, List<object>> Instances { get; }; FakeTypeRegistrar(); void Register(Type service, Type implementation); void RegisterInstance(Type service, object implementation); void RegisterLazy(Type service, Func<object> factory); ITypeResolver Build()
- Spectre.Console: `abstract class JustInTimeRenderable : Renderable` (src/Spectre.Console/Rendering/JustInTimeRenderable.cs)
  protected override sealed Measurement Measure(RenderOptions context, int maxWidth); protected override sealed IEnumerable<Segment> Render(RenderOptions context, int width); protected abstract IRenderable Build(); protected virtual bool HasDirtyChildren(); protected void MarkAsDirty(); protected void MarkAsDirty(Action action)
- Spectre.Console.Json: `class JsonArray : JsonSyntax` (src/Spectre.Console.Json/Syntax/JsonArray.cs)
  List<JsonSyntax> Items { get; }; JsonArray()
- Spectre.Console.Cli: `class CommandOptionAttribute : Attribute` (src/Spectre.Console.Cli/Annotations/CommandOptionAttribute.cs)
  IReadOnlyList<string> LongNames { get; }; IReadOnlyList<string> ShortNames { get; }; string ValueName { get; }; bool ValueIsOptional { get; }; bool IsHidden { get; set; }; CommandOptionAttribute(string template)
- Spectre.Console.Testing: `class TestConsoleInput : IAnsiConsoleInput` (src/Spectre.Console.Testing/TestConsoleInput.cs)
  TestConsoleInput(); void PushText(string input); void PushTextWithEnter(string input); void PushCharacter(char input); … +5
- Spectre.Console: `class Grid : JustInTimeRenderable, IExpandable, IAlignable` (src/Spectre.Console/Widgets/Grid.cs)
  IReadOnlyList<GridColumn> Columns { get; }; IReadOnlyList<GridRow> Rows { get; }; bool Expand { get; set; }; Justify? Alignment { get; set; }; int? Width { get; set; }; Grid(); Grid AddColumn(); Grid AddColumn(GridColumn column); … +3
- Spectre.Console.Json: `class JsonBoolean : JsonSyntax` (src/Spectre.Console.Json/Syntax/JsonBoolean.cs)
  string Lexeme { get; }; JsonBoolean(string lexeme)
- Spectre.Console.Cli: `class CommandArgumentAttribute : Attribute` (src/Spectre.Console.Cli/Annotations/CommandArgumentAttribute.cs)
  int Position { get; }; string ValueName { get; }; bool IsRequired { get; }; CommandArgumentAttribute(int position, string template)
- Spectre.Console.Testing: `class TestCapabilities : IReadOnlyCapabilities` (src/Spectre.Console.Testing/TestCapabilities.cs)
  ColorSystem ColorSystem { get; set; }; bool Ansi { get; set; }; bool Links { get; set; }; bool Legacy { get; set; }; … +4
- Spectre.Console: `class Recorder : IAnsiConsole, IDisposable` (src/Spectre.Console/Recorder.cs)
  Profile Profile { get; }; IAnsiConsoleCursor Cursor { get; }; IAnsiConsoleInput Input { get; }; IExclusivityMode ExclusivityMode { get; }; RenderPipeline Pipeline { get; }; Recorder(IAnsiConsole console); void Dispose(); void Clear(bool home); … +2
- Spectre.Console.Json: `class JsonNull : JsonSyntax` (src/Spectre.Console.Json/Syntax/JsonNull.cs)
  string Lexeme { get; }; JsonNull(string lexeme)
