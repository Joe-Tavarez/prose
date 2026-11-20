## Repository map (from Roslyn, at the starting commit; declarations only)
Solution `Moq.sln`, .NET SDK 6.0.300, 2 C# projects (1 test). Projects are listed most relevant to the issue first.

### Projects
- Moq.Tests (`tests/Moq.Tests/Moq.Tests.csproj`; net472, netcoreapp3.1) — tests Moq
- **Moq** (`src/Moq/Moq.csproj`; net45, netstandard2.0) → no project refs; 74 public types; ns Moq, Moq.Language.Flow, Moq.Language

### Key public types (members abbreviated)
- Moq: `interface IInvocation` (src/Moq/IInvocation.cs)
  MethodInfo Method { get; }; IReadOnlyList<object> Arguments { get; }; ISetup MatchingSetup { get; }; bool IsVerified { get; }; object ReturnValue { get; }
- Moq: `interface ICallback<TMock, TResult> : IFluentInterface` (src/Moq/Language/ICallback.cs)
  IReturnsThrows<TMock, TResult> Callback(InvocationAction action); IReturnsThrows<TMock, TResult> Callback(Delegate callback); IReturnsThrows<TMock, TResult> Callback(Action action); IReturnsThrows<TMock, TResult> Callback<T>(Action<T> action); IReturnsThrows<TMock, TResult> Callback<T1, T2>(Action<T1, T2> action); IReturnsThrows<TMock, TResult> Callback<T1, T2, T3>(Action<T1, T2, T3> action); IReturnsThrows<TMock, TResult> Callback<T1, T2, T3, T4>(Action<T1, T2, T3, T4> action); IReturnsThrows<TMock, TResult> Callback<T1, T2, T3, T4, T5>(Action<T1, T2, T3, T4, T5> action); … +11
- Moq: `struct InvocationAction` (src/Moq/InvocationAction.cs)
  InvocationAction(Action<IInvocation> action)
- Moq: `struct InvocationFunc` (src/Moq/InvocationFunc.cs)
  InvocationFunc(Func<IInvocation, object> func)
- Moq: `interface IInvocationList : IReadOnlyList<IInvocation>` (src/Moq/IInvocationList.cs)
  void Clear()
- Moq: `abstract class Mock : IInterceptor, IFluentInterface` (src/Moq/Interception/Mock.cs)
  static T Of<T>(); static T Of<T>(MockBehavior behavior); static T Of<T>(Expression<Func<T, bool>> predicate); static T Of<T>(Expression<Func<T, bool>> predicate, MockBehavior behavior); protected Mock(); static Mock<T> Get<T>(T mocked); static void Verify(params Mock[] mocks); static void VerifyAll(params Mock[] mocks); … +13
- Moq: `abstract class LookupOrFallbackDefaultValueProvider : DefaultValueProvider` (src/Moq/LookupOrFallbackDefaultValueProvider.cs)
  protected LookupOrFallbackDefaultValueProvider(); protected void Deregister(Type factoryKey); protected void Register(Type factoryKey, Func<Type, Mock, object> factory); protected override sealed object GetDefaultParameterValue(ParameterInfo parameter, Mock mock); protected override sealed object GetDefaultReturnValue(MethodInfo method, Mock mock); protected override sealed object GetDefaultValue(Type type, Mock mock); protected virtual object GetFallbackDefaultValue(Type type, Mock mock)
- Moq: `abstract class DefaultValueProvider` (src/Moq/DefaultValueProvider.cs)
  static DefaultValueProvider Empty { get; }; static DefaultValueProvider Mock { get; }; protected DefaultValueProvider(); protected abstract object GetDefaultValue(Type type, Mock mock); protected virtual object GetDefaultParameterValue(ParameterInfo parameter, Mock mock); protected virtual object GetDefaultReturnValue(MethodInfo method, Mock mock)
- Moq: `interface IThrows : IFluentInterface` (src/Moq/Language/IThrows.cs)
  IThrowsResult Throws(Exception exception); IThrowsResult Throws<TException>()
