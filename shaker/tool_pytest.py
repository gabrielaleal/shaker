from pathlib import Path

from base_tool import BaseTool
from util import subprocess_run


class Pytest(BaseTool):
    def setup(self):
        requirements_file = Path(self.directory / "requirements.txt")
        pipfile = Path(self.directory / "Pipfile")

        print("Pytest tool setup")
        import pdb; pdb.set_trace()

        if requirements_file.exists():
            print(f"> Installing requirements from requirements.txt...")
            command = "pip install -r requirements.txt"
            subprocess_run(command, cwd=str(requirements_file.parent))
        elif pipfile.exists():
            print(f"> Installing requirements from Pipfile")
            command = "pip install -r requirements.txt"
            subprocess_run("pipenv lock -r", cwd=str(requirements_file.parent))
            subprocess_run(command, cwd=str(requirements_file.parent))


    def run_tests(self, report_folder):
        report_file = report_folder / "TEST-pytest.xml"

        command = f"pytest {self.specific_tests_path} --junitxml {report_file.absolute()}"
        
        # pytest Test_filename::Test_classname::Test_funcname --junitxml {}
        print(f"> {command}")
        subprocess_run(command, cwd=str(self.directory))
