## Repository map (from Roslyn, at the starting commit; declarations only)
Solution `RestSharp.sln`, .NET SDK 7.0.100, 10 C# projects (7 test). Projects are listed most relevant to the issue first.

### Projects
- **RestSharp** (`src/RestSharp/RestSharp.csproj`; net5.0, net6.0, netstandard2.0) → no project refs; 52 public types; ns RestSharp, RestSharp.Authenticators.OAuth, RestSharp.Serializers
- RestSharp.Tests (`test/RestSharp.Tests/RestSharp.Tests.csproj`; net6.0) — tests RestSharp
- RestSharp.Serializers.Xml.Tests (`test/RestSharp.Serializers.Xml.Tests/RestSharp.Serializers.Xml.Tests.csproj`; net6.0) — tests RestSharp, RestSharp.Serializers.Xml
- RestSharp.IntegrationTests (`test/RestSharp.IntegrationTests/RestSharp.IntegrationTests.csproj`; net6.0) — tests RestSharp, RestSharp.Serializers.Xml
- **RestSharp.Serializers.Xml** (`src/RestSharp.Serializers.Xml/RestSharp.Serializers.Xml.csproj`; net5.0, net6.0, netstandard2.0) → RestSharp; 8 public types; ns RestSharp.Serializers.Xml, RestSharp.Serializers
- **RestSharp.Serializers.NewtonsoftJson** (`src/RestSharp.Serializers.NewtonsoftJson/RestSharp.Serializers.NewtonsoftJson.csproj`; net5.0, net6.0, netstandard2.0) → RestSharp; 2 public types; ns RestSharp.Serializers.NewtonsoftJson
- RestSharp.Tests.Shared (`test/RestSharp.Tests.Shared/RestSharp.Tests.Shared.csproj`; net6.0) — tests —
- RestSharp.InteractiveTests (`test/RestSharp.InteractiveTests/RestSharp.InteractiveTests.csproj`; net6.0) — tests RestSharp
- RestSharp.Serializers.Json.Tests (`test/RestSharp.Serializers.Json.Tests/RestSharp.Serializers.Json.Tests.csproj`; net6.0) — tests RestSharp, RestSharp.Serializers.NewtonsoftJson
- RestSharp.Benchmarks (`benchmarks/RestSharp.Benchmarks/RestSharp.Benchmarks.csproj`; net6.0) — tests RestSharp, RestSharp.Serializers.NewtonsoftJson

### Key public types (members abbreviated)
- RestSharp: `class RestClient` (src/RestSharp/RestClient.Async.cs)
  Task<RestResponse> ExecuteAsync(RestRequest request, CancellationToken cancellationToken); Task<Stream> DownloadStreamAsync(RestRequest request, CancellationToken cancellationToken); Task<byte[]> DownloadDataAsync(RestRequest request, CancellationToken cancellationToken); RestClient(); RestClient(HttpClient httpClient, RestClientOptions options); RestClient(HttpMessageHandler handler); RestClient(RestClientOptions options); RestClient(Uri baseUrl); … +11
- RestSharp.Serializers.Xml: `class SerializeAsAttribute : Attribute` (src/RestSharp.Serializers.Xml/SerializeAsAttribute.cs)
  SerializeAsAttribute(); string Name { get; set; }; bool Attribute { get; set; }; bool Content { get; set; }; CultureInfo Culture { get; set; }; NameStyle NameStyle { get; set; }; int Index { get; set; }; string TransformName(string input)
- RestSharp.Serializers.NewtonsoftJson: `static class RestClientExtensions` (src/RestSharp.Serializers.NewtonsoftJson/RestClientExtensions.cs)
  static RestClient UseNewtonsoftJson(this RestClient client); static RestClient UseNewtonsoftJson(this RestClient client, JsonSerializerSettings settings)
- RestSharp: `class RestRequest` (src/RestSharp/Request/RestRequest.cs)
  RestRequest(); RestRequest(string resource, Method method, DataFormat dataFormat); RestRequest(Uri resource, Method method, DataFormat dataFormat); bool AlwaysMultipartFormData { get; set; }; ParametersCollection Parameters { get; }; IReadOnlyCollection<FileParameter> Files { get; }; Method Method { get; set; }; int Timeout { get; set; }; … +11
- RestSharp.Serializers.Xml: `class XmlDeserializer : IXmlDeserializer, IWithRootElement, IWithDateFormat` (src/RestSharp.Serializers.Xml/XmlDeserializer.cs)
  XmlDeserializer(); CultureInfo Culture { get; set; }; string RootElement { get; set; }; string Namespace { get; set; }; string DateFormat { get; set; }; virtual T Deserialize<T>(RestResponse response); protected virtual object Map(object x, XElement root); protected virtual object CreateAndMap(Type t, XElement element); … +3
