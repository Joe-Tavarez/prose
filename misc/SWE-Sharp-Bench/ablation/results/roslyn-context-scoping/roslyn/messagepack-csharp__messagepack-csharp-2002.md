## Repository map (from Roslyn, at the starting commit; declarations only)
Solution `MessagePack.sln`, .NET SDK 8.0.404, 28 C# projects (8 test). Projects are listed most relevant to the issue first.

### Projects
- **MessagePack** (`src/MessagePack/MessagePack.csproj`; net472, net8.0, netstandard2.0, netstandard2.1) → MessagePack.Analyzers, MessagePack.Annotations; 247 public types; ns MessagePack.Formatters, MessagePack, MessagePack.Resolvers
- **DynamicCodeDumper** (`sandbox/DynamicCodeDumper/DynamicCodeDumper.csproj`; net472) → no project refs; 152 public types; ns SharedData, MessagePack, MessagePack.Internal
- **MessagePack.SourceGenerator** (`src/MessagePack.SourceGenerator/MessagePack.SourceGenerator.csproj`; netstandard2.0) → no project refs; 62 public types; ns MessagePack.SourceGenerator.CodeAnalysis, MessagePack.SourceGenerator.Transforms, System.Diagnostics.CodeAnalysis
- MessagePack.Tests (`tests/MessagePack.Tests/MessagePack.Tests.csproj`; net8.0) — tests MessagePack, MessagePack.Analyzers, MessagePack.Annotations, MessagePack.ImmutableCollection, MessagePack.ReactiveProperty, MessagePack.UnityShims, SharedData
- **SerializerBenchmark** (`benchmark/SerializerBenchmark/SerializerBenchmark.csproj`; net8.0) → MessagePack, MessagePack.Analyzers, MessagePack.Annotations; 129 public types; ns Benchmark.Models, Benchmark.Serializers, Benchmark.Fixture
- **PerfBenchmarkDotNet** (`sandbox/PerfBenchmarkDotNet/PerfBenchmarkDotNet.csproj`; net472, net8.0) → MessagePack, MessagePack.Analyzers, MessagePack.Annotations; 25 public types; ns PerfBenchmarkDotNet, System.Diagnostics.CodeAnalysis, GeneratedFormatter.MessagePack.Formatters
- **MessagePack.Annotations** (`src/MessagePack.Annotations/MessagePack.Annotations.csproj`; netstandard2.0) → no project refs; 10 public types; ns System.Diagnostics.CodeAnalysis, MessagePack
- **SharedData** (`sandbox/SharedData/SharedData.csproj`; netstandard2.0) → MessagePack, MessagePack.Analyzers, MessagePack.Annotations; 87 public types; ns SharedData, (global), System.Diagnostics.CodeAnalysis
- MessagePack.SourceGenerator.Tests (`tests/MessagePack.SourceGenerator.Tests/MessagePack.SourceGenerator.Tests.csproj`; net8.0) — tests MessagePack, MessagePack.Analyzers, MessagePack.Analyzers.CodeFixes, MessagePack.Annotations, MessagePack.SourceGenerator
- **MessagePack.AspNetCoreMvcFormatter** (`src/MessagePack.AspNetCoreMvcFormatter/MessagePack.AspNetCoreMvcFormatter.csproj`; net8.0, netstandard2.0) → MessagePack, MessagePack.Analyzers, MessagePack.Annotations; 2 public types; ns System.Diagnostics.CodeAnalysis, MessagePack.AspNetCoreMvcFormatter
- **MessagePack.UnityShims** (`src/MessagePack.UnityShims/MessagePack.UnityShims.csproj`; netstandard2.0) → MessagePack, MessagePack.Analyzers, MessagePack.Annotations; 63 public types; ns MessagePack.Unity, UnityEngine, MessagePack.Unity.Extension
- **Sandbox** (`sandbox/Sandbox/Sandbox.csproj`; net8.0) → MessagePack, MessagePack.Analyzers, MessagePack.Annotations, MessagePack.UnityShims, SharedData; 30 public types; ns Sandbox
- MessagePack.Internal.Tests (`tests/MessagePack.Internal.Tests/MessagePack.Internal.Tests.csproj`; net8.0) — tests MessagePack.Internal
- **MessagePack.Analyzers.CodeFixes** (`src/MessagePack.Analyzers.CodeFixes/MessagePack.Analyzers.CodeFixes.csproj`; netstandard2.0) → MessagePack.SourceGenerator; 3 public types; ns System.Diagnostics.CodeAnalysis, MessagePack.Analyzers.CodeFixes
- MessagePack.AspNetCoreMvcFormatter.Tests (`tests/MessagePack.AspNetCoreMvcFormatter.Tests/MessagePack.AspNetCoreMvcFormatter.Tests.csproj`; net8.0) — tests MessagePack, MessagePack.Analyzers, MessagePack.Annotations, MessagePack.AspNetCoreMvcFormatter, MessagePack.ImmutableCollection, MessagePack.ReactiveProperty, MessagePack.UnityShims, SharedData
- **TestData2** (`sandbox/TestData2/TestData2.csproj`; net462) → no project refs; 18 public types; ns TestData2, System.Diagnostics.CodeAnalysis, System.Runtime.CompilerServices
- **MessagePack.Experimental** (`src/MessagePack.Experimental/MessagePack.Experimental.csproj`; net8.0) → MessagePack, MessagePack.Analyzers, MessagePack.Annotations; 12 public types; ns MessagePack.Formatters, MessagePack.Resolvers
- **MessagePack.ReactiveProperty** (`src/MessagePack.ReactiveProperty/MessagePack.ReactiveProperty.csproj`; netstandard2.0) → MessagePack, MessagePack.Analyzers, MessagePack.Annotations; 9 public types; ns MessagePack.ReactivePropertyExtension, System.Diagnostics.CodeAnalysis
- MessagePack.SourceGenerator.ExecutionTests (`tests/MessagePack.SourceGenerator.ExecutionTests/MessagePack.SourceGenerator.ExecutionTests.csproj`; net8.0) — tests MessagePack, MessagePack.Analyzers, MessagePack.Annotations
- … 9 more: PerfNetFramework, MessagePack.GeneratedCode.Tests, MessagePack.SourceGenerator.MapModeExecutionTests, CollectionsMarshalBenchmark, ExperimentalBenchmark, MessagePack.Analyzers, MessagePack.ImmutableCollection, MessagePack.Internal, MessagePack.Experimental.Tests

