## Repository map (from Roslyn, at the starting commit; declarations only)
Solution `BenchmarkDotNet.sln`, .NET SDK 8.0.200, 15 C# projects (3 test). Projects are listed most relevant to the issue first.

### Projects
- **BenchmarkDotNet** (`src/BenchmarkDotNet/BenchmarkDotNet.csproj`; net6.0, netstandard2.0) → BenchmarkDotNet.Annotations; 476 public types; ns BenchmarkDotNet.Attributes, JetBrains.Annotations, BenchmarkDotNet.Columns
- BenchmarkDotNet.Tests (`tests/BenchmarkDotNet.Tests/BenchmarkDotNet.Tests.csproj`; net462, net7.0) — tests BenchmarkDotNet, BenchmarkDotNet.Annotations, BenchmarkDotNet.Diagnostics.Windows
- BenchmarkDotNet.IntegrationTests (`tests/BenchmarkDotNet.IntegrationTests/BenchmarkDotNet.IntegrationTests.csproj`; net462, net7.0) — tests BenchmarkDotNet, BenchmarkDotNet.Annotations, BenchmarkDotNet.Diagnostics.Windows, BenchmarkDotNet.IntegrationTests.ConfigPerAssembly, BenchmarkDotNet.IntegrationTests.CustomPaths, BenchmarkDotNet.IntegrationTests.DisabledOptimizations, BenchmarkDotNet.IntegrationTests.EnabledOptimizations, BenchmarkDotNet.IntegrationTests.Static
- **BenchmarkDotNet.Samples** (`samples/BenchmarkDotNet.Samples/BenchmarkDotNet.Samples.csproj`; net462, net7.0) → BenchmarkDotNet, BenchmarkDotNet.Annotations, BenchmarkDotNet.Diagnostics.Windows; 84 public types; ns BenchmarkDotNet.Samples
- **BenchmarkDotNet.Annotations** (`src/BenchmarkDotNet.Annotations/BenchmarkDotNet.Annotations.csproj`; netstandard1.0, netstandard2.0) → no project refs; 15 public types; ns JetBrains.Annotations, BenchmarkDotNet.Attributes, System.Diagnostics.CodeAnalysis
- **BenchmarkDotNet.Diagnostics.Windows** (`src/BenchmarkDotNet.Diagnostics.Windows/BenchmarkDotNet.Diagnostics.Windows.csproj`; netstandard2.0) → BenchmarkDotNet, BenchmarkDotNet.Annotations; 24 public types; ns BenchmarkDotNet.Diagnostics.Windows, BenchmarkDotNet.Diagnostics.Windows.Tracing, BenchmarkDotNet.Diagnostics.Windows.Configs
- **BenchmarkDotNet.Disassembler.x64** (`src/BenchmarkDotNet.Disassembler.x64/BenchmarkDotNet.Disassembler.x64.csproj`; ?) → no project refs; 11 public types; ns BenchmarkDotNet.Disassemblers
- **BenchmarkDotNet.Disassembler.x86** (`src/BenchmarkDotNet.Disassembler.x86/BenchmarkDotNet.Disassembler.x86.csproj`; ?) → no project refs; 11 public types; ns BenchmarkDotNet.Disassemblers
- **BenchmarkDotNet.IntegrationTests.CustomPaths** (`tests/BenchmarkDotNet.IntegrationTests.CustomPaths/BenchmarkDotNet.IntegrationTests.CustomPaths.csproj`; net462) → BenchmarkDotNet, BenchmarkDotNet.Annotations; 3 public types; ns BenchmarkDotNet.IntegrationTests.CustomPaths
- BenchmarkDotNet.IntegrationTests.ManualRunning (`tests/BenchmarkDotNet.IntegrationTests.ManualRunning/BenchmarkDotNet.IntegrationTests.ManualRunning.csproj`; net462, net7.0) — tests BenchmarkDotNet, BenchmarkDotNet.Annotations, BenchmarkDotNet.Diagnostics.Windows
- **BenchmarkDotNet.IntegrationTests.ConfigPerAssembly** (`tests/BenchmarkDotNet.IntegrationTests.ConfigPerAssembly/BenchmarkDotNet.IntegrationTests.ConfigPerAssembly.csproj`; net462, net7.0) → BenchmarkDotNet, BenchmarkDotNet.Annotations; 2 public types; ns BenchmarkDotNet.IntegrationTests.ConfigPerAssembly
- **BenchmarkDotNet.IntegrationTests.Static** (`tests/BenchmarkDotNet.IntegrationTests.Static/BenchmarkDotNet.IntegrationTests.Static.csproj`; net462, net7.0) → BenchmarkDotNet, BenchmarkDotNet.Annotations; 2 public types; ns BenchmarkDotNet.IntegrationTests.Static
- **BenchmarkDotNet.IntegrationTests.DisabledOptimizations** (`tests/BenchmarkDotNet.IntegrationTests.DisabledOptimizations/BenchmarkDotNet.IntegrationTests.DisabledOptimizations.csproj`; net462, net7.0) → BenchmarkDotNet, BenchmarkDotNet.Annotations; 1 public types; ns BenchmarkDotNet.IntegrationTests.DisabledOptimizations
- **BenchmarkDotNet.IntegrationTests.EnabledOptimizations** (`tests/BenchmarkDotNet.IntegrationTests.EnabledOptimizations/BenchmarkDotNet.IntegrationTests.EnabledOptimizations.csproj`; net462, net7.0) → BenchmarkDotNet, BenchmarkDotNet.Annotations; 1 public types; ns BenchmarkDotNet.IntegrationTests.EnabledOptimizations
- **BenchmarkDotNet.Templates** (`templates/BenchmarkDotNet.Templates.csproj`; netstandard2.0) → no project refs; 0 public types; ns 

