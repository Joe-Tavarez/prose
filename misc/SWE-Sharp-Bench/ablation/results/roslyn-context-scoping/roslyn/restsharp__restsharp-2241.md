## Repository map (from Roslyn, at the starting commit; declarations only)
Solution `RestSharp.sln`, .NET SDK 8.0.404, 13 C# projects (8 test). Projects are listed most relevant to the issue first.

### Projects
- **RestSharp** (`src/RestSharp/RestSharp.csproj`; net471, net48, net6.0, net7.0, net8.0, netstandard2.0) → no project refs; 74 public types; ns RestSharp, RestSharp.Extensions, System.Diagnostics.CodeAnalysis
- RestSharp.Tests.Integrated (`test/RestSharp.Tests.Integrated/RestSharp.Tests.Integrated.csproj`; net48, net6.0, net7.0, net8.0) — tests RestSharp, RestSharp.Serializers.Xml
- RestSharp.Tests.Serializers.Xml (`test/RestSharp.Tests.Serializers.Xml/RestSharp.Tests.Serializers.Xml.csproj`; net48, net6.0, net7.0, net8.0) — tests RestSharp, RestSharp.Serializers.Xml
- RestSharp.Tests (`test/RestSharp.Tests/RestSharp.Tests.csproj`; net48, net6.0, net7.0, net8.0) — tests RestSharp
- **RestSharp.Serializers.NewtonsoftJson** (`src/RestSharp.Serializers.NewtonsoftJson/RestSharp.Serializers.NewtonsoftJson.csproj`; net471, net48, net6.0, net7.0, net8.0, netstandard2.0) → RestSharp; 2 public types; ns RestSharp.Serializers.NewtonsoftJson
- **RestSharp.Serializers.Xml** (`src/RestSharp.Serializers.Xml/RestSharp.Serializers.Xml.csproj`; net471, net48, net6.0, net7.0, net8.0, netstandard2.0) → RestSharp; 8 public types; ns RestSharp.Serializers.Xml, RestSharp.Serializers
- **RestSharp.Serializers.CsvHelper** (`src/RestSharp.Serializers.CsvHelper/RestSharp.Serializers.CsvHelper.csproj`; net471, net48, net6.0, net7.0, net8.0, netstandard2.0) → RestSharp; 2 public types; ns RestSharp.Serializers.CsvHelper
- RestSharp.InteractiveTests (`test/RestSharp.InteractiveTests/RestSharp.InteractiveTests.csproj`; net6.0) — tests RestSharp
- RestSharp.Benchmarks (`benchmarks/RestSharp.Benchmarks/RestSharp.Benchmarks.csproj`; net7.0) — tests RestSharp, RestSharp.Serializers.NewtonsoftJson
- **SourceGenerator** (`gen/SourceGenerator/SourceGenerator.csproj`; netstandard2.0) → no project refs; 2 public types; ns SourceGenerator
- RestSharp.Tests.Shared (`test/RestSharp.Tests.Shared/RestSharp.Tests.Shared.csproj`; net48, net6.0, net7.0, net8.0) — tests RestSharp
- RestSharp.Tests.Serializers.Json (`test/RestSharp.Tests.Serializers.Json/RestSharp.Tests.Serializers.Json.csproj`; net48, net6.0, net7.0, net8.0) — tests RestSharp, RestSharp.Serializers.NewtonsoftJson
- RestSharp.Tests.Serializers.Csv (`test/RestSharp.Tests.Serializers.Csv/RestSharp.Tests.Serializers.Csv.csproj`; net48, net6.0, net7.0, net8.0) — tests RestSharp, RestSharp.Serializers.CsvHelper

### Key public types (members abbreviated)
- RestSharp: `class RestClient : IRestClient` (src/RestSharp/RestClient.Async.cs)
  Task<RestResponse> ExecuteAsync(RestRequest request, CancellationToken cancellationToken); Task<Stream> DownloadStreamAsync(RestRequest request, CancellationToken cancellationToken); string[] AcceptedContentTypes { get; set; }; ReadOnlyRestClientOptions Options { get; }; RestSerializers Serializers { get; private set; }; DefaultParameters DefaultParameters { get; }; RestClient(RestClientOptions options, ConfigureHeaders configureDefaultHeaders, ConfigureSerialization configureSerialization, bool useClientFactory); RestClient(ConfigureRestClient configureRestClient, ConfigureHeaders configureDefaultHeaders, ConfigureSerialization configureSerialization, bool useClientFactory); … +7
- RestSharp.Serializers.NewtonsoftJson: `static class RestClientExtensions` (src/RestSharp.Serializers.NewtonsoftJson/RestClientExtensions.cs)
  static SerializerConfig UseNewtonsoftJson(this SerializerConfig config); static SerializerConfig UseNewtonsoftJson(this SerializerConfig config, JsonSerializerSettings settings)
