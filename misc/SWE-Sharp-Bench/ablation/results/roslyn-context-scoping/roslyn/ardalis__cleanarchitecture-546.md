## Repository map (from Roslyn, at the starting commit; declarations only)
Solution `Clean.Architecture.sln`, .NET SDK 9.0.100-rc.2.24474.11, 7 C# projects (3 test). Projects are listed most relevant to the issue first.

### Projects
- **Clean.Architecture.Web** (`src/Clean.Architecture.Web/Clean.Architecture.Web.csproj`; net7.0) → Clean.Architecture.Core, Clean.Architecture.Infrastructure, Clean.Architecture.SharedKernel; 49 public types; ns Clean.Architecture.Web.Endpoints.ProjectEndpoints, Clean.Architecture.Web.Endpoints.ContributorEndpoints, Clean.Architecture.Web.Api
- **Clean.Architecture.Core** (`src/Clean.Architecture.Core/Clean.Architecture.Core.csproj`; net7.0) → Clean.Architecture.SharedKernel; 22 public types; ns Clean.Architecture.Core.ProjectAggregate, Clean.Architecture.Core.ProjectAggregate.Specifications, Clean.Architecture.Core.Interfaces
- **Clean.Architecture.Infrastructure** (`src/Clean.Architecture.Infrastructure/Clean.Architecture.Infrastructure.csproj`; net7.0) → Clean.Architecture.Core, Clean.Architecture.SharedKernel; 9 public types; ns Clean.Architecture.Infrastructure, Clean.Architecture.Infrastructure.Data.Config, Clean.Architecture.Infrastructure.Data
- Clean.Architecture.FunctionalTests (`tests/Clean.Architecture.FunctionalTests/Clean.Architecture.FunctionalTests.csproj`; net7.0) — tests Clean.Architecture.Core, Clean.Architecture.Infrastructure, Clean.Architecture.SharedKernel, Clean.Architecture.Web
- Clean.Architecture.UnitTests (`tests/Clean.Architecture.UnitTests/Clean.Architecture.UnitTests.csproj`; net7.0) — tests Clean.Architecture.Core, Clean.Architecture.SharedKernel
- Clean.Architecture.IntegrationTests (`tests/Clean.Architecture.IntegrationTests/Clean.Architecture.IntegrationTests.csproj`; net7.0) — tests Clean.Architecture.Core, Clean.Architecture.Infrastructure, Clean.Architecture.SharedKernel
- **Clean.Architecture.SharedKernel** (`src/Clean.Architecture.SharedKernel/Clean.Architecture.SharedKernel.csproj`; net7.0) → no project refs; 9 public types; ns Clean.Architecture.SharedKernel, Clean.Architecture.SharedKernel.Interfaces

### Key public types (members abbreviated)
- Clean.Architecture.Web: `class CreateProjectDTO` (src/Clean.Architecture.Web/ApiModels/ProjectDTO.cs)
  protected CreateProjectDTO(string name); string Name { get; set; }
- Clean.Architecture.Core: `class ProjectsWithItemsByContributorIdSpec : Specification<Project>, ISingleResultSpecification` (src/Clean.Architecture.Core/ProjectAggregate/Specifications/ProjectsWithItemsByContributorId.cs)
  ProjectsWithItemsByContributorIdSpec(int contributorId)
- Clean.Architecture.Infrastructure: `class AppDbContext : DbContext` (src/Clean.Architecture.Infrastructure/Data/AppDbContext.cs)
  AppDbContext(DbContextOptions<AppDbContext> options, IDomainEventDispatcher dispatcher); DbSet<ToDoItem> ToDoItems { get; }; DbSet<Project> Projects { get; }; DbSet<Contributor> Contributors { get; }; protected override void OnModelCreating(ModelBuilder modelBuilder); override Task<int> SaveChangesAsync(CancellationToken cancellationToken); override int SaveChanges()
- Clean.Architecture.SharedKernel: `abstract class DomainEventBase : INotification` (src/Clean.Architecture.SharedKernel/DomainEventBase.cs)
  DateTime DateOccurred { get; protected set; }
- Clean.Architecture.Web: `class ProjectsController : BaseApiController` (src/Clean.Architecture.Web/Api/ProjectsController.cs)
  ProjectsController(IRepository<Project> repository); Task<IActionResult> List(); Task<IActionResult> GetById(int id); Task<IActionResult> Post(CreateProjectDTO request); Task<IActionResult> Complete(int projectId, int itemId)
- Clean.Architecture.Core: `enum ProjectStatus` (src/Clean.Architecture.Core/ProjectAggregate/ProjectStatus.cs)
  InProgress; Complete
- Clean.Architecture.Infrastructure: `class ProjectConfiguration : IEntityTypeConfiguration<Project>` (src/Clean.Architecture.Infrastructure/Data/Config/ProjectConfiguration.cs)
  void Configure(EntityTypeBuilder<Project> builder)
- Clean.Architecture.SharedKernel: `abstract class EntityBase` (src/Clean.Architecture.SharedKernel/EntityBase.cs)
  int Id { get; set; }; IEnumerable<DomainEventBase> DomainEvents { get; }; protected void RegisterDomainEvent(DomainEventBase domainEvent)
