import sys
import os
import socket as sock

sys.path.append(os.path.abspath('..'))
import simulator as sim

class VWSimulator(sim.simulator.Simulator):

    def __init__(self, start, end, socket, multiplier, **kwargs):
        super().__init__(start, end, **kwargs)
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
                    line += 'r_timestamp' + input_features[str(feature)].replace(':', '-') + ' '
                else:
                    line += str(feature) + str(input_features[str(feature)]) + ' '

            line = line[:-1] + '\n'
            self.socket.sendall(bytes(line, 'utf-8'))
            prediction = self.socket.recv(1024)
            prediction = prediction[:-1].decode('utf-8')
            return float(prediction) * self.multiplier
        except OSError as ose:
            print(ose)
            return 0.0001

    def process_line(self, line, input_features, bids):
        pass

def optimal_multiplier(start, end, min_mult, max_mult, increment):
    revenues = {}
    mult = min_mult
    file_name = '{0}{1}to{2}{3}'.format(str(start[0] + 1), str(start[1]), str(end[0] + 1), str(end[1]))

    while mult <= max_mult:

        os.system("pkill -9 -f 'vw.*--port 12345'")
        os.system("vw --daemon --port 12345 --quiet -i {0}.model -t --num_children 1".format(file_name))
        socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        socket.connect(('localhost', 12345))

        VWSim = VWSimulator(start, end, socket, mult, limit=32)
        VWSim.run_simulation()
        revenues[mult] = VWSim.stats.total_revenue

        VWSim.socket.close()
        os.system("pkill -9 -f 'vw.*--port 12345'")

        mult += increment

    print(revenues)
    optimum = max(revenues)
    return (optimum, min_mult + increment * revenues.index(optimum))

print(optimal_multiplier((11, 0), (11, 0), 0.1, 0.9, 0.2))