### Key public types (members abbreviated)
- MessagePack: `class MessagePackSerializationException : Exception` (src/MessagePack/MessagePackSerializationException.cs)
  MessagePackSerializationException(); MessagePackSerializationException(string message); MessagePackSerializationException(string message, Exception inner); protected MessagePackSerializationException(SerializationInfo info, StreamingContext context)
- DynamicCodeDumper: `class MessagePackSerializationException : Exception` (src/MessagePack/MessagePackSerializationException.cs)
  MessagePackSerializationException(); MessagePackSerializationException(string message); MessagePackSerializationException(string message, Exception inner); protected MessagePackSerializationException(SerializationInfo info, StreamingContext context)
- MessagePack.SourceGenerator: `class MsgPack00xMessagePackAnalyzer : DiagnosticAnalyzer` (src/MessagePack.SourceGenerator/Analyzers/MsgPack00xMessagePackAnalyzer.cs)
  const string UseMessagePackObjectAttributeId; const string AttributeMessagePackObjectMembersId; const string InvalidMessagePackObjectId; const string MessagePackFormatterMustBeMessagePackFormatterId; const string DeserializingConstructorId; const string AOTLimitationsId; const string CollidingFormattersId; const string InaccessibleFormatterTypeId; … +37
- SerializerBenchmark: `class Info.Site : IGenericEquality<Info.Site>` (benchmark/SerializerBenchmark/Models/Info.cs)
  string site_type { get; set; }; string name { get; set; }; string logo_url { get; set; }; string api_site_parameter { get; set; }; string site_url { get; set; }; string audience { get; set; }; string icon_url { get; set; }; List<string> aliases { get; set; }; … +12
