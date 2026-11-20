## Repository overview (file tree and README, at the starting commit)
754 tracked files, 448 .cs files, 6 .csproj files.

### Project files
- `build/_build.csproj`
- `docs-src/CsvHelper.DocsGenerator/CsvHelper.DocsGenerator.csproj`
- `performance/CsvHelper.Performance/CsvHelper.Performance.csproj`
- `src/CsvHelper.Website/CsvHelper.Website.csproj`
- `src/CsvHelper/CsvHelper.csproj`
- `tests/CsvHelper.Tests/CsvHelper.Tests.csproj`

### Directories (files; .cs files), most relevant first
- `src/` (334; 0 .cs)
- `tests/` (242; 0 .cs)
- `docs/` (110; 0 .cs)
- `docs-src/` (23; 0 .cs)
- `logo/` (11; 0 .cs)
- `build/` (8; 2 .cs)
- `.github/` (4; 0 .cs)
- `.vscode/` (3; 0 .cs)
- `performance/` (3; 0 .cs)
- `.nuke/` (2; 0 .cs)
- `tests/CsvHelper.Tests/` (242; 38 .cs)
- `src/CsvHelper/` (199; 33 .cs)
- `src/CsvHelper.Website/` (135; 2 .cs)
- `docs/examples/` (37; 0 .cs)
- `docs/migration/` (30; 0 .cs)
- `docs/favicons/` (25; 0 .cs)
- `docs-src/CsvHelper.DocsGenerator/` (23; 7 .cs)
- `docs/styles/` (5; 0 .cs)
- `.github/ISSUE_TEMPLATE/` (4; 0 .cs)
- `performance/CsvHelper.Performance/` (3; 1 .cs)
- `docs/scripts/` (2; 0 .cs)
- `docs/api/` (1; 0 .cs)
- `docs/change-log/` (1; 0 .cs)
- `docs/getting-started/` (1; 0 .cs)
- `docs/images/` (1; 0 .cs)
- `src/CsvHelper.Website/input/` (122; 0 .cs)
- `tests/CsvHelper.Tests/Mappings/` (90; 90 .cs)
- `src/CsvHelper/Configuration/` (81; 81 .cs)
- `src/CsvHelper/TypeConversion/` (44; 44 .cs)
- `tests/CsvHelper.Tests/TypeConversion/` (27; 27 .cs)
- `tests/CsvHelper.Tests/Parsing/` (19; 19 .cs)
- `tests/CsvHelper.Tests/Writing/` (18; 18 .cs)
- `tests/CsvHelper.Tests/Reading/` (16; 16 .cs)
- `docs/examples/configuration/` (15; 0 .cs)
- `src/CsvHelper/Delegates/` (15; 15 .cs)
- `src/CsvHelper/Expressions/` (14; 14 .cs)
- `docs/examples/reading/` (8; 0 .cs)
- `docs-src/CsvHelper.DocsGenerator/Infos/` (7; 7 .cs)
- `tests/CsvHelper.Tests/AutoMapping/` (7; 7 .cs)
- `src/CsvHelper.Website/lib/` (6; 0 .cs)
- `docs-src/CsvHelper.DocsGenerator/Generators/` (5; 5 .cs)
- `docs/examples/writing/` (5; 0 .cs)
- `docs/examples/prerequisites/` (4; 0 .cs)
- `tests/CsvHelper.Tests/Mocks/` (4; 4 .cs)
- `docs-src/CsvHelper.DocsGenerator/Formatters/` (3; 3 .cs)
- `docs/examples/type-conversion/` (3; 0 .cs)
- `tests/CsvHelper.Tests/Async/` (2; 2 .cs)
- `tests/CsvHelper.Tests/Configuration/` (2; 2 .cs)
- `tests/CsvHelper.Tests/Exceptions/` (2; 2 .cs)
- `tests/CsvHelper.Tests/Issues/` (2; 2 .cs)
- `tests/CsvHelper.Tests/ObjectResolverTests/` (2; 2 .cs)
- `docs/examples/csvdatareader/` (1; 0 .cs)
- `docs/migration/v10/` (1; 0 .cs)
- `docs/migration/v11/` (1; 0 .cs)
- `docs/migration/v12/` (1; 0 .cs)
- `docs/migration/v13/` (1; 0 .cs)
- `docs/migration/v14/` (1; 0 .cs)
- `docs/migration/v15/` (1; 0 .cs)
- `docs/migration/v16/` (1; 0 .cs)
- `docs/migration/v17/` (1; 0 .cs)
- `docs/migration/v18/` (1; 0 .cs)
- `docs/migration/v19/` (1; 0 .cs)
- `docs/migration/v2/` (1; 0 .cs)
- `docs/migration/v20/` (1; 0 .cs)
- `docs/migration/v21/` (1; 0 .cs)
- `docs/migration/v22/` (1; 0 .cs)
- `docs/migration/v23/` (1; 0 .cs)
- `docs/migration/v24/` (1; 0 .cs)
- `docs/migration/v25/` (1; 0 .cs)
- `docs/migration/v26/` (1; 0 .cs)
- `docs/migration/v27/` (1; 0 .cs)
- `docs/migration/v28/` (1; 0 .cs)
- `docs/migration/v29/` (1; 0 .cs)
- `docs/migration/v3/` (1; 0 .cs)
- `docs/migration/v30/` (1; 0 .cs)
- `docs/migration/v4/` (1; 0 .cs)
- `docs/migration/v5/` (1; 0 .cs)
- `docs/migration/v6/` (1; 0 .cs)
- `docs/migration/v7/` (1; 0 .cs)
- `docs/migration/v8/` (1; 0 .cs)
- `docs/migration/v9/` (1; 0 .cs)
- `src/CsvHelper/Properties/` (1; 1 .cs)
- `tests/CsvHelper.Tests/Culture/` (1; 1 .cs)
- `tests/CsvHelper.Tests/DataTableTests/` (1; 1 .cs)
- `tests/CsvHelper.Tests/Defaults/` (1; 1 .cs)
- `tests/CsvHelper.Tests/Reflection/` (1; 1 .cs)

