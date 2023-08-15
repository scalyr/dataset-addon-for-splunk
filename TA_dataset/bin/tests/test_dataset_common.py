from unittest import TestCase

class Test(TestCase):
    def test_normalize_time(self):
        dataset_time_nanos = int(1692099758000000000)
        from TA_dataset.bin.dataset_common import normalize_time
        splunk_time_seconds = normalize_time(dataset_time_nanos)
        self.assertEqual(splunk_time_seconds, int(1692099758))

