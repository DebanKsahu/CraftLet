# CraftLet CLI Documentation

Complete documentation of all CraftLet CLI functions with examples, parameters, and explanations.

---

## Table of Contents

1. [load-template](#load-template)
2. [show-cache](#show-cache)
3. [cache-template](#cache-template)

---

## load-template

Load a project template from GitHub and initialize it in your current directory.

### Description

The `load-template` command fetches a GitHub repository template and extracts it to a new project directory. It supports interactive prompts to gather necessary information and can optionally generate environment variable files.

### Command Syntax

```bash
craftlet load-template [OPTIONS]
```

### Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--github` | Boolean | `False` | Load the template from a GitHub repository URL |
| `--generate-env` | Boolean | `False` | Generate a `.env` environment variable file with configured values |
| `--help` | - | - | Show help message |

### Parameters (Interactive Prompts)

When executing with `--github` flag, you will be prompted for:

1. **Template Repo URL** - The full GitHub repository URL (e.g., `https://github.com/owner/template-name`)
2. **Project Name** - The name of the project directory to create

### Examples

#### Example 1: Basic Template Loading

Load a template from GitHub and create a new project directory:

```bash
craftlet load-template --github
```

**Interactive Input:**
```
Enter Template Repo URL: https://github.com/myorg/react-template
Enter The Project Name: my-react-app
```

**Output:**
- Creates a new directory `my-react-app` in the current working directory
- Extracts all template files to the new directory
- Processes the template's `templateConfig.json` if present

---

#### Example 2: Template Loading with Environment Variables

Load a template and automatically generate a `.env` file:

```bash
craftlet load-template --github --generate-env
```

**Interactive Input:**
```
Enter Template Repo URL: https://github.com/myorg/nodejs-template
Enter The Project Name: my-node-api
```

**Output:**
- Creates a new directory `my-node-api` in the current working directory
- Extracts template files
- Generates a `.env` file with all configured environment variables from the template configuration

---

### How It Works

1. **Repository Fetch**: The command converts the GitHub URL to a Codeload API URL to download the repository as a ZIP archive
2. **Template Extraction**: The ZIP archive is extracted to the target project directory
3. **Configuration Processing**: If a `templateConfig.json` exists in the template, it prompts the user for required values
4. **Environment File Generation**: If `--generate-env` is enabled, creates a `.env` file with the configured environment variables

### Prerequisites

- Valid GitHub repository URL with a project template
- Write permissions in the current directory
- Internet connection to fetch from GitHub

---

## show-cache

Display the contents of the CraftLet template cache.

### Description

The `show-cache` command lists cached templates and template references stored on your system. This is useful for managing offline template repositories and seeing what templates are available for quick loading.

### Command Syntax

```bash
craftlet show-cache [SPECIFIC_FOLDER]
```

### Arguments

| Argument | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `SPECIFIC_FOLDER` | String | No | `""` (empty) | Relative path within the cache directory to inspect |

### Examples

#### Example 1: Show All Cached Templates

Display the complete cache structure:

```bash
craftlet show-cache
```

**Output:**
```
craftlet Cache Contents:
├── github-templates/
│   ├── react-template/
│   │   ├── name: react-template
│   │   ├── coreData: [bytes]
│   │   └── payload: {...}
│   └── nodejs-template/
│       ├── name: nodejs-template
│       └── ...
└── template-references/
    ├── my-template-ref/
    │   ├── name: my-template-ref
    │   └── ...
```

---

#### Example 2: Show Cache for Specific Folder

Display only templates in a specific subdirectory:

```bash
craftlet show-cache github-templates
```

**Output:**
```
craftlet Cache Contents for github-templates:
├── react-template/
│   ├── name: react-template
│   └── ...
└── nodejs-template/
    ├── name: nodejs-template
    └── ...
```

---

#### Example 3: Show Cache for Deeply Nested Path

Display contents of a specific template directory:

```bash
craftlet show-cache github-templates/react-template
```

**Output:**
```
craftlet Cache Contents for github-templates/react-template:
├── name: react-template
├── coreData: [bytes]
└── payload: {"ownerName": "myorg", "template_url": "..."}
```

---

### Cache Locations

The cache directory varies based on your environment:

- **Virtual Environment**: `{venv_path}/craftlet/.cache/`
- **System Installation**: OS-specific cache directory
  - **Windows**: `%APPDATA%\craftlet\.cache\`
  - **macOS**: `~/Library/Caches/craftlet/.cache/`
  - **Linux**: `~/.cache/craftlet/.cache/`

---

## cache-template

Cache a template locally for offline use or quick access.

### Description

The `cache-template` command downloads and stores a GitHub template repository in your local cache. This allows you to use templates without re-downloading them and enables offline template management. You can cache the entire template or just a reference to it.

### Command Syntax

```bash
craftlet cache-template <TEMPLATE_URL> [OPTIONS]
```

### Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `TEMPLATE_URL` | String | Yes | Full GitHub repository URL (e.g., `https://github.com/owner/template-name`) |

### Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--only-ref` | Boolean | `False` | Cache only the template reference metadata instead of the entire template |
| `--help` | - | - | Show help message |

### Examples

#### Example 1: Cache Complete Template

Download and store the entire template locally:

```bash
craftlet cache-template https://github.com/myorg/react-template
```

**Output:**
```
Template cached successfully!
Location: {cache_dir}/react-template
```

**What Gets Cached:**
- Complete repository ZIP file contents
- Metadata (owner name, template URL)
- Configuration files (templateConfig.json)
- All project files and directories

---

#### Example 2: Cache Template Reference Only

Cache only the metadata/reference to a template (minimal storage):

```bash
craftlet cache-template https://github.com/myorg/nodejs-template --only-ref
```

**Output:**
```
Template reference cached successfully!
Location: {cache_dir}/nodejs-template
```

**What Gets Cached:**
- Template name
- Template URL
- Owner information
- No actual template files (will be downloaded when needed)

---

#### Example 3: Cache Multiple Templates

Cache several templates sequentially:

```bash
craftlet cache-template https://github.com/myorg/react-template
craftlet cache-template https://github.com/myorg/vue-template
craftlet cache-template https://github.com/myorg/svelte-template
```

**Result:**
- All three templates are now cached and available offline
- Each can be loaded quickly without re-downloading from GitHub

---

### Supported Platforms

Currently, CraftLet supports caching from:

- **GitHub**: URLs starting with `https://github.com/`

Format: `https://github.com/{owner}/{repository}`

### Caching Strategies

#### Strategy 1: Cache Full Template (Recommended for Frequent Use)

```bash
craftlet cache-template https://github.com/myorg/my-template
```

**Pros:**
- Offline availability
- Faster template loading
- No network dependency

**Cons:**
- Higher disk space usage
- Templates become outdated if repository changes

---

#### Strategy 2: Cache Template Reference Only (Recommended for Storage)

```bash
craftlet cache-template https://github.com/myorg/my-template --only-ref
```

**Pros:**
- Minimal disk space usage
- Always up-to-date template metadata

**Cons:**
- Requires network access when loading
- Slower than full template cache

---

### Error Handling

#### Invalid URL Format

```bash
craftlet cache-template invalid-url
# Error: Unrecognized platform
```

**Solution**: Ensure the URL follows the format `https://github.com/owner/repository`

---

#### Network Errors

If the template cannot be downloaded (full cache):

```bash
# Error: Network connection failed
# Solution: Check internet connection and GitHub repository accessibility
```

---

### Cache Management

#### View Cached Templates

```bash
craftlet show-cache
```

#### Remove Cache (Manual)

Remove the cache directory manually:
- **Windows**: Delete `%APPDATA%\craftlet\.cache\`
- **macOS/Linux**: Delete `~/.cache/craftlet/.cache/`

---

## Common Workflows

### Workflow 1: Quick Start from GitHub Template

```bash
# 1. Load a template from GitHub
craftlet load-template --github

# 2. Follow interactive prompts
Enter Template Repo URL: https://github.com/myorg/starter-template
Enter The Project Name: my-new-project

# 3. Project is ready to use
cd my-new-project
npm install  # or your project's setup command
```

---

### Workflow 2: Setup Offline Templates for Team

```bash
# 1. Cache company templates locally
craftlet cache-template https://github.com/mycompany/react-template
craftlet cache-template https://github.com/mycompany/nodejs-template

# 2. View cached templates
craftlet show-cache

# 3. Team members can use templates offline
craftlet load-template --github
```

---

### Workflow 3: Template with Environment Setup

```bash
# 1. Load template with environment generation
craftlet load-template --github --generate-env

# 2. Follow prompts
Enter Template Repo URL: https://github.com/myorg/api-template
Enter The Project Name: my-api-server

# 3. .env file is automatically created with configured values
# 4. View generated .env
cat my-api-server/.env
```

---

## Tips and Best Practices

1. **Use `--generate-env` for API/Backend Templates**: Automatically sets up environment variables needed for development
2. **Cache Frequently Used Templates**: Improves project creation speed and works offline
3. **Keep Cache Organized**: Use `show-cache` regularly to manage cached templates
4. **Version Control**: Ensure `.env` files are added to `.gitignore` before committing
5. **Validate Templates**: Test templates before caching company-wide to ensure they work correctly

---

## Troubleshooting

### Issue: Template URL Not Found

```bash
# Error: Repository not found
# Solution: Verify GitHub URL is correct and repository is public
```

### Issue: Permission Denied When Creating Project

```bash
# Error: Cannot write to directory
# Solution: Check write permissions in current directory
```

### Issue: Cache Not Appearing

```bash
# run show-cache and check location
craftlet show-cache
# Check if cache directory exists at the displayed location
```

---

## Related Documentation

- [CraftLet Project Documentation](README.md)
- [CraftLet GitHub Repository](https://github.com)

