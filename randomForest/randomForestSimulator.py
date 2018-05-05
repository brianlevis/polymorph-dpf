import tensorflow as tf
import numpy as np

import gzip
import json
import boto3
import os
import random
import time

from simulator.simulator import Simulator


class RandomForestSimulator(Simulator):
    def __init__(self, start=(11, 0), stop=(11, 0), limit=None, download=True, delete=True):
        super().__init__(start, stop, limit, download, delete)
        self.bucket = boto3.resource('s3').Bucket(name="codebase-pm-dpf")
        self.train_data, self.train_labels = self.get_data()
        self.test_data, self.test_labels = self.get_data()
        params = tf.contrib.tensor_forest.python.tensor_forest.ForestHParams(
            num_classes=1,
            num_features=16,
            regression=True
        )
        print("Creating Estimator ...")
        self.classifier = tf.contrib.tensor_forest.client.random_forest.TensorForestEstimator(params, model_dir='./randomForestModel')
        print("finished creating estimator")
        self.classifier.fit(input_fn=self.input_fn)
        y_out = list(self.classifier.predict(x=self.test_data))
        total = 0
        overs = 0
        print("evaluating")
        for i, prediction in enumerate(y_out):
            distance = prediction['scores'] - self.test_labels[i]
            if distance > 0:
                overs += 1
            total += distance
            if i < 10:
                print(prediction['scores'], "vs", self.test_labels[i])
        print(overs / len(y_out), "% over")
        input(total)


    def json_to_features(self, data):
        values = []

        values.append(data.get("ad_type", [""])[0])
        values.append(data.get("geo_country_code2", ""))
        values.append(data.get("rate_metric", ""))
        values.append(str(data.get("site_id", "")))
        values.append(data.get("geo_timezone", ""))
        values.append(data.get("ua_device_type", ""))
        values.append(str(len(data.get("bid_requests", []))))
        values.append(data.get("ua_os", ""))
        values.append(str(data.get("zone_id", "")))
        values.append(data.get("geo_continent_code", ""))
        values.append(data.get("ua_os_name", ""))
        values.append(data.get("ua_device", ""))
        values.append(data.get("ua_name", ""))
        values.append(str(data.get("geo_area_code", "")))
        values.append(data.get("geo_city_name", ""))
        values.append(str(data.get("r_timestamp", data.get("i_timestamp", "1T15")).split("T")[1][:2]))

        return values

    def get_data(self):
        train_data = []
        train_labels = []
        file_keys = []
        for _ in range(20):
            file_keys.append("%02d/%02d/part-00%03d.gz" % (random.randint(11, 14), random.randint(0, 23), random.randint(0, 127)))
        for file_key in file_keys:
            print(file_key)
            self.bucket.download_file(Key=file_key, Filename="input.gz")
            with gzip.open("input.gz", 'rt') as f:
                lines = f.readlines()
            for line in lines:
                data = json.loads(line)
                values = self.json_to_features(data)
                if len(data["bid_responses"]) == 0:
                    continue
                if len(data["bid_responses"]) == 1:
                    label = data["bid_responses"][0]["bid_price"] / 2
                else:
                    bids = sorted([x["bid_price"] for x in data["bid_responses"]])
                    label = bids[-2] + (bids[-1] - bids[-2]) / 2

                train_data.append(values)
                train_labels.append(label)
            os.remove("input.gz")
        return np.array(train_data), np.array(train_labels)

    def input_fn(self):
        return tf.convert_to_tensor(self.train_data), tf.convert_to_tensor(self.train_labels)

    def calculate_price_floor(self, input_features):
        start = time.time()
        values = self.json_to_features(input_features) 
        y_out = self.classifier.predict(x=np.array([values]))
        print(time.time()-start)
        return list(y_out)[0]['scores']

    def process_line(self, line, input_features, bid):
        pass


if __name__ == "__main__":
    randomForestSimulator = RandomForestSimulator(limit=1)

    randomForestSimulator.run_simulation()
