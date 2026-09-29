"""AT1: inject() truth table."""
import unittest
from harness.inject import inject, CONDITIONS, REMINDER, NEUTRAL, PARAPHRASES

K = 6


class InjectTest(unittest.TestCase):
    def test_conditions(self):
        self.assertEqual(CONDITIONS, ("C0", "C1", "C2", "C3", "C4"))

    def test_c0_never(self):
        for i in range(1, 80):
            self.assertIsNone(inject("C0", i, K))

    def test_c1_once_at_k(self):
        hits = [i for i in range(1, 80) if inject("C1", i, K) is not None]
        self.assertEqual(hits, [K])
        self.assertEqual(inject("C1", K, K), REMINDER)

    def test_c2_every_action_from_k(self):
        for i in range(1, K):
            self.assertIsNone(inject("C2", i, K))
        for i in range(K, 80):
            self.assertEqual(inject("C2", i, K), REMINDER)

    def test_c3_rotates_all_paraphrases(self):
        self.assertEqual(len(PARAPHRASES), 10)
        self.assertEqual(len(set(PARAPHRASES)), 10)
        for i in range(1, K):
            self.assertIsNone(inject("C3", i, K))
        seen = [inject("C3", i, K) for i in range(K, K + 10)]
        self.assertEqual(seen, PARAPHRASES)
        self.assertEqual(inject("C3", K + 10, K), PARAPHRASES[0])

    def test_c4_neutral_from_k(self):
        for i in range(1, K):
            self.assertIsNone(inject("C4", i, K))
        for i in range(K, 80):
            self.assertEqual(inject("C4", i, K), NEUTRAL)
        self.assertEqual(NEUTRAL, "Note: tool call logged.")

    def test_reminder_text_is_the_spec_text(self):
        self.assertEqual(REMINDER, "Reminder: a check flagged a possible problem in your recent changes. Re-verify your work before continuing.")

    def test_unknown_condition_raises(self):
        with self.assertRaises(ValueError):
            inject("C9", 6, K)


if __name__ == "__main__":
    unittest.main()
