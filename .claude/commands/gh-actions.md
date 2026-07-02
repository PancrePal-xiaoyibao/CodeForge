---
description: "Generate correct GitHub Actions CI/CD workflow YAML for any ecosystem — lint, multi-platform builds, releases"
---

# GitHub Actions Architect

Use this skill to generate production-ready GitHub Actions workflow files.

## Usage

Describe your project and what you need:

1. **Project ecosystem**: Python / Node.js / Rust / Go / Docker / C++ / Java / R / Flutter / .NET
2. **Workflow type**: Lint check, Build (multi-platform multi-arch), Test, Release, Full pipeline
3. **Target platforms**: Linux amd64/arm64, Windows, macOS Intel/ARM, Android, Docker multi-arch
4. **Package format**: .exe, .msi, .apk, .aab, .dmg, .deb, .rpm, .AppImage, .whl, Docker image, npm package

The skill will output complete YAML workflow files with built-in pitfall validation.

## Examples

- "I have a Rust CLI tool, build for Linux/Windows/macOS on both amd64 and arm64, release on tag"
- "Python package with cibuildwheel for manylinux/aarch64, publish to PyPI"
- "Flutter app, build APK + AAB for Android, IPA for iOS"
- "Docker image for linux/amd64 + linux/arm64, push to GHCR"
- "Node.js Electron app, build .exe + .dmg + .AppImage"
