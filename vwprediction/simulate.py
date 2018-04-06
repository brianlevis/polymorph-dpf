import sys
import os

import socket as sock
import time

sys.path.append(os.path.abspath('..'))
import simulator as sim

sim.utils.INPUT_FEATURES.add('campaign_id')

class VWSimulator(sim.simulator.Simulator):

    def calculate_price_floor(self, input_features, prepared_line, line_num, socket):

        campaign_id, site_id, zone_id = 0, 0, 0

        if 'site_id' in input_features:
            site_id = input_features['site_id']
        if 'zone_id' in input_features:
            zone_id = input_features['zone_id']
        if prepared_line['bids']:
            for br in prepared_line['bid_responses']:
                if br['bid_price'] == prepared_line['bids'][0]:
                    campaign_id = br['id']
        else:
            campaign_id = input_features['campaign_id']

        try:
            socket.sendall(bytes('| campaign_id:{0} site_id:{1} zone_id:{2}\n'.format(campaign_id, site_id, zone_id), 'utf-8'))
            prediction = socket.recv(1024)
            prediction = prediction[:-1].decode('utf-8')
            return float(prediction)
        except OSError as ose:
            print(ose)
            return None

    def process_line(self, line, input_features, bids):
        pass

    def run_simulation(self, multiplier, socket, output='normal'):
        line_iterator = sim.utils.get_line_iterator(start=self.start, stop=self.stop, limit=self.limit, download=self.download,
                                          delete=self.delete)
        line_num = 0
        for line in line_iterator:
            line_num += 1
            if line_num % 2 == 0:
                prepared_line = sim.utils.prepare_line(line)
                bids, input_features = prepared_line['bids'], prepared_line['input_features']
                price_floor = self.calculate_price_floor(input_features, prepared_line, line_num, socket)
                if price_floor == None:
                    break
                price_floor *= multiplier
                self.stats.process_line(bids, input_features, price_floor)
        if output != 'none':
            print('Multiplier:' + str(multiplier))
            self.stats.print_stats()

class DefaultSimulator(sim.simulator.Simulator):
    """Represents a static, universal price floor. Note that Polymorph has a default floor of $0.10 CPM,
    but not a universal floor. """

    def calculate_price_floor(self, input_features):
        return sim.simulator.DEFAULT_FLOOR

    def process_line(self, line, input_features, bids):
        pass

def optimal_multiplier(start, end, min_mult, max_mult, increment):
    revenues = []
    mult = min_mult
    file_name = '{0}{1}to{2}{3}'.format(str(start[0] + 1), str(start[1]), str(end[0] + 1), '2')
    while mult <= max_mult:

        VWSim = VWSimulator(start, end)

        os.system("pkill -9 -f 'vw.*--port 12345'")
        os.system("vw --daemon --port 12345 --quiet -i {0}.model -t --num_children 1".format(file_name))
        socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        socket.connect(('localhost', 12345))

        VWSim.run_simulation(mult, socket)
        revenues.append(VWSim.stats.total_revenue)

        socket.close()
        os.system("pkill -9 -f 'vw.*--port 12345'")

        mult += increment
    print(revenues)
    optimum = max(revenues)
    return (optimum, min_mult + increment * revenues.index(optimum))

print(optimal_multiplier((11, 0), (11, 1), 3.2, 4, 0.2))
