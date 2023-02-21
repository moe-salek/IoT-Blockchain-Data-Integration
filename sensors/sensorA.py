from utils.csv_reader import read_csv_data_loop


class SensorA:

    def __init__(self, dataset_csv_filepath):
        self.dataset_csv_filepath = dataset_csv_filepath

    def get_data_from_dataset(self):
        return read_csv_data_loop(self.dataset_csv_filepath)