- RestSharp.Serializers.Xml: `class SerializeAsAttribute : Attribute` (src/RestSharp.Serializers.Xml/SerializeAsAttribute.cs)
  SerializeAsAttribute(); string Name { get; set; }; bool Attribute { get; set; }; bool Content { get; set; }; CultureInfo Culture { get; set; }; NameStyle NameStyle { get; set; }; int Index { get; set; }; string TransformName(string input)
- RestSharp.Serializers.CsvHelper: `static class RestClientExtensions` (src/RestSharp.Serializers.CsvHelper/RestClientExtensions.cs)
  static SerializerConfig UseCsvHelper(this SerializerConfig config); static SerializerConfig UseCsvHelper(this SerializerConfig config, CsvConfiguration configuration)
- SourceGenerator: `class ImmutableGenerator : ISourceGenerator` (gen/SourceGenerator/ImmutableGenerator.cs)
  void Initialize(GeneratorInitializationContext context); void Execute(GeneratorExecutionContext context)
- RestSharp: `class DefaultParameters : ParametersCollection` (src/RestSharp/Parameters/DefaultParameters.cs)
  DefaultParameters(ReadOnlyRestClientOptions options); DefaultParameters AddParameter(Parameter parameter); DefaultParameters RemoveParameter(string name, ParameterType type); DefaultParameters ReplaceParameter(Parameter parameter)
- RestSharp.Serializers.NewtonsoftJson: `class JsonNetSerializer : IRestSerializer, ISerializer, IDeserializer` (src/RestSharp.Serializers.NewtonsoftJson/JsonNetSerializer.cs)
  static readonly JsonSerializerSettings DefaultSettings; JsonNetSerializer(); JsonNetSerializer(JsonSerializerSettings settings); string Serialize(object obj); string Serialize(Parameter bodyParameter); T Deserialize<T>(RestResponse response); ISerializer Serializer { get; }; IDeserializer Deserializer { get; }; … +4
- RestSharp.Serializers.Xml: `class XmlDeserializer : IXmlDeserializer, IWithRootElement, IWithDateFormat` (src/RestSharp.Serializers.Xml/XmlDeserializer.cs)
  XmlDeserializer(); CultureInfo Culture { get; set; }; string RootElement { get; set; }; string Namespace { get; set; }; string DateFormat { get; set; }; virtual T Deserialize<T>(RestResponse response); protected virtual object Map(object x, XElement root); protected virtual object CreateAndMap(Type t, XElement element); … +3
- RestSharp.Serializers.CsvHelper: `class CsvHelperSerializer : IDeserializer, IRestSerializer, ISerializer` (src/RestSharp.Serializers.CsvHelper/CsvHelperSerializer.cs)
  CsvHelperSerializer(CsvConfiguration configuration); ISerializer Serializer { get; }; IDeserializer Deserializer { get; }; string[] AcceptedContentTypes { get; }; … +7
- SourceGenerator: `class InheritedCloneGenerator : ISourceGenerator` (gen/SourceGenerator/InheritedCloneGenerator.cs)
  void Initialize(GeneratorInitializationContext context); void Execute(GeneratorExecutionContext context)
- RestSharp: `class RestClientOptions` (src/RestSharp/Options/RestClientOptions.cs)
  RestClientOptions(); RestClientOptions(Uri baseUrl); RestClientOptions(string baseUrl); Uri BaseUrl { get; set; }; Func<HttpMessageHandler, HttpMessageHandler> ConfigureMessageHandler { get; set; }; CalculateResponseStatus CalculateResponseStatus { get; set; }; IAuthenticator Authenticator { get; set; }; List<Interceptor> Interceptors { get; set; }; … +24
- RestSharp.Serializers.Xml: `enum NameStyle` (src/RestSharp.Serializers.Xml/SerializeAsAttribute.cs)
  AsIs; CamelCase; LowerCase; PascalCase
- RestSharp: `enum ParameterType` (src/RestSharp/Enum.cs)
  GetOrPost; UrlSegment; HttpHeader; RequestBody; QueryString
- RestSharp.Serializers.Xml: `class DeserializeAsAttribute : Attribute` (src/RestSharp.Serializers.Xml/DeserializeAsAttribute.cs)
  string Name { get; set; }; bool Attribute { get; set; }; bool Content { get; set; }
- RestSharp: `class RequestParameters : ParametersCollection` (src/RestSharp/Parameters/RequestParameters.cs)
  RequestParameters(); RequestParameters(IEnumerable<Parameter> parameters); ParametersCollection AddParameters(IEnumerable<Parameter> parameters); ParametersCollection AddParameters(ParametersCollection parameters); void AddParameter(Parameter parameter); void RemoveParameter(string name); void RemoveParameter(Parameter parameter)
