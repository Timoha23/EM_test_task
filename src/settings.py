import os


PHONEBOOK_NAME = "phonebook.txt"
PHONEBOOK_PATH = os.path.join(os.path.dirname(__file__), PHONEBOOK_NAME)

TEST_PHONEBOOK_NAME = "test_phonebook.txt"
TEST_PHONEBOOK_PATH = os.path.join(
    os.path.dirname(__file__),
    TEST_PHONEBOOK_NAME
)

ITEMS_ON_PAGE = 10
