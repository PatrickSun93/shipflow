import unittest
from unittest.mock import patch, MagicMock
import os
from pathlib import Path
import tempfile
import shutil

from src.orchestrator import ShipflowOrchestrator

class TestShipflowOrchestrator(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory to act as the target repo
        self.test_dir = tempfile.mkdtemp()
        self.shipflow_repo = tempfile.mkdtemp()

        # Mock some agent files in the fake shipflow repo so the orchestrator can "find" them
        agents_dir = Path(self.shipflow_repo) / "agents"
        agents_dir.mkdir()
        for agent in [
            "discovery-moderator", "discovery-tech-persona", "discovery-ux-persona",
            "discovery-business-persona", "challenger", "tech-lead", "product-lead", "spec-author"
        ]:
            (agents_dir / f"{agent}.md").write_text(f"# Mock {agent}", encoding="utf-8")

        self.orchestrator = ShipflowOrchestrator(
            target_dir=self.test_dir,
            shipflow_repo_path=self.shipflow_repo
        )

    def tearDown(self):
        shutil.rmtree(self.test_dir)
        shutil.rmtree(self.shipflow_repo)

    @patch("src.claude_runner.subprocess.run")
    def test_sf_init(self, mock_run):
        self.orchestrator.sf_init()

        docs_dir = Path(self.test_dir) / "docs" / "shipflow"
        self.assertTrue(docs_dir.exists())
        self.assertTrue((docs_dir / "briefs").exists())
        self.assertTrue((docs_dir / "stories").exists())
        self.assertTrue((docs_dir / "index.md").exists())

    @patch("src.claude_runner.subprocess.run")
    def test_sf_discover(self, mock_run):
        # Setup mock subprocess return
        mock_run.return_value = MagicMock(stdout="Mocked claude output", returncode=0)

        # Ensure directories exist via init first
        self.orchestrator.sf_init()

        idea = "A new testing feature"

        # Fake the moderator writing questions.md
        def mock_spawn(*args, **kwargs):
            slug_dir = Path(self.test_dir) / "docs" / "shipflow" / "discovery" / "a-new-testing-feature"
            slug_dir.mkdir(parents=True, exist_ok=True)
            (slug_dir / "questions.md").write_text("1. What is the scope?", encoding="utf-8")
            return "Done"

        with patch.object(self.orchestrator.runner, 'spawn_subagent', side_effect=mock_spawn) as mock_spawn_agent:
            result = self.orchestrator.sf_discover(idea)

            self.assertEqual(result, "1. What is the scope?")

            slug_dir = Path(self.test_dir) / "docs" / "shipflow" / "discovery" / "a-new-testing-feature"
            self.assertTrue(slug_dir.exists())
            self.assertTrue((slug_dir / "seed.md").exists())

            mock_spawn_agent.assert_called_once()

    @patch("src.claude_runner.subprocess.run")
    def test_sf_brief(self, mock_run):
        self.orchestrator.sf_init()
        slug = "test-slug"

        # Create discovery structure
        idea_dir = Path(self.test_dir) / "docs" / "shipflow" / "discovery" / slug
        idea_dir.mkdir(parents=True, exist_ok=True)
        (idea_dir / "seed.md").write_text("seed", encoding="utf-8")
        (idea_dir / "questions.md").write_text("questions", encoding="utf-8")
        (idea_dir / "answers.md").write_text("answers", encoding="utf-8")

        # Mock writing the slice files as side effect of spawn_subagent
        def mock_spawn(*args, **kwargs):
            prompt = kwargs.get("task_prompt", "")
            if "discovery-tech-persona" in prompt or "tech" in kwargs.get("agent_file_path", ""):
                (idea_dir / "slice-tech.md").write_text("tech slice", encoding="utf-8")
            elif "discovery-ux-persona" in prompt or "ux" in kwargs.get("agent_file_path", ""):
                (idea_dir / "slice-ux.md").write_text("ux slice", encoding="utf-8")
            elif "discovery-business-persona" in prompt or "business" in kwargs.get("agent_file_path", ""):
                (idea_dir / "slice-business.md").write_text("business slice", encoding="utf-8")

        with patch.object(self.orchestrator.runner, 'spawn_subagent', side_effect=mock_spawn) as mock_spawn_agent:
            brief_path = self.orchestrator.sf_brief(slug)

            self.assertTrue(os.path.exists(brief_path))
            content = Path(brief_path).read_text(encoding="utf-8")
            self.assertIn("tech slice", content)
            self.assertIn("ux slice", content)
            self.assertIn("business slice", content)

            # Should be called for 3 personas + challenger
            self.assertEqual(mock_spawn_agent.call_count, 4)

    @patch("src.claude_runner.subprocess.run")
    def test_sf_check_brief_and_plan(self, mock_run):
        with patch.object(self.orchestrator.runner, 'spawn_subagent') as mock_spawn_agent:
            self.orchestrator.sf_check_brief("dummy_brief.md")
            # Should be called for tech-lead and product-lead
            self.assertEqual(mock_spawn_agent.call_count, 2)

            mock_spawn_agent.reset_mock()
            self.orchestrator.sf_check_plan()
            # Should be called for tech-lead
            self.assertEqual(mock_spawn_agent.call_count, 1)

    @patch("src.claude_runner.subprocess.run")
    def test_sf_spec(self, mock_run):
        with patch.object(self.orchestrator.runner, 'spawn_subagent') as mock_spawn_agent:
            self.orchestrator.sf_spec("dummy_brief.md")
            # Should be called for spec-author and challenger
            self.assertEqual(mock_spawn_agent.call_count, 2)

if __name__ == '__main__':
    unittest.main()
