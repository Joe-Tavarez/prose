## Repository map (from Roslyn, at the starting commit; declarations only)
Solution `Avalonia.Desktop.slnf`, .NET SDK 8.0.404, 68 C# projects (17 test). Projects are listed most relevant to the issue first.

### Projects
- **Avalonia.Base** (`src/Avalonia.Base/Avalonia.Base.csproj`; net6.0, net8.0, netstandard2.0) → no project refs; 871 public types; ns Avalonia.Media, Avalonia.Input, Avalonia.Utilities
- **Avalonia.Controls** (`src/Avalonia.Controls/Avalonia.Controls.csproj`; net6.0, net8.0, netstandard2.0) → Avalonia.Base, Avalonia.Remote.Protocol; 473 public types; ns Avalonia.Controls, Avalonia.Controls.Primitives, Avalonia.Controls.Platform
- Avalonia.Controls.UnitTests (`tests/Avalonia.Controls.UnitTests/Avalonia.Controls.UnitTests.csproj`; net8.0) — tests Avalonia, Avalonia.Base, Avalonia.Controls, Avalonia.DesignerSupport, Avalonia.Dialogs, Avalonia.Headless, Avalonia.Markup, Avalonia.Markup.Xaml, Avalonia.Markup.Xaml.Loader, Avalonia.Metal, Avalonia.MicroCom, Avalonia.OpenGL, Avalonia.Remote.Protocol, Avalonia.Themes.Simple, Avalonia.Vulkan
- Avalonia.Base.UnitTests (`tests/Avalonia.Base.UnitTests/Avalonia.Base.UnitTests.csproj`; net8.0) — tests Avalonia, Avalonia.Base, Avalonia.Controls, Avalonia.DesignerSupport, Avalonia.Dialogs, Avalonia.Headless, Avalonia.Markup, Avalonia.Markup.Xaml, Avalonia.Markup.Xaml.Loader, Avalonia.Metal, Avalonia.MicroCom, Avalonia.OpenGL, Avalonia.Remote.Protocol, Avalonia.Themes.Simple, Avalonia.Vulkan
- **ControlCatalog** (`samples/ControlCatalog/ControlCatalog.csproj`; net8.0, netstandard2.0) → Avalonia, Avalonia.Base, Avalonia.Controls, Avalonia.Controls.ColorPicker, Avalonia.DesignerSupport, Avalonia.Dialogs, Avalonia.Fonts.Inter, Avalonia.Markup, Avalonia.Markup.Xaml, Avalonia.Metal, Avalonia.MicroCom, Avalonia.OpenGL, Avalonia.Remote.Protocol, Avalonia.Skia, Avalonia.Themes.Fluent, Avalonia.Themes.Simple, Avalonia.Vulkan, ControlSamples, MiniMvvm; 110 public types; ns ControlCatalog.Pages, ControlCatalog.ViewModels, Avalonia.SourceGenerator
- Avalonia.Markup.Xaml.UnitTests (`tests/Avalonia.Markup.Xaml.UnitTests/Avalonia.Markup.Xaml.UnitTests.csproj`; net47, net8.0) — tests Avalonia, Avalonia.Base, Avalonia.Controls, Avalonia.DesignerSupport, Avalonia.Dialogs, Avalonia.Headless, Avalonia.Markup, Avalonia.Markup.Xaml, Avalonia.Markup.Xaml.Loader, Avalonia.Metal, Avalonia.MicroCom, Avalonia.OpenGL, Avalonia.Remote.Protocol, Avalonia.Themes.Simple, Avalonia.Vulkan
- **Avalonia.Markup.Xaml** (`src/Markup/Avalonia.Markup.Xaml/Avalonia.Markup.Xaml.csproj`; net6.0, net8.0, netstandard2.0) → Avalonia.Base, Avalonia.Controls, Avalonia.Markup, Avalonia.Remote.Protocol; 54 public types; ns Avalonia.Markup.Xaml.MarkupExtensions.CompiledBindings, Avalonia.Markup.Xaml.XamlIl.Runtime, Avalonia.Markup.Xaml
- **Avalonia.OpenGL** (`src/Avalonia.OpenGL/Avalonia.OpenGL.csproj`; net6.0, net8.0, netstandard2.0) → Avalonia.Base, Avalonia.Controls, Avalonia.Remote.Protocol; 39 public types; ns Avalonia.OpenGL, Avalonia.OpenGL.Egl, Avalonia.OpenGL.Features
- Avalonia.Markup.UnitTests (`tests/Avalonia.Markup.UnitTests/Avalonia.Markup.UnitTests.csproj`; net8.0) — tests Avalonia, Avalonia.Base, Avalonia.Controls, Avalonia.DesignerSupport, Avalonia.Dialogs, Avalonia.Headless, Avalonia.Markup, Avalonia.Markup.Xaml, Avalonia.Metal, Avalonia.MicroCom, Avalonia.OpenGL, Avalonia.Remote.Protocol, Avalonia.Themes.Simple, Avalonia.Vulkan
- **Avalonia.Dialogs** (`src/Avalonia.Dialogs/Avalonia.Dialogs.csproj`; net6.0, net8.0, netstandard2.0) → Avalonia.Base, Avalonia.Controls, Avalonia.Markup, Avalonia.Markup.Xaml, Avalonia.Remote.Protocol; 14 public types; ns Avalonia.Dialogs.Internal, Avalonia.Dialogs
- **Avalonia.Vulkan** (`src/Avalonia.Vulkan/Avalonia.Vulkan.csproj`; net6.0, net8.0, netstandard2.0) → Avalonia.Base, Avalonia.Controls, Avalonia.Remote.Protocol; 19 public types; ns Avalonia.Vulkan.UnmanagedInterop, Avalonia.Vulkan, Avalonia.Vulkan.Interop
- Avalonia.Skia.RenderTests (`tests/Avalonia.Skia.RenderTests/Avalonia.Skia.RenderTests.csproj`; net8.0) — tests Avalonia, Avalonia.Base, Avalonia.Controls, Avalonia.DesignerSupport, Avalonia.Dialogs, Avalonia.Headless, Avalonia.Markup, Avalonia.Markup.Xaml, Avalonia.Metal, Avalonia.MicroCom, Avalonia.OpenGL, Avalonia.Remote.Protocol, Avalonia.Skia, Avalonia.Themes.Simple, Avalonia.Vulkan
- … 56 more projects (not listed)

