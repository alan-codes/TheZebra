#! /usr/bin/python

import unittest
import os
import csv
import logging
import aggregator as aggr

logging.disable(logging.CRITICAL)

class testDataValidation(unittest.TestCase):

    def setUp(self):
        self.home = os.path.join(aggr.INPUT_DIR,
                                 'Homework - Home Insurance.csv')
        self.auto = os.path.join(aggr.INPUT_DIR,
                                 'Homework - Auto Insurance.csv')

        self.home_fields, self.auto_fields = [], []
        self.full_match, self.empty_pn, self.empty_addr = {}, {}, {}

        with open(self.home, "r") as h, open(self.auto, "r") as a:
            home_reader = csv.DictReader(h)
            auto_reader = csv.DictReader(a)

            # Get Headers
            self.home_fields.extend(home_reader.fieldnames)
            self.auto_fields.extend(auto_reader.fieldnames)

            # Get fields
            count = 2
            for row in home_reader:
                if count == 2:
                    self.full_match = row
                elif count == 4:
                    self.empty_addr = row
                elif count == 5:
                    self.empty_pn = row

                count += 1


    def testValidateHeaders(self):
        # Extra Fields
        self.assertTrue(
            aggr.validate_headers(self.home_fields, 'test', logging))
        # Exact Fields
        self.assertTrue(
            aggr.validate_headers(self.auto_fields, 'test', logging))
        # Missing Fields
        self.assertFalse(
            aggr.validate_headers([], 'test', logging))

    def testValidateFields(self):
        # Full Match with double quote cleanup
        expected = {'Redirect Link': 'homerus.com', 'CampaignID': 'HOME',
                    'TestColumn': 'testColumn', 'Phone Number': '1234567',
                    'Cost Per Ad Click': 5.0, 'Zipcode': '78705',
                    'Provider Name': "Home R' Us", 'Address': 'Tim Street'}
        valid, row = aggr.validate_data(self.full_match, 0, 'test', logging)
        self.assertTrue(valid)
        # test string to float for float field
        self.assertEqual(row['Cost Per Ad Click'], 5.0)
        # remove triple double quotes
        self.assertEqual(row['Zipcode'], '78705')
        # test full match
        self.assertEqual(row, expected)

        # Missing Nullable Field - Phone Number. Writes to file
        valid, row = aggr.validate_data(self.empty_pn, 0, 'test', logging)
        self.assertTrue(valid)

        # Missing Non-Nullable Field - Address. Skips line
        valid, row = aggr.validate_data(self.empty_addr, 0, 'test', logging)
        self.assertFalse(valid)

        # Corrupt field - {Cost Per Ad Click': 'five'}
        corrupt = {'Redirect Link': 'homerus.com', 'CampaignID': 'HOME',
                   'TestColumn': 'testColumn', 'Phone Number': '1234567',
                   'Cost Per Ad Click': 'five', 'Zipcode': '78705',
                   'Provider Name': "Home R' Us", 'Address': 'Tim Street'}
        valid, row = aggr.validate_data(corrupt, 0, 'test', logging)
        self.assertFalse(valid)

if __name__ == '__main__':
    unittest.main()
