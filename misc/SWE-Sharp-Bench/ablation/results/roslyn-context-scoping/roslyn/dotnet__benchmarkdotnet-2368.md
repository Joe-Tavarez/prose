## Repository map (from Roslyn, at the starting commit; declarations only)
Solution `BenchmarkDotNet.sln`, .NET SDK 8.0.200, 16 C# projects (3 test). Projects are listed most relevant to the issue first.

### Projects
- **BenchmarkDotNet** (`src/BenchmarkDotNet/BenchmarkDotNet.csproj`; net6.0, netstandard2.0) → BenchmarkDotNet.Annotations; 479 public types; ns BenchmarkDotNet.Attributes, JetBrains.Annotations, BenchmarkDotNet.Columns
- BenchmarkDotNet.Tests (`tests/BenchmarkDotNet.Tests/BenchmarkDotNet.Tests.csproj`; net462, net7.0) — tests BenchmarkDotNet, BenchmarkDotNet.Annotations, BenchmarkDotNet.Diagnostics.Windows, BenchmarkDotNet.Diagnostics.dotTrace
- **BenchmarkDotNet.Samples** (`samples/BenchmarkDotNet.Samples/BenchmarkDotNet.Samples.csproj`; net462, net7.0) → BenchmarkDotNet, BenchmarkDotNet.Annotations, BenchmarkDotNet.Diagnostics.Windows, BenchmarkDotNet.Diagnostics.dotTrace; 88 public types; ns BenchmarkDotNet.Samples
- BenchmarkDotNet.IntegrationTests (`tests/BenchmarkDotNet.IntegrationTests/BenchmarkDotNet.IntegrationTests.csproj`; net7.0) — tests BenchmarkDotNet, BenchmarkDotNet.Annotations, BenchmarkDotNet.Diagnostics.dotTrace, BenchmarkDotNet.IntegrationTests.ConfigPerAssembly, BenchmarkDotNet.IntegrationTests.DisabledOptimizations, BenchmarkDotNet.IntegrationTests.EnabledOptimizations, BenchmarkDotNet.IntegrationTests.Static
- **BenchmarkDotNet.Diagnostics.Windows** (`src/BenchmarkDotNet.Diagnostics.Windows/BenchmarkDotNet.Diagnostics.Windows.csproj`; netstandard2.0) → BenchmarkDotNet, BenchmarkDotNet.Annotations; 24 public types; ns BenchmarkDotNet.Diagnostics.Windows, BenchmarkDotNet.Diagnostics.Windows.Tracing, BenchmarkDotNet.Diagnostics.Windows.Configs
- **BenchmarkDotNet.Annotations** (`src/BenchmarkDotNet.Annotations/BenchmarkDotNet.Annotations.csproj`; netstandard1.0, netstandard2.0) → no project refs; 15 public types; ns JetBrains.Annotations, BenchmarkDotNet.Attributes, System.Diagnostics.CodeAnalysis
- **BenchmarkDotNet.IntegrationTests.CustomPaths** (`tests/BenchmarkDotNet.IntegrationTests.CustomPaths/BenchmarkDotNet.IntegrationTests.CustomPaths.csproj`; net462) → BenchmarkDotNet, BenchmarkDotNet.Annotations; 3 public types; ns BenchmarkDotNet.IntegrationTests.CustomPaths
- **BenchmarkDotNet.Diagnostics.dotTrace** (`src/BenchmarkDotNet.Diagnostics.dotTrace/BenchmarkDotNet.Diagnostics.dotTrace.csproj`; net462, net6.0, netcoreapp3.1) → BenchmarkDotNet, BenchmarkDotNet.Annotations; 3 public types; ns BenchmarkDotNet.Diagnostics.dotTrace
- **BenchmarkDotNet.IntegrationTests.ConfigPerAssembly** (`tests/BenchmarkDotNet.IntegrationTests.ConfigPerAssembly/BenchmarkDotNet.IntegrationTests.ConfigPerAssembly.csproj`; net462, net7.0) → BenchmarkDotNet, BenchmarkDotNet.Annotations; 2 public types; ns BenchmarkDotNet.IntegrationTests.ConfigPerAssembly
- BenchmarkDotNet.IntegrationTests.ManualRunning (`tests/BenchmarkDotNet.IntegrationTests.ManualRunning/BenchmarkDotNet.IntegrationTests.ManualRunning.csproj`; net462, net7.0) — tests BenchmarkDotNet, BenchmarkDotNet.Annotations, BenchmarkDotNet.Diagnostics.Windows
- **BenchmarkDotNet.Disassembler.x64** (`src/BenchmarkDotNet.Disassembler.x64/BenchmarkDotNet.Disassembler.x64.csproj`; ?) → no project refs; 11 public types; ns BenchmarkDotNet.Disassemblers
- **BenchmarkDotNet.Disassembler.x86** (`src/BenchmarkDotNet.Disassembler.x86/BenchmarkDotNet.Disassembler.x86.csproj`; ?) → no project refs; 11 public types; ns BenchmarkDotNet.Disassemblers
- **BenchmarkDotNet.IntegrationTests.Static** (`tests/BenchmarkDotNet.IntegrationTests.Static/BenchmarkDotNet.IntegrationTests.Static.csproj`; net462, net7.0) → BenchmarkDotNet, BenchmarkDotNet.Annotations; 2 public types; ns BenchmarkDotNet.IntegrationTests.Static
- **BenchmarkDotNet.IntegrationTests.DisabledOptimizations** (`tests/BenchmarkDotNet.IntegrationTests.DisabledOptimizations/BenchmarkDotNet.IntegrationTests.DisabledOptimizations.csproj`; net462, net7.0) → BenchmarkDotNet, BenchmarkDotNet.Annotations; 1 public types; ns BenchmarkDotNet.IntegrationTests.DisabledOptimizations
- **BenchmarkDotNet.IntegrationTests.EnabledOptimizations** (`tests/BenchmarkDotNet.IntegrationTests.EnabledOptimizations/BenchmarkDotNet.IntegrationTests.EnabledOptimizations.csproj`; net462, net7.0) → BenchmarkDotNet, BenchmarkDotNet.Annotations; 1 public types; ns BenchmarkDotNet.IntegrationTests.EnabledOptimizations
- **BenchmarkDotNet.Templates** (`templates/BenchmarkDotNet.Templates.csproj`; netstandard2.0) → no project refs; 0 public types; ns 