- Clean.Architecture.Web: `class ProjectListResponse` (src/Clean.Architecture.Web/Endpoints/ProjectEndpoints/List.ProjectListResponse.cs)
  List<ProjectRecord> Projects { get; set; }
- Clean.Architecture.Core: `class Project : EntityBase, IAggregateRoot` (src/Clean.Architecture.Core/ProjectAggregate/Project.cs)
  string Name { get; private set; }; IEnumerable<ToDoItem> Items { get; }; ProjectStatus Status { get; }; PriorityStatus Priority { get; }; Project(string name, PriorityStatus priority); void AddItem(ToDoItem newItem); void UpdateName(string newName)
- Clean.Architecture.Infrastructure: `class DefaultInfrastructureModule : Module` (src/Clean.Architecture.Infrastructure/DefaultInfrastructureModule.cs)
  DefaultInfrastructureModule(bool isDevelopment, Assembly callingAssembly); protected override void Load(ContainerBuilder builder)
- Clean.Architecture.SharedKernel: `abstract class ValueObject : IComparable, IComparable<ValueObject>` (src/Clean.Architecture.SharedKernel/ValueObject.cs)
  protected abstract IEnumerable<object> GetEqualityComponents(); override bool Equals(object obj); override int GetHashCode(); int CompareTo(object obj); … +3
- Clean.Architecture.Web: `class CreateProjectResponse` (src/Clean.Architecture.Web/Endpoints/ProjectEndpoints/Create.CreateProjectResponse.cs)
  CreateProjectResponse(int id, string name); int Id { get; set; }; string Name { get; set; }
- Clean.Architecture.Core: `class DeleteContributorService : IDeleteContributorService` (src/Clean.Architecture.Core/Services/DeleteContributorService.cs)
  DeleteContributorService(IRepository<Contributor> repository, IMediator mediator); Task<Result> DeleteContributor(int contributorId)
- Clean.Architecture.Infrastructure: `class FakeEmailSender : IEmailSender` (src/Clean.Architecture.Infrastructure/FakeEmailSender.cs)
  FakeEmailSender(ILogger<FakeEmailSender> logger); Task SendEmailAsync(string to, string from, string subject, string body)
- Clean.Architecture.SharedKernel: `interface IAggregateRoot` (src/Clean.Architecture.SharedKernel/Interfaces/IAggregateRoot.cs)
- Clean.Architecture.Web: `class DeleteProjectRequest` (src/Clean.Architecture.Web/Endpoints/ProjectEndpoints/Delete.DeleteProjectRequest.cs)
  const string Route; static string BuildRoute(int projectId); int ProjectId { get; set; }
- Clean.Architecture.Core: `interface IDeleteContributorService` (src/Clean.Architecture.Core/Interfaces/IDeleteContributorService.cs)
  Task<Result> DeleteContributor(int contributorId)
- Clean.Architecture.Infrastructure: `class SmtpEmailSender : IEmailSender` (src/Clean.Architecture.Infrastructure/SmtpEmailSender.cs)
  SmtpEmailSender(ILogger<SmtpEmailSender> logger); Task SendEmailAsync(string to, string from, string subject, string body)
- Clean.Architecture.SharedKernel: `interface IDomainEventDispatcher` (src/Clean.Architecture.SharedKernel/Interfaces/IDomainEventDispatcher.cs)
  Task DispatchAndClearEvents(IEnumerable<EntityBase> entitiesWithEvents)
- Clean.Architecture.Web: `class CreateProjectRequest` (src/Clean.Architecture.Web/Endpoints/ProjectEndpoints/Create.CreateProjectRequest.cs)
  const string Route; string Name { get; set; }
- Clean.Architecture.Core: `class ToDoItemSearchService : IToDoItemSearchService` (src/Clean.Architecture.Core/Services/ToDoItemSearchService.cs)
  ToDoItemSearchService(IRepository<Project> repository); Task<Result<List<ToDoItem>>> GetAllIncompleteItemsAsync(int projectId, string searchString); Task<Result<ToDoItem>> GetNextIncompleteItemAsync(int projectId)
- Clean.Architecture.Infrastructure: `class ContributorConfiguration : IEntityTypeConfiguration<Contributor>` (src/Clean.Architecture.Infrastructure/Data/Config/ContributorConfiguration.cs)
  void Configure(EntityTypeBuilder<Contributor> builder)
- Clean.Architecture.SharedKernel: `interface IReadRepository<T> : IReadRepositoryBase<T>` (src/Clean.Architecture.SharedKernel/Interfaces/IReadRepository.cs)
- Clean.Architecture.Web: `class GetProjectByIdResponse` (src/Clean.Architecture.Web/Endpoints/ProjectEndpoints/GetById.GetProjectByIdResponse.cs)
  GetProjectByIdResponse(int id, string name, List<ToDoItemRecord> items); int Id { get; set; }; string Name { get; set; }; List<ToDoItemRecord> Items { get; set; }
