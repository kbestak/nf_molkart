# nf-core/molkart: Changelog

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## v1.0dev - [2023.17.10]

Functionality to match metromap achieved by adding tifftohdf5, ilastik pixel classification and ilastik multicut.

### `Added`

- README documentation
- CITATIONS
- tiffh5convert local process
- application of ilastik/pixelclassification and ilastik/multicut nf-core modules
- custom_ilastik_model parameter

### `Fixed`

### `Dependencies`

### `Deprecated`

## v1.0dev - [2023.12.10]

Molkart adapted to most nf-core standards with optional parameters, multiple segmentation options, as well as membrane channel handling. Started work on creating training subset functionality.

### `Added`

- parameters for pipeline execution
- ext.args logic for almost all modules with external parameters
- channel logic for membrane handling
- create stack process if membrane image present for Cellpose
- optional clahe
- started work on create subset functionality

### `Fixed`

### `Dependencies`

### `Deprecated`

## v1.0dev - [date]

Initial release of nf-core/molkart, created with the [nf-core](https://nf-co.re/) template.

### `Added`

### `Fixed`

### `Dependencies`

### `Deprecated`