### Key public types (members abbreviated)
- BenchmarkDotNet: `static class BenchmarkRunner` (src/BenchmarkDotNet/Running/BenchmarkRunnerDirty.cs)
  static Summary Run<T>(IConfig config, string[] args); static Summary Run(Type type, IConfig config, string[] args); static Summary[] Run(Type[] types, IConfig config, string[] args); static Summary Run(Type type, MethodInfo[] methods, IConfig config); static Summary[] Run(Assembly assembly, IConfig config, string[] args); static Summary Run(BenchmarkRunInfo benchmarkRunInfo); static Summary[] Run(BenchmarkRunInfo[] benchmarkRunInfos); static Summary RunUrl(string url, IConfig config); … +1
- BenchmarkDotNet.Samples: `class Program` (samples/BenchmarkDotNet.Samples/Program.cs)
  static void Main(string[] args)
- BenchmarkDotNet.Diagnostics.Windows: `static class HardwareCounters` (src/BenchmarkDotNet.Diagnostics.Windows/HardwareCounters.cs)
  static IEnumerable<ValidationError> Validate(ValidationParameters validationParameters, bool mandatory)
- BenchmarkDotNet.Annotations: `class GenericTypeArgumentsAttribute : Attribute` (src/BenchmarkDotNet.Annotations/Attributes/GenericTypeArgumentsAttribute.cs)
  Type[] GenericTypeArguments { get; }; GenericTypeArgumentsAttribute(Type type); GenericTypeArgumentsAttribute(Type type1, Type type2); GenericTypeArgumentsAttribute(Type type1, Type type2, Type type3)
- BenchmarkDotNet.IntegrationTests.CustomPaths: `class BenchmarksThatReturnTypeFromCustomPathDll` (tests/BenchmarkDotNet.IntegrationTests.CustomPaths/BenchmarksThatReturnTypeFromCustomPathDll.cs)
  SingleClass Benchmark()
