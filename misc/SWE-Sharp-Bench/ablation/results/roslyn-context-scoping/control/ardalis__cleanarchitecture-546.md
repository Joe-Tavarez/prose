## Repository overview (file tree and README, at the starting commit)
217 tracked files, 113 .cs files, 7 .csproj files.

### Project files
- `src/Clean.Architecture.Core/Clean.Architecture.Core.csproj`
- `src/Clean.Architecture.Infrastructure/Clean.Architecture.Infrastructure.csproj`
- `src/Clean.Architecture.SharedKernel/Clean.Architecture.SharedKernel.csproj`
- `src/Clean.Architecture.Web/Clean.Architecture.Web.csproj`
- `tests/Clean.Architecture.FunctionalTests/Clean.Architecture.FunctionalTests.csproj`
- `tests/Clean.Architecture.IntegrationTests/Clean.Architecture.IntegrationTests.csproj`
- `tests/Clean.Architecture.UnitTests/Clean.Architecture.UnitTests.csproj`

### Directories (files; .cs files), most relevant first
- `src/Clean.Architecture.Web/Api/` (3; 3 .cs)
- `src/Clean.Architecture.Web/ApiModels/` (2; 2 .cs)
- `src/Clean.Architecture.Web/` (123; 2 .cs)
- `src/Clean.Architecture.Web/wwwroot/` (60; 0 .cs)
- `src/Clean.Architecture.Web/Endpoints/` (33; 33 .cs)
- `src/Clean.Architecture.Web/Views/` (8; 0 .cs)
- `src/Clean.Architecture.Web/Pages/` (6; 2 .cs)
- `src/Clean.Architecture.Web/ViewModels/` (3; 3 .cs)
- `src/Clean.Architecture.Web/Controllers/` (2; 2 .cs)
- `src/Clean.Architecture.Web/Filters/` (1; 1 .cs)
- `src/Clean.Architecture.Web/Properties/` (1; 0 .cs)
- `src/Clean.Architecture.Core/ProjectAggregate/` (13; 13 .cs)
- `src/Clean.Architecture.Core/` (23; 1 .cs)
- `tests/Clean.Architecture.UnitTests/` (13; 2 .cs)
- `tests/Clean.Architecture.FunctionalTests/` (12; 1 .cs)
- `src/Clean.Architecture.Infrastructure/` (10; 4 .cs)
- `src/Clean.Architecture.SharedKernel/` (10; 5 .cs)
- `tests/Clean.Architecture.IntegrationTests/` (5; 0 .cs)
- `tests/Clean.Architecture.UnitTests/Core/` (9; 9 .cs)
- `src/Clean.Architecture.Infrastructure/Data/` (5; 5 .cs)
- `tests/Clean.Architecture.FunctionalTests/ApiEndpoints/` (5; 5 .cs)
- `src/Clean.Architecture.SharedKernel/Interfaces/` (4; 4 .cs)
- `tests/Clean.Architecture.IntegrationTests/Data/` (4; 4 .cs)
- `src/Clean.Architecture.Core/ContributorAggregate/` (3; 3 .cs)
- `src/Clean.Architecture.Core/Interfaces/` (3; 3 .cs)
- `tests/Clean.Architecture.FunctionalTests/ControllerApis/` (3; 3 .cs)
- `src/Clean.Architecture.Core/Services/` (2; 2 .cs)
- `tests/Clean.Architecture.FunctionalTests/ControllerViews/` (1; 1 .cs)
- `src/` (166; 0 .cs)
- `tests/` (30; 0 .cs)
- `.github/` (9; 0 .cs)
- `.template.config/` (1; 0 .cs)
- `.github/ISSUE_TEMPLATE/` (3; 0 .cs)
- `.github/workflows/` (3; 0 .cs)

### README.md (start)
 &nbsp;
