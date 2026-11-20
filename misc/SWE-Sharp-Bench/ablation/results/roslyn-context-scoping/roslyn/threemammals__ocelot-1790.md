## Repository map (from Roslyn, at the starting commit; declarations only)
Solution `Ocelot.sln`, .NET SDK 9.0.100, 26 C# projects (3 test). Projects are listed most relevant to the issue first.

### Projects
- **Ocelot** (`src/Ocelot/Ocelot.csproj`; net7.0) → no project refs; 359 public types; ns Ocelot.Configuration.Creator, Ocelot.LoadBalancer.LoadBalancers, Ocelot.Requester
- Ocelot.UnitTests (`test/Ocelot.UnitTests/Ocelot.UnitTests.csproj`; net7.0) — tests Ocelot, Ocelot.Administration, Ocelot.Cache.CacheManager, Ocelot.Provider.Consul, Ocelot.Provider.Eureka, Ocelot.Provider.Kubernetes, Ocelot.Provider.Polly, Ocelot.Tracing.Butterfly
- Ocelot.AcceptanceTests (`test/Ocelot.AcceptanceTests/Ocelot.AcceptanceTests.csproj`; net7.0) — tests Ocelot, Ocelot.Cache.CacheManager, Ocelot.ManualTest, Ocelot.Provider.Consul, Ocelot.Provider.Eureka, Ocelot.Provider.Polly, Ocelot.Tracing.Butterfly, Ocelot.Tracing.OpenTracing
- **Ocelot.Cache.CacheManager** (`src/Ocelot.Cache.CacheManager/Ocelot.Cache.CacheManager.csproj`; net7.0) → Ocelot; 2 public types; ns Ocelot.Cache.CacheManager
- **Ocelot.Provider.Consul** (`src/Ocelot.Provider.Consul/Ocelot.Provider.Consul.csproj`; net7.0) → Ocelot; 10 public types; ns Ocelot.Provider.Consul
- **Ocelot.Provider.Kubernetes** (`src/Ocelot.Provider.Kubernetes/Ocelot.Provider.Kubernetes.csproj`; net7.0) → Ocelot; 6 public types; ns Ocelot.Provider.Kubernetes
- **Ocelot.Provider.Polly** (`src/Ocelot.Provider.Polly/Ocelot.Provider.Polly.csproj`; net7.0) → Ocelot; 6 public types; ns Ocelot.Provider.Polly, Ocelot.Provider.Polly.Interfaces
- **Ocelot.Administration** (`src/Ocelot.Administration/Ocelot.Administration.csproj`; net7.0) → Ocelot; 5 public types; ns Ocelot.Administration
- **Ocelot.Provider.Eureka** (`src/Ocelot.Provider.Eureka/Ocelot.Provider.Eureka.csproj`; net7.0) → Ocelot; 4 public types; ns Ocelot.Provider.Eureka
- **Ocelot.Tracing.Butterfly** (`src/Ocelot.Tracing.Butterfly/Ocelot.Tracing.Butterfly.csproj`; net7.0) → Ocelot; 2 public types; ns Ocelot.Tracing.Butterfly
- **Ocelot.Tracing.OpenTracing** (`src/Ocelot.Tracing.OpenTracing/Ocelot.Tracing.OpenTracing.csproj`; net7.0) → Ocelot; 1 public types; ns Ocelot.Tracing.OpenTracing
- Ocelot.IntegrationTests (`test/Ocelot.IntegrationTests/Ocelot.IntegrationTests.csproj`; net7.0) — tests Ocelot, Ocelot.Administration, Ocelot.Cache.CacheManager, Ocelot.Provider.Consul, Ocelot.Provider.Eureka, Ocelot.Provider.Polly
- **Ocelot.Samples.ServiceDiscovery.DownstreamService** (`samples/OcelotServiceDiscovery/DownstreamService/Ocelot.Samples.ServiceDiscovery.DownstreamService.csproj`; net7.0) → no project refs; 9 public types; ns Ocelot.Samples.ServiceDiscovery.DownstreamService.Models, Ocelot.Samples.ServiceDiscovery.DownstreamService.Controllers, Ocelot.Samples.ServiceDiscovery.DownstreamService
- **Ocelot.Benchmarks** (`test/Ocelot.Benchmarks/Ocelot.Benchmarks.csproj`; net7.0) → Ocelot; 6 public types; ns Ocelot.Benchmarks
- **Ocelot.Samples.OcelotKube.DownstreamService** (`samples/OcelotKube/DownstreamService/Ocelot.Samples.OcelotKube.DownstreamService.csproj`; net7.0) → no project refs; 4 public types; ns Ocelot.Samples.OcelotKube.DownstreamService.Controllers, Ocelot.Samples.OcelotKube.DownstreamService, Ocelot.Samples.OcelotKube.DownstreamService.Models
- **OcelotGraphQL** (`samples/OcelotGraphQL/OcelotGraphQL.csproj`; net7.0) → no project refs; 4 public types; ns OcelotGraphQL
- **DownstreamService** (`samples/OcelotEureka/DownstreamService/DownstreamService.csproj`; net7.0) → no project refs; 3 public types; ns DownstreamService, DownstreamService.Controllers
- **Ocelot.Samples.ServiceDiscovery.ApiGateway** (`samples/OcelotServiceDiscovery/ApiGateway/Ocelot.Samples.ServiceDiscovery.ApiGateway.csproj`; net7.0) → Ocelot; 3 public types; ns Ocelot.Samples.ServiceDiscovery.ApiGateway.ServiceDiscovery, Ocelot.Samples.ServiceDiscovery.ApiGateway
- … 8 more: OcelotApplicationApiGateway, Ocelot.ManualTest, Ocelot.Samples.OcelotBasic.ApiGateway, Ocelot.Samples.OcelotKube.ApiGateway, OcelotApplicationService, AdministrationApi, ApiGateway, OcelotOpenTracing