- Moq: `interface IReturnsThrowsGetter<TMock, TProperty> : IReturnsGetter<TMock, TProperty>, IThrows, IFluentInterface` (src/Moq/Language/Flow/IReturnsThrows.cs)
- Moq: `static class SequenceExtensions` (src/Moq/Obsolete/SequenceExtensions.cs)
  static ISetupSequentialResult<TResult> SetupSequence<TMock, TResult>(this Mock<TMock> mock, Expression<Func<TMock, TResult>> expression); static ISetupSequentialAction SetupSequence<TMock>(this Mock<TMock> mock, Expression<Action<TMock>> expression); static ISetupSequentialResult<Task<TResult>> ReturnsAsync<TResult>(this ISetupSequentialResult<Task<TResult>> setup, TResult value); static ISetupSequentialResult<Task<TResult>> ReturnsAsync<TResult>(this ISetupSequentialResult<Task<TResult>> setup, Func<TResult> valueFunction); static ISetupSequentialResult<ValueTask<TResult>> ReturnsAsync<TResult>(this ISetupSequentialResult<ValueTask<TResult>> setup, TResult value); static ISetupSequentialResult<ValueTask<TResult>> ReturnsAsync<TResult>(this ISetupSequentialResult<ValueTask<TResult>> setup, Func<TResult> valueFunction); static ISetupSequentialResult<Task> PassAsync(this ISetupSequentialResult<Task> setup); static ISetupSequentialResult<ValueTask> PassAsync(this ISetupSequentialResult<ValueTask> setup); … +4
- Moq: `interface IThrowsResult : IOccurrence, IVerifies, IFluentInterface` (src/Moq/Language/Flow/IThrowsResult.cs)
- Moq: `interface IReturnsGetter<TMock, TProperty> : IFluentInterface` (src/Moq/Language/IReturnsGetter.cs)
  IReturnsResult<TMock> Returns(TProperty value); IReturnsResult<TMock> Returns(Func<TProperty> valueFunction); IReturnsResult<TMock> CallBase()
- Moq: `interface ISetupSequentialAction` (src/Moq/Language/ISetupSequentialAction.cs)
  ISetupSequentialAction Pass(); ISetupSequentialAction Throws<TException>(); ISetupSequentialAction Throws(Exception exception)
- Moq: `interface ICallbackGetter<TMock, TProperty> : IFluentInterface` (src/Moq/Language/ICallbackGetter.cs)
  IReturnsThrowsGetter<TMock, TProperty> Callback(Action action)
- Moq: `interface ICallbackSetter<TProperty> : IFluentInterface` (src/Moq/Language/ICallbackSetter.cs)
  ICallbackResult Callback(Action<TProperty> action)
- Moq: `interface IMocked` (src/Moq/IMocked.cs)
  Mock Mock { get; }
- Moq: `interface IReturnsThrows<TMock, TResult> : IReturns<TMock, TResult>, IThrows, IFluentInterface` (src/Moq/Language/Flow/IReturnsThrows.cs)
- Moq: `interface ISetupGetter<TMock, TProperty> : ICallbackGetter<TMock, TProperty>, IReturnsThrowsGetter<TMock, TProperty>, IVerifies` (src/Moq/Language/Flow/ISetup.cs)
- Moq: `interface ISetupSetter<TMock, TProperty> : ICallbackSetter<TProperty>, ICallbackResult, IRaise<TMock>` (src/Moq/Language/Flow/ISetup.cs)
- Moq: `interface IMocked<T> : IMocked` (src/Moq/IMocked.cs)
  Mock<T> Mock { get; }
- Moq: `interface ISetupSequentialResult<TResult>` (src/Moq/Language/ISetupSequentialResult.cs)
  ISetupSequentialResult<TResult> Returns(TResult value); ISetupSequentialResult<TResult> Returns(Func<TResult> valueFunction); ISetupSequentialResult<TResult> Throws(Exception exception); ISetupSequentialResult<TResult> Throws<TException>(); ISetupSequentialResult<TResult> CallBase()
- Moq: `class Mock<T> : Mock, IMock<T>` (src/Moq/Mock.Generic.cs)
  Mock(); Mock(params object[] args); Mock(MockBehavior behavior); Mock(MockBehavior behavior, params object[] args); … +66
- Moq: `static class GeneratedReturnsExtensions` (src/Moq/ReturnsExtensions.Generated.cs)
  static IReturnsResult<TMock> ReturnsAsync<T, TMock, TResult>(this IReturns<TMock, Task<TResult>> mock, Func<T, TResult> valueFunction); static IReturnsResult<TMock> ReturnsAsync<T1, T2, TMock, TResult>(this IReturns<TMock, Task<TResult>> mock, Func<T1, T2, TResult> valueFunction); static IReturnsResult<TMock> ReturnsAsync<T1, T2, T3, TMock, TResult>(this IReturns<TMock, Task<TResult>> mock, Func<T1, T2, T3, TResult> valueFunction); static IReturnsResult<TMock> ReturnsAsync<T1, T2, T3, T4, TMock, TResult>(this IReturns<TMock, Task<TResult>> mock, Func<T1, T2, T3, T4, TResult> valueFunction); … +26
