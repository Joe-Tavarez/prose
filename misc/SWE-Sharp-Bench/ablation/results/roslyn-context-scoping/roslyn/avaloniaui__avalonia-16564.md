## Repository map (from Roslyn, at the starting commit; declarations only)
Solution `Avalonia.Desktop.slnf`, .NET SDK 8.0.404, 68 C# projects (18 test). Projects are listed most relevant to the issue first.

### Projects
- **Avalonia.Controls** (`src/Avalonia.Controls/Avalonia.Controls.csproj`; net6.0, net8.0, netstandard2.0) → Avalonia.Base, Avalonia.Remote.Protocol; 463 public types; ns Avalonia.Controls, Avalonia.Controls.Primitives, Avalonia.Controls.Platform
- **Avalonia.Base** (`src/Avalonia.Base/Avalonia.Base.csproj`; net6.0, net8.0, netstandard2.0) → no project refs; 857 public types; ns Avalonia.Media, Avalonia.Input, Avalonia.Utilities
- Avalonia.Controls.UnitTests (`tests/Avalonia.Controls.UnitTests/Avalonia.Controls.UnitTests.csproj`; net8.0) — tests Avalonia, Avalonia.Base, Avalonia.Controls, Avalonia.DesignerSupport, Avalonia.Dialogs, Avalonia.Headless, Avalonia.Markup, Avalonia.Markup.Xaml, Avalonia.Markup.Xaml.Loader, Avalonia.Metal, Avalonia.MicroCom, Avalonia.OpenGL, Avalonia.Remote.Protocol, Avalonia.Themes.Simple, Avalonia.Vulkan
- Avalonia.Base.UnitTests (`tests/Avalonia.Base.UnitTests/Avalonia.Base.UnitTests.csproj`; net8.0) — tests Avalonia, Avalonia.Base, Avalonia.Controls, Avalonia.DesignerSupport, Avalonia.Dialogs, Avalonia.Headless, Avalonia.Markup, Avalonia.Markup.Xaml, Avalonia.Markup.Xaml.Loader, Avalonia.Metal, Avalonia.MicroCom, Avalonia.OpenGL, Avalonia.Remote.Protocol, Avalonia.Themes.Simple, Avalonia.Vulkan
- **ControlCatalog** (`samples/ControlCatalog/ControlCatalog.csproj`; net8.0, netstandard2.0) → Avalonia, Avalonia.Base, Avalonia.Controls, Avalonia.Controls.ColorPicker, Avalonia.Controls.DataGrid, Avalonia.DesignerSupport, Avalonia.Dialogs, Avalonia.Fonts.Inter, Avalonia.Markup, Avalonia.Markup.Xaml, Avalonia.Metal, Avalonia.MicroCom, Avalonia.OpenGL, Avalonia.Remote.Protocol, Avalonia.Skia, Avalonia.Themes.Fluent, Avalonia.Themes.Simple, Avalonia.Vulkan, ControlSamples, MiniMvvm; 111 public types; ns ControlCatalog.Pages, ControlCatalog.ViewModels, ControlCatalog.Models
- Avalonia.IntegrationTests.Appium (`tests/Avalonia.IntegrationTests.Appium/Avalonia.IntegrationTests.Appium.csproj`; net8.0) — tests Avalonia.Base, Avalonia.Controls, Avalonia.Remote.Protocol
- Avalonia.Markup.Xaml.UnitTests (`tests/Avalonia.Markup.Xaml.UnitTests/Avalonia.Markup.Xaml.UnitTests.csproj`; net47, net8.0) — tests Avalonia, Avalonia.Base, Avalonia.Controls, Avalonia.DesignerSupport, Avalonia.Dialogs, Avalonia.Headless, Avalonia.Markup, Avalonia.Markup.Xaml, Avalonia.Markup.Xaml.Loader, Avalonia.Metal, Avalonia.MicroCom, Avalonia.OpenGL, Avalonia.Remote.Protocol, Avalonia.Themes.Simple, Avalonia.Vulkan
- **Avalonia.Controls.DataGrid** (`src/Avalonia.Controls.DataGrid/Avalonia.Controls.DataGrid.csproj`; net6.0, net8.0, netstandard2.0) → Avalonia.Base, Avalonia.Controls, Avalonia.Markup, Avalonia.Markup.Xaml, Avalonia.Remote.Protocol; 60 public types; ns Avalonia.Controls, Avalonia.Collections, Avalonia.Controls.Utils
- **Avalonia.Win32** (`src/Windows/Avalonia.Win32/Avalonia.Win32.csproj`; net6.0, net8.0, netstandard2.0) → Avalonia, Avalonia.Base, Avalonia.Controls, Avalonia.DesignerSupport, Avalonia.Dialogs, Avalonia.Markup, Avalonia.Markup.Xaml, Avalonia.Metal, Avalonia.MicroCom, Avalonia.OpenGL, Avalonia.Remote.Protocol, Avalonia.Vulkan; 46 public types; ns Avalonia.Win32.WinRT.Impl, Avalonia.Win32.DirectX.Impl, Avalonia.Win32.Interop
- **Avalonia.OpenGL** (`src/Avalonia.OpenGL/Avalonia.OpenGL.csproj`; net6.0, net8.0, netstandard2.0) → Avalonia.Base, Avalonia.Controls, Avalonia.Remote.Protocol; 38 public types; ns Avalonia.OpenGL, Avalonia.OpenGL.Egl, Avalonia.OpenGL.Features
- **Avalonia.Native** (`src/Avalonia.Native/Avalonia.Native.csproj`; net6.0, net8.0, netstandard2.0) → Avalonia, Avalonia.Base, Avalonia.Controls, Avalonia.DesignerSupport, Avalonia.Dialogs, Avalonia.Markup, Avalonia.Markup.Xaml, Avalonia.Metal, Avalonia.MicroCom, Avalonia.OpenGL, Avalonia.Remote.Protocol, Avalonia.Vulkan; 4 public types; ns Avalonia.Native.Interop.Impl, Avalonia.Native.Interop, Avalonia.Native
- … 57 more projects (not listed)