- RestSharp.Serializers.NewtonsoftJson: `class JsonNetSerializer : IRestSerializer, ISerializer, IDeserializer` (src/RestSharp.Serializers.NewtonsoftJson/JsonNetSerializer.cs)
  static readonly JsonSerializerSettings DefaultSettings; JsonNetSerializer(); JsonNetSerializer(JsonSerializerSettings settings); string Serialize(object obj); … +7
- RestSharp: `static class RestClientExtensions` (src/RestSharp/RestClientExtensions.cs)
  static Task<RestResponse<T>> ExecuteGetAsync<T>(this RestClient client, RestRequest request, CancellationToken cancellationToken); static Task<RestResponse<T>> ExecutePostAsync<T>(this RestClient client, RestRequest request, CancellationToken cancellationToken); static Task<RestResponse> ExecuteGetAsync(this RestClient client, RestRequest request, CancellationToken cancellationToken); static Task<RestResponse> ExecutePostAsync(this RestClient client, RestRequest request, CancellationToken cancellationToken); static Task<RestResponse<T>> ExecuteAsync<T>(this RestClient client, RestRequest request, CancellationToken cancellationToken); static Task<RestResponse> ExecuteAsync(this RestClient client, RestRequest request, Method httpMethod, CancellationToken cancellationToken); static Task<RestResponse<T>> ExecuteAsync<T>(this RestClient client, RestRequest request, Method httpMethod, CancellationToken cancellationToken); static Task<T> GetAsync<T>(this RestClient client, RestRequest request, CancellationToken cancellationToken); … +26
- RestSharp.Serializers.Xml: `enum NameStyle` (src/RestSharp.Serializers.Xml/SerializeAsAttribute.cs)
  AsIs; CamelCase; LowerCase; PascalCase
- RestSharp: `abstract class RestResponseBase` (src/RestSharp/Response/RestResponseBase.cs)
  protected RestResponseBase(); RestRequest Request { get; set; }; string ContentType { get; init; }; long? ContentLength { get; init; }; ICollection<string> ContentEncoding { get; init; }; string Content { get; init; }; HttpStatusCode StatusCode { get; set; }; bool IsSuccessful { get; init; }; … +11
- RestSharp.Serializers.Xml: `class DeserializeAsAttribute : Attribute` (src/RestSharp.Serializers.Xml/DeserializeAsAttribute.cs)
  string Name { get; set; }; bool Attribute { get; set; }; bool Content { get; set; }
- RestSharp: `class RestClientOptions` (src/RestSharp/RestClientOptions.cs)
  RestClientOptions(); RestClientOptions(Uri baseUrl); RestClientOptions(string baseUrl); Uri BaseUrl { get; set; }; Func<HttpMessageHandler, HttpMessageHandler> ConfigureMessageHandler { get; set; }; ICredentials Credentials { get; set; }; bool UseDefaultCredentials { get; set; }; DecompressionMethods AutomaticDecompression { get; set; }; … +16
- RestSharp.Serializers.Xml: `class XmlSerializer : IXmlSerializer, IWithRootElement, IWithDateFormat` (src/RestSharp.Serializers.Xml/XmlSerializer.cs)
  XmlSerializer(); XmlSerializer(string @namespace); string Serialize(object obj); string RootElement { get; set; }; … +3
- RestSharp: `class RestResponse : RestResponseBase` (src/RestSharp/Response/RestResponse.cs)
- RestSharp.Serializers.Xml: `class XmlAttributeDeserializer : XmlDeserializer` (src/RestSharp.Serializers.Xml/XmlAttributeDeserializer.cs)
  protected override object GetValueFromXml(XElement root, XName name, PropertyInfo prop, bool useExactName)
- RestSharp: `class RestResponse<T> : RestResponse` (src/RestSharp/Response/RestResponse.cs)
  T Data { get; internal set; }; static RestResponse<T> FromResponse(RestResponse response)
- RestSharp.Serializers.Xml: `static class XmlExtensions` (src/RestSharp.Serializers.Xml/XmlExtensions.cs)
  static XName AsNamespaced(this string name, string @namespace)
- RestSharp: `static class RestRequestExtensions` (src/RestSharp/Request/RestRequestExtensions.cs)
  static RestRequest AddParameter(this RestRequest request, string name, object value, bool encode); static RestRequest AddParameter(this RestRequest request, string name, object value, ParameterType type, bool encode); static RestRequest AddParameter(this RestRequest request, string name, object value, string contentType, ParameterType type, bool encode); static RestRequest AddOrUpdateParameter(this RestRequest request, Parameter parameter); static RestRequest AddOrUpdateParameters(this RestRequest request, IEnumerable<Parameter> parameters); static RestRequest AddOrUpdateParameter(this RestRequest request, string name, object value); static RestRequest AddOrUpdateParameter(this RestRequest request, string name, object value, ParameterType type, bool encode); static RestRequest AddOrUpdateParameter(this RestRequest request, string name, object value, string contentType, ParameterType type, bool encode); … +21
