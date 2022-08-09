from pathlib import Path

from base_tool import BaseTool
from util import subprocess_run, run_bash_command_with_output


class Pytest(BaseTool):
    def _create_virtual_environment(self):
        env_name = "env"
        create_env_command = f"python3 -m venv {env_name}"
        subprocess_run(create_env_command, cwd=str(self.directory))

        activate_env_command = f"source {env_name}/bin/activate"
        run_bash_command_with_output(activate_env_command, cwd=str(self.directory), shell=True)

    def _deactivate_virtual_environment(self):
        activate_env_command = "deactivate"
        run_bash_command_with_output(activate_env_command, cwd=str(self.directory), shell=True)

    def setup(self):
        self._create_virtual_environment()

        requirements_file = Path(self.directory / "requirements.txt")

        if requirements_file.exists():
            print(f"> Installing dependencies from requirements.txt")
            command = "pip install -r requirements.txt"
            subprocess_run(command, cwd=str(requirements_file.parent))
        else:
            print(f"> Requirements file not found. Installing package...")

            # Install packages that were breaking the tests
            install_pytest = "pip3 install pytest"
            run_bash_command_with_output(install_pytest, cwd=str(self.directory), shell=True)

            install_pytest = "pip3 install hypothesis"
            run_bash_command_with_output(install_pytest, cwd=str(self.directory), shell=True)

            command = "pip3 install git+%(url)s" % {"url": self.project_url}
            run_bash_command_with_output(command, cwd=str(requirements_file.parent), shell=True)

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