### Key public types (members abbreviated)
- Avalonia.Base: `class StyledElement : Animatable, IDataContextProvider, ILogical` (src/Avalonia.Base/StyledElement.cs)
  static readonly StyledProperty<object> DataContextProperty; static readonly DirectProperty<StyledElement, string> NameProperty; static readonly DirectProperty<StyledElement, StyledElement> ParentProperty; static readonly DirectProperty<StyledElement, AvaloniaObject> TemplatedParentProperty; static readonly StyledProperty<ControlTheme> ThemeProperty; StyledElement(); EventHandler<LogicalTreeAttachmentEventArgs> AttachedToLogicalTree; EventHandler<LogicalTreeAttachmentEventArgs> DetachedFromLogicalTree; … +31
- Avalonia.Controls: `class SelectingItemsControl : ItemsControl` (src/Avalonia.Controls/Primitives/SelectingItemsControl.cs)
  static readonly StyledProperty<bool> AutoScrollToSelectedItemProperty; static readonly DirectProperty<SelectingItemsControl, int> SelectedIndexProperty; static readonly DirectProperty<SelectingItemsControl, object> SelectedItemProperty; static readonly StyledProperty<object> SelectedValueProperty; static readonly StyledProperty<IBinding> SelectedValueBindingProperty; protected static readonly DirectProperty<SelectingItemsControl, IList> SelectedItemsProperty; protected static readonly DirectProperty<SelectingItemsControl, ISelectionModel> SelectionProperty; protected static readonly StyledProperty<SelectionMode> SelectionModeProperty; … +40
