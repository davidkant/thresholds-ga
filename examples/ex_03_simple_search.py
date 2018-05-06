import genalg
import OSC

"""
# a search should consist of:
  - a spec including all parameters and their ranges
  - a randoroams of all parameters searched
  - render params: folder, duration, wait, batch_size
  - ga params: pop size, mutation prob, inbreeding prob
  - ga functions: fitness, weight
"""

m = genalg.model.Model()

m.spec = genalg.spec.ControlSpec()
m.spec.add('koscRA', [0.1, 40.0, 'exp'])
m.spec.add('lowPassPot', [0, 1, 'linear'])
m.spec.add('preAmpPotA', [0, 1, 'linear'])
m.spec.add('powAmpPotA', [0, 1, 'linear'])
m.spec.add('lfoPotA', [0.1, 1, 'linear'])
m.spec.add('vactrolAttackA', [0.001, 0.3, 'exp'])
m.spec.add('vactrolDecayA', [0.01, 3.0, 'exp'])
m.spec.add('vactrolHysteresisA', [0.0, 100.0, 'linear'])

m.randorams = [
    'koscRA', 
    'lowPassPot',
    'preAmpPotA', 
    'powAmpPotA', 
    'lfoPotA', 
    'vactrolAttackA', 
    'vactrolDecayA',
    'vactrolHysteresisA'
]

m.render_params =  {
    'foldername': "/Users/davidkant/Develop/Python Modules/thresholds-ga/search/180505",
    'duration':  20.0,
    'wait': 0.0,
    'batch_size': 8,
}

m.ga_params = {
    'population_size': 16,
    'mutation_prob': 0.1,
    'inbreeding_prob': 0.5
}

m.weight_func = lambda x: x*100 + 1
m.fitness_func = genalg.sonicfeatures.silence_ratio

py_server = genalg.pyserv.PyServer(('127.0.0.1', 57126), 666).start()
osc_client = OSC.OSCClient()
osc_client.connect(('127.0.0.1', 6667))
renderer = genalg.render.Renderer(osc_client, py_server, m.render_params)
ga = genalg.genalg.GeneticAlgorithm(renderer, m)
renderer.setup()

ga.initialize_population_and_render()
for i in range(3):
    ga.evolve_once()

alpha = sorted(ga.population, key=lambda x: x.score)
for x in alpha[-20:]: 
    renderer.render(x, filename='{0}_gen{1}'.format(x.score, x.gen))
