## Repository map (from Roslyn, at the starting commit; declarations only)
Solution `Terminal.sln`, .NET SDK 7.0.200, 5 C# projects (1 test). Projects are listed most relevant to the issue first.

### Projects
- **Terminal.Gui** (`Terminal.Gui/Terminal.Gui.csproj`; net472, net7.0, netstandard2.1) → no project refs; 176 public types; ns Terminal.Gui, Unix.Terminal, Terminal.Gui.Graphs
- UnitTests (`UnitTests/UnitTests.csproj`; net7.0) — tests Terminal.Gui, UICatalog
- **UICatalog** (`UICatalog/UICatalog.csproj`; net7.0) → Terminal.Gui; 100 public types; ns UICatalog.Scenarios, UICatalog
- **ReactiveExample** (`ReactiveExample/ReactiveExample.csproj`; net7.0) → Terminal.Gui; 4 public types; ns ReactiveExample, ReactiveMarbles.ObservableEvents, Terminal.Gui
- **Example** (`Example/Example.csproj`; net7.0) → Terminal.Gui; 1 public types; ns (global)

### Key public types (members abbreviated)
- Terminal.Gui: `class TextField : View` (Terminal.Gui/Views/TextField.cs)
  bool Used { get; set; }; bool ReadOnly { get; set; }; Action<TextChangingEventArgs> TextChanging; Action<ustring> TextChanged; TextField(string text); TextField(); TextField(ustring text); TextField(int x, int y, int w, ustring text); … +34
- UICatalog: `class ASCIICustomButtonTest.ASCIICustomButton : Button` (UICatalog/Scenarios/ASCIICustomButton.cs)
  string Description { get; }; Action<ASCIICustomButton> PointerEnter; ASCIICustomButton(string text, Pos x, Pos y, int width, int height); ASCIICustomButton(string id, string text, Pos x, Pos y, int width, int height); override bool OnMouseEvent(MouseEvent mouseEvent); override bool OnEnter(View view); override bool OnLeave(View view)
- ReactiveExample: `class LoginViewModel : ReactiveObject` (ReactiveExample/LoginViewModel.cs)
  LoginViewModel(); ustring Username { get; set; }; ustring Password { get; set; }; int UsernameLength { get; }; int PasswordLength { get; }; ReactiveCommand<Unit, Unit> Login { get; }; ReactiveCommand<Unit, Unit> Clear { get; }; bool IsValid { get; }
- Example: `class ExampleWindow : Window` (Example/Example.cs)
  TextField usernameText; ExampleWindow()
- Terminal.Gui: `class ListView : View` (Terminal.Gui/Views/ListView.cs)
  IListDataSource Source { get; set; }; void SetSource(IList source); Task SetSourceAsync(IList source); bool AllowsMarking { get; set; }; bool AllowsMultipleSelection { get; set; }; int TopItem { get; set; }; int LeftItem { get; set; }; int Maxlength { get; }; … +32
- UICatalog: `class DynamicMenuBar.DynamicMenuBarDetails : FrameView` (UICatalog/Scenarios/DynamicMenuBar.cs)
  MenuItem _menuItem; TextField _txtTitle; TextField _txtHelp; TextView _txtAction; CheckBox _ckbIsTopLevel; CheckBox _ckbSubMenu; RadioGroup _rbChkStyle; TextField _txtShortcut; … +6
- ReactiveExample: `class TerminalScheduler : LocalScheduler` (ReactiveExample/TerminalScheduler.cs)
  static readonly TerminalScheduler Default; override IDisposable Schedule<TState>(TState state, TimeSpan dueTime, Func<IScheduler, TState, IDisposable> action)
- Terminal.Gui: `class TextFieldAutocomplete : Autocomplete` (Terminal.Gui/Views/TextField.cs)
  protected override void DeleteTextBackwards(); protected override string GetCurrentWord(int columnOffset); protected override void InsertText(string accepted)
- UICatalog: `class DynamicStatusBar.DynamicStatusBarDetails : FrameView` (UICatalog/Scenarios/DynamicStatusBar.cs)
  StatusItem _statusItem; TextField _txtTitle; TextView _txtAction; TextField _txtShortcut; DynamicStatusBarDetails(StatusItem statusItem); DynamicStatusBarDetails(ustring title); DynamicStatusItem EnterStatusItem(); void EditStatusItem(StatusItem statusItem); … +1
- ReactiveExample: `class LoginView : Window, IViewFor<LoginViewModel>` (ReactiveExample/LoginView.cs)
  LoginView(LoginViewModel viewModel); LoginViewModel ViewModel { get; set; }; protected override void Dispose(bool disposing)