- ControlCatalog: `class TreeViewPageViewModel.Node` (samples/ControlCatalog/ViewModels/TreeViewPageViewModel.cs)
  Node(); Node(Node parent, int index); Node Parent { get; }; string Header { get; }; bool AreChildrenInitialized { get; }; ObservableCollection<Node> Children { get; }; void AddItem(); void RemoveItem(Node child); … +1
- Avalonia.Markup.Xaml: `class DataTemplate : IRecyclingDataTemplate, ITypedDataTemplate` (src/Markup/Avalonia.Markup.Xaml/Templates/DataTemplate.cs)
  Type DataType { get; set; }; object Content { get; set; }; bool Match(object data); Control Build(object data); Control Build(object data, Control existing)
- Avalonia.OpenGL: `class GlInterface : GlBasicInfoInterface` (src/Avalonia.OpenGL/GlInterface.cs)
  string Version { get; }; string Vendor { get; }; string Renderer { get; }; GlContextInfo ContextInfo { get; }; GlInterface(GlVersion version, Func<string, IntPtr> getProcAddress); IntPtr GetProcAddress(string proc); void ClearStencil(int s); void ClearColor(float r, float g, float b, float a); … +78
- Avalonia.Dialogs: `class ManagedFileChooserFilterViewModel : AvaloniaDialogsInternalViewModelBase` (src/Avalonia.Dialogs/Internal/ManagedFileChooserFilterViewModel.cs)
  string Name { get; }; ManagedFileChooserFilterViewModel(FilePickerFileType filter); bool Match(string filename); override string ToString()
- Avalonia.Vulkan: `interface IVulkanExternalImage : IDisposable` (src/Avalonia.Vulkan/IVulkanContextExternalObjectsFeature.cs)
  VulkanImageInfo Info { get; }
- Avalonia.Remote.Protocol: `enum Key` (src/Avalonia.Base/Input/Key.cs)
  None; Cancel; Back; Tab; LineFeed; Clear; Return; Enter; … +215
- RenderDemo: `class MainWindowViewModel : ViewModelBase` (samples/RenderDemo/ViewModels/MainWindowViewModel.cs)
  MainWindowViewModel(); bool DrawDirtyRects { get; set; }; bool DrawFps { get; set; }; bool DrawLayoutTimeGraph { get; set; }; bool DrawRenderTimeGraph { get; set; }; double Width { get; set; }; double Height { get; set; }; MiniCommand ToggleDrawDirtyRects { get; }; … +4
- Avalonia.Markup: `enum RelativeSourceMode` (src/Markup/Avalonia.Markup/Data/RelativeSource.cs)
  DataContext; TemplatedParent; Self; FindAncestor
- Avalonia.Skia: `static class SkiaApplicationExtensions` (src/Skia/Avalonia.Skia/SkiaApplicationExtensions.cs)
  static AppBuilder UseSkia(this AppBuilder builder)
- IntegrationTestApp: `class ComboBoxPage : UserControl` (samples/IntegrationTestApp/Pages/ComboBoxPage.axaml.cs)
  ComboBoxPage(); void InitializeComponent(bool loadXaml)
- DevGenerators: `class EnumMemberDictionaryGenerator : IIncrementalGenerator` (src/tools/DevGenerators/EnumMemberDictionaryGenerator.cs)
  void Initialize(IncrementalGeneratorInitializationContext context)
- Avalonia.LinuxFramebuffer: `enum DrmModeSubPixel` (src/Linux/Avalonia.LinuxFramebuffer/Output/Drm.cs)
  DRM_MODE_SUBPIXEL_UNKNOWN; DRM_MODE_SUBPIXEL_HORIZONTAL_RGB; DRM_MODE_SUBPIXEL_HORIZONTAL_BGR; DRM_MODE_SUBPIXEL_VERTICAL_RGB; DRM_MODE_SUBPIXEL_VERTICAL_BGR; DRM_MODE_SUBPIXEL_NONE
