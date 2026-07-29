import csv
import hashlib
import json
import os
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "course-profile.json"
DATA_COMMAND = ROOT / "bin" / "course-data"
DATASETS = ROOT / "datasets" / "datasets.json"


class CourseDataTest(unittest.TestCase):
    def test_course_profile_points_to_existing_assets(self):
        profile = json.loads(PROFILE.read_text())
        install = profile["install"]

        self.assertEqual(profile["schema_version"], 1)
        self.assertEqual(profile["course_id"], "kg26")
        self.assertTrue((ROOT / install["python_requirements"]).is_file())
        self.assertTrue((ROOT / install["dataset_manifest"]).is_file())
        for command in install["commands"]:
            self.assertTrue((ROOT / command["path"]).is_file())
        for skill in install["skills"]:
            self.assertTrue((ROOT / skill["path"] / "SKILL.md").is_file())
        for lesson in install["lessons"]:
            self.assertTrue((ROOT / lesson["path"]).is_dir())

    def test_mashina_manifest_pins_source_and_removes_identifiers(self):
        manifest = json.loads(DATASETS.read_text())
        mashina = manifest["datasets"]["mashina"]

        self.assertEqual(
            mashina["source"]["dataset_spec"],
            "vinnyg110g/mashina-kyrgyzstan-dataset/1",
        )
        self.assertEqual(
            mashina["source"]["sha256"],
            "b91b085d146f9efb8f7cb0724656950a57d3f3694f3eacd10e0110d64416f2be",
        )
        self.assertEqual(mashina["remove_columns"], ["License plate", "VIN"])

    def test_data_command_verifies_and_sanitizes_download(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            fixture = temp / "source.csv"
            fixture.write_text(
                "title,price_usd,License plate,VIN\n"
                "Toyota,$ 12000,01KG123ABC,JT123\n",
                encoding="utf-8",
            )
            source_sha256 = hashlib.sha256(fixture.read_bytes()).hexdigest()
            manifest = temp / "datasets.json"
            manifest.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "datasets": {
                            "mashina": {
                                "title": "test",
                                "source": {
                                    "type": "kaggle",
                                    "dataset_spec": "owner/dataset/1",
                                    "file": "mashina_raw.csv",
                                    "sha256": source_sha256,
                                },
                                "output": "data/mashina/mashina.csv",
                                "remove_columns": ["License plate", "VIN"],
                            }
                        },
                    }
                ),
                encoding="utf-8",
            )

            bin_dir = temp / "bin"
            bin_dir.mkdir()
            fake_kaggle = bin_dir / "kaggle"
            fake_kaggle.write_text(
                "#!/bin/sh\n"
                "output_dir=''\n"
                "file_name=''\n"
                "while [ \"$#\" -gt 0 ]; do\n"
                "  case \"$1\" in\n"
                "    --path) output_dir=\"$2\"; shift 2 ;;\n"
                "    --file) file_name=\"$2\"; shift 2 ;;\n"
                "    *) shift ;;\n"
                "  esac\n"
                "done\n"
                "cp \"$COURSE_TEST_FIXTURE\" \"$output_dir/$file_name\"\n",
                encoding="utf-8",
            )
            fake_kaggle.chmod(fake_kaggle.stat().st_mode | stat.S_IXUSR)

            workspace = temp / "workspace"
            environment = {
                **os.environ,
                "COURSE_TEST_FIXTURE": str(fixture),
                "PATH": f"{bin_dir}:{os.environ['PATH']}",
            }
            result = subprocess.run(
                [
                    os.environ.get("PYTHON", "python3"),
                    str(DATA_COMMAND),
                    "--manifest",
                    str(manifest),
                    "--workspace",
                    str(workspace),
                    "fetch",
                    "mashina",
                    "--accept-terms",
                ],
                capture_output=True,
                check=False,
                env=environment,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            output = workspace / "data" / "mashina" / "mashina.csv"
            with output.open(encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(list(rows[0]), ["title", "price_usd"])
            self.assertEqual(rows[0]["title"], "Toyota")

            metadata = json.loads(
                (output.parent / "manifest.json").read_text(encoding="utf-8")
            )
            self.assertEqual(metadata["row_count"], 1)
            self.assertEqual(
                metadata["removed_columns"],
                ["License plate", "VIN"],
            )
            self.assertEqual(metadata["source_sha256"], source_sha256)

    def test_skill_uses_shared_course_data_command(self):
        skill = (
            ROOT / ".opencode/skills/day-1-fetch-data/SKILL.md"
        ).read_text()

        self.assertIn("course-data fetch mashina", skill)
        self.assertNotIn("kg26-data", skill)


if __name__ == "__main__":
    unittest.main()
