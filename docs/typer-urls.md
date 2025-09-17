# Typer Documentation Navigation Guide

Quick access to key Typer documentation sections for Claude development tasks.

## Essential URLs by Topic

### Core Concepts
- **Getting Started**: https://typer.tiangolo.com/tutorial/first-steps/
- **Arguments**: https://typer.tiangolo.com/tutorial/arguments/
- **Options**: https://typer.tiangolo.com/tutorial/options/
- **Commands**: https://typer.tiangolo.com/tutorial/commands/

### Organization & Structure
- **One File Per Command**: https://typer.tiangolo.com/tutorial/one-file-per-command/
- **Subcommands**: https://typer.tiangolo.com/tutorial/subcommands/
- **Building a Package**: https://typer.tiangolo.com/tutorial/package/

### Type System & Validation
- **Parameter Types**: https://typer.tiangolo.com/tutorial/parameter-types/
- **Enums**: https://typer.tiangolo.com/tutorial/parameter-types/enum/
- **Path Parameters**: https://typer.tiangolo.com/tutorial/parameter-types/path/
- **DateTime**: https://typer.tiangolo.com/tutorial/parameter-types/datetime/

### User Experience
- **Printing & Colors**: https://typer.tiangolo.com/tutorial/printing/
- **Progress Bars**: https://typer.tiangolo.com/tutorial/progressbar/
- **Prompts**: https://typer.tiangolo.com/tutorial/prompt/
- **Help Text**: https://typer.tiangolo.com/tutorial/options/help/

### Advanced Features
- **Multiple Values**: https://typer.tiangolo.com/tutorial/multiple-values/
- **Environment Variables**: https://typer.tiangolo.com/tutorial/options/envvar/
- **App Directory**: https://typer.tiangolo.com/tutorial/app-dir/
- **Launching Apps**: https://typer.tiangolo.com/tutorial/launch/

### Testing & Quality
- **Testing**: https://typer.tiangolo.com/tutorial/testing/
- **Exceptions**: https://typer.tiangolo.com/tutorial/exceptions/
- **Typer Command**: https://typer.tiangolo.com/tutorial/typer-command/

### Integration
- **Using Click**: https://typer.tiangolo.com/tutorial/using-click/

## Search Strategies

### When building CLI commands:
1. **Start with**: First Steps → Arguments → Options → Commands
2. **For validation**: Parameter Types → Enums/Path/DateTime
3. **For organization**: One File Per Command → Subcommands
4. **For UX**: Printing → Progress → Prompts

### When troubleshooting:
1. **Type errors**: Parameter Types documentation
2. **Validation issues**: Specific type documentation (Enum, Path, etc.)
3. **Help text**: Options/Help and Arguments documentation  
4. **Testing failures**: Testing documentation and CliRunner examples

### When adding features:
1. **Interactive input**: Prompts documentation
2. **File operations**: Path Parameters and App Directory
3. **Progress indication**: Progress Bars documentation
4. **Multiple inputs**: Multiple Values documentation

## Quick Pattern Lookup

### Need to...
- **Add a command**: Commands → One File Per Command
- **Validate input**: Parameter Types → Specific type docs
- **Get user input**: Prompts documentation
- **Show progress**: Progress Bars documentation
- **Handle files**: Path Parameters documentation
- **Add colors**: Printing documentation
- **Create tests**: Testing documentation
- **Package app**: Building a Package documentation
- **Add help**: Options/Help documentation
- **Handle errors**: Exceptions documentation

## Search Keywords for Documentation

### For specific features:
- "typer argument" - required positional parameters
- "typer option" - optional flag parameters  
- "typer enum" - choice validation
- "typer path" - file/directory validation
- "typer prompt" - interactive input
- "typer progress" - progress indicators
- "typer testing" - CliRunner and test patterns
- "typer subcommand" - nested command structure
- "typer help" - documentation and help text
- "typer environment variable" - env var integration

### For troubleshooting:
- "typer error" + error message
- "typer exception" + exception type
- "typer exit code" - exit handling
- "typer validation" - parameter validation
- "typer callback" - custom validation functions