import os
import subprocess
import sys

import pytest


@pytest.mark.parametrize(
    ("jwt_secret", "admin_password", "expected_error"),
    [
        (None, "test-admin-password-long-enough", "JWT_SECRET_KEY"),
        ("too-short", "test-admin-password-long-enough", "JWT_SECRET_KEY"),
        ("x" * 32, None, "ADMIN_PASSWORD"),
        ("x" * 32, "short", "ADMIN_PASSWORD"),
    ],
)
def test_config_rejects_missing_or_weak_credentials(jwt_secret, admin_password, expected_error):
    env = os.environ.copy()
    env.pop("JWT_SECRET_KEY", None)
    env.pop("ADMIN_PASSWORD", None)
    if jwt_secret is not None:
        env["JWT_SECRET_KEY"] = jwt_secret
    if admin_password is not None:
        env["ADMIN_PASSWORD"] = admin_password

    result = subprocess.run(
        [sys.executable, "-c", "import app.config"],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )

    assert result.returncode != 0
    assert expected_error in result.stderr
