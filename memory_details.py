# import psutil
# from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout
# from PyQt5.QtCore import QTimer
# import pyqtgraph as pg

# class MemoryMonitorWidget(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)

#         layout = QGridLayout(self)
#         self.mem_plot = pg.PlotWidget(title="Memory Usage (%)")
#         self.mem_plot.setYRange(0, 100)
#         self.mem_plot.showGrid(x=True, y=True)
#         self.mem_curve = self.mem_plot.plot(pen='c')
#         layout.addWidget(self.mem_plot, 0, 0, 1, 2)

#         self.details_label = QLabel()
#         layout.addWidget(self.details_label, 1, 0, 1, 2)

#         self.mem_usage_data = [0] * 60

#         self.timer = QTimer()
#         self.timer.timeout.connect(self.update_stats)
#         self.timer.start(1000)

#     def update_stats(self):
#         mem = psutil.virtual_memory()
#         self.mem_usage_data = self.mem_usage_data[1:] + [mem.percent]
#         self.mem_curve.setData(self.mem_usage_data)

#         details = (
#             f"<b>Total:</b> {mem.total / (1024 ** 3):.2f} GB<br>"
#             f"<b>Available:</b> {mem.available / (1024 ** 3):.2f} GB<br>"
#             f"<b>Used:</b> {mem.used / (1024 ** 3):.2f} GB<br>"
#             f"<b>Free:</b> {mem.free / (1024 ** 3):.2f} GB<br>"
#             f"<b>Percent:</b> {mem.percent}%"
#         )
#         self.details_label.setText(details)

# import psutil
# from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout
# from PyQt5.QtCore import QThread, pyqtSignal
# import pyqtgraph as pg
# import time

# class MemoryWorker(QThread):
#     data_updated = pyqtSignal(float, dict)

#     def run(self):
#         while True:
#             mem = psutil.virtual_memory()
#             details = {
#                 'total': mem.total / (1024 ** 3),
#                 'available': mem.available / (1024 ** 3),
#                 'used': mem.used / (1024 ** 3),
#                 'free': mem.free / (1024 ** 3),
#                 'percent': mem.percent
#             }
#             self.data_updated.emit(mem.percent, details)
#             time.sleep(1)


# class MemoryMonitorWidget(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)

#         layout = QGridLayout(self)

#         self.mem_plot = pg.PlotWidget(title="Memory Usage (%)")
#         self.mem_plot.setYRange(0, 100)
#         self.mem_plot.showGrid(x=True, y=True)
#         self.mem_curve = self.mem_plot.plot(pen='c')
#         layout.addWidget(self.mem_plot, 0, 0, 1, 2)

#         self.details_label = QLabel()
#         layout.addWidget(self.details_label, 1, 0, 1, 2)

#         self.mem_usage_data = [0] * 60

#         self.worker_thread = MemoryWorker()
#         self.worker_thread.data_updated.connect(self.update_display)
#         self.worker_thread.start()

#     def update_display(self, percent, details):
#         self.mem_usage_data = self.mem_usage_data[1:] + [percent]
#         self.mem_curve.setData(self.mem_usage_data)

#         details_str = (
#             f"<b>Total:</b> {details['total']:.2f} GB<br>"
#             f"<b>Available:</b> {details['available']:.2f} GB<br>"
#             f"<b>Used:</b> {details['used']:.2f} GB<br>"
#             f"<b>Free:</b> {details['free']:.2f} GB<br>"
#             f"<b>Percent:</b> {details['percent']}%"
#         )
#         self.details_label.setText(details_str)

#     def closeEvent(self, event):
#         self.worker_thread.running = False
#         self.worker_thread.stop()
#         self.worker_thread.quit()
#         self.worker_thread.wait()
#         self.worker_thread.deleteLater()
#         event.accept()


# import psutil
# from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QHBoxLayout, QSizePolicy
# from PyQt5.QtCore import QThread, pyqtSignal, Qt
# import pyqtgraph as pg
# import time

