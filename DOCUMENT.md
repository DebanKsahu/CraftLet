# CraftLet CLI Documentation

Complete documentation of all CraftLet CLI functions with examples, parameters, and explanations.

---

## Table of Contents

1. [load-template](#load-template)
2. [show-cache](#show-cache)
3. [cache-template](#cache-template)
4. [Repository Format and Structure](#repository-format-and-structure)

---

## load-template

Load a project template from GitHub or local cache and initialize it in your current directory.

### Description

The `load-template` command fetches a GitHub repository template or loads a cached template and extracts it to a new project directory. It supports interactive prompts to gather necessary information and can optionally generate environment variable files.

### Command Syntax

```bash
craftlet load-template [OPTIONS] [LOCAL_PROFILE]
```

### Arguments

| Argument | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `LOCAL_PROFILE` | String | No | `None` | Profile name for loading from online profile cache |

### Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--github` | Boolean | `False` | Load the template from a GitHub repository URL |
| `--local` | Boolean | `False` | Load the template from local cache |
| `--generate-env` | Boolean | `False` | Generate a `.env` environment variable file with configured values |
| `--help` | - | - | Show help message |

### Behavior

- If `--github` is specified: Loads from GitHub repository
- If `--local` is specified: Loads from local cache
- If neither is specified: Defaults to GitHub mode

### Examples

#### Example 1: Basic Template Loading from GitHub

Load a template from GitHub and create a new project directory:

```bash
craftlet load-template --github
```

**Interactive Input:**
```
Enter Github Template Repo URL: https://github.com/myorg/react-template
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
Enter Github Template Repo URL: https://github.com/myorg/nodejs-template
Enter The Project Name: my-node-api
```

**Output:**
- Creates a new directory `my-node-api` in the current working directory
- Extracts template files
- Generates a `.env` file with all configured environment variables from the template configuration

---

#### Example 3: Load Template from Local Cache

Load a previously cached template:

```bash
craftlet load-template --local
```

**Interactive Input:**
```
Enter the source of template: github-templates
Enter The name of the template: react-template
Enter The Project Name: my-cached-app
```

**Output:**
- Creates a new directory `my-cached-app` in the current working directory
- Extracts the cached template files
- Processes configuration if available

---

#### Example 4: Load Template with Environment Variables from Cache

Load a cached template and generate environment variables:

```bash
craftlet load-template --local --generate-env
```

**Interactive Input:**
```
Enter the source of template: github-templates
Enter The name of the template: nodejs-api-template
Enter The Project Name: my-api-project
```

**Output:**
- Creates a new directory `my-api-project`
- Extracts cached template
- Generates `.env` file with configured variables

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

### Cache Structure

```
.cache/
├── offline/
│   └── template/
│       ├── {platform}/          # e.g., github-templates
│       │   └── {template-name}/
│       │       └── template.tar.gz
│       └── template-references/
│           └── {reference-name}/
│               └── reference.data
```

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

## Repository Format and Structure

CraftLet works with GitHub repositories that follow a specific template structure. This section describes the required and optional components that make a repository compatible with CraftLet.

### Basic Repository Structure

A CraftLet-compatible template repository should have the following structure:

```
my-template-repo/
├── templateConfig.json          # Optional: Configuration file
├── README.md                    # Recommended: Template documentation
├── .gitignore                   # Recommended: Git ignore rules
├── package.json                 # For Node.js projects
├── requirements.txt             # For Python projects
├── Dockerfile                   # For containerized projects
└── src/                         # Project source code
    ├── ...
    └── ...
```

### Template Configuration File (`templateConfig.json`)

The `templateConfig.json` file is **optional** but highly recommended for interactive template customization. It defines user prompts and environment variables.

#### Basic Structure

```json
{
  "projectName": {
    "prompt": "Enter your project name",
    "input": null,
    "isEnv": false
  },
  "database": {
    "host": {
      "prompt": "Database host",
      "input": null,
      "isEnv": true
    },
    "port": {
      "prompt": "Database port",
      "input": null,
      "isEnv": true
    }
  }
}
```

#### Configuration Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `prompt` | String | Yes | The text displayed to the user when prompting for input |
| `input` | Any | No | Initially `null`, replaced with user input during template loading |
| `isEnv` | Boolean | No | Whether this value should be written to `.env` file |

#### Example: Node.js API Template

```json
{
  "project": {
    "name": {
      "prompt": "What is your project name?",
      "input": null,
      "isEnv": false
    },
    "description": {
      "prompt": "Project description",
      "input": null,
      "isEnv": false
    }
  },
  "database": {
    "url": {
      "prompt": "Database connection URL",
      "input": null,
      "isEnv": true
    },
    "name": {
      "prompt": "Database name",
      "input": null,
      "isEnv": true
    }
  },
  "jwt": {
    "secret": {
      "prompt": "JWT secret key",
      "input": null,
      "isEnv": true
    }
  }
}
```

#### Example: React Application Template

```json
{
  "app": {
    "title": {
      "prompt": "Application title",
      "input": null,
      "isEnv": false
    },
    "port": {
      "prompt": "Development server port",
      "input": null,
      "isEnv": true
    }
  },
  "api": {
    "baseUrl": {
      "prompt": "API base URL",
      "input": null,
      "isEnv": true
    }
  }
}
```

### Environment Variable Generation

When using `--generate-env` flag, CraftLet automatically creates a `.env` file with all variables marked as `"isEnv": true`.

**Example Generated `.env`:**

```
DATABASE.URL=postgresql://localhost:5432/myapp
DATABASE.NAME=myapp_db
JWT.SECRET=my-secret-key
API.BASEURL=https://api.example.com
```

### Local Template Format

When caching templates locally, CraftLet stores them as compressed TAR archives (`.tar.gz` format). The local cache structure follows this pattern:

```
.cache/
├── offline/
│   └── template/
│       ├── github-templates/
│       │   ├── react-template/
│       │   │   └── template.tar.gz
│       │   └── nodejs-template/
│       │       └── template.tar.gz
│       └── template-references/
│           └── my-template-ref/
│               └── reference.data
```

**Local Template Contents:**
- `template.tar.gz`: Compressed archive containing all template files
- Original repository structure preserved inside the archive
- `templateConfig.json` included for configuration processing

### Repository Requirements

#### GitHub Repository Requirements

- **Public Access**: Repository must be publicly accessible
- **Main Branch**: Template files should be on the `main` branch (default)
- **Valid Structure**: Repository should contain valid project files

#### Template Best Practices

1. **Include Documentation**: Add a comprehensive `README.md` explaining the template
2. **Use Configuration**: Include `templateConfig.json` for user customization
3. **Environment Variables**: Mark sensitive configuration as environment variables
4. **Ignore Files**: Include appropriate `.gitignore` for the project type
5. **Dependencies**: Include dependency files (`package.json`, `requirements.txt`, etc.)

### Example Template Repositories

#### Example 1: Node.js REST API Template

```
nodejs-api-template/
├── templateConfig.json
├── package.json
├── README.md
├── .gitignore
├── src/
│   ├── app.js
│   ├── routes/
│   └── models/
├── tests/
└── docker/
    └── Dockerfile
```

**templateConfig.json:**
```json
{
  "project": {
    "name": {
      "prompt": "Project name",
      "input": null,
      "isEnv": false
    }
  },
  "server": {
    "port": {
      "prompt": "Server port",
      "input": null,
      "isEnv": true
    }
  },
  "database": {
    "url": {
      "prompt": "Database URL",
      "input": null,
      "isEnv": true
    }
  }
}
```

#### Example 2: React Frontend Template

```
react-app-template/
├── templateConfig.json
├── package.json
├── README.md
├── .gitignore
├── public/
│   ├── index.html
│   └── favicon.ico
├── src/
│   ├── App.js
│   ├── components/
│   └── utils/
└── .env.example
```

**templateConfig.json:**
```json
{
  "app": {
    "title": {
      "prompt": "Application title",
      "input": null,
      "isEnv": false
    }
  },
  "api": {
    "endpoint": {
      "prompt": "API endpoint URL",
      "input": null,
      "isEnv": true
    }
  }
}
```

#### Example 3: Python FastAPI Template

```
fastapi-template/
├── templateConfig.json
├── requirements.txt
├── README.md
├── .gitignore
├── main.py
├── app/
│   ├── __init__.py
│   ├── routes/
│   └── models/
└── tests/
```

**templateConfig.json:**
```json
{
  "project": {
    "name": {
      "prompt": "Project name",
      "input": null,
      "isEnv": false
    }
  },
  "database": {
    "url": {
      "prompt": "Database connection string",
      "input": null,
      "isEnv": true
    }
  },
  "security": {
    "secret_key": {
      "prompt": "Secret key for JWT",
      "input": null,
      "isEnv": true
    }
  }
}
```

### Creating Your Own Template

#### Step 1: Set Up Repository

1. Create a new GitHub repository
2. Add your project files and structure
3. Create a `templateConfig.json` file

#### Step 2: Test Template

```bash
# Test locally (if you have CraftLet installed)
craftlet load-template --github
# Enter your repository URL when prompted
```

#### Step 3: Document Template

Add a comprehensive `README.md` explaining:
- What the template provides
- Configuration options
- Setup instructions
- Usage examples

### Limitations

- **Branch Support**: Currently only supports `main` branch
- **Variable Substitution**: No template variable replacement in files yet
- **GitHub Only**: Currently only supports GitHub repositories
- **File Size**: Large repositories may take time to download

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
craftlet load-template --local
```

---

### Workflow 3: Template with Environment Setup

```bash
# 1. Load template with environment generation
craftlet load-template --github --generate-env

# 2. Follow prompts
Enter Github Template Repo URL: https://github.com/myorg/api-template
Enter The Project Name: my-api-server

# 3. .env file is automatically created with configured values
# 4. View generated .env
cat my-api-server/.env
```

---

### Workflow 4: Offline Development with Cached Templates

```bash
# 1. Cache templates when online
craftlet cache-template https://github.com/myorg/fastapi-template
craftlet cache-template https://github.com/myorg/react-dashboard

# 2. Work offline - load from cache
craftlet load-template --local --generate-env

# Interactive prompts:
# Enter the source of template: github-templates
# Enter The name of the template: fastapi-template
# Enter The Project Name: offline-api

# 3. Template loads from local cache without internet
```

---

## Tips and Best Practices

1. **Use `--generate-env` for API/Backend Templates**: Automatically sets up environment variables needed for development
2. **Cache Frequently Used Templates**: Improves project creation speed and enables offline usage with `--local` flag
3. **Keep Cache Organized**: Use `show-cache` regularly to manage cached templates and references
4. **Version Control**: Ensure `.env` files are added to `.gitignore` before committing
5. **Offline Development**: Cache templates when online, then use `--local` flag for offline development
6. **Template Sources**: When loading from cache, use descriptive source names (e.g., "github-templates", "company-templates")
7. **Reference vs Full Cache**: Use `--only-ref` for quick access to template metadata without storing full content

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

### Issue: Local Template Not Found

```bash
# Error: Template File doesn't exist
# Solution: 
# 1. Verify template was cached: craftlet show-cache
# 2. Check correct source name (e.g., "github-templates")
# 3. Ensure template.tar.gz exists in cache directory
```

### Issue: Local Profile Loading Not Working

```bash
# Note: local_profile argument is currently not fully implemented
# Use --local flag with interactive prompts instead
```

---

## Related Documentation

- [CraftLet Project Documentation](README.md)
- [CraftLet GitHub Repository](https://github.com)

