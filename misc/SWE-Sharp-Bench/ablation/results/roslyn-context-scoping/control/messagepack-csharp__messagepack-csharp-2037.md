## Repository overview (file tree and README, at the starting commit)
929 tracked files, 669 .cs files, 30 .csproj files.

### Project files
- `src/MessagePack/MessagePack.csproj`
- `src/MessagePack.SourceGenerator/MessagePack.SourceGenerator.csproj`
- `tests/MessagePack.SourceGenerator.ExecutionTests/MessagePack.SourceGenerator.ExecutionTests.csproj`
- `tests/MessagePack.SourceGenerator.MapModeExecutionTests/MessagePack.SourceGenerator.MapModeExecutionTests.csproj`
- `tests/MessagePack.SourceGenerator.Tests/MessagePack.SourceGenerator.Tests.csproj`
- `sandbox/MessagePack.Internal/MessagePack.Internal.csproj`
- `src/MessagePack.Analyzers.CodeFixes/MessagePack.Analyzers.CodeFixes.csproj`
- `src/MessagePack.Analyzers/MessagePack.Analyzers.csproj`
- `src/MessagePack.Annotations/MessagePack.Annotations.csproj`
- `tests/MessagePack.GeneratedCode.Tests/MessagePack.GeneratedCode.Tests.csproj`
- `tests/MessagePack.Internal.Tests/MessagePack.Internal.Tests.csproj`
- `benchmark/CollectionsMarshalBenchmark/CollectionsMarshalBenchmark.csproj`
- `benchmark/SerializerBenchmark/SerializerBenchmark.csproj`
- `src/MessagePack.AspNetCoreMvcFormatter/MessagePack.AspNetCoreMvcFormatter.csproj`
- `src/MessagePack.Experimental/MessagePack.Experimental.csproj`
- `src/MessagePack.ImmutableCollection/MessagePack.ImmutableCollection.csproj`
- `src/MessagePack.ReactiveProperty/MessagePack.ReactiveProperty.csproj`
- `src/MessagePack.UnityShims/MessagePack.UnityShims.csproj`
- `tests/MessagePack.AspNetCoreMvcFormatter.Tests/MessagePack.AspNetCoreMvcFormatter.Tests.csproj`
- `tests/MessagePack.Experimental.Tests/MessagePack.Experimental.Tests.csproj`
- `tests/MessagePack.Tests/MessagePack.Tests.csproj`
- `benchmark/ExperimentalBenchmark/ExperimentalBenchmark.csproj`
- `sandbox/DynamicCodeDumper/DynamicCodeDumper.csproj`
- `sandbox/PerfBenchmarkDotNet/PerfBenchmarkDotNet.csproj`
- `sandbox/PerfNetFramework/PerfNetFramework.csproj`
- `sandbox/Sandbox/Sandbox.csproj`
- `sandbox/SharedData/SharedData.csproj`
- `sandbox/TestData.InvalidProject/TestData.InvalidProject.csproj`
- `sandbox/TestData.InvalidSyntax/TestData.InvalidSyntax.csproj`
- `sandbox/TestData2/TestData2.csproj`