- PerfBenchmarkDotNet: `class TypelessDeserializeBenchmark` (sandbox/PerfBenchmarkDotNet/TypelessDeserializeBenchmark.cs)
  ContractType Old_MessagePackSerializer_Deserialize_StandardResolver(); ContractlessType Old_MessagePackSerializer_Deserialize_ContractlessStandardResolver(); TypelessPrimitiveType Old_MessagePackSerializer_Deserialize_TypelessContractlessStandardResolver(); TypelessPrimitiveType Old_MessagePackSerializer_Deserialize_TypelessContractlessStandardResolverComplexBytes(); ContractType MessagePackSerializer_Deserialize_StandardResolver(); ContractlessType MessagePackSerializer_Deserialize_ContractlessStandardResolver(); TypelessPrimitiveType MessagePackSerializer_Deserialize_TypelessContractlessStandardResolver(); TypelessPrimitiveType MessagePackSerializer_Deserialize_TypelessContractlessStandardResolverComplexBytes()
- MessagePack.Annotations: `class MessagePackFormatterAttribute : Attribute` (src/MessagePack.Annotations/Attributes.cs)
  Type FormatterType { get; }; object[] Arguments { get; }; MessagePackFormatterAttribute(Type formatterType); MessagePackFormatterAttribute(Type formatterType, params object[] arguments)
- SharedData: `class MessagePackFormatterFieldUser` (sandbox/SharedData/Class1.cs)
  DateTime Timestamp { get; set; }
- MessagePack.AspNetCoreMvcFormatter: `class MessagePackInputFormatter : InputFormatter` (src/MessagePack.AspNetCoreMvcFormatter/MessagePackInputFormatter.cs)
  MessagePackInputFormatter(); MessagePackInputFormatter(MessagePackSerializerOptions options); override Task<InputFormatterResult> ReadRequestBodyAsync(InputFormatterContext context)
- MessagePack.UnityShims: `class UnityResolver : IFormatterResolver` (src/MessagePack.UnityClient/Assets/Scripts/MessagePack/UnityResolver.cs)
  static readonly IFormatterResolver Instance; static readonly IFormatterResolver InstanceWithStandardResolver; IMessagePackFormatter<T> GetFormatter<T>()
- Sandbox: `class GeneratedMessagePackResolver` (sandbox/Sandbox/GeneratedMessagePackResolver.cs)
- MessagePack.Analyzers.CodeFixes: `class MessagePackCodeFixProvider : CodeFixProvider` (src/MessagePack.Analyzers.CodeFixes/CodeFixes/MessagePackCodeFixProvider.cs)
  const string AddKeyAttributeEquivanceKey; const string AddIgnoreMemberAttributeEquivalenceKey; override ImmutableArray<string> FixableDiagnosticIds { get; }; override FixAllProvider GetFixAllProvider(); override Task RegisterCodeFixesAsync(CodeFixContext context)
- TestData2: `class PropNameCheck1` (sandbox/TestData2/PropNameCheck1.cs)
  string MyProperty1 { get; set; }; virtual string MyProperty2 { get; set; }
- MessagePack.Experimental: `class PrimitiveArrayResolver : IFormatterResolver` (src/MessagePack.Experimental/HardwareIntrinsics/PrimitiveArrayResolver.cs)
  static readonly PrimitiveArrayResolver Instance; IMessagePackFormatter<T> GetFormatter<T>()
- MessagePack.ReactiveProperty: `class ReactivePropertyResolver : IFormatterResolver` (src/MessagePack.ReactiveProperty/ReactivePropertyResolver.cs)
  static readonly ReactivePropertyResolver Instance; IMessagePackFormatter<T> GetFormatter<T>()
- PerfNetFramework: `class Person : IEquatable<Person>` (sandbox/PerfNetFramework/Person.cs)
  virtual int Age { get; set; }; virtual string FirstName { get; set; }; virtual string LastName { get; set; }; virtual Sex Sex { get; set; }; bool Equals(Person other)
