# PyELEGANT

Python Interface to the 6D Accelerator Program ELEGANT (ELEctron Generation ANd Tracking)

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

## Overview

PyELEGANT provides a comprehensive Python interface to the ELEGANT accelerator physics simulation code, enabling advanced beam dynamics calculations, lattice optimization, and analysis workflows.

## Installation

### Prerequisites

- Python 3.12.* (for pixi setup)
- [pixi](https://pixi.sh) (recommended) or conda/mamba

### Using Pixi (Recommended)

Pixi is a fast, modern package manager that simplifies environment management. Install it following the [official instructions](https://pixi.sh/latest/#installation).

#### Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/NSLS-II/PyELEGANT.git
   cd PyELEGANT
   ```

2. **Configure for your facility:**
   ```bash
   cp .env.example .env
   # Edit .env and set PYELEGANT_REMOTE to your facility (e.g., nsls2pluto)
   ```

3. **Install with pixi (installs from git by default):**
   ```bash
   pixi install
   ```

4. **Activate the environment:**
   ```bash
   pixi shell
   ```
   The `.env` file will be automatically loaded, setting `PYELEGANT_REMOTE` for your facility.

5. **For development, install in editable mode:**
   ```bash
   pixi run install-editable
   ```

6. **Run commands in the environment:**
   ```bash
   pixi run python your_script.py
   pixi run jupyter lab
   ```

**Note:** The pixi configuration includes cluster compatibility requirements (Python 3.12.*, icu < 78) to prevent library version conflicts on compute clusters. Environment variables from `.env` are automatically loaded when importing pyelegant.

#### Available Environments

PyELEGANT provides multiple environments for different use cases. By default, pyelegant is installed from the git repository. For development, run `pixi run install-editable` to switch to editable mode:

- **default**: Base installation with Jupyter support (Python 3.12.*)
  ```bash
  pixi install
  pixi run install-editable  # For development work
  ```

- **parallel**: Includes MPI support for parallel computing (mpi4py installed via pip)
  ```bash
  pixi install --environment parallel
  pixi shell --environment parallel
  ```

- **genreport**: Includes tools for report generation (PyLaTeX, XlsxWriter)
  ```bash
  pixi install --environment genreport
  ```

- **all**: All optional dependencies
  ```bash
  pixi install --environment all
  ```

- **dev**: Development environment with testing tools
  ```bash
  pixi install --environment dev
  pixi run test  # Run tests
  ```

### Using Poetry (Alternative)

If you prefer poetry:

```bash
poetry install
poetry install --extras "all"  # Install all optional dependencies
```

### Using pip (Basic Installation)

```bash
pip install -e .
pip install -e ".[all]"  # Install all optional dependencies
```

## Features

### Core Functionality

- **Twiss Calculations**: Linear optics and Twiss parameters
- **Closed Orbit Analysis**: On-momentum and off-momentum closed orbits
- **Nonlinear Dynamics**: Frequency map analysis, dynamic aperture
- **Tune & Chromaticity Correction**: Automated optimization routines
- **Lattice Generation**: Programmatic LTE file creation
- **Parallel Computing**: MPI-based parallel tracking and optimization

### Optional Features

- **Jupyter Integration** (`jupy`): Interactive notebooks with plotting support
- **Parallel Computing** (`parallel`): MPI support for distributed calculations
- **Report Generation** (`genreport`): Automated LaTeX/Excel report creation
- **All Features** (`all`): Complete installation with all optional dependencies

## Quick Start

### Basic Twiss Calculation

```python
import pyelegant as pe

# Calculate ring twiss parameters
LTE_filepath = 'your_lattice.lte'
E_MeV = 3000  # Beam energy in MeV
output_filepath = 'twiss_results.hdf5'

pe.calc_ring_twiss(output_filepath, LTE_filepath, E_MeV,
                   radiation_integrals=True)

# Plot results
pe.plot_twiss(output_filepath)
```

### Using Jupyter Notebooks

Launch Jupyter Lab:
```bash
pixi run jupyter lab
```

Example notebooks are available in the `demo/` directory.

## Console Scripts

PyELEGANT provides several command-line utilities:

### Common Scripts
- `pyele_zip_lte`: Compress LTE files
- `pyele_unzip_lte`: Decompress LTE files
- `pyele_report`: Generate analysis reports

### SLURM Cluster Scripts (NSLS-II specific)
- `pyele_slurm_print_queue`: Display SLURM queue status
- `pyele_slurm_print_load`: Show cluster load
- `pyele_scancel_regex_jobname`: Cancel jobs by pattern
- `pyele_slurm_nfree_change`: Monitor available cores

### GUI Applications
- `pyele_gui_slurm`: SLURM job management GUI
- `pyele_gui_report_wiz`: Report generation wizard

## Development

### Running Tests

```bash
pixi run test
```

Or with pytest directly:

```bash
pixi run pytest tests/
```

### Pre-commit Hooks

Set up pre-commit hooks for code quality:

```bash
pixi run -e dev pre-commit install
```

## Documentation

- Detailed examples in `demo/` directory
- Jupyter notebooks demonstrating key features
- API documentation (coming soon)

## Requirements

### System Requirements
- **Python**: 3.12.* (pinned for cluster compatibility)
- **icu**: < 78 (required to avoid CXXABI version conflicts on compute clusters)

### Core Dependencies
- numpy >= 2.3.2
- scipy >= 1.16.1
- matplotlib >= 3.10
- h5py >= 3.14.0
- pydantic >= 2.12
- ruamel.yaml 0.17.*

### Optional Dependencies
- jupyter, ipympl (for Jupyter support)
- mpi4py, dill (for parallel computing)
- PyQt5, QtPy (for GUI applications)
- PyLaTeX, XlsxWriter (for report generation)

## License

BSD 3-Clause License. See [LICENSE](LICENSE) for details.

## Authors

- **Yoshiteru Hidaka** - *Maintainer* - yhidaka@bnl.gov

## Repository

GitHub: [https://github.com/NSLS-II/PyELEGANT](https://github.com/NSLS-II/PyELEGANT)

## Acknowledgments

Developed at Brookhaven National Laboratory's National Synchrotron Light Source II (NSLS-II).
