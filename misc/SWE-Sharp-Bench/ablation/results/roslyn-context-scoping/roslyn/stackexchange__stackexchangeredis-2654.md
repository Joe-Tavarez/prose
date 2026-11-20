## Repository map (from Roslyn, at the starting commit; declarations only)
Solution `StackExchange.Redis.sln`, .NET SDK 8.0.404, 10 C# projects (1 test). Projects are listed most relevant to the issue first.

### Projects
- **StackExchange.Redis** (`src/StackExchange.Redis/StackExchange.Redis.csproj`; net461, net472, net6.0, netcoreapp3.1, netstandard2.0) → no project refs; 126 public types; ns StackExchange.Redis, System.Diagnostics.CodeAnalysis, StackExchange.Redis.KeyspaceIsolation
- **StackExchange.Redis.Server** (`toys/StackExchange.Redis.Server/StackExchange.Redis.Server.csproj`; netstandard2.0) → StackExchange.Redis; 8 public types; ns StackExchange.Redis.Server, StackExchange.Redis
- StackExchange.Redis.Tests (`tests/StackExchange.Redis.Tests/StackExchange.Redis.Tests.csproj`; net472, net6.0) — tests StackExchange.Redis
- **KestrelRedisServer** (`toys/KestrelRedisServer/KestrelRedisServer.csproj`; net6.0) → StackExchange.Redis, StackExchange.Redis.Server; 3 public types; ns KestrelRedisServer
- **BasicTest** (`tests/BasicTest/BasicTest.csproj`; net472, net6.0) → StackExchange.Redis; 2 public types; ns BasicTest
- **BasicTestBaseline** (`tests/BasicTestBaseline/BasicTestBaseline.csproj`; net472, net6.0) → no project refs; 2 public types; ns BasicTest
- **ConsoleTest** (`tests/ConsoleTest/ConsoleTest.csproj`; net6.0) → StackExchange.Redis; 0 public types; ns (global)
- **ConsoleTestBaseline** (`tests/ConsoleTestBaseline/ConsoleTestBaseline.csproj`; net6.0) → no project refs; 0 public types; ns (global)
- **TestConsole** (`toys/TestConsole/TestConsole.csproj`; net472, net6.0) → StackExchange.Redis; 0 public types; ns TestConsole
- **TestConsoleBaseline** (`toys/TestConsoleBaseline/TestConsoleBaseline.csproj`; net461, net462, net47, net472, net6.0) → no project refs; 0 public types; ns TestConsole

### Key public types (members abbreviated)
- StackExchange.Redis: `struct NameValueEntry : IEquatable<NameValueEntry>` (src/StackExchange.Redis/APITypes/NameValueEntry.cs)
  NameValueEntry(RedisValue name, RedisValue value); RedisValue Name { get; }; RedisValue Value { get; }; static implicit operator KeyValuePair<RedisValue, RedisValue>(NameValueEntry value); static implicit operator NameValueEntry(KeyValuePair<RedisValue, RedisValue> value); override string ToString(); override int GetHashCode(); override bool Equals(object obj); … +3
- StackExchange.Redis.Server: `abstract class RespServer : IDisposable` (toys/StackExchange.Redis.Server/RespServer.cs)
  protected RespServer(TextWriter output); string GetStats(); protected virtual void AppendStats(StringBuilder sb); virtual RedisClient CreateClient(); int ClientCount { get; }; int TotalClientCount { get; private set; }; RedisClient AddClient(); bool RemoveClient(RedisClient client); … +15
- KestrelRedisServer: `class Startup : IDisposable` (toys/KestrelRedisServer/Startup.cs)
  void ConfigureServices(IServiceCollection services); void Dispose(); void Configure(IApplicationBuilder app, IWebHostEnvironment env, IHostApplicationLifetime lifetime)
- BasicTest: `class RedisBenchmarks : IDisposable` (tests/BasicTest/Program.cs)
  void Setup(); int ExecuteIncrBy(); Task<int> ExecuteIncrByAsync(); int ExecuteGeoRadius(); … +5
- BasicTestBaseline: `class RedisBenchmarks : IDisposable` (tests/BasicTest/Program.cs)
  void Setup(); int ExecuteIncrBy(); Task<int> ExecuteIncrByAsync(); int ExecuteGeoRadius(); … +5
- StackExchange.Redis: `class ClientInfo` (src/StackExchange.Redis/ClientInfo.cs)
  EndPoint Address { get; private set; }; int AgeSeconds { get; private set; }; int Database { get; private set; }; ClientFlags Flags { get; private set; }; string FlagsRaw { get; private set; }; string Host { get; }; int IdleSeconds { get; private set; }; string LastCommand { get; private set; }; … +13
