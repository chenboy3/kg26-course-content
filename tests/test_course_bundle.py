import hashlib
import importlib.machinery
import importlib.util
import json
import subprocess
import tarfile
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILDER_PATH = ROOT / "bin" / "build-course-bundle"
LOADER = importlib.machinery.SourceFileLoader(
    "course_bundle",
    str(BUILDER_PATH),
)
SPEC = importlib.util.spec_from_loader("course_bundle", LOADER)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("Cannot load course bundle builder")
COURSE_BUNDLE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(COURSE_BUNDLE)


class CourseBundleTest(unittest.TestCase):
    def test_build_is_repeatable_and_contains_only_committed_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            first = temp / "first"
            second = temp / "second"
            base_url = "https://content.example/courses"

            first_result = COURSE_BUNDLE.build_bundle(
                ROOT,
                "HEAD",
                first,
                "course-profile.json",
                base_url,
            )
            second_result = COURSE_BUNDLE.build_bundle(
                ROOT,
                "HEAD",
                second,
                "course-profile.json",
                base_url,
            )

            first_bundle = Path(first_result["bundle_path"])
            second_bundle = Path(second_result["bundle_path"])
            self.assertEqual(first_bundle.read_bytes(), second_bundle.read_bytes())
            for first_path in sorted(first.iterdir()):
                second_path = second / first_path.name
                self.assertTrue(second_path.is_file())
                self.assertEqual(first_path.read_bytes(), second_path.read_bytes())

            expected_sha256 = hashlib.sha256(first_bundle.read_bytes()).hexdigest()
            self.assertEqual(first_result["bundle_sha256"], expected_sha256)
            checksum = first / f"{first_bundle.name}.sha256"
            self.assertEqual(
                checksum.read_text(encoding="utf-8"),
                f"{expected_sha256}  {first_bundle.name}\n",
            )

            tracked = set(
                subprocess.run(
                    ["git", "-C", str(ROOT), "ls-tree", "-r", "--name-only", "HEAD"],
                    capture_output=True,
                    check=True,
                    text=True,
                ).stdout.splitlines()
            )
            with tarfile.open(first_bundle, "r:gz") as archive:
                bundled = {
                    member.name.removeprefix("course-content/")
                    for member in archive.getmembers()
                    if member.isfile()
                }
            self.assertEqual(bundled, tracked)

            catalog = json.loads(
                Path(first_result["catalog_path"]).read_text(encoding="utf-8")
            )
            self.assertEqual(
                catalog,
                {
                    "kg26": {
                        "bundle_sha256": expected_sha256,
                        "bundle_url": (
                            f"{base_url}/{first_bundle.name}"
                        ),
                        "profile_path": "course-profile.json",
                    }
                },
            )

            manifest = json.loads(
                Path(first_result["manifest_path"]).read_text(encoding="utf-8")
            )
            self.assertEqual(manifest["bundle_sha256"], expected_sha256)
            self.assertEqual(
                manifest["source_commit"],
                subprocess.run(
                    ["git", "-C", str(ROOT), "rev-parse", "HEAD"],
                    capture_output=True,
                    check=True,
                    text=True,
                ).stdout.strip(),
            )

    def test_profile_validation_rejects_missing_assets(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "course-profile.json").write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "course_id": "test-course",
                        "content_version": "1.0",
                        "install": {
                            "python_requirements": "missing.txt",
                            "commands": [],
                            "skills": [],
                            "dataset_manifest": "datasets.json",
                            "lessons": [],
                        },
                    }
                ),
                encoding="utf-8",
            )
            (root / "datasets.json").write_text("{}", encoding="utf-8")

            with self.assertRaisesRegex(
                COURSE_BUNDLE.BundleError,
                "install.python_requirements is not a file",
            ):
                COURSE_BUNDLE.validate_profile(root, "course-profile.json")

    def test_catalog_url_rejects_unsafe_values(self):
        unsafe_urls = [
            "http://content.example/courses",
            "https://token@content.example/courses",
            "https://content.example/courses?token=secret",
        ]

        for value in unsafe_urls:
            with self.subTest(value=value):
                with self.assertRaises(COURSE_BUNDLE.BundleError):
                    COURSE_BUNDLE.bundle_url(value, "course.tar.gz")


if __name__ == "__main__":
    unittest.main()