# class MemoryWorker(QThread):
#     data_updated = pyqtSignal(float, dict)
#     def __init__(self):
#         super().__init__()
#         self.total_mem = psutil.virtual_memory().total / (1024 ** 3)
#     def run(self):
#         while True:
#             mem = psutil.virtual_memory()
#             details = {
#                 'total': self.total_mem,
#                 'available': mem.available / (1024 ** 3),
#                 'used': mem.used / (1024 ** 3),
#                 'free': mem.free / (1024 ** 3),
#                 'percent': mem.percent,
#                 'cached': getattr(mem,'cached',mem.available/4) / (1024**3),
#                 'commited': mem.total * mem.percent / 100 / (1024**3)
#             }
#             self.data_updated.emit(mem.percent, details)
#             time.sleep(1)

# class MemoryMonitorWidget(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)

#         self.mem_usage_data = [0] * 60

#         self.worker_thread = MemoryWorker()
#         self.worker_thread.data_updated.connect(self.update_display)
#         self.worker_thread.start()

#         layout = QGridLayout(self)

#         top_label = QHBoxLayout()
#         self.left_label = QLabel("Memory")
#         self.left_label.setStyleSheet("color: white; font-size: 20pt;")
#         self.right_label = QLabel(f"{round(self.worker_thread.total_mem):.1f} GB")
#         self.right_label.setStyleSheet("color: white; font-size: 12pt;")
#         top_label.addWidget(self.left_label, alignment=Qt.AlignLeft)
#         top_label.addWidget(self.right_label, alignment=Qt.AlignRight)
#         layout.addLayout(top_label, 0, 0, 1, 2)

#         # Top labels
#         top_labels = QHBoxLayout()
#         self.top_left_label = QLabel("Memory Usage")
#         self.top_left_label.setStyleSheet("color: white; font-size: 10pt;")
#         self.top_right_label = QLabel(f"{self.worker_thread.total_mem:.1f} GB")
#         self.top_right_label.setStyleSheet("color: white; font-size: 10pt;")
#         top_labels.addWidget(self.top_left_label, alignment=Qt.AlignLeft)
#         top_labels.addWidget(self.top_right_label, alignment=Qt.AlignRight)
#         layout.addLayout(top_labels, 1, 0, 1, 2)

#         # Plot setup
#         self.mem_plot = pg.PlotWidget()
#         self.mem_plot.setBackground('#1C1C1C')
#         self.mem_plot.getPlotItem().showGrid(x=True, y=True, alpha=0.7)
#         self.mem_plot.getPlotItem().showAxis('top', True)
#         self.mem_plot.getPlotItem().showAxis('right', True)
#         self.mem_plot.getPlotItem().getAxis('bottom').setTicks([])
#         self.mem_plot.getPlotItem().getAxis('left').setTicks([])
#         self.mem_plot.getPlotItem().getAxis('top').setTicks([])
#         self.mem_plot.getPlotItem().getAxis('right').setTicks([])
#         self.mem_plot.setYRange(0, 100)
#         self.mem_plot.setMouseEnabled(x=False, y=False)
#         self.mem_plot.setMenuEnabled(False)
#         self.mem_plot.getPlotItem().hideButtons()
#         self.mem_curve = self.mem_plot.plot(pen=pg.mkPen('#32CD32', width=2), fillLevel=0, brush=(50, 205, 50, 80))
#         self.mem_plot.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
#         self.mem_plot.setMinimumHeight(300)
#         self.mem_plot.setMinimumWidth(600)
#         layout.addWidget(self.mem_plot, 2, 0, 1, 2)

#         # Bottom X-axis labels
#         x_label_layout = QHBoxLayout()
#         self.left_x_label = QLabel("60 seconds")
#         self.left_x_label.setStyleSheet("color: #E0E0E0; font-size: 10pt;")
#         self.right_x_label = QLabel("0")
#         self.right_x_label.setStyleSheet("color: #E0E0E0; font-size: 10pt;")
#         x_label_layout.addWidget(self.left_x_label, alignment=Qt.AlignLeft)
#         x_label_layout.addWidget(self.right_x_label, alignment=Qt.AlignRight)
#         layout.addLayout(x_label_layout, 3, 0, 1, 2)

#         composition_label = QHBoxLayout()
#         self.label = QLabel("Memory Composition")
#         self.label.setStyleSheet("color: white; font-size: 10pt;")
#         composition_label.addWidget(self.label, alignment=Qt.AlignLeft)
#         layout.addLayout(composition_label, 4, 0, 1, 2)

