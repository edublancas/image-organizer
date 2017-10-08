import pytest
from shutil import copyfile, rmtree
from os import listdir, makedirs
from os.path import isfile, join, dirname, realpath, exists
import sys
import glob

from organizer.command_line import main


@pytest.fixture
def sample_input():
    return join(dirname(realpath(__file__)), 'sample_input')


@pytest.fixture
def sample_output():
    return join(dirname(realpath(__file__)), 'sample_output')


def test_files_are_organized_correctly(sample_input, sample_output):
    sample_media = join(dirname(realpath(__file__)), 'sample_media')
    if not exists(sample_output):
        makedirs(sample_output)

    if not exists(sample_input):
        makedirs(sample_input)

    # make a copy of the sample media files
    files = [f for f in listdir(sample_media)
             if isfile(join(sample_media, f)) and not f.startswith('.')]

    for f in files:
        copyfile(join(sample_media, f), join(sample_input, f))

    sys.argv = ['organizer', sample_input, sample_output]
    main()

    # check that files are in the right locations
    res = [f for f in glob.iglob(join(sample_output, '**/**'))
           if isfile(f) and not f.startswith('.')]

    expected = ['Screenshots/screenshot.png',
                'Pictures/picture.jpg',
                'Videos/video.mp4',
                'Generic/generic.jpg',
                'Unknown/unknown.txt']
    expected = [join(sample_output, f) for f in expected]

    assert res == expected


def teardown_function():
    rmtree(sample_input())
    rmtree(sample_output())
