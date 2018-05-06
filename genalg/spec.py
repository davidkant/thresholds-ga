import math

class ControlSpec: 
    """A very basic SC-style control spec."""

    def __init__(self):
        self.data = dict()

    def add(self, param, spec):
        """Store in dict."""
        self.data[param] = spec

    def map_spec(self, param, val):
        """Map from normal."""
        lo, hi, curve = self.data[param]
        val = self.clip(val, 0.0, 1.0)
        if curve is 'linear':
            return self.linear_map(float(val), float(lo), float(hi))
        if curve is 'exp':
            return self.exp_map(float(val), float(lo), float(hi))

    def unmap_spec(self, param, val):
        """Unmap to normal."""
        lo, hi, curve = self.data[param]
        clip_lo = min(lo, hi)
        clip_hi = max(lo, hi)
        val = self.clip(val, clip_lo, clip_hi)
        if curve is 'linear':
            return self.linear_unmap(float(val), float(lo), float(hi))
        if curve is 'exp':
            return self.exp_unmap(float(val), float(lo), float(hi))

    def linear_map(self, val, lo, hi):
        """Linear mapping."""
        return val * (hi - lo) + lo

    def linear_unmap(self, val, lo, hi):
        """Linear mapping."""
        return (val - lo) / (hi - lo)

    def exp_map(self, val, lo, hi):
        """Exponential mapping."""
        return pow(hi / lo, val) * lo

    def exp_unmap(self, val, lo, hi):
        """Exponential mapping."""
        return math.log(val / lo) / math.log(hi / lo)

    def clip(self, val, lo, hi):
        """Clip to hi and lo."""
        return lo if val < lo else hi if val > hi else val

def default_spec():
    spec = ControlSpec()
    spec.add('koscFreq', [1, 1, 'linear'])
    spec.add('koscError', [0.5, 15, 'linear'])
    spec.add('lowPassPot', [0, 1, 'linear'])
    # --- OSC1 --- 
    # spec.add('koscRA', [0, 40.0, 'linear'])
    spec.add('koscRA', [0.1, 40.0, 'exp'])
    spec.add('preAmpPotA', [0, 1, 'linear'])
    spec.add('powAmpPotA', [0, 1, 'linear'])
    spec.add('lfoPotA', [0.1, 1, 'linear'])
    spec.add('lfoCapSwitchA', [0, 1, 'linear', 1])
    spec.add('lfoIPhaseA', [0, 1, 'linear'])
    spec.add('lfoLowPassPotA', [0, 1, 'linear'])
    spec.add('vactrolScalarA', [0.1, 2.0, 'linear'])
    # spec.add('vactrolAttackA', [0.001, 0.03, 'exp'])
    spec.add('vactrolAttackA', [0.001, 0.3, 'exp'])
    spec.add('vactrolDecayA', [0.01, 3.0, 'exp'])
    spec.add('vactrolHysteresisA', [0.0, 100.0, 'linear'])
    spec.add('vactrolDepthA', [1.0, 6.0, 'linear'])
    spec.add('koscGateA', [0, 1, 'linear', 1])
    spec.add('vactrolGateA', [0, 1, 'linear', 1])
    spec.add('lfoGateA', [0, 1, 'linear', 1])
    # spec.add('fbackXA', [0, 1, 'linear'])
    # spec.add('fbackYA', [0, 1, 'linear'])
    # spec.add('fbackZA', [0, 1, 'linear'])
    spec.add('outXA', [0, 1, 'linear'])
    spec.add('outYA', [0, 1, 'linear'])
    spec.add('outZA', [0, 1, 'linear'])
    spec.add('outX', [0, 1, 'linear']) # need these for master params
    spec.add('outY', [0, 1, 'linear']) # need these for master params
    spec.add('outZ', [0, 1, 'linear']) # need these for master params
    # --- OSC2 --- 2 
    spec.add('koscRB', [0, 40.0, 'linear'])
    spec.add('preAmpPotB', [0, 1, 'linear'])
    spec.add('powAmpPotB', [0, 1, 'linear'])
    spec.add('lfoPotB', [0.1, 1, 'linear'])
    spec.add('lfoCapSwitchB', [0, 1, 'linear', 1])
    spec.add('lfoLowPassPotB', [0, 1, 'linear'])
    spec.add('vactrolScalarB', [0.1, 2.0, 'linear'])
    spec.add('vactrolAttackB', [0.001, 0.03, 'exp'])
    spec.add('vactrolDecayB', [0.01, 3.0, 'exp'])
    spec.add('vactrolHysteresisB', [0.0, 100.0, 'linear'])
    spec.add('vactrolDepthB', [1.0, 6.0, 'linear'])
    spec.add('koscGateB', [0, 1, 'linear', 1])
    spec.add('vactrolGateB', [0, 1, 'linear', 1])
    spec.add('lfoGateB', [0, 1, 'linear', 1])
    # spec.add('fbackXB', [0, 1, 'linear'])
    # spec.add('fbackYB', [0, 1, 'linear'])
    # spec.add('fbackZB', [0, 1, 'linear'])
    spec.add('outXB', [0, 1, 'linear'])
    spec.add('outYB', [0, 1, 'linear'])
    spec.add('outZB', [0, 1, 'linear'])
    return spec

def test_linear():
    spec = ControlSpec()
    spec.add('koscFreq', [1, 99, 'linear'])
    print(spec.map_spec('koscFreq', -0.1) == 1.0)
    print(spec.map_spec('koscFreq', 0.0) == 1.0)
    print(spec.map_spec('koscFreq', 0.5) == 50.0)
    print(spec.map_spec('koscFreq', 1.0) == 99.0)
    print(spec.map_spec('koscFreq', 1.1) == 99.0)
    print(spec.unmap_spec('koscFreq', 0) == 0.0)
    print(spec.unmap_spec('koscFreq', 1) == 0.0)
    print(spec.unmap_spec('koscFreq', 50) == 0.5)
    print(spec.unmap_spec('koscFreq', 99) == 1.0)
    print(spec.unmap_spec('koscFreq', 100) == 1.0)

def test_exp():
    spec.add('koscFreq', [0.001, 100, 'exp'])
    print(spec.map_spec('koscFreq', -0.1) == 0.001)
    print(spec.map_spec('koscFreq', 0.0) == 0.001)
    print(abs(spec.map_spec('koscFreq', 0.5) - 0.316227766017) < 1e-12)
    print(spec.map_spec('koscFreq', 1) == 100.0)
    print(spec.map_spec('koscFreq', 1.1) == 100.0)
    print(spec.unmap_spec('koscFreq', 0.0) == 0.0)
    print(spec.unmap_spec('koscFreq', 0.001) == 0.0)
    print(abs(spec.unmap_spec('koscFreq', 50) - 0.939794000867) <1e-12)
    print(spec.unmap_spec('koscFreq', 100) == 1.0)
    print(spec.unmap_spec('koscFreq', 101) == 1.0)

if __name__ == "__main__":
    test_linear()
    test_exp()