- RestSharp.Serializers.Xml: `class XmlSerializer : IXmlSerializer, IWithRootElement, IWithDateFormat` (src/RestSharp.Serializers.Xml/XmlSerializer.cs)
  XmlSerializer(); XmlSerializer(string @namespace); string Serialize(object obj); string RootElement { get; set; }; … +3
- RestSharp: `interface IRestClient : IDisposable` (src/RestSharp/IRestClient.cs)
  ReadOnlyRestClientOptions Options { get; }; RestSerializers Serializers { get; }; DefaultParameters DefaultParameters { get; }; Task<RestResponse> ExecuteAsync(RestRequest request, CancellationToken cancellationToken); Task<Stream> DownloadStreamAsync(RestRequest request, CancellationToken cancellationToken)
- RestSharp.Serializers.Xml: `class XmlAttributeDeserializer : XmlDeserializer` (src/RestSharp.Serializers.Xml/XmlAttributeDeserializer.cs)
  protected override object GetValueFromXml(XElement root, XName name, PropertyInfo prop, bool useExactName)
- RestSharp: `class RestRequest` (src/RestSharp/Request/RestRequest.cs)
  RestRequest(); RestRequest(string resource, Method method); RestRequest(Uri resource, Method method); bool AlwaysMultipartFormData { get; set; }; bool AlwaysSingleFileAsContent { get; set; }; bool MultipartFormQuoteParameters { get; set; }; bool MultipartFormQuoteBoundary { get; set; }; string FormBoundary { get; set; }; … +21
- RestSharp.Serializers.Xml: `static class XmlExtensions` (src/RestSharp.Serializers.Xml/XmlExtensions.cs)
  static XName AsNamespaced(this string name, string @namespace)
- RestSharp: `static class RestClientExtensions` (src/RestSharp/RestClient.Extensions.cs)
  static RestResponse<T> Deserialize<T>(this IRestClient client, RestResponse response); static ValueTask<RestResponse<T>> Deserialize<T>(this IRestClient client, RestResponse response, CancellationToken cancellationToken); static Task<RestResponse<T>> ExecuteAsync<T>(this IRestClient client, RestRequest request, CancellationToken cancellationToken); static RestResponse<T> Execute<T>(this IRestClient client, RestRequest request); static RestResponse Execute(this IRestClient client, RestRequest request); static Task<RestResponse> ExecuteAsync(this IRestClient client, RestRequest request, Method httpMethod, CancellationToken cancellationToken); static RestResponse Execute(this IRestClient client, RestRequest request, Method httpMethod); static Task<RestResponse<T>> ExecuteAsync<T>(this IRestClient client, RestRequest request, Method httpMethod, CancellationToken cancellationToken); … +95
- RestSharp.Serializers.Xml: `static class XmlSerializerClientExtensions` (src/RestSharp.Serializers.Xml/XmlSerializerClientExtensions.cs)
  static SerializerConfig UseXmlSerializer(this SerializerConfig config, string xmlNamespace, string rootElement, bool useAttributeDeserializer)
- RestSharp: `static class RestClientExtensions` (src/RestSharp/Serializers/Json/RestClientExtensions.cs)
  static SerializerConfig UseSystemTextJson(this SerializerConfig serializerConfig); static SerializerConfig UseSystemTextJson(this SerializerConfig serializerConfig, JsonSerializerOptions options)
- RestSharp: `class ReadOnlyRestClientOptions` (src/RestSharp/Options/ReadOnlyRestClientOptions.cs)
  IReadOnlyCollection<Interceptor> Interceptors { get; private set; }
- RestSharp: `delegate ConfigureRestClient` (src/RestSharp/RestClient.cs)
- RestSharp: `abstract class ParametersCollection : IReadOnlyCollection<Parameter>` (src/RestSharp/Parameters/ParametersCollection.cs)
  protected readonly List<Parameter> Parameters; bool Exists(Parameter parameter); Parameter TryFind(string parameterName); IEnumerable<Parameter> GetParameters(ParameterType parameterType); IEnumerable<T> GetParameters<T>(); IEnumerator<Parameter> GetEnumerator(); int Count { get; }
- RestSharp: `static class KnownHeaders` (src/RestSharp/KnownHeaders.cs)
  const string Authorization; const string Accept; const string AcceptLanguage; const string Allow; const string Expires; const string ContentDisposition; const string ContentEncoding; const string ContentLanguage; … +11
- RestSharp: `record FileParameter : IEquatable<FileParameter>` (src/RestSharp/Parameters/FileParameter.cs)
  string Name { get; }; string FileName { get; }; ContentType ContentType { get; }; Func<Stream> GetFile { get; }; FileParameterOptions Options { get; }; static FileParameter Create(string name, byte[] data, string filename, ContentType contentType, FileParameterOptions options); static FileParameter Create(string name, Func<Stream> getFile, string fileName, ContentType contentType, FileParameterOptions options); static FileParameter FromFile(string fullPath, string name, ContentType contentType, FileParameterOptions options)