### Key public types (members abbreviated)
- Avalonia.Controls: `class ToolTip : ContentControl, IPopupHostProvider` (src/Avalonia.Controls/ToolTip.cs)
  static readonly AttachedProperty<object> TipProperty; static readonly AttachedProperty<bool> IsOpenProperty; static readonly AttachedProperty<PlacementMode> PlacementProperty; static readonly AttachedProperty<double> HorizontalOffsetProperty; static readonly AttachedProperty<double> VerticalOffsetProperty; static readonly AttachedProperty<int> ShowDelayProperty; static readonly AttachedProperty<int> BetweenShowDelayProperty; static readonly AttachedProperty<bool> ShowOnDisabledProperty; … +25
- Avalonia.Base: `class InputElement : Interactive, IInputElement` (src/Avalonia.Base/Input/InputElement.cs)
  static readonly StyledProperty<bool> FocusableProperty; static readonly StyledProperty<bool> IsEnabledProperty; static readonly DirectProperty<InputElement, bool> IsEffectivelyEnabledProperty; static readonly StyledProperty<Cursor> CursorProperty; static readonly DirectProperty<InputElement, bool> IsKeyboardFocusWithinProperty; static readonly DirectProperty<InputElement, bool> IsFocusedProperty; static readonly StyledProperty<bool> IsHitTestVisibleProperty; static readonly DirectProperty<InputElement, bool> IsPointerOverProperty; … +65
- ControlCatalog: `class ToolTipPage : UserControl` (samples/ControlCatalog/Pages/ToolTipPage.xaml.cs)
  ToolTipPage()
