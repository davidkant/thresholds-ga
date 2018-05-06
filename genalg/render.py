import display

import OSC
import math
import datetime
import time
from threading import Thread

class Renderer:

    def __init__(self, osc_client, py_server, render_params):
        self.osc_client = osc_client
        self.py_server = py_server
        self.render_params = render_params

    def setup(self):
        # foldername
        msg = OSC.OSCMessage()
        msg.setAddress("/render/set_foldername")
        msg.append(self.render_params['foldername'])
        self.osc_client.send(msg)
        # duration
        msg = OSC.OSCMessage()
        msg.setAddress("/render/set_duration")
        msg.append(self.render_params['duration'])
        self.osc_client.send(msg)
        # wait
        msg = OSC.OSCMessage()
        msg.setAddress("/render/set_wait")
        msg.append(self.render_params['wait'])
        self.osc_client.send(msg)
        return self

    def render(self, sample, filename='sample', verbose=True):
        """Ask rs server to render sample."""
        a = datetime.datetime.now()
        rid = '{0}{1}{2}{3}{4}{5}{6}'.format(a.year, a.month, a.day, a.hour,
                                             a.minute, a.second, a.microsecond)
        # store it
        sample.filename = '{0}_{1:02d}'.format(filename, sample.index)
        sample.rid = rid
        # print it
        print('{0}requesting to render: {1}, index: {2}'
              .format(display.TO_RS, sample.rid, sample.index))
        # set filename
        msg = OSC.OSCMessage()
        msg.setAddress('/render/set_filename')
        msg.append(sample.filename)
        self.osc_client.send(msg)
        # set id
        msg = OSC.OSCMessage()
        msg.setAddress('/render/set_id')
        msg.append(sample.rid)
        self.osc_client.send(msg)
        # render 
        time.sleep(0.1)
        msg = OSC.OSCMessage()
        msg.setAddress('/render/quad_with_params')
        msg.append(sample.genotype)
        self.osc_client.send(msg)
        return self

    def render_and_do(self, sample, do_func, func_args, filename='sample', verbose=True):
        """Render sample and do do_func upon completion."""
        self.render(sample, filename=filename, verbose=verbose)
        # function to call upon complete
        def foo(pat, tags, args, source):
            # print('{0}render complete: {1}'.format(display.FRM_RS, sample.rid))
            self.py_server.server.delMsgHandler('/{0}'.format(sample.rid))
            # launch analysis on separate thread
            t = Thread(target=do_func, args=func_args)
            t.start()
        # add to message handler
        self.py_server.server.addMsgHandler('/{0}'.format(sample.rid), foo)
        return self

    def render_and_score(self, sample, filename='sample', verbose=True, deleteme=True):
        """Render and score fitness."""
        self.render_and_do(sample, sample.fitness, (self, deleteme), filename, verbose)
        return self

    def batch_render(self, samples, batch_size=8, deleteme=True):
        """Render samples in groups of batch_size at a time."""
        for bi in range(int(math.floor((len(samples) - 1) / batch_size)) + 1):
            batch = samples[bi * batch_size: min((bi + 1) * batch_size, len(samples))]
            # print('rendering batch {0}'.format(bi))
            for sample in batch:
                self.render_and_score(sample, deleteme=deleteme)
            print('{0}waiting for batch {1}\n'. format(display.WAITING, bi)),
            while any([sample.score is None for sample in batch]): pass
        return self

    def batch_render_single_analysis(self, samples, batch_size=8, deleteme=True):
        """Render samples in groups of batch_size at a time."""
        for bi in range(int(math.floor((len(samples) - 1) / batch_size)) + 1):
            batch = samples[bi * batch_size: min((bi + 1) * batch_size, len(samples))]
            # print('rendering batch {0}'.format(bi))
            notifications = [True]*len(batch)
            def notify_func(index=0):
                notifications[index] = False
            for i,sample in enumerate(batch):
                self.render_and_do(sample, notify_func, (i,))
            print('{0}waiting for batch {1}\n'. format(display.WAITING, bi)),
            while any(notifications): 
                pass
            map(lambda sample: sample.fitness(self), batch)
        return self

    def __repr__(self):
        return '<Renderer()>'.format(self)