- Terminal.Gui: `static class FakeConsole` (Terminal.Gui/ConsoleDrivers/FakeDriver/FakeConsole.cs)
  const int WIDTH; const int HEIGHT; static int WindowWidth { get; set; }; static bool IsOutputRedirected { get; }; static bool IsErrorRedirected { get; }; static TextReader In { get; }; static TextWriter Out { get; }; static TextWriter Error { get; }; … +82
- UICatalog: `class RunTExample.ExampleWindow : Window` (UICatalog/Scenarios/RunTExample.cs)
  TextField usernameText; ExampleWindow()
- ReactiveExample: `static class Program` (ReactiveExample/Program.cs)
- Terminal.Gui: `class View : Responder, ISupportInitializeNotification` (Terminal.Gui/Core/View.cs)
  Action<View> Added; Action<View> Removed; Action<FocusEventArgs> Enter; Action<FocusEventArgs> Leave; Action<MouseEventArgs> MouseEnter; Action<MouseEventArgs> MouseLeave; Action<MouseEventArgs> MouseClick; Action CanFocusChanged; … +139
- UICatalog: `class Scenario : IDisposable` (UICatalog/Scenario.cs)
  Window Win { get; set; }; virtual void Init(ColorScheme colorScheme); string GetName(); string GetDescription(); … +8
- Terminal.Gui: `abstract class ConsoleDriver` (Terminal.Gui/Core/ConsoleDriver.cs)
  protected Action TerminalResized; abstract int Cols { get; }; abstract int Rows { get; }; abstract int Left { get; }; abstract int Top { get; }; abstract IClipboard Clipboard { get; }; abstract bool EnableConsoleScrolling { get; set; }; abstract bool HeightAsBuffer { get; set; }; … +76
- UICatalog: `class DynamicMenuBar.DynamicMenuItem` (UICatalog/Scenarios/DynamicMenuBar.cs)
  ustring title; ustring help; ustring action; bool isTopLevel; … +6
- Terminal.Gui: `class FakeDriver : ConsoleDriver` (Terminal.Gui/ConsoleDrivers/FakeDriver/FakeDriver.cs)
  static Behaviors FakeBehaviors; override int Cols { get; }; override int Rows { get; }; override int Left { get; }; override int Top { get; }; override bool EnableConsoleScrolling { get; set; }; override bool HeightAsBuffer { get; set; }; override IClipboard Clipboard { get; }; … +32
- UICatalog: `class Animation.BitmapToBraille` (UICatalog/Scenarios/Animation.cs)
  const int CHAR_WIDTH; const int CHAR_HEIGHT; int WidthPixels { get; }; int HeightPixels { get; }; … +3
- Terminal.Gui: `class Responder : IDisposable` (Terminal.Gui/Core/Responder.cs)
  bool WasDisposed; int DisposedCount; static List<Responder> Instances; Responder(); virtual bool CanFocus { get; set; }; virtual bool HasFocus { get; }; virtual bool Enabled { get; set; }; virtual bool Visible { get; set; }; … +15
- UICatalog: `interface DynamicMenuBar.IValueConverter` (UICatalog/Scenarios/DynamicMenuBar.cs)
  object Convert(object value, object parameter)
- Terminal.Gui: `interface ITextValidateProvider` (Terminal.Gui/Views/TextValidateField.cs)
  bool Fixed { get; }; int Cursor(int pos); int CursorLeft(int pos); int CursorRight(int pos); int CursorStart(); int CursorEnd(); bool Delete(int pos); bool InsertAt(char ch, int pos); … +3
- UICatalog: `interface DynamicStatusBar.IValueConverter` (UICatalog/Scenarios/DynamicStatusBar.cs)
  object Convert(object value, object parameter)
- Terminal.Gui: `class ColorPicker : View` (Terminal.Gui/Views/ColorPicker.cs)
  Point Cursor { get; set; }; Action ColorChanged; Color SelectedColor { get; set; }; ColorPicker(); ColorPicker(ustring title); ColorPicker(Point point, ustring title); ColorPicker(int x, int y, ustring title); override void Redraw(Rect bounds); … +6
- UICatalog: `class DynamicMenuBar.DynamicMenuItemModel : INotifyPropertyChanged` (UICatalog/Scenarios/DynamicMenuBar.cs)
  PropertyChangedEventHandler PropertyChanged; ustring MenuBar { get; set; }; ustring Parent { get; set; }; List<DynamicMenuItemList> Menus { get; set; }; … +2
