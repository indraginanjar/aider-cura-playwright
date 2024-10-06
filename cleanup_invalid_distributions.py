import pkg_resources
import subprocess
import sys

def cleanup_invalid_distributions():
    # Get the list of installed distributions
    installed_packages = pkg_resources.working_set
    for package in installed_packages:
        try:
            # Attempt to uninstall the package
            subprocess.check_call([sys.executable, '-m', 'pip', 'uninstall', '-y', package.project_name])
            print(f"Uninstalled {package.project_name}")
        except Exception as e:
            print(f"Failed to uninstall {package.project_name}: {e}")

if __name__ == "__main__":
    cleanup_invalid_distributions()
