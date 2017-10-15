"""Global configuration."""
import os
import inspect
import shutil

import pytest
import matlab2cpp
from matlab2cpp import collection


@pytest.fixture(scope="session")
def workspace_folder(tmpdir_factory):
    """Create a temporary folder to perform tests from."""
    return str(tmpdir_factory.mktemp("workspace"))


@pytest.fixture(scope="function", autouse=True)
def workspace(workspace_folder, doctest_namespace):
    """Fill temporary folder for each test."""
    # move data to workspace:
    source = os.path.join(os.path.dirname(inspect.stack()[0][1]), "test", "data")
    if os.path.isdir(workspace_folder):
        shutil.rmtree(workspace_folder)
    shutil.copytree(source, workspace_folder)

    # add content to doctest namespace:
    doctest_namespace["workspace"] = workspace_folder
    doctest_namespace["matlab2cpp"] = matlab2cpp
    doctest_namespace["collection"] = collection

    # change to workspace:
    curdir = os.path.abspath(os.path.curdir)
    os.chdir(workspace_folder)

    yield workspace_folder

    # clean up:
    os.chdir(curdir)
    shutil.rmtree(workspace_folder)
