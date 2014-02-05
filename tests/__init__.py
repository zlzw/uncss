import os.path
from discover import DiscoveringTestLoader


def get_tests():
    start_dir = os.path.dirname(__file__) + '/unit/'
    test_loader = DiscoveringTestLoader()
    return test_loader.discover(start_dir, pattern="test_*.py")