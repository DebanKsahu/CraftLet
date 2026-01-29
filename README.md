# CraftLet

**CraftLet** is a Python-based CLI (Command-Line Interface) tool designed to streamline project template management and initialization. It enables developers to quickly scaffold new projects from GitHub-hosted templates with minimal configuration overhead.

## Core Purpose

CraftLet automates the process of:
1. **Template Loading from GitHub** - Fetches project templates directly from GitHub repositories
2. **Local Template Caching** - Downloads and caches templates locally for offline use
3. **Dynamic Project Configuration** - Prompts users for configuration values based on a template configuration schema
4. **Interactive Plugin Selection** - Allows users to selectively enable/disable template plugins with rich UI
5. **Environment Variable Generation** - Automatically creates `.env` files with configured environment variables
6. **Template Instantiation** - Extracts and customizes template files into a target directory

## Key Features

- **GitHub Integration** - Converts GitHub repository URLs to downloadable zip archives using the Codeload API
- **Local Caching System** - Cache templates locally for offline access and faster loading
- **Interactive Configuration** - Uses Typer to create an interactive CLI that prompts users for required inputs
- **Plugin Configuration System** - Interactive selection of template plugins/modules with:
  - Rich terminal UI with navigation (arrow keys, space to toggle, enter to confirm)
  - Visual selection indicators and descriptions for each plugin
  - Automatic exclusion of unselected plugin files during template extraction
- **Template Configuration Schema** - Supports JSON-based `templateConfig.json` files that define:
  - User input prompts
  - Environment variable mappings
  - Nested configuration structures
  - Plugin definitions with module paths and descriptions
- **Asynchronous Operations** - Leverages async/await for efficient HTTP requests using httpx
- **Project Initialization** - Extracts template files while preserving directory structure and optionally generates environment configuration
- **Cross-Platform Support** - Works on multiple platforms with platform-aware caching

## Technology Stack

- **Framework** - Typer (modern CLI framework)
- **HTTP Client** - httpx (async HTTP client)
- **UI Library** - Rich (rich terminal formatting and interactive components)
- **Input Handling** - readchar (keyboard input for interactive selection)
- **Serialization** - cbor2 (CBOR encoding for cache storage)
- **Python Version** - 3.12+
- **Dependencies** - typer, httpx, cbor2, rich, readchar

## Architecture

- **CLI Module** (`src/craftlet/cli/CraftLetCLI.py`) - Command registration and user-facing CLI commands
- **Features Module** (`src/craftlet/features/`) - Core functionality including:
  - `CraftLet.py` - Template loading and extraction
  - `CraftLetCache.py` - Local caching system
  - `DirectoryTree.py` - Directory structure analysis
  - `ModuleDependencyGraph.py` - Module dependency tracking
  - `TemplatePluginConfiguration.py` - Interactive plugin selection
- **Models Module** (`src/craftlet/models/`) - Data models for cacheable objects, directory trees, and imports
- **Utils Module** (`src/craftlet/utils/`) - Helper functions including:
  - Configuration building and caching
  - URL mapping and hash utilities
  - **UI Submodule** (`ui/`) - Rich terminal UI components for interactive selection

## Project Structure

```
CraftLet/
├── DOCUMENT.md
├── pyproject.toml
├── README.md
├── src/
│   └── craftlet/
│       ├── main.py
│       ├── __pycache__/
│       ├── cli/
│       │   ├── CraftLetCLI.py
│       │   └── __pycache__/
│       ├── features/
│       │   ├── CraftLet.py
│       │   ├── CraftLetCache.py
│       │   ├── DirectoryTree.py
│       │   ├── ModuleDependencyGraph.py
│       │   ├── TemplatePluginConfiguration.py
│       │   └── __pycache__/
│       ├── models/
│       │   ├── Cacheable.py
│       │   ├── DirectoryTreeNode.py
│       │   ├── ImportItem.py
│       │   └── __pycache__/
│       └── utils/
│           ├── enums.py
│           ├── exceptions.py
│           ├── hashUtils.py
│           ├── helperFunctions.py
│           ├── mappers.py
│           ├── ui/
│           │   ├── CliRadioButton.py
│           │   └── __pycache__/
│           └── __pycache__/
├── craftlet.egg-info/
│   ├── dependency_links.txt
│   ├── entry_points.txt
│   ├── PKG-INFO
│   ├── requires.txt
│   ├── SOURCES.txt
│   └── top_level.txt
└── test/
    ├── astTest.py
    ├── directoryTreeTest.py
    └── temp.py
```

## Target Use Case

CraftLet is ideal for project maintainers who want to distribute boilerplate code/templates, allowing end-users to clone and customize templates without manual file editing or complex setup steps.

## Related Repositories

This project is part of the CraftLet ecosystem. For a complete solution, explore these related repositories:

- **[craftletKMP](https://github.com/DebanKsahu/craftletKMP)** - Frontend application built with Kotlin Multiplatform (KMP). Provides a user-friendly interface for template management and project creation.
- **[craftlet-server](https://github.com/DebanKsahu/CraftLet_Server)** - Backend API server. Handles template storage, user management, and provides services that the CLI utilizes for extended functionality.

The CraftLet CLI works in conjunction with these services to deliver a complete project templating and scaffolding solution.

## Installation

```bash
pip install -e .
```

## Usage

### Load a Template from GitHub

Load a template directly from a GitHub repository:

```bash
craftlet load-template --github
```

When prompted, provide:
- The GitHub repository URL for the template
- The desired project name

### Load a Cached Template

Load a template from your local cache:

```bash
craftlet load-template --local
```

When prompted, provide:
- The template source
- The template name
- The desired project name

### Generate Environment Variables

Add the `--generate-env` flag to any load command to automatically create an `.env` file:

```bash
craftlet load-template --github --generate-env
```

### Interactive Plugin Selection

When loading a template that includes plugin configurations in its `templateConfig.json`, CraftLet presents an interactive UI allowing you to select which plugins/modules to include in your project:

- **Navigation**: Use arrow keys (↑/↓) to navigate through available plugins
- **Selection**: Press Space to toggle plugin selection
- **Confirmation**: Press Enter to confirm your selections
- **Quit**: Press 'q' to cancel the operation

Each plugin displays:
- A visual selection indicator (✔ for selected, ○ for unselected)
- Plugin name and description
- Associated module paths that will be included/excluded

Selected plugins will be included in your project, while unselected plugins and their associated files will be automatically excluded during template extraction.

### Cache Management

#### Cache a Template

Download and cache a template for offline use:

```bash
craftlet cache-template https://github.com/username/template-repo
```

Cache only the template reference (metadata only):

```bash
craftlet cache-template https://github.com/username/template-repo --only-ref
```

#### View Cache Contents

Display the contents of your cache directory:

```bash
craftlet show-cache
```

View a specific folder in the cache:

```bash
craftlet show-cache offline/template
```

## Caching System

CraftLet includes a sophisticated caching system that allows you to store templates locally for offline access and faster loading:

### Cache Storage
- **Environment Cache**: When running in a virtual environment, cache is stored in the environment directory
- **User Cache**: When running globally, cache is stored in the user's OS-specific cache directory

### Cache Structure
```
.cache/
├── offline/
│   └── template/
│       └── [platform]/
│           └── [template-name]/
└── [other cache types]
```

### Benefits
- **Offline Access**: Use cached templates without internet connection
- **Faster Loading**: Skip download time for frequently used templates
- **Version Control**: Cache specific versions of templates
- **Reduced Bandwidth**: Avoid re-downloading the same templates
