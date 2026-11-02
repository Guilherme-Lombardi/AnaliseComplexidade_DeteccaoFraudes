import sys
from pathlib import Path

# Os testes reutilizam scripts/comum.py (threads, sys.path do NodeWatch e do XGBoost isolado).
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import comum  # noqa: E402,F401
