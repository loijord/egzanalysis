from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

class Cubeview:
    X = np.array([[[0, 0, 0], [0, 1, 0], [1, 1, 0], [1, 0, 0]],
                  [[0, 0, 0], [0, 0, 1], [1, 0, 1], [1, 0, 0]],
                  [[1, 0, 1], [1, 0, 0], [1, 1, 0], [1, 1, 1]],
                  [[0, 0, 1], [0, 0, 0], [0, 1, 0], [0, 1, 1]],
                  [[0, 1, 0], [0, 1, 1], [1, 1, 1], [1, 1, 0]],
                  [[0, 1, 1], [0, 0, 1], [1, 0, 1], [1, 1, 1]]]).astype(float)

    def __init__(self, cubes_xyz=[], size_info=(1, 1, 1), translate_info=(0, 0, 0)):
        self.cubes_xyz = cubes_xyz  # cube indexes estimated to be np.arrays
        self.size_info = size_info  # their size
        self.translate_info = translate_info  # their starting position
        self.event_handle = False

    @staticmethod
    def vectorised_sum(a,b): return np.array([np.sum([a,n],axis=0) for n in b])

    @staticmethod
    def vectorised_prod(a, b): return np.array([np.prod([a, n], axis=0) for n in b])

    @staticmethod
    def _fix_view(scalefactor=1.5, ax=None):
        bbox = np.array([getattr(ax, 'get_{}lim'.format(dim))() for dim in 'xyz'])
        bbox_center = np.mean(bbox, axis=1)
        bbox_dim = np.max(bbox, axis=1) - np.min(bbox, axis=1)
        scaling_factors = scalefactor * bbox_dim / np.max(bbox_dim)
        tr1, tr2, tr3 = bbox_center
        s1, s2, s3 = scaling_factors
        A = np.array([[1, 0, 0, -tr1], [0, 1, 0, -tr2], [0, 0, 1, -tr3], [0, 0, 0, 1]])
        T = np.array([[s1, 0, 0, 0], [0, s2, 0, 0], [0, 0, s3, 0], [0, 0, 0, 1]]) #replace s3 with 2*s3 sometimes
        B = np.array([[1, 0, 0, tr1], [0, 1, 0, tr2], [0, 0, 1, tr3], [0, 0, 0, 1]])
        ax.get_proj = lambda: np.dot(np.dot(np.dot(Axes3D.get_proj(ax), B), T), A)

    def add_preview(self, fig=None, block=True, closing=True):
        if fig is None:
            raise AttributeError('fig parameter required')
        def onclose(event): fig.canvas.stop_event_loop()
        fig.show()
        if block:
            fig.canvas.mpl_connect('close_event', onclose)
            fig.canvas.start_event_loop()
        if closing: plt.close(fig)

    def cuboid_data(self):
        translation = self.cubes_xyz.min(axis=0)  # translation vector of cube
        translated_locii = self.cubes_xyz - translation  # every cube is pushed so that its corner stands at (0,0,0)
        scaled_locii = translated_locii * self.size_info
        extended_locii = self.translate_info + scaled_locii
        data = self.vectorised_sum((self.X + translation) * self.size_info,  extended_locii)
        return data

    def set_lims(self, mode='fitted', ax=None, on_last=False):
        if on_last:
            lim0 = np.min(ax.collections[-1]._vec[:3], axis=1)
            lim1 = np.max(ax.collections[-1]._vec[:3], axis=1)
        else:
            lim0 = np.min(np.array([np.min(pc._vec[:3], axis=1) for pc in ax.collections]), axis=0)
            lim1 = np.max(np.array([np.max(pc._vec[:3], axis=1) for pc in ax.collections]), axis=0)
        bound = lim1 - lim0
        if mode == 'normal':
            (xlim, ylim, zlim) = zip(lim0, lim0 + np.repeat(np.max(bound), 3))
        if mode == 'fitted':
            (xlim, ylim, zlim) = zip(lim0, lim0 + bound)
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        ax.set_zlim(zlim)

    def voxplot(self, facecolors, edgecolors='none', labels=None, ax=None, mode = 'fitted', fontsize=18, textcolor='#999999', focus=False, zorder=1):
        data = self.cuboid_data()
        pc = Poly3DCollection(np.concatenate(data), facecolors=np.repeat(facecolors, 6, axis=0),
                                edgecolors=np.repeat(edgecolors, 6, axis=0), zorder=zorder)
        ax.add_collection3d(pc)
        self.set_lims(mode=mode, ax=ax, on_last=focus)
        if labels is not None:
            positions = iter(np.mean(data[:,-1,:,:], axis=1))
            for n in labels: ax.text(*next(positions), n, zorder=100, fontsize=fontsize, color=textcolor)
        #self._fix_view(ax=ax)
        return self.get_focus(ax=ax)

    def get_focus(self, ax=None): return (ax.get_xlim(), ax.get_ylim(), ax.get_zlim())

    def set_focus(self, fc, ax=None):
        ax.set_xlim(fc[0])
        ax.set_ylim(fc[1])
        ax.set_zlim(fc[2])
        self._fix_view(ax=ax)

    def wait_for_event(self, event, koef=35, ax=None, fig=None):
        if event.key in ["up", "down", "right", "left", "ctrl+down", "ctrl+up"]:
            # taken from https://github.com/matplotlib/matplotlib/issues/110
            ax.autoscale(enable=False, axis='both')  # I have no idea, it this line have some effect at all
            ## Set nearly similar speed of motion in dependency on zoom
            xkoef = (ax.get_xbound()[0] - ax.get_xbound()[1]) / koef
            ykoef = (ax.get_ybound()[0] - ax.get_ybound()[1]) / koef
            zkoef = (ax.get_zbound()[0] - ax.get_zbound()[1]) / koef
            if event.key == "up":
                ax.set_ybound(ax.get_ybound()[0] + xkoef, ax.get_ybound()[1] + xkoef)
            elif event.key == "down":
                ax.set_ybound(ax.get_ybound()[0] - xkoef, ax.get_ybound()[1] - xkoef)
            elif event.key == "right":
                ax.set_xbound(ax.get_xbound()[0] + ykoef, ax.get_xbound()[1] + ykoef)
            elif event.key == "left":
                ax.set_xbound(ax.get_xbound()[0] - ykoef, ax.get_xbound()[1] - ykoef)
            elif event.key == "ctrl+down":
                ax.set_zbound(ax.get_zbound()[0] - zkoef, ax.get_zbound()[1] - zkoef)
            elif event.key == "ctrl+up":
                ax.set_zbound(ax.get_zbound()[0] + zkoef, ax.get_zbound()[1] + zkoef)
            fig.canvas.draw()
        else:
            self.event_handle = event.key
            fig.canvas.stop_event_loop()



#fig = plt.figure('inspection')

'''fig = plt.figure()
fig.canvas.mpl_connect("key_press_event", Cubeview().move_view)
fig.canvas.mpl_connect("key_press_event", Cubeview().register_view)
ax = fig.gca(projection='3d')

vvx = Cubeview(np.array([[1, 2, 3], [2, 3, 4], [6, 4, 5], [1, 4, 5], [3, 7, 1]]), (12, 12, 12), (1, 1, 1))
vvx.voxplot(ax=ax, facecolors='green', edgecolors='purple', labels = range(5))

vvx2 = Cubeview(np.array([[-1,-1,-1], [-2,-2,-2]]), (12, 12, 12), (1, 1, 1))
vvx2.voxplot(ax=ax, facecolors='red', edgecolors='purple')

#mng = plt.get_current_fig_manager()
#mng.window.state('zoomed')
plt.show()'''