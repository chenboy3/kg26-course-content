import importlib.machinery
import importlib.util
import json
import stat
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SUBMIT_PATH = ROOT / "bin" / "kg26-submit"
CONFIGURE_PATH = ROOT / "bin" / "kg26-configure"
LOADER = importlib.machinery.SourceFileLoader("kg26_submit", str(SUBMIT_PATH))
SPEC = importlib.util.spec_from_loader("kg26_submit", LOADER)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("Cannot load kg26-submit")
KG26_SUBMIT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(KG26_SUBMIT)
CONFIGURE_LOADER = importlib.machinery.SourceFileLoader(
    "kg26_configure",
    str(CONFIGURE_PATH),
)
CONFIGURE_SPEC = importlib.util.spec_from_loader(
    "kg26_configure",
    CONFIGURE_LOADER,
)
if CONFIGURE_SPEC is None or CONFIGURE_SPEC.loader is None:
    raise RuntimeError("Cannot load kg26-configure")
KG26_CONFIGURE = importlib.util.module_from_spec(CONFIGURE_SPEC)
CONFIGURE_SPEC.loader.exec_module(KG26_CONFIGURE)


class FakeResponse:
    def __init__(self, payload: dict):
        self.payload = json.dumps(payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def read(self) -> bytes:
        return self.payload


def _artifact() -> dict:
    return {
        "team": "blue-bottle",
        "day": 4,
        "decisions": {
            "prices": {
                "coffee": 5.0,
                "matcha": 6.5,
                "cookie": 3.0,
            }
        },
        "prediction": {
            "profit_mean": 18000,
            "interval_80": [15000, 21000],
        },
        "rationale": "Evidence-based team decision.",
    }


class SubmitClientTest(unittest.TestCase):
    def test_submit_uses_server_release_for_idempotency_and_saves_receipt(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            artifact_path = root / "submission.json"
            artifact_path.write_text(
                json.dumps(_artifact(), indent=2),
                encoding="utf-8",
            )
            receipt = {
                "schema_version": 1,
                "submission_id": "sub_0123456789abcdef01234567",
                "run_id": "kg26-pilot",
                "stage": "cafe-sim-day4",
                "team": "blue-bottle",
                "release_version": "2026.1",
                "revision": 1,
                "received_at": "2026-08-06T22:00:00Z",
                "artifact_sha256": "a" * 64,
                "artifact_bytes": 100,
                "validation": {"status": "accepted", "notes": []},
            }
            requests = []

            def fake_urlopen(request, timeout):
                self.assertEqual(timeout, 20)
                requests.append(request)
                if request.full_url.endswith("/healthz"):
                    return FakeResponse(
                        {
                            "run_id": "kg26-pilot",
                            "release_version": "2026.1",
                            "open_day": 4,
                            "submissions_open": True,
                        }
                    )
                return FakeResponse(receipt)

            with patch.object(KG26_SUBMIT, "urlopen", side_effect=fake_urlopen):
                returned, receipt_path = KG26_SUBMIT.submit(
                    artifact_path,
                    "https://course.example",
                    "secret-team-token",
                    root,
                )

            self.assertEqual(returned, receipt)
            self.assertEqual(
                json.loads(receipt_path.read_text(encoding="utf-8")),
                receipt,
            )
            self.assertEqual(len(requests), 2)
            post = requests[1]
            self.assertEqual(post.method, "POST")
            self.assertEqual(
                post.get_header("Authorization"),
                "Bearer secret-team-token",
            )
            self.assertRegex(
                post.get_header("Idempotency-key"),
                r"^kg26-[0-9a-f]{40}$",
            )
            self.assertEqual(json.loads(post.data), _artifact())

    def test_idempotency_key_changes_with_release_or_artifact(self):
        first_artifact = (
            json.dumps(_artifact(), sort_keys=True, separators=(",", ":")) + "\n"
        ).encode("utf-8")
        changed = _artifact()
        changed["prediction"]["profit_mean"] = 19000
        changed_artifact = (
            json.dumps(changed, sort_keys=True, separators=(",", ":")) + "\n"
        ).encode("utf-8")
        health = {
            "run_id": "kg26-pilot",
            "release_version": "2026.1",
            "open_day": 4,
        }

        first = KG26_SUBMIT.idempotency_key(health, first_artifact)
        self.assertEqual(
            first,
            KG26_SUBMIT.idempotency_key(dict(health), first_artifact),
        )
        self.assertNotEqual(
            first,
            KG26_SUBMIT.idempotency_key(health, changed_artifact),
        )
        next_release = {**health, "release_version": "2026.2"}
        self.assertNotEqual(
            first,
            KG26_SUBMIT.idempotency_key(next_release, first_artifact),
        )

    def test_service_url_requires_https_except_localhost(self):
        self.assertEqual(
            KG26_SUBMIT.service_url("https://course.example/"),
            "https://course.example",
        )
        self.assertEqual(
            KG26_SUBMIT.service_url("http://127.0.0.1:8080"),
            "http://127.0.0.1:8080",
        )
        for unsafe in (
            "http://course.example",
            "https://token@course.example",
            "https://course.example?token=secret",
        ):
            with self.subTest(unsafe=unsafe):
                with self.assertRaises(KG26_SUBMIT.SubmitError):
                    KG26_SUBMIT.service_url(unsafe)

    def test_configure_writes_owner_only_credentials_used_by_submit(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            path = KG26_CONFIGURE.write_config(
                workspace,
                "https://course.example/",
                "team-token-1234567890-abcdef",
                force=False,
            )

            self.assertEqual(path.stat().st_mode & 0o777, 0o600)
            self.assertEqual(path.parent.stat().st_mode & 0o777, 0o700)
            self.assertEqual(
                KG26_SUBMIT.load_credentials(workspace, None),
                (
                    "https://course.example",
                    "team-token-1234567890-abcdef",
                ),
            )
            with self.assertRaisesRegex(
                KG26_CONFIGURE.ConfigureError,
                "already exists",
            ):
                KG26_CONFIGURE.write_config(
                    workspace,
                    "https://course.example",
                    "different-token-1234567890-abc",
                    force=False,
                )

    def test_submit_command_is_executable(self):
        self.assertTrue(SUBMIT_PATH.stat().st_mode & stat.S_IXUSR)
        self.assertTrue(CONFIGURE_PATH.stat().st_mode & stat.S_IXUSR)


if __name__ == "__main__":
    unittest.main()