- Moq: `interface IProtectedMock<TMock> : IFluentInterface` (src/Moq/Protected/IProtectedMock.cs)
  IProtectedAsMock<TMock, TAnalog> As<TAnalog>(); ISetup<TMock> Setup(string voidMethodName, params object[] args); ISetup<TMock> Setup(string voidMethodName, bool exactParameterMatch, params object[] args); ISetup<TMock> Setup(string voidMethodName, Type[] genericTypeArguments, bool exactParameterMatch, params object[] args); … +21
- Moq: `interface IRaise<T> : IFluentInterface` (src/Moq/Language/IRaise.cs)
  IVerifies Raises(Action<T> eventExpression, EventArgs args); IVerifies Raises(Action<T> eventExpression, Func<EventArgs> func); IVerifies Raises(Action<T> eventExpression, params object[] args); IVerifies Raises<T1>(Action<T> eventExpression, Func<T1, EventArgs> func); … +15
- Moq: `interface ICallback : IFluentInterface` (src/Moq/Language/ICallback.cs)
  ICallbackResult Callback(InvocationAction action); ICallbackResult Callback(Delegate callback); ICallbackResult Callback(Action action); ICallbackResult Callback<T>(Action<T> action); … +15
- Moq: `interface IReturns<TMock, TResult> : IFluentInterface` (src/Moq/Language/IReturns.cs)
  IReturnsResult<TMock> Returns(TResult value); IReturnsResult<TMock> Returns(InvocationFunc valueFunction); IReturnsResult<TMock> Returns(Delegate valueFunction); IReturnsResult<TMock> Returns(Func<TResult> valueFunction); … +17
- Moq: `interface IVerifies : IFluentInterface` (src/Moq/Language/IVerifies.cs)
  void Verifiable(); void Verifiable(string failMessage)
- Moq: `interface ITypeMatcher` (src/Moq/ITypeMatcher.cs)
  bool Matches(Type typeArgument)
- Moq: `class MockFactory` (src/Moq/Obsolete/MockFactory.cs)
  MockFactory(MockBehavior defaultBehavior); bool CallBase { get; set; }; DefaultValue DefaultValue { get; set; }; DefaultValueProvider DefaultValueProvider { get; set; }; … +12
- Moq: `static class ReturnsExtensions` (src/Moq/ReturnsExtensions.cs)
  static IReturnsResult<TMock> ReturnsAsync<TMock, TResult>(this IReturns<TMock, Task<TResult>> mock, TResult value); static IReturnsResult<TMock> ReturnsAsync<TMock, TResult>(this IReturns<TMock, ValueTask<TResult>> mock, TResult value); static IReturnsResult<TMock> ReturnsAsync<TMock, TResult>(this IReturns<TMock, Task<TResult>> mock, Func<TResult> valueFunction); static IReturnsResult<TMock> ReturnsAsync<TMock, TResult>(this IReturns<TMock, ValueTask<TResult>> mock, Func<TResult> valueFunction); … +15
- Moq: `struct Times : IEquatable<Times>` (src/Moq/Times.cs)
  void Deconstruct(out int from, out int to); static Times AtLeast(int callCount); static Times AtLeastOnce(); static Times AtMost(int callCount); … +12
- Moq: `static class It` (src/Moq/It.cs)
  static TValue IsAny<TValue>(); static TValue IsNotNull<TValue>(); static TValue Is<TValue>(Expression<Func<TValue, bool>> match); static TValue Is<TValue>(Expression<Func<object, Type, bool>> match); … +10
- Moq: `interface ISetup` (src/Moq/ISetup.cs)
  LambdaExpression Expression { get; }; Mock InnerMock { get; }; bool IsConditional { get; }; bool IsMatched { get; }; … +6
- Moq: `interface IProtectedAsMock<T, TAnalog> : IFluentInterface` (src/Moq/Protected/IProtectedAsMock.cs)
  ISetup<T> Setup(Expression<Action<TAnalog>> expression); ISetup<T, TResult> Setup<TResult>(Expression<Func<TAnalog, TResult>> expression); ISetupGetter<T, TProperty> SetupGet<TProperty>(Expression<Func<TAnalog, TProperty>> expression); Mock<T> SetupProperty<TProperty>(Expression<Func<TAnalog, TProperty>> expression, TProperty initialValue); … +5
- Moq: `interface ICallbackResult : ICallBase, ICallBaseResult, IThrows` (src/Moq/Language/Flow/ICallbackResult.cs)
- Moq: `abstract class Match : IMatcher` (src/Moq/Match.cs)
  static T Create<T>(Predicate<T> condition); static T Create<T>(Predicate<T> condition, Expression<Func<T>> renderExpression); static T Create<T>(Func<object, Type, bool> condition, Expression<Func<T>> renderExpression)