### Directories (files; .cs files), most relevant first
- `src/MessagePack/Formatters/` (28; 24 .cs)
- `src/MessagePack.ImmutableCollection/` (2; 1 .cs)
- `src/MessagePack/Resolvers/` (24; 24 .cs)
- `src/MessagePack.SourceGenerator/Analyzers/` (3; 3 .cs)
- `tests/MessagePack.SourceGenerator.Tests/` (250; 20 .cs)
- `src/MessagePack.SourceGenerator/` (60; 6 .cs)
- `tests/MessagePack.SourceGenerator.ExecutionTests/` (26; 25 .cs)
- `tests/MessagePack.SourceGenerator.MapModeExecutionTests/` (6; 5 .cs)
- `src/MessagePack.SourceGenerator.Unity/` (1; 1 .cs)
- `tests/MessagePack.SourceGenerator.Tests/Resources/` (218; 217 .cs)
- `src/MessagePack.SourceGenerator/Transforms/` (20; 12 .cs)
- `src/MessagePack.SourceGenerator/CodeAnalysis/` (19; 19 .cs)
- `tests/MessagePack.SourceGenerator.Tests/Verifiers/` (8; 8 .cs)
- `src/MessagePack.SourceGenerator/Utils/` (3; 3 .cs)
- `tests/MessagePack.SourceGenerator.Tests/CodeAnalysis/` (3; 3 .cs)
- `src/MessagePack.SourceGenerator/Shims/` (1; 1 .cs)
- `src/MessagePack.Analyzers.CodeFixes/` (7; 1 .cs)
- `src/MessagePack.Annotations/` (4; 3 .cs)
- `src/MessagePack.Analyzers/` (3; 0 .cs)
- `tests/MessagePack.GeneratedCode.Tests/` (3; 2 .cs)
- `sandbox/MessagePack.Internal/` (2; 1 .cs)
- `tests/MessagePack.Internal.Tests/` (2; 1 .cs)
- `src/MessagePack/Internal/` (23; 22 .cs)
- `src/MessagePack.Analyzers.CodeFixes/CodeFixes/` (3; 3 .cs)
- `src/MessagePack.Analyzers/build/` (1; 0 .cs)
- `src/MessagePack/` (126; 35 .cs)
- `tests/MessagePack.Tests/` (74; 65 .cs)
- `src/MessagePack.UnityClient/` (71; 0 .cs)
- `src/MessagePack.Experimental/` (16; 0 .cs)
- `tests/MessagePack.Experimental.Tests/` (4; 1 .cs)
- `src/MessagePack.AspNetCoreMvcFormatter/` (3; 2 .cs)
- `src/MessagePack.ReactiveProperty/` (3; 2 .cs)
- `src/MessagePack.UnityShims/` (2; 1 .cs)
- `tests/MessagePack.AspNetCoreMvcFormatter.Tests/` (2; 1 .cs)
- `src/MessagePack.UnityClient/Assets/` (42; 7 .cs)
- `src/MessagePack.UnityClient/ProjectSettings/` (23; 0 .cs)
- `src/MessagePack.Experimental/HardwareIntrinsics/` (8; 5 .cs)
- `src/MessagePack.Experimental/UnsafeUnmanagedStructFormatter/` (6; 5 .cs)
- `src/MessagePack/LZ4/` (5; 5 .cs)
- `tests/MessagePack.Tests/ExtensionTests/` (5; 5 .cs)
- `src/MessagePack.UnityClient/Packages/` (2; 0 .cs)
- `src/MessagePack/net472/` (2; 0 .cs)
- `src/MessagePack/net8.0/` (2; 0 .cs)
- `src/MessagePack/netstandard2.0/` (2; 0 .cs)
- `src/MessagePack/netstandard2.1/` (2; 0 .cs)
- `tests/MessagePack.Tests/Utils/` (2; 2 .cs)
- `src/MessagePack.UnityClient/.config/` (1; 0 .cs)
- `src/MessagePack.UnityClient/UserSettings/` (1; 0 .cs)
- `tests/MessagePack.Experimental.Tests/UnsafeUnmanagedStruct/` (1; 1 .cs)
- `benchmark/SerializerBenchmark/Serializers/` (16; 16 .cs)
- `benchmark/SerializerBenchmark/` (71; 5 .cs)
- `benchmark/CollectionsMarshalBenchmark/` (5; 4 .cs)
- `benchmark/SerializerBenchmark/Models/` (31; 31 .cs)
- `benchmark/SerializerBenchmark/Fixture/` (16; 16 .cs)
- `doc/analyzers/` (19; 0 .cs)
- `tests/` (372; 0 .cs)
- `src/` (304; 1 .cs)
- `benchmark/` (87; 0 .cs)
- `sandbox/` (61; 0 .cs)
- `azure-pipelines/` (34; 0 .cs)
- `doc/` (25; 0 .cs)
- `.github/` (6; 0 .cs)
- `tools/` (6; 0 .cs)
- `.vscode/` (4; 0 .cs)
- `.devcontainer/` (2; 0 .cs)
- `.config/` (1; 0 .cs)
- `sandbox/PerfBenchmarkDotNet/` (27; 24 .cs)
- `azure-pipelines/artifacts/` (11; 0 .cs)
- `sandbox/TestData2/` (11; 10 .cs)
- `benchmark/ExperimentalBenchmark/` (9; 8 .cs)
- `sandbox/PerfNetFramework/` (7; 5 .cs)
- `azure-pipelines/variables/` (3; 0 .cs)
- `sandbox/Sandbox/` (3; 2 .cs)
- `sandbox/SharedData/` (3; 2 .cs)
- `.github/ISSUE_TEMPLATE/` (2; 0 .cs)
- `.github/workflows/` (2; 0 .cs)
- `sandbox/DynamicCodeDumper/` (2; 1 .cs)
- `sandbox/TestData.InvalidProject/` (2; 1 .cs)