- Terminal.Gui: `class TextRegexProvider : ITextValidateProvider` (Terminal.Gui/Views/TextValidateField.cs)
  TextRegexProvider(string pattern); ustring Pattern { get; set; }; ustring Text { get; set; }; ustring DisplayText { get; }; bool IsValid { get; }; bool Fixed { get; }; bool ValidateOnInput { get; set; }; int Cursor(int pos); … +6
- UICatalog: `class DynamicStatusBar.DynamicStatusItem` (UICatalog/Scenarios/DynamicStatusBar.cs)
  ustring title; ustring action; ustring shortcut; DynamicStatusItem(); … +2
- Terminal.Gui: `class NetMaskedTextProvider : ITextValidateProvider` (Terminal.Gui/Views/TextValidateField.cs)
  NetMaskedTextProvider(string mask); ustring Mask { get; set; }; ustring Text { get; set; }; bool IsValid { get; }; bool Fixed { get; }; ustring DisplayText { get; }; int Cursor(int pos); int CursorStart(); … +5
- UICatalog: `class ListViewWithSelection : Scenario` (UICatalog/Scenarios/ListViewWithSelection.cs)
  CheckBox _customRenderCB; CheckBox _allowMarkingCB; CheckBox _allowMultipleCB; ListView _listView; … +2
- Terminal.Gui: `class TreeView<T> : View, ITreeView` (Terminal.Gui/Views/TreeView.cs)
  ITreeBuilder<T> TreeBuilder { get; set; }; TreeStyle Style { get; set; }; bool MultiSelect { get; set; }; int MaxDepth { get; set; }; bool AllowLetterBasedNavigation { get; set; }; T SelectedObject { get; set; }; Action<ObjectActivatedEventArgs<T>> ObjectActivated; Key ObjectActivationKey { get; set; }; … +62
- UICatalog: `class DynamicMenuBar.Binding` (UICatalog/Scenarios/DynamicMenuBar.cs)
  View Target { get; private set; }; View Source { get; private set; }; string SourcePropertyName { get; private set; }; string TargetPropertyName { get; private set; }; … +1
- Terminal.Gui: `enum MouseFlags` (Terminal.Gui/Core/Event.cs)
  Button1Pressed; Button1Released; Button1Clicked; Button1DoubleClicked; Button1TripleClicked; Button2Pressed; Button2Released; Button2Clicked; … +21
- UICatalog: `class DynamicMenuBar.DynamicMenuItemList` (UICatalog/Scenarios/DynamicMenuBar.cs)
  ustring Title { get; set; }; MenuItem MenuItem { get; set; }; DynamicMenuItemList(); DynamicMenuItemList(ustring title, MenuItem menuItem); … +1
- Terminal.Gui: `enum Curses.Event` (Terminal.Gui/ConsoleDrivers/CursesDriver/constants.cs)
  Button1Pressed; Button1Released; Button1Clicked; Button1DoubleClicked; Button1TripleClicked; Button2Pressed; Button2Released; Button2Clicked; … +19
- UICatalog: `class DynamicStatusBar.Binding` (UICatalog/Scenarios/DynamicStatusBar.cs)
  View Target { get; private set; }; View Source { get; private set; }; string SourcePropertyName { get; private set; }; string TargetPropertyName { get; private set; }; … +1
- Terminal.Gui: `class HexView : View` (Terminal.Gui/Views/HexView.cs)
  HexView(Stream source); HexView(); Action<KeyValuePair<long, byte>> Edited; Action<HexViewEventArgs> PositionChanged; Stream Source { get; set; }; long DisplayStart { get; set; }; override Rect Frame { get; set; }; override void Redraw(Rect bounds); … +14
- UICatalog: `class DynamicStatusBar.DynamicStatusItemList` (UICatalog/Scenarios/DynamicStatusBar.cs)
  ustring Title { get; set; }; StatusItem StatusItem { get; set; }; DynamicStatusItemList(); DynamicStatusItemList(ustring title, StatusItem statusItem); … +1
- Terminal.Gui: `class TextView : View` (Terminal.Gui/Views/TextView.cs)
  Action TextChanged; Action<ContentsChangedEventArgs> ContentsChanged; Action<Point> UnwrappedCursorPosition; IAutocomplete Autocomplete { get; protected set; }; TextView(Rect frame); TextView(); bool Used { get; set; }; override ustring Text { get; set; }; … +61
- UICatalog: `class DynamicStatusBar.DynamicStatusItemModel : INotifyPropertyChanged` (UICatalog/Scenarios/DynamicStatusBar.cs)
  PropertyChangedEventHandler PropertyChanged; ustring StatusBar { get; set; }; List<DynamicStatusItemList> Items { get; set; }; DynamicStatusItemModel(); … +1
