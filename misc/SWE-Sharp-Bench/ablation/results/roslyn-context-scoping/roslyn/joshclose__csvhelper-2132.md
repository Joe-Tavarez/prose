## Repository map (from Roslyn, at the starting commit; declarations only)
Solution `CsvHelper.sln`, .NET SDK 6.0.100, 5 C# projects (2 test). Projects are listed most relevant to the issue first.

### Projects
- **CsvHelper** (`src/CsvHelper/CsvHelper.csproj`; net45, net47, net5.0, net6.0, netstandard2.0, netstandard2.1) → no project refs; 213 public types; ns CsvHelper, CsvHelper.Configuration.Attributes, CsvHelper.Configuration
- CsvHelper.Tests (`tests/CsvHelper.Tests/CsvHelper.Tests.csproj`; net6.0) — tests CsvHelper
- **CsvHelper.Performance** (`performance/CsvHelper.Performance/CsvHelper.Performance.csproj`; net6.0) → CsvHelper; 1 public types; ns CsvHelper.Performance
- **_build** (`build/_build.csproj`; net6.0) → no project refs; 1 public types; ns (global)
- CsvHelper.Website (`src/CsvHelper.Website/CsvHelper.Website.csproj`; net6.0) — tests —

### Key public types (members abbreviated)
- CsvHelper: `class CsvReader : IReader` (src/CsvHelper/CsvReader.cs)
  virtual int ColumnCount { get; }; virtual int CurrentIndex { get; }; virtual string[] HeaderRecord { get; }; virtual CsvContext Context { get; }; virtual IReaderConfiguration Configuration { get; private set; }; virtual IParser Parser { get; }; CsvReader(TextReader reader, CultureInfo culture, bool leaveOpen); CsvReader(TextReader reader, IReaderConfiguration configuration, bool leaveOpen); … +58
- CsvHelper.Performance: `class Benchmarks` (performance/CsvHelper.Performance/Program.cs)
  void GlobalSetup(); void GlobalCleanup(); void IterationSetup(); void IterationCleanup(); void GetRecordsFieldCache(); void GetRecordsSpan(); void Parse()
- _build: `class Configuration : Enumeration` (build/Configuration.cs)
  static Configuration Debug; static Configuration Release; static implicit operator string(Configuration configuration)
- CsvHelper: `record CsvConfiguration : IReaderConfiguration, IWriterConfiguration, IEquatable<CsvConfiguration>` (src/CsvHelper/Configuration/CsvConfiguration.cs)
  virtual bool AllowComments { get; set; }; virtual BadDataFound BadDataFound { get; set; }; virtual int BufferSize { get; set; }; virtual bool CacheFields { get; set; }; virtual char Comment { get; set; }; virtual bool CountBytes { get; set; }; virtual CultureInfo CultureInfo { get; protected set; }; virtual string Delimiter { get; set; }; … +40
- CsvHelper: `interface IParserConfiguration` (src/CsvHelper/Configuration/IParserConfiguration.cs)
  CultureInfo CultureInfo { get; }; bool CacheFields { get; }; string NewLine { get; }; bool IsNewLineSet { get; }; CsvMode Mode { get; }; int BufferSize { get; }; int ProcessFieldBufferSize { get; }; bool CountBytes { get; }; … +17
- CsvHelper: `class DelimiterAttribute : Attribute, IClassMapper` (src/CsvHelper/Configuration/Attributes/DelimiterAttribute.cs)
  string Delimiter { get; private set; }; DelimiterAttribute(string delimiter); void ApplyTo(CsvConfiguration configuration)
- CsvHelper: `interface IWriterConfiguration` (src/CsvHelper/Configuration/IWriterConfiguration.cs)
  int BufferSize { get; }; CsvMode Mode { get; }; string Delimiter { get; }; char Quote { get; }; char Escape { get; }; TrimOptions TrimOptions { get; }; InjectionOptions InjectionOptions { get; }; char[] InjectionCharacters { get; }; … +16
- CsvHelper: `enum TrimOptions` (src/CsvHelper/Configuration/TrimOptions.cs)
  None; Trim; InsideQuotes
- CsvHelper: `class CultureInfoAttribute : Attribute, IMemberMapper, IParameterMapper` (src/CsvHelper/Configuration/Attributes/CultureInfoAttribute.cs)
  CultureInfo CultureInfo { get; private set; }; CultureInfoAttribute(string culture); void ApplyTo(MemberMap memberMap); void ApplyTo(ParameterMap parameterMap)
- CsvHelper: `class HasHeaderRecordAttribute : Attribute, IClassMapper` (src/CsvHelper/Configuration/Attributes/HasHeaderRecordAttribute.cs)
  bool HasHeaderRecord { get; private set; }; HasHeaderRecordAttribute(bool hasHeaderRecord); void ApplyTo(CsvConfiguration configuration)
