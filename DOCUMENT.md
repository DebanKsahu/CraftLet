# CraftLet CLI Documentation

Complete documentation of all CraftLet CLI functions with examples, parameters, and explanations.

---

## Table of Contents

1. [Writing templateConfig.json](#writing-templateconfigjson)
2. [load-template](#load-template)
3. [show-cache](#show-cache)
4. [cache-template](#cache-template)
5. [Repository Format and Structure](#repository-format-and-structure)
6. [Plugin System](#plugin-system)

---

## Writing templateConfig.json

The `templateConfig.json` file is the heart of CraftLet's template customization system. This section provides a comprehensive guide on how to create this file for your templates, explaining how CraftLet processes it and how each field works.

### Overview

The `templateConfig.json` file should be placed in the **root directory** of your template repository. When a user loads your template, CraftLet:

1. **Reads** the `templateConfig.json` file from the template
2. **Processes** configuration prompts and collects user input
3. **Builds** environment variables from fields marked with `isEnv: true`
4. **Displays** plugin selection UI if `ProjectPlugin` section exists
5. **Excludes** files/directories from unselected plugins
6. **Removes** the `templateConfig.json` file from the final project (it's not copied)

### File Location

```
your-template-repo/
├── templateConfig.json    ← Must be in root directory
├── src/
├── tests/
└── README.md
```

---

### Basic Structure

The `templateConfig.json` file consists of three main types of entries:

1. **Simple Configuration Fields** - Direct user input prompts
2. **Nested Configuration Groups** - Hierarchical configuration organization
3. **ProjectPlugin Section** - Optional module selection

```json
{
  "simpleField": {
    "prompt": "Enter a value",
    "input": null,
    "isEnv": false
  },
  "nestedGroup": {
    "field1": {
      "prompt": "Enter field 1",
      "input": null,
      "isEnv": true
    },
    "field2": {
      "prompt": "Enter field 2",
      "input": null,
      "isEnv": true
    }
  },
  "ProjectPlugin": {
    "PluginName": {
      "about": "Plugin description",
      "modulePath": [["path", "to", "module"]]
    }
  }
}
```

---

### Configuration Fields

#### Field Properties

Each configuration field (that's not a group or plugin) must have these properties:

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `prompt` | String | Yes | The question/prompt shown to the user |
| `input` | Any | Yes | Initially set to `null`. CraftLet fills this with user input |
| `isEnv` | Boolean | No | If `true`, adds this value to the `.env` file. Default: `false` |

#### How CraftLet Processes Fields

**Step 1: Field Detection**

CraftLet identifies a configuration field by checking if it has an `input` property:

```json
{
  "projectName": {
    "prompt": "What is your project name?",
    "input": null,     ← This marks it as a configuration field
    "isEnv": false
  }
}
```

**Step 2: User Prompting**

CraftLet displays the `prompt` to the user and waits for input:

```bash
What is your project name?: my-awesome-project
```

**Step 3: Value Storage**

The user's input replaces the `null` value:

```json
{
  "projectName": {
    "prompt": "What is your project name?",
    "input": "my-awesome-project",  ← Filled by user
    "isEnv": false
  }
}
```

**Step 4: Environment Variable Generation**

If `isEnv` is `true`, CraftLet adds this to the `.env` file:

```json
{
  "apiKey": {
    "prompt": "Enter your API key",
    "input": null,
    "isEnv": true    ← Will be added to .env
  }
}
```

Generates in `.env`:
```
APIKEY=user-provided-api-key
```

---

### Nested Configuration

#### How Nesting Works

CraftLet supports hierarchical configuration. Any object that **doesn't** have an `input` property is treated as a configuration group:

```json
{
  "database": {          ← This is a GROUP (no "input" property)
    "host": {            ← This is a FIELD (has "input" property)
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

#### Environment Variable Naming for Nested Fields

CraftLet generates environment variable names using **dot notation** and **uppercase**:

**Example Configuration:**
```json
{
  "database": {
    "connection": {
      "host": {
        "prompt": "Database host",
        "input": null,
        "isEnv": true
      }
    }
  }
}
```

**Generated Environment Variable Name:**
```
DATABASE.CONNECTION.HOST=localhost
```

#### Naming Rules

1. **Group names** are concatenated with dots (`.`)
2. **All letters** are converted to uppercase
3. **Spaces** are replaced with underscores (`_`)
4. **Top-level fields** have no prefix

**Examples:**

| JSON Path | Environment Variable Name |
|-----------|---------------------------|
| `apiKey` | `APIKEY` |
| `database.url` | `DATABASE.URL` |
| `email service.api key` | `EMAIL_SERVICE.API_KEY` |
| `app.security.jwt.secret` | `APP.SECURITY.JWT.SECRET` |

---

### Complete Field Examples

#### Example 1: Simple String Input

```json
{
  "projectName": {
    "prompt": "What is your project name?",
    "input": null,
    "isEnv": false
  }
}
```

**User Experience:**
```bash
What is your project name?: my-project
```

**Result:** Value stored but NOT added to `.env` (since `isEnv` is false)

---

#### Example 2: API Key (Environment Variable)

```json
{
  "apiKey": {
    "prompt": "Enter your API key",
    "input": null,
    "isEnv": true
  }
}
```

**User Experience:**
```bash
Enter your API key: sk-1234567890abcdef
```

**Generated `.env`:**
```
APIKEY=sk-1234567890abcdef
```

---

#### Example 3: Nested Database Configuration

```json
{
  "database": {
    "host": {
      "prompt": "Database host (e.g., localhost)",
      "input": null,
      "isEnv": true
    },
    "port": {
      "prompt": "Database port (e.g., 5432)",
      "input": null,
      "isEnv": true
    },
    "name": {
      "prompt": "Database name",
      "input": null,
      "isEnv": true
    },
    "credentials": {
      "username": {
        "prompt": "Database username",
        "input": null,
        "isEnv": true
      },
      "password": {
        "prompt": "Database password",
        "input": null,
        "isEnv": true
      }
    }
  }
}
```

**User Experience:**
```bash
Database host (e.g., localhost): localhost
Database port (e.g., 5432): 5432
Database name: myapp_db
Database username: admin
Database password: secret123
```

**Generated `.env`:**
```
DATABASE.HOST=localhost
DATABASE.PORT=5432
DATABASE.NAME=myapp_db
DATABASE.CREDENTIALS.USERNAME=admin
DATABASE.CREDENTIALS.PASSWORD=secret123
```

---

### ProjectPlugin Section

The `ProjectPlugin` section is **special** and **optional**. It enables users to select which optional modules to include in their project.

#### Structure

```json
{
  "ProjectPlugin": {
    "PluginName": {
      "about": "Description of the plugin",
      "modulePath": [
        ["path", "segment1", "segment2"],
        ["another", "path"]
      ]
    }
  }
}
```

#### Plugin Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `about` | String | No | Description shown in the selection UI (default: "No Description") |
| `modulePath` | Array of Arrays | Yes | List of file/directory paths to exclude if plugin is not selected |

#### How CraftLet Processes Plugins

**Step 1: Plugin Detection**

CraftLet looks for a top-level `ProjectPlugin` key in the configuration.

**Step 2: Interactive UI Display**

If plugins are found, CraftLet displays a rich terminal UI:

```
┌─ Project Plugin Options ──────────────────────────┐
│                                                    │
│  1.  ✔  Authentication    │ ┌─ About ──────────┐ │
│  2.  ✔  Admin Panel       │ │ JWT-based auth   │ │
│  3.  ○  Email Service     │ │ with login/      │ │
│                            │ │ register APIs    │ │
│                            │ └──────────────────┘ │
└──────── ↑/↓ move • Space toggle • Enter confirm ──┘
```

**Step 3: Path Exclusion**

When extracting the template, CraftLet **skips** all files/directories in the `modulePath` of **unselected** plugins.

#### Module Path Format

Paths are specified as **arrays of path segments**:

```json
"modulePath": [
  ["src", "auth"],              // Represents: src/auth/
  ["tests", "test_auth.py"],    // Represents: tests/test_auth.py
  ["config", "auth.json"]       // Represents: config/auth.json
]
```

**Why arrays?** This ensures cross-platform compatibility (Windows vs Unix paths).

---

### Complete Real-World Examples

#### Example 1: Node.js REST API Template

```json
{
  "project": {
    "name": {
      "prompt": "Project name",
      "input": null,
      "isEnv": false
    },
    "description": {
      "prompt": "Project description",
      "input": null,
      "isEnv": false
    }
  },
  "server": {
    "port": {
      "prompt": "Server port (default: 3000)",
      "input": null,
      "isEnv": true
    },
    "host": {
      "prompt": "Server host (default: localhost)",
      "input": null,
      "isEnv": true
    }
  },
  "database": {
    "type": {
      "prompt": "Database type (postgres/mysql/mongodb)",
      "input": null,
      "isEnv": true
    },
    "url": {
      "prompt": "Database connection URL",
      "input": null,
      "isEnv": true
    }
  },
  "auth": {
    "jwt": {
      "secret": {
        "prompt": "JWT secret key",
        "input": null,
        "isEnv": true
      },
      "expiration": {
        "prompt": "JWT token expiration (e.g., 24h)",
        "input": null,
        "isEnv": true
      }
    }
  },
  "ProjectPlugin": {
    "Authentication": {
      "about": "JWT-based authentication with login/register/logout endpoints",
      "modulePath": [
        ["src", "auth"],
        ["src", "middleware", "auth.js"],
        ["tests", "auth.test.js"]
      ]
    },
    "User Management": {
      "about": "User CRUD operations with role-based access control",
      "modulePath": [
        ["src", "users"],
        ["tests", "users.test.js"]
      ]
    },
    "File Upload": {
      "about": "Multer-based file upload with S3 integration",
      "modulePath": [
        ["src", "upload"],
        ["src", "middleware", "upload.js"]
      ]
    },
    "Email Notifications": {
      "about": "Nodemailer email service with templates",
      "modulePath": [
        ["src", "email"],
        ["templates", "email"]
      ]
    }
  }
}
```

**Generated `.env` (with example inputs):**
```
SERVER.PORT=3000
SERVER.HOST=localhost
DATABASE.TYPE=postgres
DATABASE.URL=postgresql://user:pass@localhost:5432/mydb
AUTH.JWT.SECRET=my-super-secret-key-123
AUTH.JWT.EXPIRATION=24h
```

---

#### Example 2: Python Flask Application

```json
{
  "app": {
    "name": {
      "prompt": "Application name",
      "input": null,
      "isEnv": false
    },
    "environment": {
      "prompt": "Environment (development/production)",
      "input": null,
      "isEnv": true
    }
  },
  "flask": {
    "secret_key": {
      "prompt": "Flask secret key",
      "input": null,
      "isEnv": true
    },
    "debug": {
      "prompt": "Enable debug mode? (true/false)",
      "input": null,
      "isEnv": true
    }
  },
  "database": {
    "uri": {
      "prompt": "SQLAlchemy database URI",
      "input": null,
      "isEnv": true
    }
  },
  "ProjectPlugin": {
    "SQLAlchemy ORM": {
      "about": "Database ORM with models and migrations",
      "modulePath": [
        ["app", "models"],
        ["migrations"]
      ]
    },
    "Flask-Login": {
      "about": "User session management",
      "modulePath": [
        ["app", "auth"],
        ["app", "templates", "auth"]
      ]
    },
    "REST API": {
      "about": "RESTful API with Flask-RESTful",
      "modulePath": [
        ["app", "api"],
        ["app", "schemas"]
      ]
    },
    "Admin Dashboard": {
      "about": "Flask-Admin dashboard for data management",
      "modulePath": [
        ["app", "admin"],
        ["app", "templates", "admin"],
        ["app", "static", "admin"]
      ]
    }
  }
}
```

**Generated `.env`:**
```
APP.ENVIRONMENT=development
FLASK.SECRET_KEY=random-secret-key-here
FLASK.DEBUG=true
DATABASE.URI=postgresql://localhost/myapp
```

---

#### Example 3: React Frontend Application

```json
{
  "app": {
    "title": {
      "prompt": "Application title",
      "input": null,
      "isEnv": false
    },
    "port": {
      "prompt": "Development server port (default: 3000)",
      "input": null,
      "isEnv": true
    }
  },
  "api": {
    "baseUrl": {
      "prompt": "API base URL (e.g., http://localhost:8000)",
      "input": null,
      "isEnv": true
    },
    "timeout": {
      "prompt": "API request timeout in ms (default: 10000)",
      "input": null,
      "isEnv": true
    }
  },
  "ProjectPlugin": {
    "Redux Toolkit": {
      "about": "State management with Redux Toolkit",
      "modulePath": [
        ["src", "store"],
        ["src", "features"]
      ]
    },
    "React Router": {
      "about": "Client-side routing",
      "modulePath": [
        ["src", "routes"],
        ["src", "pages"]
      ]
    },
    "Material-UI": {
      "about": "Material Design component library",
      "modulePath": [
        ["src", "theme"],
        ["src", "components", "mui"]
      ]
    },
    "Authentication": {
      "about": "User login/logout with JWT tokens",
      "modulePath": [
        ["src", "auth"],
        ["src", "components", "Login.jsx"],
        ["src", "components", "ProtectedRoute.jsx"]
      ]
    }
  }
}
```

**Generated `.env`:**
```
APP.PORT=3000
API.BASEURL=http://localhost:8000
API.TIMEOUT=10000
```

---

### Best Practices

#### 1. Clear and Descriptive Prompts

❌ **Bad:**
```json
{
  "db": {
    "prompt": "DB",
    "input": null,
    "isEnv": true
  }
}
```

✅ **Good:**
```json
{
  "database_url": {
    "prompt": "Database connection URL (e.g., postgresql://user:pass@host:5432/dbname)",
    "input": null,
    "isEnv": true
  }
}
```

#### 2. Provide Examples in Prompts

```json
{
  "api_key": {
    "prompt": "API Key (e.g., sk-1234567890abcdef)",
    "input": null,
    "isEnv": true
  }
}
```

#### 3. Use Logical Grouping

Group related configuration together:

```json
{
  "email": {
    "smtp_host": { "prompt": "...", "input": null, "isEnv": true },
    "smtp_port": { "prompt": "...", "input": null, "isEnv": true },
    "username": { "prompt": "...", "input": null, "isEnv": true },
    "password": { "prompt": "...", "input": null, "isEnv": true }
  }
}
```

#### 4. Mark Sensitive Data as Environment Variables

Always set `isEnv: true` for:
- API keys
- Passwords
- Secret keys
- Database credentials
- Any sensitive configuration

#### 5. Use Clear Plugin Descriptions

```json
"ProjectPlugin": {
  "Authentication": {
    "about": "JWT authentication with login/register/logout and password reset",
    "modulePath": [["src", "auth"]]
  }
}
```

#### 6. Include All Related Files in Plugin Paths

Don't forget tests, configuration, and related files:

```json
"Authentication": {
  "about": "User authentication system",
  "modulePath": [
    ["src", "auth"],              // Main code
    ["tests", "test_auth.py"],    // Tests
    ["config", "auth.yaml"],      // Config
    ["docs", "auth.md"]           // Documentation
  ]
}
```

---

### Common Patterns

#### Pattern 1: Database Configuration

```json
{
  "database": {
    "url": {
      "prompt": "Database connection URL",
      "input": null,
      "isEnv": true
    },
    "pool_size": {
      "prompt": "Connection pool size (default: 10)",
      "input": null,
      "isEnv": true
    }
  }
}
```

#### Pattern 2: API Configuration

```json
{
  "api": {
    "key": {
      "prompt": "API Key",
      "input": null,
      "isEnv": true
    },
    "endpoint": {
      "prompt": "API Endpoint URL",
      "input": null,
      "isEnv": true
    }
  }
}
```

#### Pattern 3: Authentication Configuration

```json
{
  "auth": {
    "jwt_secret": {
      "prompt": "JWT Secret Key",
      "input": null,
      "isEnv": true
    },
    "token_expiration": {
      "prompt": "Token expiration time (e.g., 24h, 7d)",
      "input": null,
      "isEnv": true
    }
  }
}
```

---

### Testing Your templateConfig.json

1. **Validate JSON Syntax**: Use a JSON validator to ensure proper formatting
2. **Test Prompts**: Load your template and verify all prompts appear correctly
3. **Check Environment Variables**: Verify `.env` file contains expected variables with correct names
4. **Test Plugin Selection**: Ensure unselected plugins are properly excluded
5. **Test Nested Structures**: Verify nested configuration generates correct environment variable names

---

### Troubleshooting

#### Issue: Prompt Not Appearing

**Cause**: Missing `input` property or incorrect nesting

**Solution**: Ensure every field that should prompt has an `input` property:
```json
{
  "myField": {
    "prompt": "Enter value",
    "input": null,    ← Must be present
    "isEnv": false
  }
}
```

#### Issue: Environment Variable Not Generated

**Cause**: `isEnv` not set to `true` or `--generate-env` flag not used

**Solution**:
1. Set `"isEnv": true` in the field
2. Use `craftlet load-template --github --generate-env`

#### Issue: Plugin Not Excluding Files

**Cause**: Incorrect path format in `modulePath`

**Solution**: Use array format, not string:

❌ **Wrong:**
```json
"modulePath": ["src/auth"]
```

✅ **Correct:**
```json
"modulePath": [["src", "auth"]]
```

---

## load-template

Load a project template from GitHub or local cache and initialize it in your current directory.

### Description

The `load-template` command fetches a GitHub repository template or loads a cached template and extracts it to a new project directory. It supports interactive prompts to gather necessary information, allows selection of optional plugins/modules, and can optionally generate environment variable files.

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
2. **Configuration Processing**: If a `templateConfig.json` exists in the template, it prompts the user for required values
3. **Plugin Selection**: If the template defines plugins in `ProjectPlugin` section, displays an interactive menu for selecting which modules to include
4. **Template Extraction**: The ZIP archive is extracted to the target project directory, excluding unselected plugin modules
5. **Environment File Generation**: If `--generate-env` is enabled, creates a `.env` file with the configured environment variables

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
  },
  "ProjectPlugin": {
    "Authentication": {
      "about": "JWT-based authentication module",
      "modulePath": [["src", "auth"], ["tests", "auth_tests.py"]]
    },
    "Admin Dashboard": {
      "about": "Admin panel with user management",
      "modulePath": [["src", "admin"], ["static", "admin"]]
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

## Plugin System

CraftLet includes a powerful plugin system that allows template creators to define optional modules or features that users can selectively include in their projects. This enables flexible, modular templates that can be customized during initialization.

### Overview

The plugin system provides:
- **Interactive Selection UI**: Rich terminal interface with keyboard navigation
- **Module Exclusion**: Unselected plugins are automatically excluded from the generated project
- **Descriptions**: Each plugin can include an "about" description to help users decide
- **Multi-Selection**: Users can select multiple plugins simultaneously

### How It Works

1. **Template Definition**: Template creators define plugins in the `ProjectPlugin` section of `templateConfig.json`
2. **Interactive Selection**: When loading a template, users see a rich UI to select desired plugins
3. **Path Exclusion**: Files and directories associated with unselected plugins are excluded during extraction
4. **Clean Output**: Only selected plugin modules are included in the final project

### Configuration Format

Plugins are defined in the `ProjectPlugin` section of `templateConfig.json`:

```json
{
  "ProjectPlugin": {
    "PluginName": {
      "about": "Description of what this plugin provides",
      "modulePath": [
        ["path", "to", "plugin", "file.py"],
        ["path", "to", "plugin", "directory"]
      ]
    }
  }
}
```

### Configuration Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `about` | String | No | Human-readable description of the plugin (shown in UI) |
| `modulePath` | Array of Arrays | Yes | List of file/directory paths to include/exclude. Each path is an array of path segments |

### Interactive UI Controls

When the plugin selection screen appears:

- **↑/↓ Arrow Keys**: Navigate between plugins
- **Space**: Toggle plugin selection on/off
- **Enter**: Confirm selection and proceed
- **q**: Quit/deselect all and cancel

**Visual Indicators:**
- ✔ (green checkmark): Plugin is selected
- ○ (circle): Plugin is not selected
- Highlighted row: Current cursor position
- Right panel: Shows description of currently highlighted plugin

### Example: Full Stack Application Template

```json
{
  "project": {
    "name": {
      "prompt": "What is your project name?",
      "input": null,
      "isEnv": false
    }
  },
  "database": {
    "url": {
      "prompt": "Database connection URL",
      "input": null,
      "isEnv": true
    }
  },
  "ProjectPlugin": {
    "Authentication": {
      "about": "JWT-based user authentication with login/register endpoints",
      "modulePath": [
        ["src", "auth"],
        ["tests", "test_auth.py"]
      ]
    },
    "Admin Dashboard": {
      "about": "Full-featured admin panel with user management and analytics",
      "modulePath": [
        ["src", "admin"],
        ["static", "admin"],
        ["templates", "admin"]
      ]
    },
    "Email Service": {
      "about": "Email notification system with templates and queue support",
      "modulePath": [
        ["src", "email"],
        ["templates", "email"]
      ]
    },
    "Payment Integration": {
      "about": "Stripe payment processing with webhook handling",
      "modulePath": [
        ["src", "payments"],
        ["tests", "test_payments.py"]
      ]
    },
    "API Documentation": {
      "about": "Auto-generated API docs with Swagger/OpenAPI",
      "modulePath": [
        ["src", "docs"],
        ["static", "swagger"]
      ]
    }
  }
}
```

### Example: React Template with Features

```json
{
  "app": {
    "name": {
      "prompt": "Application name",
      "input": null,
      "isEnv": false
    }
  },
  "ProjectPlugin": {
    "Redux State Management": {
      "about": "Redux Toolkit for centralized state management",
      "modulePath": [
        ["src", "store"],
        ["src", "slices"]
      ]
    },
    "React Router": {
      "about": "Client-side routing with React Router v6",
      "modulePath": [
        ["src", "routes"],
        ["src", "pages"]
      ]
    },
    "Material-UI Components": {
      "about": "Pre-built Material-UI component library",
      "modulePath": [
        ["src", "components", "mui"],
        ["src", "theme"]
      ]
    },
    "API Client": {
      "about": "Axios-based API client with interceptors",
      "modulePath": [
        ["src", "api"],
        ["src", "services"]
      ]
    },
    "Testing Setup": {
      "about": "Jest and React Testing Library configuration",
      "modulePath": [
        ["src", "__tests__"],
        ["src", "setupTests.js"]
      ]
    }
  }
}
```

### Usage Example

#### Step 1: Load Template

```bash
craftlet load-template --github
```

#### Step 2: Enter Template Information

```
Enter Github Template Repo URL: https://github.com/myorg/fullstack-template
Enter The Project Name: my-awesome-app
```

#### Step 3: Configure Values (if any prompts exist)

```
What is your project name?: my-awesome-app
Database connection URL: postgresql://localhost:5432/mydb
```

#### Step 4: Select Plugins

The interactive plugin selection UI appears:

```
┌─ Project Plugin Options ──────────────────────────────────────────────────┐
│                                                                            │
│  1.  ✔  Authentication              │ ┌─ About ─────────────────────────┐ │
│  2.  ✔  Admin Dashboard             │ │                                 │ │
│  3.  ○  Email Service               │ │ Email notification system with  │ │
│  4.  ✔  Payment Integration         │ │ templates and queue support     │ │
│  5.  ✔  API Documentation           │ │                                 │ │
│                                     │ └─────────────────────────────────┘ │
│                                                                            │
└────────────────────────────────── ↑/↓ move • Space toggle • Enter confirm • q quit ┘
```

- User navigates with arrow keys
- Toggles plugins with Space
- Presses Enter to confirm

#### Step 5: Project Generated

CraftLet creates the project with only the selected plugins:

```
my-awesome-app/
├── src/
│   ├── auth/              # ✔ Included (Authentication selected)
│   ├── admin/             # ✔ Included (Admin Dashboard selected)
│   ├── payments/          # ✔ Included (Payment Integration selected)
│   ├── docs/              # ✔ Included (API Documentation selected)
│   └── (email/ excluded)  # ✘ Not included (Email Service not selected)
├── tests/
├── .env                   # Generated if --generate-env was used
└── ...
```

### Path Resolution

**Module paths are relative to the template root:**

```json
"modulePath": [
  ["src", "auth"],           // Excludes: template-root/src/auth/
  ["tests", "test_auth.py"]  // Excludes: template-root/tests/test_auth.py
]
```

**Multiple paths per plugin:**

A single plugin can specify multiple files and directories:

```json
"Admin Dashboard": {
  "about": "Admin panel with UI",
  "modulePath": [
    ["src", "admin"],          // Backend code
    ["static", "admin"],       // Static assets
    ["templates", "admin"],    // HTML templates
    ["config", "admin.json"]   // Configuration file
  ]
}
```

### Best Practices

#### 1. Clear Descriptions

Provide concise, helpful descriptions:

```json
"Authentication": {
  "about": "JWT-based auth with login/register/logout endpoints"
}
```

#### 2. Logical Grouping

Group related files in the same plugin:

```json
"Blog Feature": {
  "about": "Complete blogging system",
  "modulePath": [
    ["src", "blog"],           // Backend
    ["src", "components", "blog"],  // Frontend components
    ["migrations", "001_blog.sql"]  // Database migrations
  ]
}
```

#### 3. Default Selections

By default, **all plugins are selected**. Users can deselect what they don't need. Design your template assuming all plugins are included, making each independently functional.

#### 4. Dependencies

If plugins depend on each other, document this in the `about` field:

```json
"Advanced Admin": {
  "about": "Extended admin features (requires 'Authentication' plugin)"
}
```

#### 5. Testing

Always test your template with different plugin combinations to ensure:
- Unselected plugins don't break the project
- Selected plugins work independently
- No missing dependencies when plugins are excluded

### Limitations

- **No Automatic Dependency Resolution**: If Plugin B depends on Plugin A, users must manually select both
- **Path-Based Only**: Plugin system works by excluding file paths; it doesn't modify file contents
- **No Partial File Exclusion**: You can only exclude entire files or directories, not sections within a file

### Advanced Use Cases

#### Conditional Features

```json
"ProjectPlugin": {
  "SQLite Database": {
    "about": "Lightweight SQLite database (good for development)",
    "modulePath": [["src", "db", "sqlite.py"]]
  },
  "PostgreSQL Database": {
    "about": "Production-ready PostgreSQL database",
    "modulePath": [["src", "db", "postgresql.py"]]
  },
  "MongoDB Database": {
    "about": "NoSQL MongoDB database",
    "modulePath": [["src", "db", "mongodb.py"]]
  }
}
```

#### Development vs Production

```json
"ProjectPlugin": {
  "Development Tools": {
    "about": "Debug toolbar, profiler, and dev utilities",
    "modulePath": [
      ["src", "debug"],
      ["middleware", "dev.py"]
    ]
  },
  "Production Monitoring": {
    "about": "APM, logging, and error tracking",
    "modulePath": [
      ["src", "monitoring"],
      ["config", "sentry.json"]
    ]
  }
}
```

---

## Related Documentation

- [CraftLet Project Documentation](README.md)
- [CraftLet GitHub Repository](https://github.com)

