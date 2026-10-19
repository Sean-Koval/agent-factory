import unittest
import xml.etree.ElementTree as ET

from tests import _path  # noqa: F401
from bot import forms

# The schemas hangar sends today (hangar mcp_steer.APPROVAL_SCHEMA, mcp_tasks.ANSWER_SCHEMA), copied as the contract.
HANGAR_APPROVAL = {
    "type": "object",
    "properties": {
        "decision": {"type": "string", "enum": ["allow", "deny", "allow_always"], "title": "Decision"},
        "message": {"type": "string", "title": "Note to the agent", "description": "Optional; sent with a denial."},
    },
    "required": ["decision"],
}
HANGAR_ANSWER = {"type": "object", "properties": {"answer": {"type": "string", "title": "Your answer"}},
                 "required": ["answer"]}


def parse(ml: str) -> ET.Element:
    return ET.fromstring(ml)  # well-formed MessageML, whatever the text held


class ElicitationToFormTest(unittest.TestCase):
    def test_approval_schema_is_one_button_per_decision(self) -> None:
        fid = forms.FormId("elicit", "job-1", "k1")
        root = parse(forms.elicitation_form(fid, "Job job-1: the agent asks to use Bash: make deploy", HANGAR_APPROVAL))
        form = root.find("form")
        self.assertEqual(form.get("id"), "hangar:elicit:job-1:k1")
        self.assertEqual([b.get("name") for b in form.iter("button")], ["allow", "deny", "allow_always"])
        self.assertEqual([t.get("name") for t in form.iter("textarea")], ["message"])
        self.assertIsNone(form.find("select"))

    def test_answer_schema_is_a_text_box_with_send_and_decline(self) -> None:
        root = parse(forms.question_form("job-2", "Which queue: <orders> or & payments?", "Job job-2"))
        form = root.find("form")
        self.assertEqual(form.find("textarea").get("name"), "answer")
        self.assertEqual(form.find("textarea").get("required"), "true")
        self.assertEqual([b.get("name") for b in form.iter("button")], ["submit", "decline"])
        self.assertIn("<orders>", form.find("p").text)  # escaped on the way in, intact once parsed

    def test_generic_schema_fields(self) -> None:
        schema = {"type": "object", "required": ["env"], "properties": {
            "env": {"type": "string", "enum": ["dev", "staging"]}, "dry_run": {"type": "boolean"},
            "count": {"type": "integer", "title": "How many"}}}
        form = parse(forms.elicitation_form(forms.FormId("elicit", "s", "k"), "?", schema)).find("form")
        self.assertEqual([o.get("value") for o in form.find("select").iter("option")], ["dev", "staging"])
        self.assertEqual(form.find("checkbox").get("name"), "dry_run")
        self.assertEqual(form.find("text-field").get("label"), "How many")


class SubmissionTest(unittest.TestCase):
    def test_live_elicitation_content_is_typed_and_limited_to_the_schema(self) -> None:
        schema = {"type": "object", "required": ["env"], "properties": {
            "env": {"type": "string", "enum": ["dev", "staging"]}, "dry_run": {"type": "boolean"},
            "count": {"type": "integer"}}}
        a = forms.answer("hangar:elicit:s:k", {"action": "submit", "env": "dev", "dry_run": ["true"], "count": "3",
                                               "extra": "dropped"}, schema)
        self.assertEqual((a.action, a.content), ("accept", {"env": "dev", "dry_run": True, "count": 3}))
        self.assertEqual(forms.answer("hangar:elicit:s:k", {"action": "decline"}, schema).action, "decline")
        with self.assertRaises(forms.InvalidSubmission):
            forms.answer("hangar:elicit:s:k", {"action": "submit", "env": "prod"}, schema)
        with self.assertRaises(forms.InvalidSubmission):
            forms.answer("hangar:elicit:s:k", {"action": "submit"}, schema)

    def test_approval_button_becomes_the_decision(self) -> None:
        a = forms.answer("hangar:elicit:job-1:k", {"action": "deny", "message": "not on prod"}, HANGAR_APPROVAL)
        self.assertEqual(a.content, {"decision": "deny", "message": "not on prod"})

    def test_offline_forms_become_hangar_calls(self) -> None:
        a = forms.answer("hangar:approval:job-1:ap-7", {"action": "allow_always", "message": ""})
        self.assertEqual((a.tool, a.args), ("answer_approval", {"ref": "job-1", "approval": "ap-7",
                                                                "decision": "allow_always"}))
        q = forms.answer("hangar:question:job-2:", {"action": "submit", "answer": "orders"})
        self.assertEqual((q.tool, q.args), ("follow_up_job", {"job": "job-2", "message": "orders"}))

    def test_foreign_or_malformed_form_ids_are_refused(self) -> None:
        for fid in ("other:approval:a:b", "hangar:delete:a:b", "hangar:approval"):
            with self.assertRaises(forms.InvalidSubmission):
                forms.answer(fid, {"action": "allow"})


if __name__ == "__main__":
    unittest.main()
