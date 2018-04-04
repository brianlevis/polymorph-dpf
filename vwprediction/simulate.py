import sys
import os
sys.path.append(os.path.abspath('..'))
import simulator as sim

"""We tune this to achieve max revenue."""
HYPER_PARAM = 1

sim.utils.INPUT_FEATURES.add('campaign_id')

class VWSimulator(sim.simulator.Simulator):

    def calculate_price_floor(self, input_features):
        #os.system("vw formatted.txt -p prediction.txt")
        #os.remove("prediction.txt")
        os.system("vw --daemon --port 26542 --quiet -i 5_passes.model -t --num_children 1")
        os.system("echo '| campaign_id:{0} site_id:{1} zone_id:{2}' | nc localhost 26542".format(input_features['campaign_id'], input_features['site_id'], input_features['zone_id']))
        os.system("pkill -9 -f 'vw.*--port 26542'")
        price_floor *= HYPER_PARAM
        return price_floor

    def process_line(self, line, input_features, bids):
        pass

def optimal_hyper_param():
    VWSim = VWSimulator((12, 0), (12, 0))
    revenues = []
    while HYPER_PARAM > 0:
        revenues.append(VWSim.run_simulation().stats.total_revenue)
        HYPER_PARAM -= 0.1
    optimum = max(revenues)
    return (optimum, 1 - 0.1 * revenues.index(optimum))

optimal_hyper_param()