- BenchmarkDotNet.Diagnostics.dotTrace: `class DotTraceDiagnoserAttribute : Attribute, IConfigSource` (src/BenchmarkDotNet.Diagnostics.dotTrace/DotTraceDiagnoserAttribute.cs)
  IConfig Config { get; }; DotTraceDiagnoserAttribute(); DotTraceDiagnoserAttribute(Uri nugetUrl, string toolsDownloadFolder)
- BenchmarkDotNet.IntegrationTests.ConfigPerAssembly: `class AssemblyConfigAttribute : Attribute, IConfigSource` (tests/BenchmarkDotNet.IntegrationTests.ConfigPerAssembly/AssemblyConfigAttribute.cs)
  IConfig Config { get; }; static bool IsActivated; AssemblyConfigAttribute()
- BenchmarkDotNet.Disassembler.x64: `class Sharp : SourceCode` (src/BenchmarkDotNet.Disassembler.x64/DataContracts.cs)
  string Text { get; set; }; string FilePath { get; set; }; int LineNumber { get; set; }
- BenchmarkDotNet.Disassembler.x86: `class Sharp : SourceCode` (src/BenchmarkDotNet.Disassembler.x64/DataContracts.cs)
  string Text { get; set; }; string FilePath { get; set; }; int LineNumber { get; set; }
- BenchmarkDotNet.IntegrationTests.Static: `class BenchmarkClassWithInstanceMethod` (tests/BenchmarkDotNet.IntegrationTests.Static/BenchmarkClassWithStaticMethod.cs)
  void NonStaticMethod()
- BenchmarkDotNet.IntegrationTests.DisabledOptimizations: `class OptimizationsDisabledInCsproj` (tests/BenchmarkDotNet.IntegrationTests.DisabledOptimizations/OptimizationsDisabledInCsproj.cs)
  string Benchmark()
- BenchmarkDotNet.IntegrationTests.EnabledOptimizations: `class OptimizationsEnabledInCsproj` (tests/BenchmarkDotNet.IntegrationTests.EnabledOptimizations/OptimizationsEnabledInCsproj.cs)
  string Benchmark()
- BenchmarkDotNet: `class RunMode : JobMode<RunMode>` (src/BenchmarkDotNet/Jobs/RunMode.cs)
  static readonly Characteristic<RunStrategy> RunStrategyCharacteristic; static readonly Characteristic<int> LaunchCountCharacteristic; static readonly Characteristic<long> InvocationCountCharacteristic; static readonly Characteristic<int> UnrollFactorCharacteristic; static readonly Characteristic<int> IterationCountCharacteristic; static readonly Characteristic<int> MinIterationCountCharacteristic; static readonly Characteristic<int> MaxIterationCountCharacteristic; static readonly Characteristic<TimeInterval> IterationTimeCharacteristic; … +22
- BenchmarkDotNet.Samples: `class IntroHardwareCounters` (samples/BenchmarkDotNet.Samples/IntroHardwareCounters.cs)
  IntroHardwareCounters(); int SortedBranch(); int UnsortedBranch(); int SortedBranchless(); int UnsortedBranchless()
- BenchmarkDotNet.Diagnostics.Windows: `class EtwProfilerConfig` (src/BenchmarkDotNet.Diagnostics.Windows/EtwProfilerConfig.cs)
  const ulong MatchAnyKeywords; bool PerformExtraBenchmarksRun { get; }; int BufferSizeInMb { get; }; float CpuSampleIntervalInMilliseconds { get; }; Keywords KernelKeywords { get; }; Keywords KernelStackKeywords { get; }; IReadOnlyDictionary<HardwareCounter, Func<ProfileSourceInfo, int>> IntervalSelectors { get; }; IReadOnlyCollection<(Guid providerGuid, TraceEventLevel providerLevel, ulong keywords, TraceEventProviderOptions options)> Providers { get; }; … +2
- BenchmarkDotNet.Annotations: `class BenchmarkAttribute : Attribute` (src/BenchmarkDotNet.Annotations/Attributes/BenchmarkAttribute.cs)
  BenchmarkAttribute(int sourceCodeLineNumber, string sourceCodeFile); string Description { get; set; }; bool Baseline { get; set; }; int OperationsPerInvoke { get; set; }; int SourceCodeLineNumber { get; }; string SourceCodeFile { get; }
