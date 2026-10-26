"""Public-edition regressions using synthetic isolated installations only."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[3]
for name in ("Runner", "Contracts", "LibraryBridge"):
    sys.path.insert(0, str(ROOT/name/"current"))
import textura
import library_bridge

class PublicEditionTests(unittest.TestCase):
    def setUp(self):
        outputs = ROOT/"Quality/current/outputs"
        outputs.mkdir(exist_ok=True, parents=True)
        self.boundary = outputs.resolve()
        self.temp = tempfile.TemporaryDirectory(prefix="public-", dir=outputs)
        self.root = Path(self.temp.name).resolve()
        for name in ("Configuration", "Topics", "Sources"):
            (self.root/name/"current").mkdir(parents=True)
        self.settings = {"release": "0.1.2-test", "default_processing_policy": "local_only",
                         "bibliotheca": {"enabled": False, "root": None}}
        self.save()

    def save(self):
        (self.root/"Configuration/current/settings.json").write_text(json.dumps(self.settings),encoding="utf-8")

    def tearDown(self):
        if self.root == self.boundary or not self.root.is_relative_to(self.boundary) or not self.root.name.startswith("public-"):
            raise ValueError("Unsafe fixture cleanup")
        self.temp.cleanup()

    def dispatch(self, *args):
        return textura.dispatch(textura.parser().parse_args(["--root", str(self.root), *args]))

    def test_doctor_without_library_does_not_discover_or_call_node(self):
        with mock.patch.object(library_bridge, "node_binary") as node, mock.patch.object(library_bridge.subprocess, "run") as run:
            result = self.dispatch("doctor")
        node.assert_not_called()
        run.assert_not_called()
        self.assertFalse(result["bibliotheca_configured"])
        self.assertFalse(result["bibliotheca_entry_available"])

    def test_disabled_and_missing_root_bridge_never_starts_process(self):
        for config in ({}, {"enabled":False,"root":str(self.root)}, {"enabled":True,"root":None},
                       {"enabled":True,"root":""}):
            self.settings["bibliotheca"]=config
            self.save()
            with self.subTest(config=config), mock.patch.object(library_bridge,"node_binary") as node, \
                 mock.patch.object(library_bridge.subprocess,"run") as run:
                with self.assertRaisesRegex(ValueError,"disabled or unconfigured"):
                    library_bridge.run(self.root,"search","test")
                node.assert_not_called()
                run.assert_not_called()

    def test_relative_enabled_library_root_is_rejected(self):
        with self.assertRaisesRegex(ValueError,"absolute"):
            library_bridge.configured_library({"bibliotheca":{"enabled":True,"root":"library"}})

    def test_cli_defaults_local_and_allows_explicit_policy(self):
        topic=self.dispatch("topic","--title","Synthetic topic")
        source=self.dispatch("source","--title","Synthetic link","--url","https://example.invalid/")
        explicit=self.dispatch("topic","--title","Explicit policy","--policy","cloud_allowed")
        self.assertEqual(topic["processing_policy"],"local_only")
        self.assertEqual(source["processing_policy"],"local_only")
        self.assertEqual(explicit["processing_policy"],"cloud_allowed")

    def test_configured_default_and_restrictive_parent_are_honored(self):
        self.settings["default_processing_policy"]="cloud_allowed"
        self.save()
        default=self.dispatch("topic","--title","Configured default")
        restricted=self.dispatch("topic","--title","Restricted parent","--policy","local_only")
        work=self.dispatch("work","--title","Synthetic child","--language","en","--topic",restricted["id"])
        self.assertEqual(default["processing_policy"],"cloud_allowed")
        self.assertEqual(work["processing_policy"],"local_only")

    def test_invalid_configured_default_is_rejected_before_record_creation(self):
        self.settings["default_processing_policy"]="automatic"
        self.save()
        with self.assertRaisesRegex(ValueError,"default_processing_policy"):
            self.dispatch("topic","--title","Invalid policy")
        self.assertFalse((self.root/"Topics/current/records").exists())

    def test_node_discovery_uses_explicit_environment(self):
        with mock.patch.dict(library_bridge.os.environ,{"TEXTURA_NODE":"custom-node"}), \
             mock.patch.object(library_bridge.shutil,"which",return_value="resolved-node") as which:
            self.assertEqual(library_bridge.node_binary(),"resolved-node")
            which.assert_called_once_with("custom-node")

if __name__ == "__main__":
    unittest.main()
