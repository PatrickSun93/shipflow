import unittest
from unittest.mock import patch, MagicMock
from src.orchestrator import ShipflowOrchestrator
import tempfile
import shutil

class TestBuildAndShip(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.shipflow_repo = tempfile.mkdtemp()
        self.orchestrator = ShipflowOrchestrator(
            target_dir=self.test_dir,
            shipflow_repo_path=self.shipflow_repo
        )

    def tearDown(self):
        shutil.rmtree(self.test_dir)
        shutil.rmtree(self.shipflow_repo)

    @patch("src.claude_runner.subprocess.run")
    def test_build_verify_ship_phases(self, mock_run):
        mock_run.return_value = MagicMock(stdout="Mocked claude output", returncode=0)

        with patch.object(self.orchestrator.runner, 'spawn_subagent') as mock_spawn_agent:
            self.orchestrator.sf_build("dummy_story.md")
            self.orchestrator.sf_check_build()
            self.orchestrator.sf_verify("dummy_story.md")
            self.orchestrator.sf_check_ship()
            self.orchestrator.sf_ship()

            self.assertEqual(mock_spawn_agent.call_count, 5)

if __name__ == '__main__':
    unittest.main()