- Clean.Architecture.Core: `class IncompleteItemsSearchSpec : Specification<ToDoItem>` (src/Clean.Architecture.Core/ProjectAggregate/Specifications/IncompleteItemsSearchSpec.cs)
  IncompleteItemsSearchSpec(string searchString)
- Clean.Architecture.Infrastructure: `class EfRepository<T> : RepositoryBase<T>, IReadRepository<T>, IRepository<T>` (src/Clean.Architecture.Infrastructure/Data/EfRepository.cs)
  EfRepository(AppDbContext dbContext)
- Clean.Architecture.SharedKernel: `interface IRepository<T> : IRepositoryBase<T>` (src/Clean.Architecture.SharedKernel/Interfaces/IRepository.cs)
- Clean.Architecture.Web: `class CreateContributorResponse` (src/Clean.Architecture.Web/Endpoints/ContributorEndpoints/Create.CreateContributorResponse.cs)
  CreateContributorResponse(int id, string name); int Id { get; set; }; string Name { get; set; }
- Clean.Architecture.Core: `class ProjectByIdWithItemsSpec : Specification<Project>, ISingleResultSpecification` (src/Clean.Architecture.Core/ProjectAggregate/Specifications/ProjectByIdWithItemsSpec.cs)
  ProjectByIdWithItemsSpec(int projectId)
- Clean.Architecture.Infrastructure: `static class StartupSetup` (src/Clean.Architecture.Infrastructure/StartupSetup.cs)
  static void AddDbContext(this IServiceCollection services, string connectionString)
- Clean.Architecture.SharedKernel: `class DomainEventDispatcher : IDomainEventDispatcher` (src/Clean.Architecture.SharedKernel/DomainEventDispatcher.cs)
  DomainEventDispatcher(IMediator mediator); Task DispatchAndClearEvents(IEnumerable<EntityBase> entitiesWithEvents)
- Clean.Architecture.Web: `record ProjectRecord : IEquatable<ProjectRecord>` (src/Clean.Architecture.Web/Endpoints/ProjectEndpoints/ProjectRecord.cs)
  ProjectRecord(int Id, string Name); int Id { get; init; }; string Name { get; init; }
- Clean.Architecture.Core: `interface IToDoItemSearchService` (src/Clean.Architecture.Core/Interfaces/IToDoItemSearchService.cs)
  Task<Result<ToDoItem>> GetNextIncompleteItemAsync(int projectId); Task<Result<List<ToDoItem>>> GetAllIncompleteItemsAsync(int projectId, string searchString)
- Clean.Architecture.Infrastructure: `class ToDoConfiguration : IEntityTypeConfiguration<ToDoItem>` (src/Clean.Architecture.Infrastructure/Data/Config/ToDoConfiguration.cs)
  void Configure(EntityTypeBuilder<ToDoItem> builder)
- Clean.Architecture.SharedKernel: `class IgnoreMemberAttribute : Attribute` (src/Clean.Architecture.SharedKernel/IgnoreMemberAttribute.cs)
- Clean.Architecture.Web: `class UpdateProjectResponse` (src/Clean.Architecture.Web/Endpoints/ProjectEndpoints/Update.UpdateProjectResponse.cs)
  UpdateProjectResponse(ProjectRecord project); ProjectRecord Project { get; set; }
- Clean.Architecture.Core: `class Contributor : EntityBase, IAggregateRoot` (src/Clean.Architecture.Core/ContributorAggregate/Contributor.cs)
  string Name { get; private set; }; Contributor(string name); void UpdateName(string newName)
- Clean.Architecture.Web: `class CreateToDoItemRequest` (src/Clean.Architecture.Web/Endpoints/ProjectEndpoints/CreateToDoItem.CreateToDoItemRequest.cs)
  const string Route; static string BuildRoute(int projectId); int ProjectId { get; set; }; string Title { get; set; }; string Description { get; set; }; int? ContributorId { get; set; }
- Clean.Architecture.Core: `class NewItemAddedEvent : DomainEventBase` (src/Clean.Architecture.Core/ProjectAggregate/Events/NewItemAddedEvent.cs)
  ToDoItem NewItem { get; set; }; Project Project { get; set; }; NewItemAddedEvent(Project project, ToDoItem newItem)
- Clean.Architecture.Web: `class Create : Endpoint<CreateContributorRequest, CreateContributorResponse>` (src/Clean.Architecture.Web/Endpoints/ContributorEndpoints/Create.cs)
  Create(IRepository<Contributor> repository); override void Configure(); override Task HandleAsync(CreateContributorRequest request, CancellationToken cancellationToken)
- Clean.Architecture.Core: `class ToDoItem : EntityBase` (src/Clean.Architecture.Core/ProjectAggregate/ToDoItem.cs)
  string Title { get; set; }; string Description { get; set; }; int? ContributorId { get; private set; }; bool IsDone { get; private set; }; … +4
- Clean.Architecture.Web: `class Delete : Endpoint<DeleteContributorRequest>` (src/Clean.Architecture.Web/Endpoints/ContributorEndpoints/Delete.cs)
  Delete(IDeleteContributorService service); override void Configure(); override Task HandleAsync(DeleteContributorRequest request, CancellationToken cancellationToken)