- StackExchange.Redis.Server: `class RedisClient : IDisposable` (toys/StackExchange.Redis.Server/RedisClient.cs)
  int SubscriptionCount { get; }; int Database { get; set; }; string Name { get; set; }; bool Closed { get; internal set; }; int Id { get; internal set; }; void Dispose()
- KestrelRedisServer: `static class Program` (toys/KestrelRedisServer/Program.cs)
  static void Main(string[] args); static IWebHostBuilder CreateWebHostBuilder(string[] args)
- BasicTest: `class Issue898 : IDisposable` (tests/BasicTest/Program.cs)
  void Dispose(); Issue898(); void Load(); Task LoadAsync(); … +2
- BasicTestBaseline: `class Issue898 : IDisposable` (tests/BasicTest/Program.cs)
  void Dispose(); Issue898(); void Load(); Task LoadAsync(); … +2
- StackExchange.Redis: `interface IServer : IRedis` (src/StackExchange.Redis/Interfaces/IServer.cs)
  ClusterConfiguration ClusterConfiguration { get; }; EndPoint EndPoint { get; }; RedisFeatures Features { get; }; bool IsConnected { get; }; RedisProtocol Protocol { get; }; bool IsSlave { get; }; bool IsReplica { get; }; bool AllowSlaveWrites { get; set; }; … +119
- StackExchange.Redis.Server: `abstract class RedisServer : RespServer` (toys/StackExchange.Redis.Server/RedisServer.cs)
  static bool IsMatch(string pattern, string key); protected RedisServer(int databases, TextWriter output); protected override void AppendStats(StringBuilder sb); int Databases { get; }; protected virtual TypedRedisValue Sadd(RedisClient client, RedisRequest request); protected virtual bool Sadd(int database, RedisKey key, RedisValue value); protected virtual TypedRedisValue Srem(RedisClient client, RedisRequest request); protected virtual bool Srem(int database, RedisKey key, RedisValue value); … +63
- KestrelRedisServer: `class RedisConnectionHandler : ConnectionHandler` (toys/KestrelRedisServer/RedisConnectionHandler.cs)
  RedisConnectionHandler(RespServer server); override Task OnConnectedAsync(ConnectionContext connection)
- StackExchange.Redis: `class DefaultOptionsProvider` (src/StackExchange.Redis/Configuration/DefaultOptionsProvider.cs)
  static void AddProvider(DefaultOptionsProvider provider); virtual bool IsMatch(EndPoint endpoint); static DefaultOptionsProvider GetProvider(EndPointCollection endpoints); static DefaultOptionsProvider GetProvider(EndPoint endpoint); virtual bool AbortOnConnectFail { get; }; virtual bool AllowAdmin { get; }; virtual BacklogPolicy BacklogPolicy { get; }; virtual bool CheckCertificateRevocation { get; }; … +27
- StackExchange.Redis.Server: `class RespSocketServer : SocketServer` (toys/StackExchange.Redis.Server/RespSocketServer.cs)
  RespSocketServer(RespServer server); protected override void OnStarted(EndPoint endPoint); protected override Task OnClientConnectedAsync(in ClientConnection client); protected override void Dispose(bool disposing)
- StackExchange.Redis: `class ConfigurationOptions : ICloneable` (src/StackExchange.Redis/ConfigurationOptions.cs)
  LocalCertificateSelectionCallback CertificateSelection; RemoteCertificateValidationCallback CertificateValidation; DefaultOptionsProvider Defaults { get; set; }; Action<EndPoint, ConnectionType, Socket> BeforeSocketConnect { get; set; }; bool AbortOnConnectFail { get; set; }; bool AllowAdmin { get; set; }; int AsyncTimeout { get; set; }; bool UseSsl { get; set; }; … +46
- StackExchange.Redis.Server: `enum RespServer.ShutdownReason` (toys/StackExchange.Redis.Server/RespServer.cs)
  ServerDisposed; ClientInitiated
- StackExchange.Redis: `struct HashEntry : IEquatable<HashEntry>` (src/StackExchange.Redis/APITypes/HashEntry.cs)
  HashEntry(RedisValue name, RedisValue value); RedisValue Name { get; }; RedisValue Value { get; }; RedisValue Key { get; }; static implicit operator KeyValuePair<RedisValue, RedisValue>(HashEntry value); static implicit operator HashEntry(KeyValuePair<RedisValue, RedisValue> value); override string ToString(); override int GetHashCode(); … +4
- StackExchange.Redis.Server: `class MemoryCacheRedisServer : RedisServer` (toys/StackExchange.Redis.Server/MemoryCacheRedisServer.cs)
  MemoryCacheRedisServer(TextWriter output); protected override void Dispose(bool disposing); protected override long Dbsize(int database); protected override RedisValue Get(int database, RedisKey key); … +14
