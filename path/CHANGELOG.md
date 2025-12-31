# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.1.0] - 2025-12-31

### Changed

- Respect label order

## [2.0.0] - 2025-12-29

### Changed

- Depends on "manala.utils" collection

### Removed

- Remove deprecated "default_file", "default_link" and "default_directory" filters

## [1.9.0] - 2025-12-12

### Added

- Add a "match" filter to filter a list of path dicts matching a pattern

## [1.8.0] - 2025-12-12

### Added

- Add a "match" test to check if a path dict match a pattern

### Changed

- Both "default" and "root" filters now accepts a path dict or a list of path dicts as input

## [1.7.1] - 2025-12-05

### Fixed

- The "parents" filter remove provided paths with same path as the generated ones

## [1.7.0] - 2025-12-05

### Added

- Add a "parents" filter to generate parent paths for each path in the provided list, inserting them immediately before
- Add a "state" option on "default" filter

### Changed

- Deprecate "default_file", "default_link" and "default_directory" filters in favor of "default" filter with "state" option to either "file", "link", or "directory".

## [1.6.0] - 2025-12-04

### Added

- Add a "unique" filter to create a list of unique paths from the provided paths list

## [1.5.0] - 2025-11-27

### Added

- Add a "state" filter to get the underlying state of a path dict
- Add a "default_link" filter, in line with "default_file" and "default_directory"
- Support implicit "link" state with only "src" defined

### Modified

- Include underlying state in "label" filter
- Filter relevant arguments in "label" filter

### Fixed

- The "link" test was not exported 

## [1.4.0] - 2025-11-21

### Added

- Add verbose messages in "find" module
- Support for "link"
- Find any type of files (regulars, directories, links) in "find" module

## [1.3.0] - 2025-11-07

### Added

- Add a "file" test
- Add a "directory" test
- Add a "label" filter
- Add a "root" filter
- Add  "default", "default_file" and "default_directory" filters
- Add a "relative" option to "find" module (default=false)
- Support "directory" explicit state in "path" module
- When "file" explicit state in "path" module, if no "content", "file" or "template" is provided, file is created with empty content if not exists, or just permissions updated, with no content chaned if already exists

### Changed

- Module "find" now returns absolute path by default

### Removed

- Ansible filter "join"

## [1.2.0] - 2025-10-31

### Added

- Add a "file" parameter to "path" module
- Add a "find" module
- Add an "exclusify" filter

## [1.1.0] - 2024-09-13

### Added

- Ansible filter "join"

## [1.0.0] - 2024-09-12

### Added

- Initial release
