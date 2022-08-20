from pathlib import Path

from base_tool import BaseTool
from util import subprocess_run, run_bash_command_with_output


class Pytest(BaseTool):
    def _create_virtual_environment(self):
        env_name = "env"
        create_env_command = f"python -m venv {env_name}"
        subprocess_run(create_env_command, cwd=str(self.directory))

        print("Activating virtual environment...")

        # activate_env_command = f"source {env_name}/bin/activate"
        activate_env_command = f". {env_name}/bin/activate"
        run_bash_command_with_output(activate_env_command, cwd=str(self.directory), shell=True)

    def _deactivate_virtual_environment(self):
        print("Deactivating virtual environment...")
        activate_env_command = ". deactivate"
        run_bash_command_with_output(activate_env_command, cwd=str(self.directory), shell=True)

    def setup(self):
        self._create_virtual_environment()
        requirements_file = Path(self.directory / "requirements.txt")

        # if pipfile.exists():
        #     # Install all dependencies for a project (including dev ones)
        #     command = "pipenv install --dev"
        #     # By installing, pipenv creates a virtual environment and installs all dependencies
        #     run_bash_command_with_output(command, cwd=str(pipfile.parent), shell=True)

        install_pytest = "pip install pytest"
        run_bash_command_with_output(install_pytest, cwd=str(self.directory), shell=True)

        if requirements_file.exists():
            print(f"> Installing dependencies from requirements.txt")
            command = "pip install -r requirements.txt"
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
        run_bash_command_with_output(command, cwd=str(self.directory), shell=True)
