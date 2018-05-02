import sys
import os
import socket as sock
from random import randint

sys.path.append(os.path.abspath('..'))
import simulator as sim

class VWSimulator(sim.simulator.Simulator):

    def __init__(self, socket, multiplier, **kwargs):
        super().__init__(**kwargs)
        self.socket = socket
        self.multiplier = multiplier

    def calculate_price_floor(self, input_features):
        try:
            line = '| '

            for feature in input_features:
                if str(feature) == 'bid_requests':
                    for request_id in input_features['bid_requests']:
                        line += 'campaign_id' + str(request_id) + ' '
                elif str(feature) == 'r_timestamp':
                    line += 'hour' + str(input_features[str(feature)])[11:13] + ' '
                elif 'num_ads' in str(feature) or 'r_cnt' in str(feature):
                    line += feature + ':' + str(input_features[str(feature)]) + ' '
                else:
                    line += str(feature) + str(input_features[str(feature)]) + ' '

            line = line[:-1] + '\n'
            self.socket.sendall(bytes(line, 'utf-8'))
            prediction = self.socket.recv(1024)
            prediction = prediction[:-1].decode('utf-8')
            return float(prediction) * self.multiplier
        except Exception as e:
            print(e)
            return 0.0001

    def process_line(self, line, input_features, bids):
        pass

def optimal_multiplier(start, end, min_mult, max_mult, increment, file_name):
    revenues = {}
    mult = min_mult
    #file_name = '{0}{1}to{2}{3}'.format(str(start[0] + 1), str(start[1]), str(end[0] + 1), str(end[1]))

    while mult <= max_mult:
        socket_num = randint(10000, 65000)

        os.system("pkill -9 -f 'vw.*--port {0}'".format(socket_num))
        os.system("vw --daemon --port {0} --quiet -i {1}.model -t --num_children 1".format(socket_num, file_name))
        socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        socket.connect(('localhost', socket_num))

        VWSim = VWSimulator(start, end, socket, mult)
        VWSim.run_simulation()
        revenues[mult] = VWSim.stats.total_revenue

        VWSim.socket.close()
        os.system("pkill -9 -f 'vw.*--port {0}'".format(socket_num))

        mult += increment

    return revenues

#print(optimal_multiplier((11, 0), (11, 0), 0.1, 1, 0.1))