- CsvHelper: `class IgnoreBlankLinesAttribute : Attribute, IClassMapper` (src/CsvHelper/Configuration/Attributes/IgnoreBlankLinesAttribute.cs)
  bool IgnoreBlankLines { get; private set; }; IgnoreBlankLinesAttribute(bool ignoreBlankLines); void ApplyTo(CsvConfiguration configuration)
- CsvHelper: `class TrimOptionsAttribute : Attribute, IClassMapper` (src/CsvHelper/Configuration/Attributes/TrimOptionsAttribute.cs)
  TrimOptions TrimOptions { get; private set; }; TrimOptionsAttribute(TrimOptions trimOptions); void ApplyTo(CsvConfiguration configuration)
- CsvHelper: `class DetectDelimiterAttribute : Attribute, IClassMapper` (src/CsvHelper/Configuration/Attributes/DetectDelimiterAttribute.cs)
  bool DetectDelimiter { get; private set; }; DetectDelimiterAttribute(bool detectDelimiter); void ApplyTo(CsvConfiguration configuration)
- CsvHelper: `interface IReaderConfiguration : IParserConfiguration` (src/CsvHelper/Configuration/IReaderConfiguration.cs)
  bool HasHeaderRecord { get; }; HeaderValidated HeaderValidated { get; }; MissingFieldFound MissingFieldFound { get; }; ReadingExceptionOccurred ReadingExceptionOccurred { get; }; PrepareHeaderForMatch PrepareHeaderForMatch { get; }; ShouldUseConstructorParameters ShouldUseConstructorParameters { get; }; GetConstructor GetConstructor { get; }; GetDynamicPropertyName GetDynamicPropertyName { get; }; … +6
- CsvHelper: `class MemberNameCollection : IEnumerable<string>` (src/CsvHelper/Configuration/MemberNameCollection.cs)
  string this[int index] { get; set; }; string Prefix { get; set; }; List<string> Names { get; }; int Count { get; }; void Add(string name); void Clear(); void AddRange(IEnumerable<string> names); IEnumerator<string> GetEnumerator()
- CsvHelper: `class MemberMapCollection : IList<MemberMap>` (src/CsvHelper/Configuration/MemberMapCollection.cs)
  virtual int Count { get; }; virtual bool IsReadOnly { get; }; MemberMapCollection(); MemberMapCollection(IComparer<MemberMap> comparer); virtual IEnumerator<MemberMap> GetEnumerator(); virtual void Add(MemberMap item); virtual void AddRange(ICollection<MemberMap> collection); virtual void Clear(); … +10
- CsvHelper: `interface IReader : IReaderRow, IDisposable` (src/CsvHelper/IReader.cs)
  bool ReadHeader(); bool Read(); Task<bool> ReadAsync(); IEnumerable<T> GetRecords<T>(); IEnumerable<T> GetRecords<T>(T anonymousTypeDefinition); IEnumerable<object> GetRecords(Type type); IEnumerable<T> EnumerateRecords<T>(T record)
- CsvHelper: `class MemberMapTypeConverterOption` (src/CsvHelper/Configuration/MemberMapTypeConverterOption.cs)
  MemberMapTypeConverterOption(MemberMap memberMap); virtual MemberMap CultureInfo(CultureInfo cultureInfo); virtual MemberMap DateTimeStyles(DateTimeStyles dateTimeStyle); virtual MemberMap TimespanStyles(TimeSpanStyles timeSpanStyles); virtual MemberMap NumberStyles(NumberStyles numberStyle); virtual MemberMap Format(params string[] formats); virtual MemberMap UriKind(UriKind uriKind); virtual MemberMap BooleanValues(bool isTrue, bool clearValues, params string[] booleanValues); … +3
- CsvHelper: `class TypeConverterOptions` (src/CsvHelper/TypeConversion/TypeConverterOptions.cs)
  CultureInfo CultureInfo { get; set; }; DateTimeStyles? DateTimeStyle { get; set; }; TimeSpanStyles? TimeSpanStyle { get; set; }; NumberStyles? NumberStyles { get; set; }; string[] Formats { get; set; }; UriKind? UriKind { get; set; }; bool? EnumIgnoreCase { get; set; }; List<string> BooleanTrueValues { get; }; … +3
- CsvHelper: `class ParameterMapTypeConverterOption` (src/CsvHelper/Configuration/ParameterMapTypeConverterOption.cs)
  ParameterMapTypeConverterOption(ParameterMap parameterMap); virtual ParameterMap CultureInfo(CultureInfo cultureInfo); virtual ParameterMap DateTimeStyles(DateTimeStyles dateTimeStyle); virtual ParameterMap TimespanStyles(TimeSpanStyles timeSpanStyles); virtual ParameterMap NumberStyles(NumberStyles numberStyle); virtual ParameterMap Format(params string[] formats); virtual ParameterMap UriKind(UriKind uriKind); virtual ParameterMap BooleanValues(bool isTrue, bool clearValues, params string[] booleanValues); … +2
- CsvHelper: `static class ArrayHelper` (src/CsvHelper/ArrayHelper.cs)
  static void Trim(char[] buffer, ref int start, ref int length, char[] trimChars); static bool Contains(char[] array, in char c)
