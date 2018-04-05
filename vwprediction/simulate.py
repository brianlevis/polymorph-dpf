import sys
import os
import subprocess
import socket as sock
sys.path.append(os.path.abspath('..'))
import simulator as sim

sim.utils.INPUT_FEATURES.add('campaign_id')

class VWSimulator(sim.simulator.Simulator):

    def calculate_price_floor(self, input_features, prepared_line):
        #os.system("vw formatted.txt -p prediction.txt")
        #os.remove("prediction.txt")
        campaign_id, site_id, zone_id = 0, 0, 0

        if 'site_id' in input_features:
            site_id = input_features['site_id']
        if 'zone_id' in input_features:
            zone_id = input_features['zone_id']
        if prepared_line['bids']:
            for br in prepared_line['bid_responses']:
                if br['bid_price'] == prepared_line['bids'][0]:
                    campaign_id = br['id']
        #print(prepared_line)
        print(campaign_id, site_id, zone_id)
        #os.system("vw --daemon --port 26542 --quiet -i 5_passes.model -t --num_children 1", stdout=subprocess.PIPE)
        #prediction = subprocess.check_output("| campaign_id:{0} site_id:{1} zone_id:{2}".format(campaign_id, site_id, zone_id), shell=True).communicate()[0]

        #prediction = subprocess.Popen("| campaign_id:{0} site_id:{1} zone_id:{2}".format(campaign_id, site_id, zone_id), shell=True, stdout=subprocess.PIPE, executable='/bin/bash')
        #prediction = prediction.stdout.read().decode("utf-8")
        socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        socket.connect(('localhost', 12345))
        socket.sendall(bytes('| campaign_id:{0} site_id:{1} zone_id:{2}\n'.format(campaign_id, site_id, zone_id), 'utf-8'))
        prediction = socket.recv(1024)
        socket.shutdown(sock.SHUT_RDWR)
        prediction = prediction[:-1].decode('utf-8')
        print(prediction)
        #price_floor = HYPER_PARAM * float(price_floor)
        return float(prediction)

    def process_line(self, line, input_features, bids):
        pass

    def run_simulation(self, hyper_param, output='normal'):
        line_iterator = sim.utils.get_line_iterator(start=self.start, stop=self.stop, limit=self.limit, download=self.download,
                                          delete=self.delete)
        for line in line_iterator:
            prepared_line = sim.utils.prepare_line(line)
            bids, input_features = prepared_line['bids'], prepared_line['input_features']
            price_floor = hyper_param * self.calculate_price_floor(input_features, prepared_line)
            self.stats.process_line(bids, input_features, price_floor)
            self.process_line(line, input_features, bids)
        if output != 'none':
            self.stats.print_stats()

def optimal_hyper_param():
    VWSim = VWSimulator((12, 0), (12, 0))
    revenues = []
    HYPER_PARAM = 1
    while HYPER_PARAM > 0:
        os.system("pkill -9 -f 'vw.*--port 12345'")
        os.system("vw --daemon --port 12345 --quiet -i 1_pass.model -t --num_children 1")
        #os.system("nc localhost 26542")
        revenues.append(VWSim.run_simulation(HYPER_PARAM).stats.total_revenue)
        os.system("pkill -9 -f 'vw.*--port 12345'")
        HYPER_PARAM -= 0.1
    optimum = max(revenues)
    return (optimum, 1 - 0.1 * revenues.index(optimum))

print(optimal_hyper_param())
