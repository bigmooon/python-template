"""your-project: Python 3.12 프로젝트 템플릿."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("your-project")
except PackageNotFoundError:  # pragma: no cover
    # 패키지가 설치되지 않은 환경(예: 소스만 체크아웃) fallback
    __version__ = "0.0.0"
