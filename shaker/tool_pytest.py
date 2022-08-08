from pathlib import Path
import subprocess

from base_tool import BaseTool
from util import subprocess_run


class Pytest(BaseTool):
    def _create_virtual_environment(self):
        env_name = "env"
        create_env_command = f"python3 -m venv {env_name}"
        subprocess_run(create_env_command, cwd=str(self.directory))

        activate_env_command = f"sudo source {env_name}/bin/activate"
        subprocess_run(activate_env_command, cwd=str(self.directory))

    def _deactivate_virtual_environment(self):
        activate_env_command = "deactivate"
        subprocess_run(activate_env_command, cwd=str(self.directory))

    def setup(self):
        self._create_virtual_environment()

        requirements_file = Path(self.directory / "requirements.txt")

        if requirements_file.exists():
            print(f"> Installing dependencies from requirements.txt")
            command = "pip install -r requirements.txt"
            subprocess_run(command, cwd=str(requirements_file.parent))
        else:
            print(f"> Requirements file not found. Installing package...")
            command = f"pip install git+{self.project_url}"
            subprocess_run(command, cwd=str(requirements_file.parent))

    def tear_down(self):
        self._deactivate_virtual_environment()

    def run_tests(self, report_folder):
        report_file = report_folder / "TEST-pytest.xml"
        tests_path = self.specific_tests_path or ""

        command = f"pytest {tests_path} --junitxml {report_file.absolute()}"
        command = command.replace("  ", " ")
        
        # pytest Test_filename::Test_classname::Test_funcname --junitxml {}
        print(f"> {command}")
        subprocess_run(command, cwd=str(self.directory))