#         # Composition graph
#         self.composition_plot = pg.PlotWidget()
#         self.composition_plot.setBackground('#1C1C1C')
#         self.composition_plot.hideAxis('bottom')
#         self.composition_plot.hideAxis('left')
#         self.composition_plot.setMouseEnabled(x=False,y=False)
#         # self.composition_plot.setMaximumHeight(30)
#         # self.composition_plot.setMinimumWidth(600)
#         # self.used_bar = pg.BarGraphItem(x=[0], height=[1], width=0.8, brush=(255,80,80))
#         # self.cached_bar = pg.BarGraphItem(x=[1], height=[1], width=0.8, brush=(255,215,0))
#         # self.available_bar = pg.BarGraphItem(x=[2], height=[1], width=0.8, brush=(80,100,120))
#         # self.composition_plot.addItem(self.used_bar)
#         # self.composition_plot.addItem(self.cached_bar)
#         # self.composition_plot.addItem(self.available_bar)
#         layout.addWidget(self.composition_plot, 5, 0, 1, 2)

#         # Details label
#         self.details_label = QLabel()
#         self.details_label.setStyleSheet("color: #E0E0E0; font-size: 9pt;")
#         self.details_label.setWordWrap(True)
#         layout.addWidget(self.details_label, 6, 0, 1, 2)

#         layout.setRowStretch(0, 0)   
#         layout.setRowStretch(1, 0)  
#         layout.setRowStretch(2, 8)  
#         layout.setRowStretch(3, 0)   
#         layout.setRowStretch(4, 0)
#         layout.setRowStretch(5, 2)
#         layout.setRowStretch(6, 0)

#     def update_display(self, percent, details):
#         self.mem_usage_data = self.mem_usage_data[1:] + [percent]
#         self.mem_curve.setData(self.mem_usage_data)

#         self.composition_plot.clear()
#         used_ratio = details['used']/details['total']
#         cached_ratio = details['cached']/details['total']
#         available_ratio = details['available']/details['total']

#         x_start = 0
#         bar_height = 1
#         self.composition_plot.addItem(pg.QtGui.QGraphicsRectItem(x_start, 0, used_ratio, bar_height))
#         self.composition_plot.items[-1].setBrush(pg.mkBrush('#9C27B0'))

#         x_start += used_ratio
#         self.composition_plot.addItem(pg.QtGui.QGraphicsRectItem(x_start, 0, cached_ratio, bar_height))
#         self.composition_plot.items[-1].setBrush(pg.mkBrush('#BA68C8'))

#         x_start = cached_ratio
#         self.composition_plot.addItem(pg.QtGui.QGraphicsRectItem(x_start, 0, available_ratio, bar_height))
#         self.composition_plot.items[-1].setBrush(pg.mkBrush('#E0E0E0'))
#         # self.used_bar.setOpts(x=[0], height=[used_ratio])
#         # self.cached_bar.setOpts(x=[1], height=[cached_ratio])
#         # self.available_bar.setOpts(x=[2], height=[available_ratio])

#         details_str = (
#             f"<b>Total:</b> {details['total']:.2f} GB<br>"
#             f"<b>Available:</b> {details['available']:.2f} GB<br>"
#             f"<b>Used:</b> {details['used']:.2f} GB<br>"
#             f"<b>Cached:</b> {details['cached']:.2f} GB<br>"
#             f"<b>Usage Percent:</b> {details['percent']}%"
#         )
#         self.details_label.setText(details_str)

#     def closeEvent(self, event):
#         self.worker_thread.terminate()
#         self.worker_thread.wait()
#         event.accept()


import psutil
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QHBoxLayout, QSizePolicy, QGraphicsRectItem
from PyQt5.QtCore import QThread, pyqtSignal, Qt
import pyqtgraph as pg
import time

