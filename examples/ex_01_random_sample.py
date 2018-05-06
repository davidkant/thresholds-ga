import genalg
import OSC

py_server = genalg.pyserv.PyServer(('127.0.0.1', 57126), 666).start()
osc_client = OSC.OSCClient()
osc_client.connect(('127.0.0.1', 6667))

render_params =  {
    'foldername': "/Users/davidkant/Develop/Python Modules/thresholds-ga/search/180505",
    'duration':  20.0,
    'wait': 0.0,
    'batch_size': 8,
}
renderer = genalg.render.Renderer(osc_client, py_server, render_params)
renderer.setup()

paramspec = genalg.spec.default_spec()
randorams = [
    'koscRA', 
    'lowPassPot',
    'preAmpPotA', 
    'powAmpPotA', 
    'lfoPotA', 
    'vactrolAttackA', 
    'vactrolDecayA',
    'vactrolHysteresisA'
]

x = genalg.sample.Sample.random_sample(0, randorams, paramspec)
# callback to be executed upon render complete turns off the pyhon server
def thnx(): 
    print 'thanks rust!'
    py_server.stop()
x.render_and_do(renderer, thnx, [], 'chaosmusic')
