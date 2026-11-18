"""Linux test isolation for reviewed, owned teaching fixtures."""
import math
from pathlib import Path
import shutil
import subprocess

from .policy import PolicyDenied


class BubblewrapTests:
    """Run one fixed test suite with a read-only workspace and no host network."""

    def run(self, argv, *, cwd, timeout):
        if tuple(argv[1:]) != ("-m", "unittest", "discover", "-s", "tests"):
            raise PolicyDenied("only the fixed unittest command is allowed")
        if not math.isfinite(timeout) or not 0 < timeout <= 30:
            raise PolicyDenied("test timeout must be between zero and 30 seconds")
        executable = shutil.which("bwrap")
        if executable is None or not Path("/usr/bin/python3").is_file():
            raise PolicyDenied("Bubblewrap and system Python are required")
        workspace = Path(cwd).resolve(strict=True)
        if not (workspace / "tests").is_dir():
            raise PolicyDenied("fixture tests directory required")
        command = [
            executable, "--unshare-all", "--unshare-user", "--disable-userns", "--die-with-parent",
            "--new-session", "--cap-drop", "ALL", "--clearenv",
            "--ro-bind", "/usr", "/usr", "--ro-bind-try", "/lib", "/lib",
            "--ro-bind-try", "/lib64", "/lib64", "--proc", "/proc", "--dev", "/dev",
            "--tmpfs", "/tmp", "--ro-bind", str(workspace), "/workspace",
            "--chdir", "/workspace", "--setenv", "PATH", "/usr/bin",
            "/usr/bin/python3", "-B", *argv[1:],
        ]
        try:
            result = subprocess.run(command, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                                    stderr=subprocess.DEVNULL, timeout=timeout, check=False)
        except subprocess.TimeoutExpired:
            return {"status": "timed_out"}
        except OSError as error:
            raise PolicyDenied("isolation launcher unavailable") from error
        return {"status": "passed" if result.returncode == 0 else "failed",
                "exit_code": result.returncode}
