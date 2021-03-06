import pytest
import os
import shutil
from buildtest.tools.file  import is_dir, is_file, create_file, create_dir, walk_tree, string_in_file
from buildtest.tools.log import BuildTestError

@pytest.mark.xfail(raises=BuildTestError)
def test_checking_directory():
    is_dir("/xyz123")

@pytest.mark.xfail(raises=BuildTestError)
def test_checking_file():
    is_file("$HOME/foo+boo.txt")

def test_directory_expansion():
    is_dir("$HOME")
    is_dir("~")

    assert True is os.path.isdir(os.path.expanduser("~"))
    assert True is os.path.isdir(os.path.expandvars("$HOME"))

def test_check_file():
    is_file("~/.profile")
    is_file("$HOME/.profile")

    assert True is os.path.isfile(os.path.expanduser("~/.profile"))
    assert True is os.path.isfile(os.path.expandvars("$HOME/.profile"))

def test_create_file():
    create_file("/tmp/a.txt")
    create_file("$HOME/a.txt")
    create_file("~/b.txt")

    assert True is os.path.isfile("/tmp/a.txt")
    # checking variable expansion
    assert True is os.path.isfile(os.path.expandvars("$HOME/a.txt"))
    # checking ~ expansion
    assert True is os.path.isfile(os.path.expanduser("~/b.txt"))

    os.remove("/tmp/a.txt")
    os.remove(os.path.expandvars("$HOME/a.txt"))
    os.remove(os.path.expanduser("~/b.txt"))

@pytest.mark.xfail(raises=OSError)
def test_fail_create_file():
    create_file("/etc/a.txt")


def test_create_dir():
    create_dir("$HOME/a/b/c")
    create_dir("~/x/y/z")
    assert True is os.path.isdir(os.path.expandvars("$HOME/a/b/c"))
    assert True is os.path.isdir(os.path.expanduser("~/x/y/z"))
    shutil.rmtree(os.path.expandvars("$HOME/a/"))
    shutil.rmtree(os.path.expanduser("~/x/"))

@pytest.mark.xfail(raises=OSError)
def test_fail_create_dir():
    create_dir("/xyz")

def test_walk_tree():
    list_of_files = walk_tree(os.path.join(os.getenv("BUILDTEST_ROOT"),"buildtest"),".py")
    assert len(list_of_files) > 0

@pytest.mark.xfail(raises=BuildTestError)
def test_walk_tree_invalid_dir():
    walk_tree("/xyz",".py")

def test_string_in_file():
    """Testing if string is in file."""
    fname = "a.txt"
    fd = open(fname,"w")
    fd.write("Hello World!")
    fd.close()

    assert string_in_file("Hello",fname)
    assert not string_in_file("Hello!",fname)

