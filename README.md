# thoth

## Repository Structure

thoth/
├── .env # sensitive data
├── src/ # all code
│   ├── utils/ # classes
│   ├── analysis/ # each folder represents and indepenend analysis/script
│   │   ├── analysis_2025/ # each sub-folder contains their own .venv
│   │   │   ├── analysis.ipynb
│   │   │   ├── sql/
│   │   │   │   └── query.sql
│   │   │   ├── poetry.lock # Poetry lock file for dependencies
│   │   │   ├── pyproject.toml # Poetry configuration file
├── templates/ # code for copy pasting