### Key public types (members abbreviated)
- BenchmarkDotNet: `class RunnableConstants` (src/BenchmarkDotNet/Toolchains/InProcess/Emit/Implementation/Runnable/RunnableConstants.cs)
  const string IsByRefLikeAttributeTypeName; const string OpImplicitMethodName; const string DynamicAssemblySuffix; const string EmittedTypePrefix; const string WorkloadDelegateTypeSuffix; const string OverheadDelegateTypeSuffix; const string ArgFieldPrefix; const string ArgParamPrefix; … +30
- BenchmarkDotNet.Samples: `class IntroParamsSource` (samples/BenchmarkDotNet.Samples/IntroParamsSource.cs)
  int A { get; set; }; int B; IEnumerable<int> ValuesForA { get; }; static IEnumerable<int> ValuesForB(); void Benchmark()
- BenchmarkDotNet.Annotations: `class ParamsSourceAttribute : PriorityAttribute` (src/BenchmarkDotNet.Annotations/Attributes/ParamsSourceAttribute.cs)
  string Name { get; }; ParamsSourceAttribute(string name)
- BenchmarkDotNet.Diagnostics.Windows: `abstract class JitDiagnoser<TStats> : EtwDiagnoser<TStats>, IDiagnoser` (src/BenchmarkDotNet.Diagnostics.Windows/JitDiagnoser.cs)
  protected override ulong EventType { get; }; protected override string SessionNamePrefix { get; }; override RunMode GetRunMode(BenchmarkCase benchmarkCase); abstract IEnumerable<string> Ids { get; }; void Handle(HostSignal signal, DiagnoserActionParameters parameters); virtual IEnumerable<Metric> ProcessResults(DiagnoserResults results); IEnumerable<ValidationError> Validate(ValidationParameters validationParameters); void DisplayResults(ILogger outputLogger)
- BenchmarkDotNet.Disassembler.x64: `class IntelAsm : Asm` (src/BenchmarkDotNet.Disassembler.x64/DataContracts.cs)
  Instruction Instruction { get; set; }; override string ToString()
- BenchmarkDotNet.Disassembler.x86: `class IntelAsm : Asm` (src/BenchmarkDotNet.Disassembler.x64/DataContracts.cs)
  Instruction Instruction { get; set; }; override string ToString()
- BenchmarkDotNet.IntegrationTests.CustomPaths: `class BenchmarksThatReturnTypeFromCustomPathDll` (tests/BenchmarkDotNet.IntegrationTests.CustomPaths/BenchmarksThatReturnTypeFromCustomPathDll.cs)
  SingleClass Benchmark()