- CollectionsMarshalBenchmark: `struct Matrix4x4` (benchmark/CollectionsMarshalBenchmark/RandomMatrix4x4Benchmark.cs)
  float M11; float M12; float M13; float M14; … +13
- ExperimentalBenchmark: `class BoolDeserializeTest` (benchmark/ExperimentalBenchmark/BoolDeserializeTest.cs)
  string Setting { get; set; }; void SetUp(); bool[] Old(); bool[] Simd()
- MessagePack: `struct MessagePackReader` (src/MessagePack/MessagePackReader.cs)
  MessagePackReader(ReadOnlyMemory<byte> memory); MessagePackReader(in ReadOnlySequence<byte> readOnlySequence); CancellationToken CancellationToken { get; set; }; int Depth { get; set; }; ReadOnlySequence<byte> Sequence { get; }; SequencePosition Position { get; }; long Consumed { get; }; bool End { get; }; … +35
- DynamicCodeDumper: `struct MessagePackReader` (src/MessagePack/MessagePackReader.cs)
  MessagePackReader(ReadOnlyMemory<byte> memory); MessagePackReader(in ReadOnlySequence<byte> readOnlySequence); CancellationToken CancellationToken { get; set; }; int Depth { get; set; }; ReadOnlySequence<byte> Sequence { get; }; SequencePosition Position { get; }; long Consumed { get; }; bool End { get; }; … +35
- MessagePack.SourceGenerator: `class MessagePackSerializationException : Exception` (src/MessagePack/MessagePackSerializationException.cs)
  MessagePackSerializationException(); MessagePackSerializationException(string message); MessagePackSerializationException(string message, Exception inner); protected MessagePackSerializationException(SerializationInfo info, StreamingContext context)
- SerializerBenchmark: `enum Info.Site.SiteState` (benchmark/SerializerBenchmark/Models/Info.cs)
  normal; closed_beta; open_beta; linked_meta
- PerfBenchmarkDotNet: `class TypelessSerializeBenchmark` (sandbox/PerfBenchmarkDotNet/TypelessSerializeBenchmark.cs)
  byte[] Old_MessagePackSerializer_Serialize_StandardResolver(); byte[] Old_MessagePackSerializer_Serialize_ContractlessStandardResolver(); byte[] Old_MessagePackSerializer_Serialize_TypelessContractlessStandardResolver_primitive(); byte[] Old_MessagePackSerializer_Serialize_TypelessContractlessStandardResolver_complex(); byte[] MessagePackSerializer_Serialize_StandardResolver(); byte[] MessagePackSerializer_Serialize_ContractlessStandardResolver(); byte[] MessagePackSerializer_Serialize_TypelessContractlessStandardResolver_primitive(); byte[] MessagePackSerializer_Serialize_TypelessContractlessStandardResolver_complex()
- MessagePack.Annotations: `class MessagePackObjectAttribute : Attribute` (src/MessagePack.Annotations/Attributes.cs)
  bool KeyAsPropertyName { get; }; MessagePackObjectAttribute(bool keyAsPropertyName); bool SuppressSourceGeneration { get; set; }; bool AllowPrivate { get; set; }
- SharedData: `class GeneratedMessagePackResolver` (sandbox/SharedData/GeneratedMessagePackResolver.cs)
- MessagePack.AspNetCoreMvcFormatter: `class MessagePackOutputFormatter : OutputFormatter` (src/MessagePack.AspNetCoreMvcFormatter/MessagePackOutputFormatter.cs)
  MessagePackOutputFormatter(); MessagePackOutputFormatter(MessagePackSerializerOptions options); override Task WriteResponseBodyAsync(OutputFormatterWriteContext context)
- MessagePack.UnityShims: `class UnityBlitResolver : IFormatterResolver` (src/MessagePack.UnityClient/Assets/Scripts/MessagePack/Extension/UnityBlitResolver.cs)
  static readonly UnityBlitResolver Instance; IMessagePackFormatter<T> GetFormatter<T>()