class MemoryWorker(QThread):
    data_updated = pyqtSignal(float, dict)
    def __init__(self):
        super().__init__()
        self.total_mem = psutil.virtual_memory().total / (1024 ** 3)
    def run(self):
        while True:
            mem = psutil.virtual_memory()
            details = {
                'total': self.total_mem,
                'available': mem.available / (1024 ** 3),
                'used': mem.used / (1024 ** 3),
                'free': mem.free / (1024 ** 3),
                'percent': mem.percent,
                'cached': getattr(mem,'cached',mem.available/4) / (1024**3),
                'committed': mem.total * mem.percent / 100 / (1024**3)
            }
            self.data_updated.emit(mem.percent, details)
            time.sleep(1)

class MemoryMonitorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.mem_usage_data = [0] * 60

        self.worker_thread = MemoryWorker()
        self.worker_thread.data_updated.connect(self.update_display)
        self.worker_thread.start()

        layout = QGridLayout(self)

        top_label = QHBoxLayout()
        self.left_label = QLabel("Memory")
        self.left_label.setStyleSheet("color: white; font-size: 20pt;")
        self.right_label = QLabel(f"{round(self.worker_thread.total_mem):.1f} GB")
        self.right_label.setStyleSheet("color: white; font-size: 12pt;")
        top_label.addWidget(self.left_label, alignment=Qt.AlignLeft)
        top_label.addWidget(self.right_label, alignment=Qt.AlignRight)
        layout.addLayout(top_label, 0, 0, 1, 2)

        # Memory Usage Graph
        self.mem_plot = pg.PlotWidget()
        self.mem_plot.setBackground('#1C1C1C')
        self.mem_plot.getPlotItem().showGrid(x=True, y=True, alpha=0.2)
        self.mem_plot.getPlotItem().hideAxis('bottom')
        self.mem_plot.getPlotItem().hideAxis('left')
        self.mem_plot.setYRange(0, 100)
        self.mem_curve = self.mem_plot.plot(pen=pg.mkPen('#8A2BE2', width=2), fillLevel=0, brush=(138, 43, 226, 80))
        layout.addWidget(self.mem_plot, 1, 0, 1, 2)

        # Memory Composition Bar
        self.composition_plot = pg.PlotWidget()
        self.composition_plot.setBackground('#1C1C1C')
        self.composition_plot.hideAxis('bottom')
        self.composition_plot.hideAxis('left')
        self.composition_plot.setMouseEnabled(x=False, y=False)
        layout.addWidget(self.composition_plot, 2, 0, 1, 2)

        # Details label
        self.details_label = QLabel()
        self.details_label.setStyleSheet("color: #E0E0E0; font-size: 9pt;")
        self.details_label.setWordWrap(True)
        layout.addWidget(self.details_label, 3, 0, 1, 2)

    def update_display(self, percent, details):
        self.mem_usage_data = self.mem_usage_data[1:] + [percent]
        self.mem_curve.setData(self.mem_usage_data)

        self.composition_plot.clear()
        used_ratio = details['used']/details['total']
        cached_ratio = details['cached']/details['total']
        available_ratio = details['available']/details['total']

        self.composition_plot.setYRange(0,1)

        x_start = 0
        bar_height = 1
        used_bar = QGraphicsRectItem(x_start, 0, used_ratio * 10, bar_height)
        used_bar.setBrush(pg.mkBrush('#8A2BE2'))
        self.composition_plot.addItem(used_bar)

        x_start += used_ratio
        cached_bar = QGraphicsRectItem(x_start, 0, cached_ratio * 10, bar_height)
        cached_bar.setBrush(pg.mkBrush('#BA68C8'))
        self.composition_plot.addItem(cached_bar)

        x_start += cached_ratio
        available_bar = QGraphicsRectItem(x_start, 0, available_ratio * 10, bar_height)
        available_bar.setBrush(pg.mkBrush('#E0E0E0'))
        self.composition_plot.addItem(available_bar)

        details_str = (
            f"<b>Total:</b> {details['total']:.2f} GB<br>"
            f"<b>Available:</b> {details['available']:.2f} GB<br>"
            f"<b>Used:</b> {details['used']:.2f} GB<br>"
            f"<b>Cached:</b> {details['cached']:.2f} GB<br>"
            f"<b>Usage Percent:</b> {details['percent']}%"
        )
        self.details_label.setText(details_str)

    def closeEvent(self, event):
        self.worker_thread.terminate()
        self.worker_thread.wait()
        event.accept()