# Clean Architecture
A starting point for Clean Architecture with ASP.NET Core. [Clean Architecture](https://8thlight.com/blog/uncle-bob/2012/08/13/the-clean-architecture.html) is just the latest in a series of names for the same loosely-coupled, dependency-inverted architecture. You will also find it named [hexagonal](http://alistair.cockburn.us/Hexagonal+architecture), [ports-and-adapters](http://www.dossier-andreas.net/software_architecture/ports_and_adapters.html), or [onion architecture](http://jeffreypalermo.com/blog/the-onion-architecture-part-1/).
This architecture is used in the [DDD Fundamentals course](https://www.pluralsight.com/courses/fundamentals-domain-driven-design) by [Steve Smith](https://ardalis.com) and [Julie Lerman](https://thedatafarm.com/). Contact Steve's company, [NimblePros](https://nimblepros.com/), for Clean Architecture or DDD training and/or implementation assistance for your team.
## Table Of Contents
- [Clean Architecture](#clean-architecture)
  * [Table Of Contents](#table-of-contents)
  * [Give a Star! :star:](#give-a-star-star)
  * [Now available as a project template](https://marketplace.visualstudio.com/items?itemName=GregTrevellick.CleanArchitecture)
  * [Versions](#versions)
  * [Learn More](#learn-more)
- [Getting Started](#getting-started)
  * [Using the Visual Studio Item Template](#using-the-visual-studio-item-template)
  * [Using the dotnet CLI template](#using-the-dotnet-cli-template)
  * [Using the GitHub Repository](#using-the-github-repository)
  * [Running Migrations](#running-migrations)
- [Goals](#goals)
  * [History and Shameless Plug Section](#history-and-shameless-plug-section)
- [Design Decisions and Dependencies](#design-decisions-and-dependencies)
  * [The Core Project](#the-core-project)
  * [The SharedKernel Project](#the-sharedkernel-project)
  * [The Infrastructure Project](#the-infrastructure-project)
  * [The Web Project](#the-web-project)
  * [The Test Projects](#the-test-projects)
- [Patterns Used](#patterns-used)
  * [Domain Events](#domain-events)
- [Related Projects](#related-projects)
## Give a Star! :star:
If you like or are using this project to learn or start your solution, please give it a star. Thanks!
Or if you're feeling really generous, we now support GitHub sponsorships - see the button above.
## *Now available as a [project template](https://marketplace.visualstudio.com/items?itemName=GregTrevellick.CleanArchitecture) within Visual Studio.*
## Versions
The master branch is now using .NET 7. If you need a previous version use one of these tagged commits:
- [6.0](https://github.com/ardalis/CleanArchitecture/releases/tag/dotnet-6)
- [5.0](https://github.com/ardalis/CleanArchitecture/releases/tag/dotnet-core-5)
- [3.1](https://github.com/ardalis/CleanArchitecture/tree/dotnet-core-3.1)
- [2.2](https://github.com/ardalis/CleanArchitecture/tree/dotnet-core-2.2)
- [2.0](https://github.com/ardalis/CleanArchitecture/tree/dotnet-core-2.0)
## Learn More
- [Live Stream Recordings Working on Clean Architecture](https://www.youtube.com/c/Ardalis/search?query=clean%20architecture)
- [DotNetRocks Podcast Discussion with Steve "ardalis" Smith](https://player.fm/series/net-rocks/clean-architecture-with-steve-smith)
- [Fritz and Friends Streaming Discussion with Steve "ardalis" Smith](https://www.youtube.com/watch?v=k8cZUW4MS3I)
# Getting Started
To use this template, there are a few options:
- Install using `dotnet new` (preferred - see below)
- [Install the Visual Studio Template](https://marketplace.visualstudio.com/items?itemName=GregTrevellick.CleanArchitecture) and use it within Visual Studio
- Download this Repository
These are all covered below.
## Using the Visual Studio Item Template
After installing the template, you should be able to create a new project in Visual Studio and search for Clean Architecture. You should see the template appear in your list of project templates:
After choosing this template, provide a project name and finish the project creation wizard. You should be all set.
Note that the template is generally only updated with major updates to the project. The GitHub repository will always have the latest bug fixes and enhancements.
## Using the dotnet CLI template
First, install the template from [NuGet (https://www.nuget.org/packages/Ardalis.CleanArchitecture.Template/)](https://www.nuget.org/packages/Ardalis.CleanArchitecture.Template/):
```powershell
dotnet new -i Ardalis.CleanArchitecture.Template
```
You should see the template in the list of templates from `dotnet new` after this install successfully. Look for "Steve Smith Clean Architecture" with Short Name of "clean-arch".
Navigate to the directory where you will put the new solution.
Run this command to create the solution structure in a subfolder name `Your.ProjectName`:
```
dotnet new clean-arch -o Your.ProjectName
```
The `Your.ProjectName` directory and solution file will be created, and inside that will be all of your new solution contents, properly namespaced and ready to run/test!
Example:
Thanks [@dahlsailrunner](https://github.com/dahlsailrunner) for your help getting this working!
> **Known Issue**: Don't include hyphens in the name. See [#201](https://github.com/ardalis/CleanArchitecture/issues/201).
## Using the GitHub Repository
To get started based on this repository, you need to get a copy locally. You have three options: fork, clone, or download. Most of the time, you probably just want to download.
You should **download the repository**, unblock the zip file, and extract it to a new folder if you just want to play with the project or you wish to use it as the starting point for an application.
You should **fork this repository** only if you plan on submitting a pull request. Or if you'd like to keep a copy of a snapshot of the repository in your own GitHub account.
You should **clone this repository** if you're one of the contributors and you have commit access to it. Otherwise you probably want one of the other options.
## Running Migrations
In Visual Studio, open the Package Manager Console, and run `Add-Migration InitialMigrationName -StartupProject Your.ProjectName.Web -Context AppDbContext -Project Your.ProjectName.Infrastructure`.
To use SqlServer, change `options.UseSqlite(connectionString));` to `options.UseSqlServer(connectionString));` in the `Your.ProjectName.Infrastructure.StartupSetup` file. Also remember to replace the `SqliteConnection` with `DefaultConnection` in the `Your.ProjectName.Web.Program` file, which points to your Database Server.
# Goals
The goal of this repository is to provide a basic solution structure that can be used to build Domain-Driven Design (DDD)-based or simply well-factored, SOLID applications using .NET Core. Learn more about these topics here:
- [SOLID Principles for C# Developers](https://www.pluralsight.com/courses/csharp-solid-principles)
- [SOLID Principles of Object Oriented Design](https://www.pluralsight.com/courses/principles-oo-design) (the original, longer course)
- [Domain-Driven Design Fundamentals](https://www.pluralsight.com/courses/domain-driven-design-fundamentals)
If you're used to building applications as single-project or as a set of projects that follow the traditional UI -> Business Layer -> Data Access Layer "N-Tier" architecture, I recommend you check out these two courses (ideally before DDD Fundamentals):
- [Creating N-Tier Applications in C#, Part 1](https://www.pluralsight.com/courses/n-tier-apps-part1)
- [Creating N-Tier Applications in C#, Part 2](https://www.pluralsight.com/courses/n-tier-csharp-part2)
I also maintain Microsoft's reference application, eShopOnWeb, and its associated free eBook. Check them out here:
- [eShopOnWeb on GitHub](https://github.com/dotnet-architecture/eShopOnWeb)
- [Architecting Modern Web Applications with ASP.NET Core and Microsoft Azure](https://aka.ms/webappebook) (eBook)
## History and Shameless Plug Section
I've used this starter kit to teach the basics of ASP.NET Core using Domain-Driven Design concepts and patterns for some time now (starting when ASP.NET Core was still in pre-release). Typically I teach a one- or two-day hands-on workshop ahead of events like DevIntersection, or private on-site workshops for companies looking to bring their teams up to speed with the latest development technologies and techniques. Feel free to [contact me](https://ardalis.com/contact-us) if you'd like information about upcoming workshops.
# Design Decisions and Dependencies