- RestSharp.Serializers.Xml: `static class XmlSerializerClientExtensions` (src/RestSharp.Serializers.Xml/XmlSerializerClientExtensions.cs)
  static RestClient UseXmlSerializer(this RestClient restClient, string xmlNamespace, string rootElement, bool useAttributeDeserializer)
- RestSharp: `static class RestClientExtensions` (src/RestSharp/Serializers/Json/RestClientExtensions.cs)
  static RestClient UseSystemTextJson(this RestClient client); static RestClient UseSystemTextJson(this RestClient client, JsonSerializerOptions options)
- RestSharp: `class NameValuePair` (src/RestSharp/NameValuePair.cs)
  static NameValuePair Empty; NameValuePair(string name, string value); string Name { get; }; string Value { get; }; bool IsEmpty { get; }
- RestSharp: `class OAuth2AuthorizationRequestHeaderAuthenticator : AuthenticatorBase` (src/RestSharp/Authenticators/OAuth2/OAuth2AuthorizationRequestHeaderAuthenticator.cs)
  OAuth2AuthorizationRequestHeaderAuthenticator(string accessToken); OAuth2AuthorizationRequestHeaderAuthenticator(string accessToken, string tokenType); protected override ValueTask<Parameter> GetAuthenticationParameter(string accessToken)
- RestSharp: `class InvalidRequestException : Exception` (src/RestSharp/Request/InvalidRequestException.cs)
  InvalidRequestException(string message, RestRequest request); RestRequest Request { get; }
- RestSharp: `class OAuth1Authenticator : IAuthenticator` (src/RestSharp/Authenticators/OAuth/OAuth1Authenticator.cs)
  virtual string Realm { get; set; }; virtual OAuthParameterHandling ParameterHandling { get; set; }; virtual OAuthSignatureMethod SignatureMethod { get; set; }; virtual OAuthSignatureTreatment SignatureTreatment { get; set; }; virtual OAuthType Type { get; set; }; virtual string ConsumerKey { get; set; }; virtual string ConsumerSecret { get; set; }; virtual string Token { get; set; }; … +16
- RestSharp: `record FileParameter : IEquatable<FileParameter>` (src/RestSharp/Parameters/FileParameter.cs)
  long ContentLength { get; }; Func<Stream> GetFile { get; }; string FileName { get; }; string ContentType { get; }; string Name { get; }; static FileParameter Create(string name, byte[] data, string filename, string contentType); static FileParameter Create(string name, Func<Stream> getFile, long contentLength, string fileName, string contentType); static FileParameter FromFile(string fullPath, string name, string contentType)
- RestSharp: `class RestXmlRequest : RestRequest` (src/RestSharp/Request/RestXmlRequest.cs)
  string DateFormat { get; set; }; string XmlNamespace { get; set; }
- RestSharp: `record Parameter : IEquatable<Parameter>` (src/RestSharp/Parameters/Parameter.cs)
  Parameter(string name, object value, ParameterType type, bool encode); Parameter(string name, object value, string contentType, ParameterType type, bool encode); string Name { get; set; }; object Value { get; set; }; ParameterType Type { get; set; }; DataFormat DataFormat { get; set; }; string ContentType { get; set; }; override string ToString()
- RestSharp: `enum ParameterType` (src/RestSharp/Enum.cs)
  Cookie; GetOrPost; UrlSegment; HttpHeader; RequestBody; QueryString; QueryStringWithoutEncode
- RestSharp: `enum OAuthType` (src/RestSharp/Authenticators/OAuth/Enums.cs)
  RequestToken; AccessToken; ProtectedResource; ClientAuthentication
- RestSharp: `abstract class AuthenticatorBase : IAuthenticator` (src/RestSharp/Authenticators/AuthenticatorBase.cs)
  protected AuthenticatorBase(string token); protected string Token { get; set; }; protected abstract ValueTask<Parameter> GetAuthenticationParameter(string accessToken); ValueTask Authenticate(RestClient client, RestRequest request)
- RestSharp: `interface IRestSerializer` (src/RestSharp/Serializers/IRestSerializer.cs)
  ISerializer Serializer { get; }; IDeserializer Deserializer { get; }; string[] SupportedContentTypes { get; }; DataFormat DataFormat { get; }; … +1
- RestSharp: `static class KnownHeaders` (src/RestSharp/KnownHeaders.cs)
  const string Authorization; const string Accept; const string Allow; const string Expires; … +9
- RestSharp: `interface ISerializer` (src/RestSharp/Serializers/ISerializer.cs)
  string ContentType { get; set; }; string Serialize(object obj)