### Key public types (members abbreviated)
- Ocelot: `static class HttpItemsExtensions` (src/Ocelot/Middleware/HttpItemsExtensions.cs)
  static void UpsertDownstreamRequest(this IDictionary<object, object> input, DownstreamRequest downstreamRequest); static void UpsertDownstreamResponse(this IDictionary<object, object> input, DownstreamResponse downstreamResponse); static void UpsertDownstreamRoute(this IDictionary<object, object> input, DownstreamRoute downstreamRoute); static void UpsertTemplatePlaceholderNameAndValues(this IDictionary<object, object> input, List<PlaceholderNameAndValue> tPNV); static void UpsertDownstreamRoute(this IDictionary<object, object> input, DownstreamRouteHolder downstreamRoute); static void UpsertErrors(this IDictionary<object, object> input, List<Error> errors); static void SetError(this IDictionary<object, object> input, Error error); static void SetIInternalConfiguration(this IDictionary<object, object> input, IInternalConfiguration config); … +7
- Ocelot.Cache.CacheManager: `class OcelotCacheManagerCache<T> : IOcelotCache<T>` (src/Ocelot.Cache.CacheManager/OcelotCacheManagerCache.cs)
  OcelotCacheManagerCache(ICacheManager<T> cacheManager); void Add(string key, T value, TimeSpan ttl, string region); void AddAndDelete(string key, T value, TimeSpan ttl, string region); T Get(string key, string region); void ClearRegion(string region)
- Ocelot.Provider.Consul: `static class OcelotBuilderExtensions` (src/Ocelot.Provider.Consul/OcelotBuilderExtensions.cs)
  static IOcelotBuilder AddConsul(this IOcelotBuilder builder); static IOcelotBuilder AddConfigStoredInConsul(this IOcelotBuilder builder)
- Ocelot.Provider.Kubernetes: `static class OcelotBuilderExtensions` (src/Ocelot.Provider.Kubernetes/OcelotBuilderExtensions.cs)
  static IOcelotBuilder AddKubernetes(this IOcelotBuilder builder, bool usePodServiceAccount)
- Ocelot.Provider.Polly: `static class OcelotBuilderExtensions` (src/Ocelot.Provider.Polly/OcelotBuilderExtensions.cs)
  static IOcelotBuilder AddPolly(this IOcelotBuilder builder)
- Ocelot.Administration: `static class OcelotBuilderExtensions` (src/Ocelot.Administration/OcelotBuilderExtensions.cs)
  static IOcelotAdministrationBuilder AddAdministration(this IOcelotBuilder builder, string path, string secret); static IOcelotAdministrationBuilder AddAdministration(this IOcelotBuilder builder, string path, Action<JwtBearerOptions> configureOptions)
- Ocelot.Provider.Eureka: `static class OcelotBuilderExtensions` (src/Ocelot.Provider.Eureka/OcelotBuilderExtensions.cs)
  static IOcelotBuilder AddEureka(this IOcelotBuilder builder)
- Ocelot.Tracing.Butterfly: `static class OcelotBuilderExtensions` (src/Ocelot.Tracing.Butterfly/OcelotBuilderExtensions.cs)
  static IOcelotBuilder AddButterfly(this IOcelotBuilder builder, Action<ButterflyOptions> settings)
- Ocelot.Tracing.OpenTracing: `static class OcelotBuilderExtensions` (src/Ocelot.Tracing.OpenTracing/OcelotBuilderExtensions.cs)
  static IOcelotBuilder AddOpenTracing(this IOcelotBuilder builder)
- Ocelot.Samples.ServiceDiscovery.DownstreamService: `class MicroserviceResult` (samples/OcelotServiceDiscovery/DownstreamService/Models/MicroserviceResult.cs)
  Uri Next { get; set; }