### README.md (start)
# MessagePack for C# (.NET Framework, .NET 8, Unity, Xamarin)
The extremely fast [MessagePack](http://msgpack.org/) serializer for C#.
It is 10x faster than [MsgPack-Cli](https://github.com/msgpack/msgpack-cli) and outperforms other C# serializers. MessagePack for C# also ships with built-in support for LZ4 compression - an extremely fast compression algorithm. Performance is important, particularly in applications like games, distributed computing, microservices, or data caches.
MessagePack has a compact binary size and a full set of general purpose expressive data types. Please have a look at the [comparison with JSON, protobuf, ZeroFormatter section](#comparison) and learn [why MessagePack C# is the fastest](#performance).
## Table of Contents
- [Installation](#installation)
    - [NuGet packages](#nuget-packages)
    - [Unity](#unity)
    - [Migration notes from v1.x](#migration-notes-from-v1x)
- [Quick Start](#quick-start)
- [Analyzer](#analyzer)
- [Built-in supported types](#built-in-supported-types)
- [Object Serialization](#object-serialization)
- [DataContract compatibility](#datacontract-compatibility)
- [Serializing readonly/immutable object members  (SerializationConstructor)](#serializing-readonlyimmutable-object-members--serializationconstructor)
- [Serialization Callback](#serialization-callback)
- [Union](#union)
- [Dynamic (Untyped) Deserialization](#dynamic-untyped-deserialization)
- [Object Type Serialization](#object-type-serialization)
- [Typeless](#typeless)
- [Security](#security)
- [Performance](#performance)
    - [Deserialization Performance for different options](#deserialization-performance-for-different-options)
    - [String interning](#string-interning)
- [LZ4 Compression](#lz4-compression)
    - [Attributions](#attributions)
- [Comparison with protobuf, JSON, ZeroFormatter](#comparison-with-protobuf-json-zeroformatter)
- [Hints to achieve maximum performance when using MessagePack for C#](#hints-to-achieve-maximum-performance-when-using-messagepack-for-c)
    - [Use indexed keys instead of string keys (Contractless)](#use-indexed-keys-instead-of-string-keys-contractless)
    - [Create own custom composite resolver](#create-own-custom-composite-resolver)
    - [Use native resolvers](#use-native-resolvers)
    - [Be careful when copying buffers](#be-careful-when-copying-buffers)
    - [Choosing compression](#choosing-compression)
- [Extensions](#extensions)
- [Experimental Features](#experimental-features)
- [High-Level API (`MessagePackSerializer`)](#high-level-api-messagepackserializer)
    - [Multiple MessagePack structures on a single `Stream`](#multiple-messagepack-structures-on-a-single-stream)
- [Low-Level API (`IMessagePackFormatter`)](#low-level-api-imessagepackformattert)
- [Primitive API (`MessagePackWriter`, `MessagePackReader`)](#primitive-api-messagepackwriter-messagepackreader)
    - [`MessagePackReader`](#messagepackreader)
    - [`MessagePackWriter`](#messagepackwriter)
- [Main Extension Point (`IFormatterResolver`)](#main-extension-point-iformatterresolver)
- [MessagePackFormatterAttribute](#messagepackformatterattribute)
- [IgnoreFormatter](#ignoreformatter)
- [Reserved Extension Types](#reserved-extension-types)
- [Unity support](#unity-support)
- [AOT Code Generation (support for Unity/Xamarin)](#aot)
- [RPC](#rpc)
    - [MagicOnion](#magiconion)
    - [StreamJsonRpc](#streamjsonrpc)
- [How to build](#how-to-build)
- [Author Info](#author-info)
## Installation
This library is distributed via NuGet. Special [Unity support](#unity) is available, too.
We target .NET Standard 2.0 with special optimizations for .NET 8+ and .NET Framework.
The library code is pure C# (with Just-In-Time IL code generation on some platforms or AOT safe source generators).
### NuGet packages
To install with NuGet, just install the `MessagePack` package:
```ps1
Install-Package MessagePack
```
Install the optional C# [analyzers](doc/analyzers/index.md) package to get warnings about coding mistakes and automatic fix suggestions to save you time:
```ps1
Install-Package MessagePackAnalyzer
```
There are also a range of official and third party Extension Packages available (learn more in our [extensions section](#extensions)):
```ps1
Install-Package MessagePack.ReactiveProperty
Install-Package MessagePack.UnityShims
Install-Package MessagePack.AspNetCoreMvcFormatter
