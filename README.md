# CraftLet

**CraftLet** is a Python-based CLI (Command-Line Interface) tool designed to streamline project template management and initialization. It enables developers to quickly scaffold new projects from GitHub-hosted templates with minimal configuration overhead.

## Core Purpose

CraftLet automates the process of:
1. **Template Loading from GitHub** - Fetches project templates directly from GitHub repositories
2. **Local Template Caching** - Downloads and caches templates locally for offline use
3. **Dynamic Project Configuration** - Prompts users for configuration values based on a template configuration schema
4. **Environment Variable Generation** - Automatically creates `.env` files with configured environment variables
5. **Template Instantiation** - Extracts and customizes template files into a target directory

## Key Features

- **GitHub Integration** - Converts GitHub repository URLs to downloadable zip archives using the Codeload API
- **Local Caching System** - Cache templates locally for offline access and faster loading
- **Interactive Configuration** - Uses Typer to create an interactive CLI that prompts users for required inputs
- **Template Configuration Schema** - Supports JSON-based `templateConfig.json` files that define:
  - User input prompts
  - Environment variable mappings
  - Nested configuration structures
- **Asynchronous Operations** - Leverages async/await for efficient HTTP requests using httpx
- **Project Initialization** - Extracts template files while preserving directory structure and optionally generates environment configuration
- **Cross-Platform Support** - Works on multiple platforms with platform-aware caching

## Technology Stack

- **Framework** - Typer (modern CLI framework)
- **HTTP Client** - httpx (async HTTP client)
- **Serialization** - cbor2 (CBOR encoding for cache storage)
- **Python Version** - 3.12+
- **Dependencies** - typer, httpx, cbor2

## Architecture

- **CLI Module** (`src/craftlet/cli/CraftLetCLI.py`) - Command registration and user-facing CLI commands
- **Features Module** (`src/craftlet/features/`) - Core functionality including template loading and caching
- **Models Module** (`src/craftlet/models/`) - Data models for cacheable objects
- **Utils Module** (`src/craftlet/utils/`) - Helper functions for configuration building, caching, and URL mapping

## Target Use Case

CraftLet is ideal for project maintainers who want to distribute boilerplate code/templates, allowing end-users to clone and customize templates without manual file editing or complex setup steps.

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