### README.markdown (start)
# CsvHelper
A library for reading and writing CSV files. Extremely fast, flexible, and easy to use. Supports reading and writing of custom class objects.
## Install
### Package Manager Console
```
PM> Install-Package CsvHelper
```
### .NET CLI Console
```
> dotnet add package CsvHelper
```
## Documentation
http://joshclose.github.io/CsvHelper/
### Building the Documentation
1. Install [node.js](https://nodejs.org/en/download/).
1. Go into the `CsvHelper/docs-src` folder.
1. Run `npm start` to start a local test site. Make any changes needed.
1. Run `npm run build` to build the documentation files that are output to `CsvHelper/docs`.
## License
Dual licensed
Microsoft Public License (MS-PL)
http://www.opensource.org/licenses/MS-PL
Apache License, Version 2.0
http://opensource.org/licenses/Apache-2.0
## Contributing
Want to contribute? Great! Here are a few guidelines.
1. If you want to do a feature, post an issue about the feature first. Some features are intentionally left out, some features may already be in the works, or I may have some advice on how I think it should be done. I would feel bad if time was spent on some code that won't be used.
2. If you want to do a bug fix, it might not be a bad idea to post about it too. I've had the same bug fixed by multiple people at the same time before.
3. All code should have a unit test. If you make a feature, there should be significant tests around the feature. If you do a bug fix, there should be a test specific to that bug so it doesn't happen again.
4. Pull requests should have a single commit. If you have multiple commits, squash them into a single commit before requesting a pull.
5. Try and follow the code styling already in place. If you have ReSharper there is a dotsettings file included and things should automatically be formatted for you.
## Credits
### Contributors
This project exists thanks to all the people who contribute. [[Contribute](CONTRIBUTING.md)].
### Backers
Thank you to all our backers! 🙏 [[Become a backer](https://opencollective.com/csvhelper#backer)]
### Sponsors
Support this project by becoming a sponsor. Your logo will show up here with a link to your website. [[Become a sponsor](https://opencollective.com/csvhelper#sponsor)]
