import sys
import os
sys.path.append(os.path.abspath('..'))
import simulator as sim

"""We tune this to achieve max revenue."""
HYPER_PARAM = 1

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
        os.system("vw --daemon --port 26542 --quiet -i 5_passes.model -t --num_children 1")
        os.system("echo '| campaign_id:{0} site_id:{1} zone_id:{2}' | nc localhost 26542".format(campaign_id, site_id, zone_id))
        os.system("pkill -9 -f 'vw.*--port 26542'")
        price_floor *= HYPER_PARAM
        return price_floor

    def process_line(self, line, input_features, bids):
        pass

    def run_simulation(self, output='normal'):
        line_iterator = get_line_iterator(start=self.start, stop=self.stop, limit=self.limit, download=self.download,
                                          delete=self.delete)
        for line in line_iterator:
            prepared_line = prepare_line(line)
            bids, input_features = prepared_line['bids'], prepared_line['input_features']
            price_floor = self.calculate_price_floor(input_features, prepared_line)
            self.stats.process_line(bids, input_features, price_floor)
            self.process_line(line, input_features, bids)
        if output != 'none':
            self.stats.print_stats()

def optimal_hyper_param():
    VWSim = VWSimulator((12, 0), (12, 0))
    revenues = []
    while HYPER_PARAM > 0:
        revenues.append(VWSim.run_simulation().stats.total_revenue)
        HYPER_PARAM -= 0.1
    optimum = max(revenues)
    return (optimum, 1 - 0.1 * revenues.index(optimum))

optimal_hyper_param()
