import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from plan_scenes import make_fallback_plan, sentences_from_script, infer_props

class ScenePlannerTests(unittest.TestCase):
    def test_visual_plan_uses_two_to_seven_fixed_characters(self):
        script = "Alex gets a phone notification. A child watches him react. Later, his grandfather offers advice."
        plan = make_fallback_plan(script)
        used = {shot[key]["characterId"] for shot in plan["shots"] for key in ("lead", "friend") if shot.get(key)}
        self.assertGreaterEqual(len(used), 2)
        self.assertLessEqual(len(used), 7)
        self.assertTrue(used.issubset({"alex", "maya", "ethan", "zoe", "oliver", "arthur"}))

    def test_scene_excerpts_are_taken_from_original_script(self):
        script = "The first moment feels uncomfortable. Your mind keeps replaying it."
        plan = make_fallback_plan(script)
        joined = " ".join(shot["caption"] for shot in plan["shots"])
        self.assertIn("The first moment feels uncomfortable.", joined)
        self.assertIn("Your mind keeps replaying it.", joined)

    def test_phone_visual_selects_phone_prop(self):
        self.assertIn("phone", infer_props("A notification lights up the phone screen."))

    def test_empty_script_is_rejected(self):
        with self.assertRaises(ValueError):
            make_fallback_plan("")

    def test_each_scene_has_renderable_timing_and_environment(self):
        plan = make_fallback_plan("A friend starts a conversation. Later, they walk home.")
        self.assertTrue(all(s["durationInFrames"] >= 90 for s in plan["shots"]))
        self.assertTrue(all(s["place"] in {"cafe","street","bedroom","bedroom-phone","bedroom-dawn","park","office","classroom","library","living-room"} for s in plan["shots"]))

if __name__ == "__main__":
    unittest.main()
