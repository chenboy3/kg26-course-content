import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "templates" / "prompt-first-course"
PROFILE = TEMPLATE / "course-profile.example.json"


class TemplateCourseTest(unittest.TestCase):
    def test_example_profile_points_to_existing_assets(self):
        profile = json.loads(PROFILE.read_text())
        install = profile["install"]

        self.assertEqual(profile["schema_version"], 1)
        self.assertTrue((ROOT / install["python_requirements"]).is_file())
        self.assertTrue((ROOT / install["dataset_manifest"]).is_file())
        for command in install["commands"]:
            self.assertTrue((ROOT / command["path"]).is_file())
        for skill in install["skills"]:
            self.assertTrue((ROOT / skill["path"] / "SKILL.md").is_file())
        for lesson in install["lessons"]:
            self.assertTrue((ROOT / lesson["path"] / "README.md").is_file())

    def test_skills_keep_code_optional_and_require_student_judgment(self):
        skill_paths = sorted((TEMPLATE / ".opencode" / "skills").glob("*/SKILL.md"))

        self.assertEqual(len(skill_paths), 3)
        for path in skill_paths:
            contents = path.read_text()
            self.assertIn("opencode/slash: \"true\"", contents)
            self.assertIn("student", contents.lower())
            self.assertIn("ask", contents.lower())
            self.assertIn("code", contents.lower())
            self.assertRegex(contents.lower(), r"student (asks|requests)")

    def test_labs_have_prompt_evidence_and_optional_paths(self):
        lab_paths = sorted((TEMPLATE / "labs").glob("*/README.md"))

        self.assertEqual(len(lab_paths), 3)
        for path in lab_paths:
            contents = path.read_text()
            self.assertIn("## Start with this prompt", contents)
            self.assertIn("## Evidence checkpoint", contents)
            self.assertIn("## Optional deeper coding", contents)

    def test_eval_prompts_cover_student_shortcuts(self):
        payload = json.loads((TEMPLATE / "evals" / "evals.json").read_text())
        prompts = [item["prompt"] for item in payload["evals"]]

        self.assertEqual(len(prompts), 3)
        self.assertTrue(any("tell me" in prompt for prompt in prompts))
        self.assertTrue(any("don't know python" in prompt for prompt in prompts))
        self.assertTrue(any("best model" in prompt for prompt in prompts))


if __name__ == "__main__":
    unittest.main()