- BenchmarkDotNet.IntegrationTests.ConfigPerAssembly: `class AssemblyConfigAttribute : Attribute, IConfigSource` (tests/BenchmarkDotNet.IntegrationTests.ConfigPerAssembly/AssemblyConfigAttribute.cs)
  IConfig Config { get; }; static bool IsActivated; AssemblyConfigAttribute()
- BenchmarkDotNet.IntegrationTests.Static: `class BenchmarkClassWithInstanceMethod` (tests/BenchmarkDotNet.IntegrationTests.Static/BenchmarkClassWithStaticMethod.cs)
  void NonStaticMethod()
- BenchmarkDotNet.IntegrationTests.DisabledOptimizations: `class OptimizationsDisabledInCsproj` (tests/BenchmarkDotNet.IntegrationTests.DisabledOptimizations/OptimizationsDisabledInCsproj.cs)
  string Benchmark()
- BenchmarkDotNet.IntegrationTests.EnabledOptimizations: `class OptimizationsEnabledInCsproj` (tests/BenchmarkDotNet.IntegrationTests.EnabledOptimizations/OptimizationsEnabledInCsproj.cs)
  string Benchmark()
- BenchmarkDotNet: `class PercentileValues` (src/BenchmarkDotNet/Mathematics/PercentileValues.cs)
  double Percentile(int percentile); double P0 { get; }; double P25 { get; }; double P50 { get; }; double P67 { get; }; double P80 { get; }; double P85 { get; }; double P90 { get; }; … +5
- BenchmarkDotNet.Samples: `class IntroCustomMonoArguments.ConfigWithCustomArguments : ManualConfig` (samples/BenchmarkDotNet.Samples/IntroCustomMonoArguments.cs)
  ConfigWithCustomArguments()
- BenchmarkDotNet.Annotations: `class ParamsAttribute : PriorityAttribute` (src/BenchmarkDotNet.Annotations/Attributes/ParamsAttribute.cs)
  object[] Values { get; }; ParamsAttribute(); ParamsAttribute(params object[] values)
- BenchmarkDotNet.Diagnostics.Windows: `class EtwProfiler : IDiagnoser, IHardwareCountersDiagnoser, IProfiler` (src/BenchmarkDotNet.Diagnostics.Windows/EtwProfiler.cs)
  EtwProfiler(); EtwProfiler(EtwProfilerConfig config); string ShortName { get; }; IEnumerable<string> Ids { get; }; IEnumerable<IExporter> Exporters { get; }; IEnumerable<IAnalyser> Analysers { get; }; IReadOnlyDictionary<BenchmarkCase, PmcStats> Results { get; }; RunMode GetRunMode(BenchmarkCase benchmarkCase); … +4
- BenchmarkDotNet.Disassembler.x64: `class DisassemblyResult` (src/BenchmarkDotNet.Disassembler.x64/DataContracts.cs)
  DisassembledMethod[] Methods { get; set; }; string[] Errors { get; set; }; MutablePair[] SerializedAddressToNameMapping { get; set; }; uint PointerSize { get; set; }; Dictionary<ulong, string> AddressToNameMapping { get; }; DisassemblyResult()
- BenchmarkDotNet.Disassembler.x86: `class DisassemblyResult` (src/BenchmarkDotNet.Disassembler.x64/DataContracts.cs)
  DisassembledMethod[] Methods { get; set; }; string[] Errors { get; set; }; MutablePair[] SerializedAddressToNameMapping { get; set; }; uint PointerSize { get; set; }; Dictionary<ulong, string> AddressToNameMapping { get; }; DisassemblyResult()
- BenchmarkDotNet.IntegrationTests.CustomPaths: `class BenchmarksThatUseTypeFromCustomPathDll` (tests/BenchmarkDotNet.IntegrationTests.CustomPaths/BenchmarksThatUseTypeFromCustomPathDll.cs)
  string Benchmark()
- BenchmarkDotNet.IntegrationTests.ConfigPerAssembly: `class AssemblyConfigBenchmarks` (tests/BenchmarkDotNet.IntegrationTests.ConfigPerAssembly/AssemblyConfigBenchmarks.cs)
  void Foo()
