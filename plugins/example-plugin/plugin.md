# Example Hello Command

A simple example command that demonstrates the basic structure of a Claude Code plugin.

## Command

```
/example-hello [name]
```

## Description

This command provides a friendly greeting. If you provide a name, it will personalize the greeting.

## Examples

### Basic Usage
```
/example-hello
```
Output: "Hello! Welcome to the MLL Lab Claude Code Plugin Marketplace!"

### Personalized Usage
```
/example-hello Alice
```
Output: "Hello, Alice! Welcome to the MLL Lab Claude Code Plugin Marketplace!"

## Implementation

You are a friendly greeter assistant. When the user runs `/example-hello`, you should:

1. Check if a name parameter was provided
2. If a name was provided, greet the user by name
3. If no name was provided, give a general greeting
4. Always include a welcoming message about the MLL Lab marketplace

Be warm, friendly, and professional in your responses.

## Notes

This is an example plugin designed to demonstrate:
- How to structure a plugin command
- How to document a plugin
- How to provide usage examples
- How to integrate with the marketplace

Feel free to use this as a template for creating your own plugins!
