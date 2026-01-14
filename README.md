# CraftLet

**CraftLet** is a Python-based CLI (Command-Line Interface) tool designed to streamline project template management and initialization. It enables developers to quickly scaffold new projects from GitHub-hosted templates with minimal configuration overhead.

## Core Purpose

CraftLet automates the process of:
1. **Template Loading from GitHub** - Fetches project templates directly from GitHub repositories
2. **Dynamic Project Configuration** - Prompts users for configuration values based on a template configuration schema
3. **Environment Variable Generation** - Automatically creates `.env` files with configured environment variables
4. **Template Instantiation** - Extracts and customizes template files into a target directory

## Key Features

- **GitHub Integration** - Converts GitHub repository URLs to downloadable zip archives using the Codeload API
- **Interactive Configuration** - Uses Typer to create an interactive CLI that prompts users for required inputs
- **Template Configuration Schema** - Supports JSON-based `templateConfig.json` files that define:
  - User input prompts
  - Environment variable mappings
  - Nested configuration structures
- **Asynchronous Operations** - Leverages async/await for efficient HTTP requests using httpx
- **Project Initialization** - Extracts template files while preserving directory structure and optionally generates environment configuration

## Technology Stack

- **Framework** - Typer (modern CLI framework)
- **HTTP Client** - httpx (async HTTP client)
- **Python Version** - 3.12+
- **Dependencies** - typer, httpx

## Architecture

- **CLI Module** (`src/craftlet/cli/CraftLetCLI.py`) - Command registration and user-facing CLI commands
- **Feature Module** (`src/craftlet/feature/CraftLet.py`) - Core template loading and disk writing logic
- **Utils Module** (`src/craftlet/utils/`) - Helper functions for configuration building and URL mapping

## Target Use Case

CraftLet is ideal for project maintainers who want to distribute boilerplate code/templates, allowing end-users to clone and customize templates without manual file editing or complex setup steps.

## Related Repositories

This project is part of the CraftLet ecosystem. For a complete solution, explore these related repositories:

- **[craftletKMP](https://github.com/your-username/craftletKMP)** - Frontend application built with Kotlin Multiplatform (KMP). Provides a user-friendly interface for template management and project creation.
- **[craftlet-server](https://github.com/DebanKsahu/CraftLet_Server)** - Backend API server. Handles template storage, user management, and provides services that the CLI utilizes for extended functionality.

The CraftLet CLI works in conjunction with these services to deliver a complete project templating and scaffolding solution.

## Installation

```bash
pip install -e .
```

## Usage

Load a template from GitHub:

```bash
craftlet load-template --github
```

When prompted, provide:
- The GitHub repository URL for the template
- The desired project name

Optionally generate an `.env` file:

```bash
craftlet load-template --github --generate-env
```
