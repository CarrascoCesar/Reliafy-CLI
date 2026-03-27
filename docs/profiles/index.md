# Profile Management

Profiles are YAML configuration files that control run options for analysis, design, and simulation. The `default` profile is built-in and cannot be modified.

For detailed documentation of all available profile options, see the [Profile Options Reference](profile-reference.md).

## Creating a New Profile

Create a new profile with default settings:

Usage: `reliafy profile new <name> [--description "Description"] [--force]`

Example:
```bash
reliafy profile new custom --description "My custom profile"
```

## Editing Profiles

Edit an existing profile using your preferred editor:

Using nano:

Usage: `reliafy profile nano <name>`

Using vim:

Usage: `reliafy profile vim <name>`

Using vi (alias):

Usage: `reliafy profile vi <name>`

Note: You can also manage profile YAML files directly in your IDE (for example, VS Code).

## Viewing Profiles

Display a profile's contents:

Formatted view:

Usage: `reliafy profile show <name>`

Formatted view alias:

Usage: `reliafy profile echo <name>`

Raw YAML view:

Usage: `reliafy profile show <name> --raw`

Note: You can also manage profile YAML files directly in your IDE (for example, VS Code).

## Listing All Profiles

List all available profiles:

```bash
reliafy profile list
```

Alias:

```bash
reliafy profile ls
```

## Validating Profiles

Validation checks the profile against the full option schema: verifies that all fields are recognized, required values are present, and values match the expected types and constraints.

Validate a profile's configuration:

Usage: `reliafy profile validate <name>`

Alias: `reliafy profile val <name>`

## Copying Profiles

Copy an existing profile:

Usage: `reliafy profile copy <source> <destination> [--validate]`

Alias: `reliafy profile cp <source> <destination>`

Example:
```bash
reliafy profile copy default mycopy
```

Note: You can also manage profile YAML files directly in your IDE (for example, VS Code).

## Renaming Profiles

Rename a profile:

Usage: `reliafy profile rename <old_name> <new_name> [--validate]`

Alias: `reliafy profile mv <old_name> <new_name>`

Note: You can also manage profile YAML files directly in your IDE (for example, VS Code).

## Deleting Profiles

Delete a profile (requires confirmation):

Usage: `reliafy profile delete <name>`

Aliases: `reliafy profile del <name>`, `reliafy profile rm <name>`

Note: You can also manage profile YAML files directly in your IDE (for example, VS Code).

Note: The `default` profile cannot be deleted.
