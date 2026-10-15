import unittest


# TODO: JW to implement
# Inside tests/resources, good idea to create a CSV for testing?
# Perhaps create multiple - some with typical data, some erroneous
class TestParser(unittest.TestCase):
    def test_exception_thrown_if_csv_is_rejected(self):
        """
        ValueError should be thrown when the dataset .csv file is
        rejected for any reason.
        """
        self.assertEqual(1, 1)

    def test_correct_total_of_points_generated_from_dataset(self):
        """
        After parsing, the total Point objects in HullInput should
        equal to the total records in the dataset.
        """
        self.assertEqual(1, 1)
