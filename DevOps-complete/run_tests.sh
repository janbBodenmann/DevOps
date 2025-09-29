
#!/bin/bash
set -e
python -m pip install -r app/requirements.txt pytest
pytest -q app/tests
