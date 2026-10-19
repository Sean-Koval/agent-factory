import unittest

from tests import _path  # noqa: F401
from bot.commands import parse


class CommandsTest(unittest.TestCase):
    def test_parse(self) -> None:
        self.assertEqual(parse("@hangar do SVC-412").ticket, "SVC-412")
        self.assertEqual(parse("hangar add a retry to the exporter").verb, "ask")
        self.assertIsNone(parse("hangar add a retry").ticket)
        self.assertEqual((parse("/hangar status job-3").verb, parse("/hangar status job-3").target),
                         ("status", "job-3"))
        self.assertEqual(parse("/hangar link").verb, "link")
        self.assertEqual(parse("hello").verb, "help")


if __name__ == "__main__":
    unittest.main()