- BenchmarkDotNet.IntegrationTests.Static: `class BenchmarkClassWithStaticMethodsOnly` (tests/BenchmarkDotNet.IntegrationTests.Static/BenchmarkClassWithStaticMethod.cs)
  static void StaticMethod()
- BenchmarkDotNet: `interface IOrderer` (src/BenchmarkDotNet/Order/IOrderer.cs)
  IEnumerable<BenchmarkCase> GetExecutionOrder(ImmutableArray<BenchmarkCase> benchmarksCase, IEnumerable<BenchmarkLogicalGroupRule> order); IEnumerable<BenchmarkCase> GetSummaryOrder(ImmutableArray<BenchmarkCase> benchmarksCases, Summary summary); string GetHighlightGroupKey(BenchmarkCase benchmarkCase); string GetLogicalGroupKey(ImmutableArray<BenchmarkCase> allBenchmarksCases, BenchmarkCase benchmarkCase); IEnumerable<IGrouping<string, BenchmarkCase>> GetLogicalGroupOrder(IEnumerable<IGrouping<string, BenchmarkCase>> logicalGroups, IEnumerable<BenchmarkLogicalGroupRule> order); bool SeparateLogicalGroups { get; }
- BenchmarkDotNet.Samples: `class IntroHardwareCounters` (samples/BenchmarkDotNet.Samples/IntroHardwareCounters.cs)
  IntroHardwareCounters(); int SortedBranch(); int UnsortedBranch(); int SortedBranchless(); int UnsortedBranchless()
- BenchmarkDotNet.Annotations: `class ParamsAllValuesAttribute : PriorityAttribute` (src/BenchmarkDotNet.Annotations/Attributes/ParamsAllValuesAttribute.cs)
- BenchmarkDotNet.Diagnostics.Windows: `class ConcurrencyVisualizerProfiler : IProfiler` (src/BenchmarkDotNet.Diagnostics.Windows/ConcurrencyVisualizerProfiler.cs)
  ConcurrencyVisualizerProfiler(); ConcurrencyVisualizerProfiler(EtwProfilerConfig config); string ShortName { get; }; IEnumerable<string> Ids { get; }; IEnumerable<IExporter> Exporters { get; }; IEnumerable<IAnalyser> Analysers { get; }; void DisplayResults(ILogger logger); void Handle(HostSignal signal, DiagnoserActionParameters parameters); … +3
- BenchmarkDotNet.Disassembler.x64: `class DisassembledMethod` (src/BenchmarkDotNet.Disassembler.x64/DataContracts.cs)
  string Name { get; set; }; ulong NativeCode { get; set; }; string Problem { get; set; }; Map[] Maps { get; set; }; string CommandLine { get; set; }; static DisassembledMethod Empty(string fullSignature, ulong nativeCode, string problem)
- BenchmarkDotNet.Disassembler.x86: `class DisassembledMethod` (src/BenchmarkDotNet.Disassembler.x64/DataContracts.cs)
  string Name { get; set; }; ulong NativeCode { get; set; }; string Problem { get; set; }; Map[] Maps { get; set; }; string CommandLine { get; set; }; static DisassembledMethod Empty(string fullSignature, ulong nativeCode, string problem)
- BenchmarkDotNet.IntegrationTests.CustomPaths: `class BenchmarksThatUsesFileFromOutput` (tests/BenchmarkDotNet.IntegrationTests.CustomPaths/BenchmarksThatUsesFileFromOutput.cs)
  void Verify()
- BenchmarkDotNet: `struct SizeValue` (src/BenchmarkDotNet/Columns/SizeValue.cs)
  long Bytes { get; }; SizeValue(long bytes); SizeValue(long bytes, SizeUnit unit); static readonly SizeValue B; static readonly SizeValue KB; static readonly SizeValue MB; static readonly SizeValue GB; static readonly SizeValue TB; … +9
- BenchmarkDotNet.Samples: `class IntroOrderAttr` (samples/BenchmarkDotNet.Samples/IntroOrderAttr.cs)
  int X { get; set; }; void Slow(); void Fast()