- StackExchange.Redis: `class SocketManager : IDisposable` (src/StackExchange.Redis/SocketManager.cs)
  string Name { get; }; SocketManager(string name); SocketManager(string name, bool useHighPrioritySocketThreads); SocketManager(string name, int workerCount, bool useHighPrioritySocketThreads); SocketManager(string name, int workerCount, SocketManagerOptions options); static SocketManager Shared { get; }; static SocketManager ThreadPool { get; }; override string ToString(); … +1
- StackExchange.Redis.Server: `struct TypedRedisValue` (toys/StackExchange.Redis.Server/TypedRedisValue.cs)
  static TypedRedisValue Nil { get; }; bool IsNil { get; }; bool IsNullArray { get; }; ResultType Type { get; }; … +12
- StackExchange.Redis: `enum ExportOptions` (src/StackExchange.Redis/Enums/ExportOptions.cs)
  None; Info; Config; Client; Cluster; All
- StackExchange.Redis.Server: `struct RedisRequest` (toys/StackExchange.Redis.Server/RedisRequest.cs)
  int Count { get; }; override string ToString(); override bool Equals(object obj); TypedRedisValue WrongArgCount(); … +10
- StackExchange.Redis: `struct StreamGroupInfo` (src/StackExchange.Redis/APITypes/StreamGroupInfo.cs)
  string Name { get; }; int ConsumerCount { get; }; int PendingMessageCount { get; }; string LastDeliveredId { get; }; long? EntriesRead { get; }; long? Lag { get; }
- StackExchange.Redis: `struct StreamConsumerInfo` (src/StackExchange.Redis/APITypes/StreamConsumerInfo.cs)
  string Name { get; }; int PendingMessageCount { get; }; long IdleTimeInMilliseconds { get; }
- StackExchange.Redis: `struct StreamConsumer` (src/StackExchange.Redis/APITypes/StreamConsumer.cs)
  RedisValue Name { get; }; int PendingMessageCount { get; }
- StackExchange.Redis: `struct RedisFeatures : IEquatable<RedisFeatures>` (src/StackExchange.Redis/RedisFeatures.cs)
  RedisFeatures(Version version); bool BitwiseOperations { get; }; bool ClientName { get; }; bool ClientId { get; }; bool ExecAbort { get; }; bool ExpireOverwrite { get; }; bool GetDelete { get; }; bool HashStringLength { get; }; … +41
- StackExchange.Redis: `enum ClientFlags` (src/StackExchange.Redis/Enums/ClientFlags.cs)
  None; SlaveMonitor; ReplicaMonitor; Slave; Replica; Master; Transaction; Blocked; … +10
- StackExchange.Redis: `enum ClientType` (src/StackExchange.Redis/Enums/ClientType.cs)
  Normal; Replica; Slave; PubSub
- StackExchange.Redis: `class ConnectionMultiplexer : IInternalConnectionMultiplexer` (src/StackExchange.Redis/ConnectionMultiplexer.Compat.cs)
  static TaskFactory Factory { get; set; }; bool PreserveAsyncOrder { get; set; }; bool IncludeDetailInExceptions { get; set; }; bool IncludePerformanceCountersInExceptions { get; set; }; int TimeoutMilliseconds { get; }; string ClientName { get; }; string Configuration { get; }; bool IsConnected { get; }; … +54
- StackExchange.Redis: `interface IConnectionMultiplexer : IDisposable, IAsyncDisposable` (src/StackExchange.Redis/Interfaces/IConnectionMultiplexer.cs)
  string ClientName { get; }; string Configuration { get; }; int TimeoutMilliseconds { get; }; long OperationCount { get; }; bool PreserveAsyncOrder { get; set; }; bool IsConnected { get; }; bool IsConnecting { get; }; bool IncludeDetailInExceptions { get; set; }; … +36
- StackExchange.Redis: `struct StreamEntry` (src/StackExchange.Redis/APITypes/StreamEntry.cs)
  StreamEntry(RedisValue id, NameValueEntry[] values); static StreamEntry Null { get; }; RedisValue Id { get; }; NameValueEntry[] Values { get; }; RedisValue this[RedisValue fieldName] { get; }; bool IsNull { get; }
- StackExchange.Redis: `struct LatencyLatestEntry` (src/StackExchange.Redis/APITypes/LatencyLatestEntry.cs)
  string EventName { get; }; DateTime Timestamp { get; }; int DurationMilliseconds { get; }; int MaxDurationMilliseconds { get; }
- StackExchange.Redis: `struct StreamPendingMessageInfo` (src/StackExchange.Redis/APITypes/StreamPendingMessageInfo.cs)
  RedisValue MessageId { get; }; RedisValue ConsumerName { get; }; long IdleTimeInMilliseconds { get; }; int DeliveryCount { get; }
- StackExchange.Redis: `enum ReplicationChangeOptions` (src/StackExchange.Redis/Enums/ReplicationChangeOptions.cs)
  None; SetTiebreaker; Broadcast; EnslaveSubordinates; ReplicateToOtherEndpoints; All