- BenchmarkDotNet.IntegrationTests.CustomPaths: `class BenchmarksThatUseTypeFromCustomPathDll` (tests/BenchmarkDotNet.IntegrationTests.CustomPaths/BenchmarksThatUseTypeFromCustomPathDll.cs)
  string Benchmark()
- BenchmarkDotNet.Diagnostics.dotTrace: `class DotTraceDiagnoser : IProfiler` (src/BenchmarkDotNet.Diagnostics.dotTrace/DotTraceDiagnoser.cs)
  DotTraceDiagnoser(Uri nugetUrl, string toolsDownloadFolder); IEnumerable<string> Ids { get; }; string ShortName { get; }; RunMode GetRunMode(BenchmarkCase benchmarkCase); void Handle(HostSignal signal, DiagnoserActionParameters parameters); IEnumerable<IExporter> Exporters { get; }; IEnumerable<IAnalyser> Analysers { get; }; IEnumerable<ValidationError> Validate(ValidationParameters validationParameters); … +2
- BenchmarkDotNet.IntegrationTests.ConfigPerAssembly: `class AssemblyConfigBenchmarks` (tests/BenchmarkDotNet.IntegrationTests.ConfigPerAssembly/AssemblyConfigBenchmarks.cs)
  void Foo()
- BenchmarkDotNet.Disassembler.x64: `abstract class Asm : SourceCode` (src/BenchmarkDotNet.Disassembler.x64/DataContracts.cs)
  int InstructionLength { get; set; }; ulong? ReferencedAddress { get; set; }; bool IsReferencedAddressIndirect { get; set; }
- BenchmarkDotNet.Disassembler.x86: `abstract class Asm : SourceCode` (src/BenchmarkDotNet.Disassembler.x64/DataContracts.cs)
  int InstructionLength { get; set; }; ulong? ReferencedAddress { get; set; }; bool IsReferencedAddressIndirect { get; set; }
- BenchmarkDotNet.IntegrationTests.Static: `class BenchmarkClassWithStaticMethodsOnly` (tests/BenchmarkDotNet.IntegrationTests.Static/BenchmarkClassWithStaticMethod.cs)
  static void StaticMethod()
- BenchmarkDotNet: `class BenchmarkSwitcher` (src/BenchmarkDotNet/Running/BenchmarkSwitcher.cs)
  BenchmarkSwitcher(Type[] types); BenchmarkSwitcher(Assembly assembly); BenchmarkSwitcher(Assembly[] assemblies); BenchmarkSwitcher With(Type type); BenchmarkSwitcher With(Type[] types); BenchmarkSwitcher With(Assembly assembly); BenchmarkSwitcher With(Assembly[] assemblies); static BenchmarkSwitcher FromTypes(Type[] types); … +5
- BenchmarkDotNet.Samples: `class IntroComparableComplexParam.ComplexParam : IComparable<IntroComparableComplexParam.ComplexParam>, IComparable` (samples/BenchmarkDotNet.Samples/IntroComparableComplexParam.cs)
  ComplexParam(int value, string name); int Value { get; set; }; string Name { get; set; }; override string ToString(); int CompareTo(ComplexParam other); int CompareTo(object obj)
- BenchmarkDotNet.Diagnostics.Windows: `class IterationData` (src/BenchmarkDotNet.Diagnostics.Windows/Tracing/TraceLogParser.cs)
  Dictionary<int, ulong> ProfileSourceIdToCount { get; }; IterationData(double startTimestamp, double stopTimestamp); bool TryHandle(double timeStamp, int profileSource, int interval)
- BenchmarkDotNet.Annotations: `enum RuntimeMoniker` (src/BenchmarkDotNet.Annotations/Jobs/RuntimeMoniker.cs)
  HostProcess; NotRecognized; Mono; Net461; … +31
- BenchmarkDotNet.IntegrationTests.CustomPaths: `class BenchmarksThatUsesFileFromOutput` (tests/BenchmarkDotNet.IntegrationTests.CustomPaths/BenchmarksThatUsesFileFromOutput.cs)
  void Verify()
- BenchmarkDotNet.Diagnostics.dotTrace: `class Progress : IProgress<double>` (src/BenchmarkDotNet.Diagnostics.dotTrace/Progress.cs)
  Progress(ILogger logger, string title); void Report(double value)