- Avalonia.Controls.DataGrid: `class DataGridCellPointerPressedEventArgs : EventArgs` (src/Avalonia.Controls.DataGrid/EventArgs.cs)
  DataGridCellPointerPressedEventArgs(DataGridCell cell, DataGridRow row, DataGridColumn column, PointerPressedEventArgs e); DataGridCell Cell { get; }; DataGridRow Row { get; }; DataGridColumn Column { get; }; PointerPressedEventArgs PointerPressedEventArgs { get; }
- Avalonia.Win32: `class Win32PlatformOptions` (src/Windows/Avalonia.Win32/Win32PlatformOptions.cs)
  bool OverlayPopups { get; set; }; IReadOnlyList<Win32RenderingMode> RenderingMode { get; set; }; IReadOnlyList<Win32CompositionMode> CompositionMode { get; set; }; float? WinUICompositionBackdropCornerRadius { get; set; }; bool ShouldRenderOnUIThread { get; set; }; IList<GlVersion> WglProfiles { get; set; }; IPlatformGraphics CustomPlatformGraphics { get; set; }; Win32DpiAwareness DpiAwareness { get; set; }
- Avalonia.OpenGL: `abstract class OpenGlControlBase : Control` (src/Avalonia.OpenGL/Controls/OpenGlControlBase.cs)
  protected GlVersion GlVersion { get; }; OpenGlControlBase(); protected override void OnDetachedFromVisualTree(VisualTreeAttachmentEventArgs e); protected override void OnAttachedToVisualTree(VisualTreeAttachmentEventArgs e); protected override void OnPropertyChanged(AvaloniaPropertyChangedEventArgs change); void InvalidateVisual(); void RequestNextFrameRendering(); protected virtual void OnOpenGlInit(GlInterface gl); … +3
- Avalonia.Native: `class AvaloniaNativePlatformOptions` (src/Avalonia.Native/AvaloniaNativePlatformExtensions.cs)
  IReadOnlyList<AvaloniaNativeRenderingMode> RenderingMode { get; set; }; bool OverlayPopups { get; set; }; string AvaloniaNativeLibraryPath { get; set; }; bool AppSandboxEnabled { get; set; }
- Avalonia.X11: `class X11PlatformOptions` (src/Avalonia.X11/X11Platform.cs)
  IReadOnlyList<X11RenderingMode> RenderingMode { get; set; }; bool OverlayPopups { get; set; }; bool UseDBusMenu { get; set; }; bool UseDBusFilePicker { get; set; }; bool? EnableIme { get; set; }; bool EnableInputFocusProxy { get; set; }; bool EnableSessionManagement { get; set; }; bool ShouldRenderOnUIThread { get; set; }; … +6
- Avalonia.Remote.Protocol: `abstract class PointerEventMessageBase : InputEventMessageBase` (src/Avalonia.Remote.Protocol/InputMessages.cs)
  double X { get; set; }; double Y { get; set; }
- RenderDemo: `class LineBoundsDemoControl : Control` (samples/RenderDemo/Controls/LineBoundsDemoControl.cs)
  LineBoundsDemoControl(); static readonly StyledProperty<double> AngleProperty; double Angle { get; set; }; override void Render(DrawingContext drawingContext)
- GpuInterop: `class D3D11DemoControl : DrawingSurfaceDemoBase` (samples/GpuInterop/D3DDemo/D3D11DemoControl.cs)
  protected override (bool success, string info) InitializeGraphicsResources(Compositor compositor, CompositionDrawingSurface surface, ICompositionGpuInterop interop); protected override void FreeGraphicsResources(); protected override bool SupportsDisco { get; }; protected override void RenderFrame(PixelSize pixelSize)
- Avalonia.Markup.Xaml: `class ControlTemplate : IControlTemplate` (src/Markup/Avalonia.Markup.Xaml/Templates/ControlTemplate.cs)
  object Content { get; set; }; Type TargetType { get; set; }; TemplateResult<Control> Build(TemplatedControl control)
