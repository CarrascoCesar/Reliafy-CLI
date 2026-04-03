from __future__ import annotations

from pathlib import Path

try:
    import tomllib
except Exception:  # pragma: no cover
    tomllib = None


def on_config(config):
    """Set header repo label to PyPI v<version> from pyproject.toml."""
    if tomllib is None:
        return config

    try:
        root = Path(config.config_file_path).resolve().parent
        pyproject_path = root / "pyproject.toml"
        with pyproject_path.open("rb") as f:
            data = tomllib.load(f)
        version = data["project"]["version"]
        config["repo_name"] = f"GitHub v{version}"
    except Exception:
        # Keep configured fallback when version cannot be read.
        pass

    return config


def on_post_build(config, **kwargs):
    """Write robots.txt with the sitemap URL for the active site_url."""
    site_url = str(config.get("site_url", "")).rstrip("/")
    if not site_url:
        return

    robots_path = Path(config["site_dir"]) / "robots.txt"
    robots_path.write_text(
        "User-agent: *\n" "Allow: /\n\n" f"Sitemap: {site_url}/sitemap.xml\n",
        encoding="utf-8",
    )