- Ocelot.Benchmarks: `class AllTheThingsBenchmarks : ManualConfig` (test/Ocelot.Benchmarks/AllTheThingsBenchmarks.cs)
  AllTheThingsBenchmarks(); void SetUp(); Task Baseline(); static void GivenThereIsAConfiguration(FileConfiguration fileConfiguration)
- Ocelot.Samples.OcelotKube.DownstreamService: `class ValuesController : ControllerBase` (samples/OcelotKube/DownstreamService/Controllers/ValuesController.cs)
  ActionResult<IEnumerable<string>> Get(); ActionResult<string> Get(int id); void Post(string value); void Put(int id, string value); … +1
- OcelotGraphQL: `class GraphQlDelegatingHandler : DelegatingHandler` (samples/OcelotGraphQL/Program.cs)
  GraphQlDelegatingHandler(IDocumentExecuter executer, IDocumentWriter writer); protected override Task<HttpResponseMessage> SendAsync(HttpRequestMessage request, CancellationToken cancellationToken)
- DownstreamService: `class Startup` (samples/OcelotEureka/DownstreamService/Startup.cs)
  Startup(IConfiguration configuration); IConfiguration Configuration { get; }; void ConfigureServices(IServiceCollection services); void Configure(IApplicationBuilder app, IWebHostEnvironment env)
- Ocelot.Samples.ServiceDiscovery.ApiGateway: `class MyServiceDiscoveryProvider : IServiceDiscoveryProvider` (samples/OcelotServiceDiscovery/ApiGateway/ServiceDiscovery/MyServiceDiscoveryProvider.cs)
  MyServiceDiscoveryProvider(IServiceProvider serviceProvider, ServiceProviderConfiguration config, DownstreamRoute downstreamRoute); Task<List<Service>> GetAsync()
- OcelotApplicationApiGateway: `class ServiceEventSource : EventSource` (samples/OcelotServiceFabric/src/OcelotApplicationApiGateway/ServiceEventSource.cs)
  static ServiceEventSource Current; void Message(string message, params object[] args); void Message(string message); void ServiceTypeRegistered(int hostProcessId, string serviceType); … +2
- Ocelot.ManualTest: `class FakeHandler : DelegatingHandler` (test/Ocelot.ManualTest/Program.cs)
  protected override Task<HttpResponseMessage> SendAsync(HttpRequestMessage request, CancellationToken cancellationToken)
- Ocelot.Samples.OcelotBasic.ApiGateway: `class Startup` (samples/OcelotBasic/Startup.cs)
  void ConfigureServices(IServiceCollection services); void Configure(IApplicationBuilder app, IWebHostEnvironment env)
- Ocelot.Samples.OcelotKube.ApiGateway: `class Program` (samples/OcelotKube/ApiGateway/Program.cs)
  static void Main(string[] args); static IWebHost BuildWebHost(string[] args)
- OcelotApplicationService: `class ValuesController : Controller` (samples/OcelotServiceFabric/src/OcelotApplicationService/Controllers/ValuesController.cs)
  IEnumerable<string> Get(); string Get(int id); void Post(string value); void Put(int id, string value); … +1
- AdministrationApi: `class Program` (samples/AdministrationApi/Program.cs)
  static void Main(string[] args)
- ApiGateway: `class Program` (samples/OcelotEureka/ApiGateway/Program.cs)
  static void Main(string[] args); static IWebHost BuildWebHost(string[] args)
- Ocelot: `static class OcelotMiddlewareExtensions` (src/Ocelot/Middleware/OcelotMiddlewareExtensions.cs)
  static Task<IApplicationBuilder> UseOcelot(this IApplicationBuilder builder); static Task<IApplicationBuilder> UseOcelot(this IApplicationBuilder builder, Action<OcelotPipelineConfiguration> pipelineConfiguration); static Task<IApplicationBuilder> UseOcelot(this IApplicationBuilder builder, OcelotPipelineConfiguration pipelineConfiguration); static Task<IApplicationBuilder> UseOcelot(this IApplicationBuilder app, Action<IApplicationBuilder, OcelotPipelineConfiguration> builderAction); static Task<IApplicationBuilder> UseOcelot(this IApplicationBuilder app, Action<IApplicationBuilder, OcelotPipelineConfiguration> builderAction, OcelotPipelineConfiguration configuration)
- Ocelot.Cache.CacheManager: `static class OcelotBuilderExtensions` (src/Ocelot.Cache.CacheManager/OcelotBuilderExtensions.cs)
  static IOcelotBuilder AddCacheManager(this IOcelotBuilder builder, Action<ConfigurationBuilderCachePart> settings)
- Ocelot.Provider.Consul: `class ConsulRegistryConfiguration` (src/Ocelot.Provider.Consul/ConsulRegistryConfiguration.cs)
  const int DefaultHttpPort; ConsulRegistryConfiguration(string scheme, string host, int port, string keyOfServiceInConsul, string token); string KeyOfServiceInConsul { get; }; string Scheme { get; }; … +3