- Avalonia.Skia: `interface ISkiaSharpApiLeaseFeature` (src/Skia/Avalonia.Skia/ISkiaSharpApiLeaseFeature.cs)
  ISkiaSharpApiLease Lease()
- Avalonia.ReactiveUI: `class ReactiveUserControl<TViewModel> : UserControl, IViewFor<TViewModel>` (src/Avalonia.ReactiveUI/ReactiveUserControl.cs)
  static readonly StyledProperty<TViewModel> ViewModelProperty; ReactiveUserControl(); TViewModel ViewModel { get; set; }; protected override void OnPropertyChanged(AvaloniaPropertyChangedEventArgs change)
- ControlCatalog.NetCore: `class EmbedSampleGtk : INativeDemoControl` (samples/ControlCatalog.NetCore/NativeControls/Gtk/EmbedSample.Gtk.cs)
  IPlatformHandle CreateControl(bool isSecond, IPlatformHandle parent, Func<IPlatformHandle> createDefault)
- Avalonia.Win32.Interoperability: `class WinFormsAvaloniaControlHost : Control` (src/Windows/Avalonia.Win32.Interoperability/WinForms/WinFormsAvaloniaControlHost.cs)
  WinFormsAvaloniaControlHost(); Control Content { get; set; }; protected override void OnHandleCreated(EventArgs e); protected override void OnHandleDestroyed(EventArgs e); protected override void Dispose(bool disposing); protected override void OnGotFocus(EventArgs e); protected override void OnResize(EventArgs e); protected override void OnPaint(PaintEventArgs e)
- Avalonia.Vulkan: `interface IVulkanContextExternalObjectsFeature` (src/Avalonia.Vulkan/IVulkanContextExternalObjectsFeature.cs)
  IReadOnlyList<string> SupportedImageHandleTypes { get; }; IReadOnlyList<string> SupportedSemaphoreTypes { get; }; byte[] DeviceUuid { get; }; byte[] DeviceLuid { get; }; CompositionGpuImportedImageSynchronizationCapabilities GetSynchronizationCapabilities(string imageHandleType); IVulkanExternalImage ImportImage(IPlatformHandle handle, PlatformGraphicsExternalImageProperties properties); IVulkanExternalSemaphore ImportSemaphore(IPlatformHandle handle)
- UnloadableAssemblyLoadContextPlug: `class TestControl : TemplatedControl` (samples/UnloadableAssemblyLoadContext/UnloadableAssemblyLoadContextPlug/TestControl.axaml.cs)
- Avalonia.Controls.ColorPicker: `class ColorSpectrum : TemplatedControl` (src/Avalonia.Controls.ColorPicker/ColorSpectrum/ColorSpectrum.cs)
  protected const string pcPressed; protected const string pcDarkSelector; protected const string pcLargeSelector; protected const string pcLightSelector; EventHandler<ColorChangedEventArgs> ColorChanged; ColorSpectrum(); protected override void OnApplyTemplate(TemplateAppliedEventArgs e); protected override void OnAttachedToVisualTree(VisualTreeAttachmentEventArgs e); … +29
- UnloadableAssemblyLoadContext: `class PlugTool` (samples/UnloadableAssemblyLoadContext/UnloadableAssemblyLoadContext/PlugTool.cs)
  AssemblyLoadContextH AssemblyLoadContextH; WeakReference Unload(); Control FindControl(string type)
- Avalonia.LinuxFramebuffer: `enum DrmConnectorType` (src/Linux/Avalonia.LinuxFramebuffer/DrmConnectorType.cs)
  None; VGA; DVI_I; DVI_D; … +13
- DevGenerators: `class GClass` (src/tools/DevGenerators/CompositionGenerator/Config.cs)
  string Name { get; set; }; string Inherits { get; set; }; string ChangesBase { get; set; }; string ServerBase { get; set; }; … +7