- CsvHelper: `class NameIndexAttribute : Attribute, IMemberMapper, IParameterMapper` (src/CsvHelper/Configuration/Attributes/NameIndexAttribute.cs)
  int NameIndex { get; private set; }; NameIndexAttribute(int nameIndex); void ApplyTo(MemberMap memberMap); void ApplyTo(ParameterMap parameterMap)
- CsvHelper: `interface IReaderRow` (src/CsvHelper/IReaderRow.cs)
  int ColumnCount { get; }; int CurrentIndex { get; }; string[] HeaderRecord { get; }; IParser Parser { get; }; CsvContext Context { get; }; IReaderConfiguration Configuration { get; }; string this[int index] { get; }; string this[string name] { get; }; … +37
- CsvHelper: `class CsvDataReader : IDataReader` (src/CsvHelper/CsvDataReader.cs)
  object this[int i] { get; }; object this[string name] { get; }; int Depth { get; }; bool IsClosed { get; private set; }; int RecordsAffected { get; }; int FieldCount { get; }; CsvDataReader(CsvReader csv, DataTable schemaTable); void Close(); … +26
- CsvHelper: `abstract class ClassMap` (src/CsvHelper/Configuration/ClassMap.cs)
  virtual Type ClassType { get; private set; }; virtual List<ParameterMap> ParameterMaps { get; }; virtual MemberMapCollection MemberMaps { get; }; virtual MemberReferenceMapCollection ReferenceMaps { get; }; MemberMap Map(Type classType, MemberInfo member, bool useExistingMap); virtual MemberMap<object, object> Map(); virtual MemberReferenceMap References(Type classMapType, MemberInfo member, params object[] constructorArgs); virtual ParameterMap Parameter(string name); … +15
- CsvHelper: `class MemberMapData` (src/CsvHelper/Configuration/MemberMapData.cs)
  virtual Type Type { get; }; virtual MemberInfo Member { get; private set; }; virtual MemberNameCollection Names { get; }; virtual int NameIndex { get; set; }; virtual bool IsNameSet { get; set; }; virtual int Index { get; set; }; virtual int IndexEnd { get; set; }; virtual bool IsIndexSet { get; set; }; … +14
- CsvHelper: `interface IHasNameIndex<TClass, TMember> : IBuildableClass<TClass>` (src/CsvHelper/Configuration/ClassMapBuilder.cs)
  IHasNameIndexOptions<TClass, TMember> NameIndex(int index)
- CsvHelper: `class ParameterMapData` (src/CsvHelper/Configuration/ParameterMapData.cs)
  virtual ParameterInfo Parameter { get; private set; }; virtual MemberNameCollection Names { get; }; virtual int NameIndex { get; set; }; virtual bool IsNameSet { get; set; }; virtual int Index { get; set; }; virtual bool IsIndexSet { get; set; }; virtual ITypeConverter TypeConverter { get; set; }; virtual TypeConverterOptions TypeConverterOptions { get; set; }; … +7
- CsvHelper: `class ReaderException : CsvHelperException` (src/CsvHelper/ReaderException.cs)
  ReaderException(CsvContext context); ReaderException(CsvContext context, string message); ReaderException(CsvContext context, string message, Exception innerException)
- CsvHelper: `class IndexAttribute : Attribute, IMemberMapper, IParameterMapper` (src/CsvHelper/Configuration/Attributes/IndexAttribute.cs)
  int Index { get; private set; }; int IndexEnd { get; private set; }; IndexAttribute(int index, int indexEnd); void ApplyTo(MemberMap memberMap); void ApplyTo(ParameterMap parameterMap)
- CsvHelper: `abstract class MemberMap` (src/CsvHelper/Configuration/MemberMap.cs)
  virtual MemberMapData Data { get; protected set; }; virtual MemberMapTypeConverterOption TypeConverterOption { get; protected set; }; static MemberMap CreateGeneric(Type classType, MemberInfo member); virtual MemberMap Name(params string[] names); virtual MemberMap NameIndex(int index); virtual MemberMap Index(int index, int indexEnd); virtual MemberMap Ignore(); virtual MemberMap Ignore(bool ignore); … +7
- CsvHelper: `class MemberMap<TClass, TMember> : MemberMap` (src/CsvHelper/Configuration/MemberMap`1.cs)
  MemberMap(MemberInfo member); virtual MemberMap<TClass, TMember> Name(params string[] names); virtual MemberMap<TClass, TMember> NameIndex(int index); virtual MemberMap<TClass, TMember> Index(int index, int indexEnd); virtual MemberMap<TClass, TMember> Ignore(); virtual MemberMap<TClass, TMember> Ignore(bool ignore); virtual MemberMap<TClass, TMember> Default(TMember defaultValue, bool useOnConversionFailure); virtual MemberMap<TClass, TMember> Default(string defaultValue, bool useOnConversionFailure); … +8
