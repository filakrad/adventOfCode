from y2023.utilities import timer


class Module:
    def __init__(self, text):
        name, outs = text.split('->')
        self.name = name.strip()
        self.outs = [x.strip() for x in outs.split(',')]


class Sink(Module):
    def __init__(self, name):
        self.name = name
        self.outs = []
    def get_pulse(self, pulse, input):
        return


class FlipFlop(Module):
    def __init__(self, text):
        super().__init__(text)
        self.state = False

    def get_pulse(self, pulse, input):
        if pulse:
            return
        self.state = not self.state
        return self.state


class Conjunction(Module):
    def __init__(self, text):
        super().__init__(text)
        self.inputs = {}

    def add_input(self, name):
        self.inputs[name] = False

    def get_pulse(self, pulse, input):
        self.inputs[input] = pulse
        if all(self.inputs.values()):
            return False
        return True


class Broadcaster(Module):
    def get_pulse(self, pulse, input):
        return pulse


@timer
def parse(file_name):
    modules = {}
    with open(file_name, 'r') as f:
        for row in f.readlines():
            if row[0] == '%':
                module = FlipFlop(row[1:])
                modules[module.name] = module
            elif row[0] == '&':
                module = Conjunction(row[1:])
                modules[module.name] = module
            else:
                module = Broadcaster(row)
                modules[module.name] = module
    sinks = {}
    for module in modules.values():
        for out in module.outs:
            if out not in modules:
                sinks[out] = Sink(out)
                continue
            if type(modules[out]) is Conjunction:
                modules[out].add_input(module.name)
    modules.update(sinks)
    return modules


@timer
def part01(data):
    lows = 0
    highs = 0
    for _ in range(1000):
        pulses = [('broadcaster', False, None)]
        while pulses:
            pulse = pulses.pop(0)
            if pulse[1]:
                highs += 1
            else:
                lows += 1
            ret = data[pulse[0]].get_pulse(pulse[1], pulse[2])
            if ret is None:
                continue
            for module in data[pulse[0]].outs:
                pulses.append((module, ret, data[pulse[0]].name))
    return lows * highs


def get_state(modules):
    state = []
    for v in modules.values():
        if type(v) is FlipFlop:
            state.append(1 if v.state else 0)
        if type(v) is Conjunction:
            state += [1 if i else 0 for i in v.inputs.values()]
    return ''.join([str(i) for i in state])

@timer
def part02(data):
    presses = 0
    least = [0, 0, 0, 0]
    while True:
        presses += 1
        pulses = [('broadcaster', False, None)]
        while pulses:
            pulse = pulses.pop(0)
            if data[pulse[0]].name == 'rx' and not pulse[1]:
                return presses

            ret = data[pulse[0]].get_pulse(pulse[1], pulse[2])

            # if all of these four are true, 'rx' will be false
            if data[pulse[0]].name == 'dd' and ret:
                least[0] = presses
            if data[pulse[0]].name == 'fh' and ret:
                least[1] = presses
            if data[pulse[0]].name == 'xp' and ret:
                least[2] = presses
            if data[pulse[0]].name == 'fc' and ret:
                least[3] = presses

            if all(least): #should be probably lcm, but during testing I found out they are all primes
                return least[0] * least[1] * least[2] * least[3]

            if ret is None:
                continue
            for module in data[pulse[0]].outs:
                pulses.append((module, ret, data[pulse[0]].name))


if __name__ == "__main__":
    data = parse("data.txt")
    print(part01(data))
    data = parse("data.txt")
    print(part02(data))