- MiniMvvm: `class ViewModelBase : INotifyPropertyChanged` (samples/MiniMvvm/ViewModelBase.cs)
  PropertyChangedEventHandler PropertyChanged; protected bool RaiseAndSetIfChanged<T>(ref T field, T value, string propertyName); protected void RaisePropertyChanged(string propertyName)
- GpuInterop: `static class VulkanExtensions` (samples/GpuInterop/VulkanDemo/VulkanExtensions.cs)
  static void ThrowOnError(this Result result)
- Avalonia.ReactiveUI: `class AutoDataTemplateBindingHook : IPropertyBindingHook` (src/Avalonia.ReactiveUI/AutoDataTemplateBindingHook.cs)
  bool ExecuteHook(object source, object target, Func<IObservedChange<object, object>[]> getCurrentViewModelProperties, Func<IObservedChange<object, object>[]> getCurrentViewProperties, BindingDirection direction)
- Avalonia.Build.Tasks: `class CompileAvaloniaXamlTask : ITask` (src/Avalonia.Build.Tasks/CompileAvaloniaXamlTask.cs)
  const string AvaloniaCompileOutputMetadataName; bool Execute(); string ProjectDirectory { get; set; }; ITaskItem AssemblyFile { get; set; }; ITaskItem RefAssemblyFile { get; set; }; ITaskItem[] References { get; set; }; bool VerifyIl { get; set; }; bool DefaultCompileBindings { get; set; }; … +10
- Avalonia.Win32: `static class Win32ApplicationExtensions` (src/Windows/Avalonia.Win32/Win32Platform.cs)
  static AppBuilder UseWin32(this AppBuilder builder)
- Avalonia.Native: `class AvaloniaNativePlatformOptions` (src/Avalonia.Native/AvaloniaNativePlatformExtensions.cs)
  IReadOnlyList<AvaloniaNativeRenderingMode> RenderingMode { get; set; }; bool OverlayPopups { get; set; }; string AvaloniaNativeLibraryPath { get; set; }; bool AppSandboxEnabled { get; set; }
- Avalonia.Headless: `class AvaloniaTestApplicationAttribute : Attribute` (src/Headless/Avalonia.Headless/AvaloniaTestApplicationAttribute.cs)
  Type AppBuilderEntryPointType { get; }; AvaloniaTestApplicationAttribute(Type appBuilderEntryPointType)
- Avalonia.Direct2D1: `static class Direct2DApplicationExtensions` (src/Windows/Avalonia.Direct2D1/Direct2D1Platform.cs)
  static AppBuilder UseDirect2D1(this AppBuilder builder)
- XEmbedSample: `class AvaloniaXEmbedGtkSocket : Socket` (samples/XEmbedSample/SocketEx.cs)
  AvaloniaXEmbedGtkSocket(RGBA backgroundColor); object Content { get; set; }; protected override void OnRealized(); protected override void OnSizeAllocated(Rectangle allocation); protected override void OnDestroyed()
- Avalonia.Analyzers: `class AvaloniaAnalysisException : Exception` (src/tools/Avalonia.Analyzers/AvaloniaPropertyAnalyzer.cs)
  AvaloniaAnalysisException(string message, Exception innerException); protected AvaloniaAnalysisException(SerializationInfo info, StreamingContext context)
- Avalonia.X11: `enum X11RenderingMode` (src/Avalonia.X11/X11Platform.cs)
  Software; Glx; Egl; Vulkan
- Avalonia.Controls.ColorPicker: `static class ColorHelper` (src/Avalonia.Controls.ColorPicker/Helpers/ColorHelper.cs)
  static double GetRelativeLuminance(Color color); static bool ToDisplayNameExists { get; }; static string ToDisplayName(Color color)
