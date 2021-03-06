# This is where the optimization is done.
import tkinter as tk
from _tkinter import TclError
from tkinter.ttk import Progressbar
import ANYstructure.optimize as op
import numpy as np
import time
from tkinter import messagebox
import ANYstructure.example_data as test
from ANYstructure.helper import *
import copy

class CreateOptimizeMultipleWindow():
    '''
    This class initiates the MultiOpt window.
    '''

    def __init__(self, master, app=None):
        super(CreateOptimizeMultipleWindow, self).__init__()
        if __name__ == '__main__':
            self._load_objects = {}
            self._load_comb_dict = {}
            self._line_dict = test.get_line_dict()
            self._load_count = 0
            self._point_dict = test.get_point_dict()
            self._canvas_scale = 25
            self._line_to_struc = test.get_line_to_struc()
            self._opt_frames = {}
            self._active_points = ['point1','point4','point8','point5']
        else:
            self.app = app
            self._load_objects = app._load_dict
            self._load_comb_dict = app._new_load_comb_dict
            self._line_dict = app._line_dict
            self._load_count = 0
            self._point_dict = app._point_dict
            self._canvas_scale = app._canvas_scale
            self._line_to_struc = app._line_to_struc
            self._opt_frames = {}
            self._active_points = []

        self._opt_structure = {}
        self._opt_frames_obj = []
        self._frame = master
        self._frame.wm_title("Optimize structure")
        self._frame.geometry('1800x950')
        self._frame.grab_set()
        self._canvas_origo = (50, 720 - 50)

        self._active_lines = []
        self._add_to_lines = True
        self._lines_add_to_load = []
        self._active_point = None
        self._point_is_active = False

        # ----------------------------------COPIED FROM OPTIMIZE_WINDOW----------------------------------------------- #

        self._opt_resutls = {}
        self._opt_actual_running_time = tk.Label(self._frame, text='')

        tk.Frame(self._frame, width=770, height=5, bg="grey", colormap="new").place(x=20, y=95)
        tk.Frame(self._frame, width=770, height=5, bg="grey", colormap="new").place(x=20, y=135)

        algorithms = ('anysmart', 'random', 'random_no_delta', 'anydetail', 'pso')

        tk.Label(self._frame, text='-- Structural optimizer for multiple selections --',
                 font='Verdana 15 bold').place(x=10, y=10)

        # upper and lower bounds for optimization
        # [0.6, 0.012, 0.3, 0.01, 0.1, 0.01]
        self._new_spacing_upper = tk.DoubleVar()
        self._new_spacing_lower = tk.DoubleVar()
        self._new_pl_thk_upper = tk.DoubleVar()
        self._new_pl_thk_lower = tk.DoubleVar()
        self._new_web_h_upper = tk.DoubleVar()
        self._new_web_h_lower = tk.DoubleVar()
        self._new_web_thk_upper = tk.DoubleVar()
        self._new_web_thk_lower = tk.DoubleVar()
        self._new_fl_w_upper = tk.DoubleVar()
        self._new_fl_w_lower = tk.DoubleVar()
        self._new_fl_thk_upper = tk.DoubleVar()
        self._new_fl_thk_lower = tk.DoubleVar()
        self._new_span = tk.DoubleVar()
        self._new_width_lg = tk.DoubleVar()
        self._new_algorithm = tk.StringVar()
        self._new_algorithm_random_trials = tk.IntVar()
        self._new_delta_spacing = tk.DoubleVar()
        self._new_delta_pl_thk = tk.DoubleVar()
        self._new_delta_web_h = tk.DoubleVar()
        self._new_delta_web_thk = tk.DoubleVar()
        self._new_delta_fl_w = tk.DoubleVar()
        self._new_delta_fl_thk = tk.DoubleVar()
        self._new_swarm_size = tk.IntVar()
        self._new_omega = tk.DoubleVar()
        self._new_phip = tk.DoubleVar()
        self._new_phig = tk.DoubleVar()
        self._new_maxiter = tk.IntVar()
        self._new_minstep = tk.DoubleVar()
        self._new_minfunc = tk.DoubleVar()

        ent_w = 10
        self._ent_spacing_upper = tk.Entry(self._frame, textvariable=self._new_spacing_upper, width=ent_w)
        self._ent_spacing_lower = tk.Entry(self._frame, textvariable=self._new_spacing_lower, width=ent_w)
        self._ent_pl_thk_upper = tk.Entry(self._frame, textvariable=self._new_pl_thk_upper, width=ent_w)
        self._ent_pl_thk_lower = tk.Entry(self._frame, textvariable=self._new_pl_thk_lower, width=ent_w)
        self._ent_web_h_upper = tk.Entry(self._frame, textvariable=self._new_web_h_upper, width=ent_w)
        self._ent_web_h_lower = tk.Entry(self._frame, textvariable=self._new_web_h_lower, width=ent_w)
        self._ent_web_thk_upper = tk.Entry(self._frame, textvariable=self._new_web_thk_upper, width=ent_w)
        self._ent_web_thk_lower = tk.Entry(self._frame, textvariable=self._new_web_thk_lower, width=ent_w)
        self._ent_fl_w_upper = tk.Entry(self._frame, textvariable=self._new_fl_w_upper, width=ent_w)
        self._ent_fl_w_lower = tk.Entry(self._frame, textvariable=self._new_fl_w_lower, width=ent_w)
        self._ent_fl_thk_upper = tk.Entry(self._frame, textvariable=self._new_fl_thk_upper, width=ent_w)
        self._ent_fl_thk_lower = tk.Entry(self._frame, textvariable=self._new_fl_thk_lower, width=ent_w)
        self._ent_span = tk.Entry(self._frame, textvariable=self._new_span, width=ent_w)
        self._ent_width_lg = tk.Entry(self._frame, textvariable=self._new_width_lg, width=ent_w)
        self._ent_algorithm = tk.OptionMenu(self._frame, self._new_algorithm, command=self.selected_algorithm,
                                            *algorithms)
        self._ent_random_trials = tk.Entry(self._frame, textvariable=self._new_algorithm_random_trials)
        self._ent_delta_spacing = tk.Entry(self._frame, textvariable=self._new_delta_spacing, width=ent_w)
        self._ent_delta_pl_thk = tk.Entry(self._frame, textvariable=self._new_delta_pl_thk, width=ent_w)
        self._ent_delta_web_h = tk.Entry(self._frame, textvariable=self._new_delta_web_h, width=ent_w)
        self._ent_delta_web_thk = tk.Entry(self._frame, textvariable=self._new_delta_web_thk, width=ent_w)
        self._ent_delta_fl_w = tk.Entry(self._frame, textvariable=self._new_delta_fl_w, width=ent_w)
        self._ent_delta_fl_thk = tk.Entry(self._frame, textvariable=self._new_delta_fl_thk, width=ent_w)

        pso_width = 10
        self._ent_swarm_size = tk.Entry(self._frame, textvariable=self._new_swarm_size, width=pso_width)
        self._ent_omega = tk.Entry(self._frame, textvariable=self._new_omega, width=pso_width)
        self._ent_phip = tk.Entry(self._frame, textvariable=self._new_phip, width=pso_width)
        self._ent_phig = tk.Entry(self._frame, textvariable=self._new_phig, width=pso_width)
        self._ent_maxiter = tk.Entry(self._frame, textvariable=self._new_maxiter, width=pso_width)
        self._ent_minstep = tk.Entry(self._frame, textvariable=self._new_minstep, width=pso_width)
        self._ent_minfunc = tk.Entry(self._frame, textvariable=self._new_minfunc, width=pso_width)

        start_x, start_y, dx, dy = 20, 70, 100, 40

        self._prop_canvas_dim = (500, 450)
        self._draw_scale = 500
        self._canvas_opt = tk.Canvas(self._frame, width=self._prop_canvas_dim[0], height=self._prop_canvas_dim[1],
                                     background='azure', relief='groove', borderwidth=2)
        self._canvas_opt.place(x=start_x + 10.5 * dx, y=start_y + 3.5 * dy)
        self._select_canvas_dim = (1000, 720)
        self._canvas_select = tk.Canvas(self._frame, width=self._select_canvas_dim[0],
                                        height=self._select_canvas_dim[1],
                                        background='azure', relief='groove', borderwidth=2)
        self._canvas_select.place(x=start_x + 0 * dx, y=start_y + 3.5 * dy)

        # Labels for the pso
        self._lb_swarm_size = tk.Label(self._frame, text='swarm size')
        self._lb_omega = tk.Label(self._frame, text='omega')
        self._lb_phip = tk.Label(self._frame, text='phip')
        self._lb_phig = tk.Label(self._frame, text='phig')
        self._lb_maxiter = tk.Label(self._frame, text='maxiter')
        self._lb_minstep = tk.Label(self._frame, text='minstep')
        self._lb_minfunc = tk.Label(self._frame, text='minfunc')

        tk.Label(self._frame, text='Upper bounds [mm]', font='Verdana 9').place(x=start_x, y=start_y)
        tk.Label(self._frame, text='Iteration delta [mm]', font='Verdana 9').place(x=start_x, y=start_y + dy)
        tk.Label(self._frame, text='Lower bounds [mm]', font='Verdana 9').place(x=start_x, y=start_y + 2 * dy)
        tk.Label(self._frame, text='Spacing [mm]', font='Verdana 7 bold').place(x=start_x + 1.97 * dx,
                                                                                y=start_y - 0.6 * dy)
        tk.Label(self._frame, text='Plate thk. [mm]', font='Verdana 7 bold').place(x=start_x + 2.97 * dx,
                                                                                   y=start_y - 0.6 * dy)
        tk.Label(self._frame, text='Web height [mm]', font='Verdana 7 bold').place(x=start_x + 3.97 * dx,
                                                                                   y=start_y - 0.6 * dy)
        tk.Label(self._frame, text='Web thk. [mm]', font='Verdana 7 bold').place(x=start_x + 4.97 * dx,
                                                                                 y=start_y - 0.6 * dy)
        tk.Label(self._frame, text='Flange width [mm]', font='Verdana 7 bold').place(x=start_x + 5.97 * dx,
                                                                                     y=start_y - 0.6 * dy)
        tk.Label(self._frame, text='Flange thk. [mm]', font='Verdana 7 bold').place(x=start_x + 6.97 * dx,
                                                                                    y=start_y - 0.6 * dy)
        tk.Label(self._frame, text='Estimated running time for algorithm: ',
                 font='Verdana 9 bold').place(x=start_x, y=start_y + 2.8 * dy)
        self._runnig_time_label = tk.Label(self._frame, text='', font='Verdana 9 bold')
        self._runnig_time_label.place(x=start_x + 2.7 * dx, y=start_y + 2.8 * dy)
        tk.Label(self._frame, text='seconds ', font='Verdana 9 bold').place(x=start_x + 3.3 * dx, y=start_y + 2.8 * dy)
        self._result_label = tk.Label(self._frame, text='', font='Verdana 9 bold')
        self._result_label.place(x=start_x, y=start_y + 3.4 * dy)

        self._ent_spacing_upper.place(x=start_x + dx * 2, y=start_y)
        self._ent_delta_spacing.place(x=start_x + dx * 2, y=start_y + dy)
        self._ent_spacing_lower.place(x=start_x + dx * 2, y=start_y + 2 * dy)
        self._ent_pl_thk_upper.place(x=start_x + dx * 3, y=start_y)
        self._ent_delta_pl_thk.place(x=start_x + dx * 3, y=start_y + dy)
        self._ent_pl_thk_lower.place(x=start_x + dx * 3, y=start_y + 2 * dy)
        self._ent_web_h_upper.place(x=start_x + dx * 4, y=start_y)
        self._ent_delta_web_h.place(x=start_x + dx * 4, y=start_y + dy)
        self._ent_web_h_lower.place(x=start_x + dx * 4, y=start_y + 2 * dy)
        self._ent_web_thk_upper.place(x=start_x + dx * 5, y=start_y)
        self._ent_delta_web_thk.place(x=start_x + dx * 5, y=start_y + dy)
        self._ent_web_thk_lower.place(x=start_x + dx * 5, y=start_y + 2 * dy)
        self._ent_fl_w_upper.place(x=start_x + dx * 6, y=start_y)
        self._ent_delta_fl_w.place(x=start_x + dx * 6, y=start_y + dy)
        self._ent_fl_w_lower.place(x=start_x + dx * 6, y=start_y + 2 * dy)
        self._ent_fl_thk_upper.place(x=start_x + dx * 7, y=start_y)
        self._ent_delta_fl_thk.place(x=start_x + dx * 7, y=start_y + dy)
        self._ent_fl_thk_lower.place(x=start_x + dx * 7, y=start_y + 2 * dy)

        # setting default values
        init_dim = float(50)  # mm
        init_thk = float(2)  # mm
        self._new_delta_spacing.set(init_dim)
        self._new_delta_pl_thk.set(init_thk)
        self._new_delta_web_h.set(init_dim)
        self._new_delta_web_thk.set(init_thk)
        self._new_delta_fl_w.set(init_dim)
        self._new_delta_fl_thk.set(init_thk)
        self._new_spacing_upper.set(round(800, 5))
        self._new_spacing_lower.set(round(600, 5))
        self._new_pl_thk_upper.set(round(25, 5))
        self._new_pl_thk_lower.set(round(10, 5))
        self._new_web_h_upper.set(round(500, 5))
        self._new_web_h_lower.set(round(300, 5))
        self._new_web_thk_upper.set(round(22, 5))
        self._new_web_thk_lower.set(round(10, 5))
        self._new_fl_w_upper.set(round(250, 5))
        self._new_fl_w_lower.set(round(50, 5))
        self._new_fl_thk_upper.set(round(30, 5))
        self._new_fl_thk_lower.set(round(10, 5))
        self._new_algorithm.set('anysmart')
        self._new_algorithm_random_trials.set(10000)

        self._new_swarm_size.set(100)
        self._new_omega.set(0.5)
        self._new_phip.set(0.5)
        self._new_phig.set(0.5)
        self._new_maxiter.set(100)
        self._new_minstep.set(1e-8)
        self._new_minfunc.set(1e-8)

        self._new_delta_spacing.trace('w', self.update_running_time)
        self._new_delta_pl_thk.trace('w', self.update_running_time)
        self._new_delta_web_h.trace('w', self.update_running_time)
        self._new_delta_web_thk.trace('w', self.update_running_time)
        self._new_delta_fl_w.trace('w', self.update_running_time)
        self._new_delta_fl_thk.trace('w', self.update_running_time)
        self._new_spacing_upper.trace('w', self.update_running_time)
        self._new_spacing_lower.trace('w', self.update_running_time)
        self._new_pl_thk_upper.trace('w', self.update_running_time)
        self._new_pl_thk_lower.trace('w', self.update_running_time)
        self._new_web_h_upper.trace('w', self.update_running_time)
        self._new_web_h_lower.trace('w', self.update_running_time)
        self._new_web_thk_upper.trace('w', self.update_running_time)
        self._new_web_thk_lower.trace('w', self.update_running_time)
        self._new_fl_w_upper.trace('w', self.update_running_time)
        self._new_fl_w_lower.trace('w', self.update_running_time)
        self._new_fl_thk_upper.trace('w', self.update_running_time)
        self._new_fl_thk_lower.trace('w', self.update_running_time)
        self._new_algorithm_random_trials.trace('w', self.update_running_time)
        self._new_algorithm.trace('w', self.update_running_time)

        self.running_time_per_item = 4e-05
        self._runnig_time_label.config(text=str(self.get_running_time()))
        self._ent_algorithm.place(x=start_x + dx * 10, y=start_y + dy)
        self.algorithm_random_label = tk.Label(self._frame, text='Number of trials')
        tk.Button(self._frame, text='algorith information', command=self.algorithm_info, bg='white') \
            .place(x=start_x + dx * 10, y=start_y + dy * 2)
        self.run_button = tk.Button(self._frame, text='RUN OPTIMIZATION!', command=self.run_optimizaion, bg='red',
                                    font='Verdana 10', fg='Yellow')
        self.run_button.place(x=start_x + dx * 10, y=start_y)
        self._opt_actual_running_time.place(x=start_x + dx * 8, y=start_y + dy * 1.5)
        self.close_and_save = tk.Button(self._frame, text='Return and replace with selected optimized structure',
                                        command=self.save_and_close, bg='green', font='Verdana 10 bold', fg='yellow')
        self.close_and_save.place(x=start_x + dx * 10, y=10)

        # Selection of constraints
        self._new_check_sec_mod = tk.BooleanVar()
        self._new_check_min_pl_thk = tk.BooleanVar()
        self._new_check_shear_area = tk.BooleanVar()
        self._new_check_buckling = tk.BooleanVar()
        self._new_check_sec_mod.set(True)
        self._new_check_min_pl_thk.set(True)
        self._new_check_shear_area.set(True)
        self._new_check_buckling.set(True)
        start_y = 140
        tk.Label(self._frame, text='Check for minimum section modulus').place(x=start_x + dx * 10.5,
                                                                              y=start_y + 14 * dy)
        tk.Label(self._frame, text='Check for minimum plate thk.').place(x=start_x + dx * 10.5, y=start_y + 15 * dy)
        tk.Label(self._frame, text='Check for minimum shear area').place(x=start_x + dx * 10.5, y=start_y + 16 * dy)
        tk.Label(self._frame, text='Check for buckling (RP-C201)').place(x=start_x + dx * 10.5, y=start_y + 17 * dy)
        tk.Checkbutton(self._frame, variable=self._new_check_sec_mod).place(x=start_x + dx * 13, y=start_y + 14 * dy)
        tk.Checkbutton(self._frame, variable=self._new_check_min_pl_thk).place(x=start_x + dx * 13, y=start_y + 15 * dy)
        tk.Checkbutton(self._frame, variable=self._new_check_shear_area).place(x=start_x + dx * 13, y=start_y + 16 * dy)
        tk.Checkbutton(self._frame, variable=self._new_check_buckling).place(x=start_x + dx * 13, y=start_y + 17 * dy)

        # ----------------------------------END OF OPTIMIZE SINGLE COPY-----------------------------------------------
        self.progress_count = tk.IntVar()
        self.progress_count.set(0)
        self.progress_bar = Progressbar(self._frame, orient="horizontal", length=200, mode="determinate",
                                        variable=self.progress_count)
        self.progress_bar.place(x=start_x + dx * 10, y=start_y - dy * 2.4)

        self._active_lines = []
        self.controls()
        self.draw_select_canvas()

    def selected_algorithm(self, event):
        '''
        Action when selecting an algorithm in the optionm menu.
        :return:
        '''
        start_x, start_y, dx, dy = 20, 100, 100, 40
        if self._new_algorithm.get() == 'random' or self._new_algorithm.get() == 'random_no_delta':
            self._ent_random_trials.place_forget()
            self.algorithm_random_label.place_forget()
            self._lb_swarm_size.place_forget()
            self._lb_omega.place_forget()
            self._lb_phip.place_forget()
            self._lb_phig.place_forget()
            self._lb_maxiter.place_forget()
            self._lb_minstep.place_forget()
            self._lb_minfunc.place_forget()
            self._ent_swarm_size.place_forget()
            self._ent_omega.place_forget()
            self._ent_phip.place_forget()
            self._ent_phig.place_forget()
            self._ent_maxiter.place_forget()
            self._ent_minstep.place_forget()
            self._ent_minfunc.place_forget()
            self._ent_random_trials.place(x=start_x + dx * 11.3, y=start_y + 1.2 * dy)
            self.algorithm_random_label.place(x=start_x + dx * 11.3, y=start_y + 0.5 * dy)

        elif self._new_algorithm.get() == 'anysmart' or self._new_algorithm.get() == 'anydetail':
            self._ent_random_trials.place_forget()
            self.algorithm_random_label.place_forget()
            self._lb_swarm_size.place_forget()
            self._lb_omega.place_forget()
            self._lb_phip.place_forget()
            self._lb_phig.place_forget()
            self._lb_maxiter.place_forget()
            self._lb_minstep.place_forget()
            self._lb_minfunc.place_forget()
            self._ent_swarm_size.place_forget()
            self._ent_omega.place_forget()
            self._ent_phip.place_forget()
            self._ent_phig.place_forget()
            self._ent_maxiter.place_forget()
            self._ent_minstep.place_forget()
            self._ent_minfunc.place_forget()

        elif self._new_algorithm.get() == 'pso':
            y_place_label = 11.2
            y_place = 12.2
            self._ent_random_trials.place_forget()
            start_x = 150

            self._lb_swarm_size.place(x=start_x + dx * 11, y=start_y - 1 * dy)
            self._lb_omega.place(x=start_x + dx * 11, y=start_y - 0 * dy)
            self._lb_phip.place(x=start_x + dx * 11, y=start_y + 1 * dy)
            self._lb_phig.place(x=start_x + dx * 11, y=start_y + 2 * dy)

            self._lb_maxiter.place(x=start_x + dx * 14, y=start_y - 1 * dy)
            self._lb_minstep.place(x=start_x + dx * 14, y=start_y + 0 * dy)
            self._lb_minfunc.place(x=start_x + dx * 14, y=start_y + 1 * dy)

            self._ent_swarm_size.place(x=start_x + dx * 12, y=start_y - 1 * dy)
            self._ent_omega.place(x=start_x + dx * 12, y=start_y - 0 * dy)
            self._ent_phip.place(x=start_x + dx * 12, y=start_y + 1 * dy)
            self._ent_phig.place(x=start_x + dx * 12, y=start_y + 2 * dy)

            self._ent_maxiter.place(x=start_x + dx * 15, y=start_y - 1 * dy)
            self._ent_minstep.place(x=start_x + dx * 15, y=start_y + 0 * dy)
            self._ent_minfunc.place(x=start_x + dx * 15, y=start_y + 1 * dy)

    def run_optimizaion(self):
        '''
        Function when pressing the optimization botton inside this window.
        :return:
        '''

        self.opt_create_main_structure(self.opt_create_frames(self.opt_get_fractions()),
                                       self._active_points[0], self._active_points[1],
                                       self._active_points[2], self._active_points[3])


        contraints = (self._new_check_sec_mod.get(), self._new_check_min_pl_thk.get(),
                      self._new_check_shear_area.get(), self._new_check_buckling.get(),
                      False, False)

        self.pso_parameters = (self._new_swarm_size.get(), self._new_omega.get(), self._new_phip.get(),
                               self._new_phig.get(),self._new_maxiter.get(), self._new_minstep.get(),
                               self._new_minfunc.get())

        init_objects = []
        lateral_press = []

        for line,coord in self._opt_structure.items():
            init_objects.append(self.opt_create_struc_obj(self._opt_structure[line])[0])
            if __name__ == '__main__':
                lateral_press.append(200)  # for testing
            else:
                lateral_press.append(self.app.get_highest_pressure(self.opt_find_closest_orig_line(
                    self._opt_structure[line]))['normal'] / 1000)

        [print(obj.get_structure_prop()) for obj in init_objects]
        print(contraints)

        print(
        op.run_optmizataion(initial_structure_obj=init_objects,min_var=self.get_lower_bounds(),
                            max_var=self.get_upper_bounds(),lateral_pressure=lateral_press,deltas=self.get_deltas(),
                            algorithm='pso',side='p',const_chk = contraints,pso_options = self.pso_parameters,
                            is_geometric=True,fatigue_obj=None, fat_press_ext_int=None,min_max_span=(1,6),
                            tot_len=self.opt_get_length(),frame_height=self.opt_get_distance(),frame_cross_a=0.0122))

    def opt_get_fractions(self):
        ''' Finding initial number of fractions '''
        init_fractions = 0
        # finding number of fractions
        for dummy_i in range(1, 100):
            if 3.8 < self.opt_get_length() / dummy_i < 4.2:
                init_fractions = dummy_i
                break
        to_return = []
        for dummy_i in range(init_fractions):
            to_return.append(1/init_fractions)

        return to_return

    def opt_create_struc_obj(self,opt_line):
        ''' Creating preliminary stucture object from selected optimized line. 
        The properties of the new line oto be optimized is taken from the closest original line.'''

        pt1 = opt_line[0]
        pt2 = opt_line[1]

        vector = [pt2[0] - pt1[0], pt2[1] - pt1[1]]
        point = [pt1[0]+vector[0]*0.5,pt1[1]+vector[1]*0.5]
        objects = [copy.deepcopy(x) if x != None else None for x in
                   self._line_to_struc[self.opt_find_closest_orig_line(point)]]

        objects[0].set_span(dist(pt1,pt2))

        return objects

    def opt_find_closest_orig_line(self,coord):
        ''' Find the closest original line to the optimized line.
            Used to create initial structure objects. '''

        for key,value in self._line_dict.items():

            pt1 = list(self._point_dict['point'+str(value[0])])
            pt2 = list(self._point_dict['point'+str(value[1])])
            distance = dist(pt2,pt1)
            vector = [pt2[0]-pt1[0],pt2[1]-pt1[1]]
            current = list(self._point_dict['point'+str(value[0])])
            for dummy_i in range(1000):
                delta = distance/1000
                current[0] += (vector[0]/distance) * delta
                current[1] += (vector[1]/distance) * delta
                if dist(coord,current) <= 0.1:
                    if self._line_to_struc[key][0].get_structure_type() not in ('GENERAL_INTERNAL_NONWT', 'FRAME'):
                        return key
                    else:
                        return None

    def opt_get_distance(self):
        ''' Getting the largest disctance between the two lines to be optimized. '''
        if len(self._active_points)==4:
            return dist(self._point_dict[self._active_points[0]],self._point_dict[self._active_points[2]])
        else:
            return None

    def opt_get_length(self):
        ''' Getting the length of the lines to be optimized. '''
        if len(self._active_points)==4:
            return dist(self._point_dict[self._active_points[0]],self._point_dict[self._active_points[1]])
        else:
            return None

    def opt_get_fraction_bounds(self, max_len = 6, min_len = 2):
        ''' Return the fraction bounds(basis upper/lower) to be considered. '''
        return int(self.opt_get_length()/max_len), int(self.opt_get_length()/min_len)

    def opt_create_frames(self,fractions):
        ''' Creating frames between the the two lines to be optimized. '''
        count = 1

        self._opt_frames['opt_frame_start'] = [[self._point_dict[self._active_points[0]][0],
                                                       self._point_dict[self._active_points[0]][1]],
                                                      [self._point_dict[self._active_points[2]][0] ,
                                                       self._point_dict[self._active_points[2]][1]]]

        self._opt_frames['opt_frame_stop'] = [[self._point_dict[self._active_points[1]][0],
                                                            self._point_dict[self._active_points[1]][1]],
                                                           [self._point_dict[self._active_points[3]][0],
                                                            self._point_dict[self._active_points[3]][1]]]
        start =  0
        for fraction in fractions:
            start += fraction
            if start != 1:
                self._opt_frames['opt_frame'+str(count)] = [ [self._point_dict[self._active_points[0]][0]+
                                                              round(self.opt_get_length()*start,5),
                                                              self._point_dict[self._active_points[0]][1]],
                                                             [self._point_dict[self._active_points[2]][0]+
                                                             round(self.opt_get_length() * start,5),
                                                              self._point_dict[self._active_points[2]][1]]]
            count+=1

        return self._opt_frames

    def opt_create_main_structure(self,frames,start1,stop1,start2,stop2):
        ''' This creates line definition for the new structure objects.
         The scipt searches the line to find frames.'''
        line1_coord = self._point_dict[start1],self._point_dict[stop1]
        line2_coord = self._point_dict[start2],self._point_dict[stop2]

        structure = {}


        p1_low,p1_high = list(line1_coord[0]),list(line2_coord[0])
        p2_low,p2_high = list(line1_coord[1]),list(line2_coord[1])
        vector_low,vector_high = [p2_low[0]-p1_low[0],p2_low[1]-p1_low[1]],[p2_high[0]-p1_high[0],p2_high[1]-p1_high[1]]

        # Starting search on the lower or inner line
        count = 1
        tmp_struc = [p1_low] # starting point defined.
        found = None
        for frame, coords in frames.items():
            current = list(p1_low)
            if frame!='opt_frame_start' and frame!='opt_frame_stop':
                for jump in range(100):
                    current[0] += vector_low[0] / 100
                    current[1] += vector_low[1] / 100
                    if dist(current,coords[0]) < 0.1 and frame != found:
                        found = frame
                        tmp_struc.append(coords[0])
                        self._opt_structure['opt_struc'+str(count)] = tmp_struc # adding found line
                        tmp_struc = [coords[0]]
                        count += 1
        tmp_struc.append(p2_low)
        self._opt_structure['opt_struc'+str(count)] = tmp_struc # adding found line (end)
        count += 1

        # Starting search of upper or outer line.
        tmp_struc = [p1_high] # starting point defined.
        found = None
        for frame, coords in frames.items():
            current = list(p1_high)
            if frame!='opt_frame_start' and frame!='opt_frame_stop':
                for jump in range(100):
                    current[0] += vector_high[0] / 100
                    current[1] += vector_high[1] / 100
                    if dist(current,coords[1]) < 0.1 and frame != found:
                        found = frame
                        tmp_struc.append(coords[1])

                        self._opt_structure['opt_struc'+str(count)] = tmp_struc # adding found line
                        tmp_struc = [coords[1]]
                        count += 1
        tmp_struc.append(p2_high)
        self._opt_structure['opt_struc'+str(count)] = tmp_struc # adding found line (end)

        return self._opt_structure

    def get_running_time(self):
        '''
        Estimate the running time of the algorithm.
        :return:
        '''
        if self._new_algorithm.get() in ['anysmart', 'anydetail']:
            try:
                number_of_combinations = \
                    max((self._new_spacing_upper.get() - self._new_spacing_lower.get()) / self._new_delta_spacing.get(),
                        1) * \
                    max((self._new_pl_thk_upper.get() - self._new_pl_thk_lower.get()) / self._new_delta_pl_thk.get(),
                        1) * \
                    max((self._new_web_h_upper.get() - self._new_web_h_lower.get()) / self._new_delta_web_h.get(), 1) * \
                    max((self._new_web_thk_upper.get() - self._new_web_thk_lower.get()) / self._new_delta_web_thk.get(),
                        1) * \
                    max((self._new_fl_w_upper.get() - self._new_fl_w_lower.get()) / self._new_delta_fl_w.get(), 1) * \
                    max((self._new_fl_thk_upper.get() - self._new_fl_thk_lower.get()) / self._new_delta_fl_thk.get(), 1)
                return int(number_of_combinations * self.running_time_per_item) * len(self._active_lines)
            except TclError:
                return 0
        else:
            try:
                return int(self._new_algorithm_random_trials.get() * self.running_time_per_item) * len(
                    self._active_lines)
            except TclError:
                return 0

    def get_deltas(self):
        '''
        Return a numpy array of the deltas.
        :return:
        '''
        return np.array([float(self._ent_delta_spacing.get()) / 1000, float(self._new_delta_pl_thk.get()) / 1000,
                         float(self._new_delta_web_h.get()) / 1000, float(self._new_delta_web_thk.get()) / 1000,
                         float(self._new_delta_fl_w.get()) / 1000, float(self._new_delta_fl_thk.get()) / 1000])

    def update_running_time(self, *args):
        '''
        Estimate the running time of the algorithm.
        :return:
        '''
        try:
            self._runnig_time_label.config(text=str(self.get_running_time()))
        except ZeroDivisionError:
            pass  # _tkinter.TclError: pass

    def get_upper_bounds(self):
        '''
        Return an numpy array of upper bounds.
        :return:
        '''
        return np.array([self._new_spacing_upper.get() / 1000, self._new_pl_thk_upper.get() / 1000,
                         self._new_web_h_upper.get() / 1000, self._new_web_thk_upper.get() / 1000,
                         self._new_fl_w_upper.get() / 1000, self._new_fl_thk_upper.get() / 1000,
                         6, 10])

    def get_lower_bounds(self):
        '''
        Return an numpy array of lower bounds.
        :return:
        '''
        return np.array([self._new_spacing_lower.get() / 1000, self._new_pl_thk_lower.get() / 1000,
                         self._new_web_h_lower.get() / 1000, self._new_web_thk_lower.get() / 1000,
                         self._new_fl_w_lower.get() / 1000, self._new_fl_thk_lower.get() / 1000,
                         1, 10])

    def checkered(self, line_distance):
        '''
        Creates a grid in the properties canvas.
        :param line_distance:
        :return:
        '''
        # vertical lines at an interval of "line_distance" pixel
        for x in range(line_distance, self._prop_canvas_dim[0], line_distance):
            self._canvas_opt.create_line(x, 0, x, self._prop_canvas_dim[0], fill="grey", stipple='gray50')
        # horizontal lines at an interval of "line_distance" pixel
        for y in range(line_distance, self._prop_canvas_dim[1], line_distance):
            self._canvas_opt.create_line(0, y, self._prop_canvas_dim[0], y, fill="grey", stipple='gray50')

    def draw_properties(self, init_obj=None, opt_obj=None, line=None):
        '''
        Drawing properties in the canvas.
        :return:
        '''
        ctr_x = self._prop_canvas_dim[0] / 2
        ctr_y = self._prop_canvas_dim[1] / 2 + 200
        opt_color, opt_stippe = 'red', 'gray12'
        m = self._draw_scale

        if init_obj != None:
            self._canvas_opt.delete('all')
            self.checkered(10)
            init_color, init_stipple = 'blue', 'gray12'

            self._canvas_opt.create_rectangle(0, 0, self._prop_canvas_dim[0] + 10, 80, fill='white')
            self._canvas_opt.create_line(10, 10, 30, 10, fill=init_color, width=5)
            self._canvas_opt.create_text(270, 10, text='Initial    - Pl.: ' + str(init_obj.get_s() * 1000) + 'x' + str(
                init_obj.get_pl_thk() * 1000) +
                                                       ' Stf.: ' + str(init_obj.get_web_h() * 1000) + 'x' + str(
                init_obj.get_web_thk() * 1000) + '+' +
                                                       str(init_obj.get_fl_w() * 1000) + 'x' + str(
                init_obj.get_fl_thk() * 1000),
                                         font='Verdana 8',
                                         fill=init_color)
            self._canvas_opt.create_text(120, 30, text='Weight (per Lg width): ' +
                                                       str(int(op.calc_weight([init_obj.get_s(),
                                                                               init_obj.get_pl_thk(),
                                                                               init_obj.get_web_h(),
                                                                               init_obj.get_web_thk(),
                                                                               init_obj.get_fl_w(),
                                                                               init_obj.get_fl_thk(),
                                                                               init_obj.get_span(),
                                                                               init_obj.get_lg()]))),
                                         font='Verdana 8', fill=init_color)

            self._canvas_opt.create_rectangle(ctr_x - m * init_obj.get_s() / 2, ctr_y, ctr_x + m * init_obj.get_s() / 2,
                                              ctr_y - m * init_obj.get_pl_thk(), fill=init_color, stipple=init_stipple)
            self._canvas_opt.create_rectangle(ctr_x - m * init_obj.get_web_thk() / 2, ctr_y - m * init_obj.get_pl_thk(),
                                              ctr_x + m * init_obj.get_web_thk() / 2,
                                              ctr_y - m * (init_obj.get_web_h() + init_obj.get_pl_thk())
                                              , fill=init_color, stipple=init_stipple)
            if init_obj.get_stiffener_type() != 'L':
                self._canvas_opt.create_rectangle(ctr_x - m * init_obj.get_fl_w() / 2,
                                                  ctr_y - m * (init_obj.get_pl_thk() + init_obj.get_web_h()),
                                                  ctr_x + m * init_obj.get_fl_w() / 2,
                                                  ctr_y - m * (
                                                  init_obj.get_pl_thk() + init_obj.get_web_h() + init_obj.get_fl_thk()),
                                                  fill=init_color, stipple=init_stipple)
            else:
                self._canvas_opt.create_rectangle(ctr_x - m * init_obj.get_web_thk() / 2,
                                                  ctr_y - m * (init_obj.get_pl_thk() + init_obj.get_web_h()),
                                                  ctr_x + m * init_obj.get_fl_w(),
                                                  ctr_y - m * (
                                                  init_obj.get_pl_thk() + init_obj.get_web_h() + init_obj.get_fl_thk()),
                                                  fill=init_color, stipple=init_stipple)

        if opt_obj != None:
            # [0.6, 0.012, 0.25, 0.01, 0.1, 0.01]
            self._canvas_opt.create_rectangle(ctr_x - m * opt_obj.get_s() / 2, ctr_y,
                                              ctr_x + m * opt_obj.get_s() / 2,
                                              ctr_y - m * opt_obj.get_pl_thk(), fill=opt_color,
                                              stipple=opt_stippe)

            self._canvas_opt.create_rectangle(ctr_x - m * opt_obj.get_web_thk() / 2, ctr_y -
                                              m * opt_obj.get_pl_thk(),
                                              ctr_x + m * opt_obj.get_web_thk() / 2,
                                              ctr_y - m * (
                                                  opt_obj.get_web_h() + opt_obj.get_pl_thk())
                                              , fill=opt_color, stipple=opt_stippe)
            if init_obj.get_stiffener_type() != 'L':
                self._canvas_opt.create_rectangle(ctr_x - m * opt_obj.get_fl_w() / 2, ctr_y
                                                  - m * (
                                                      opt_obj.get_pl_thk() + opt_obj.get_web_h()),
                                                  ctr_x + m * opt_obj.get_fl_w() / 2, ctr_y -
                                                  m * (
                                                      opt_obj.get_pl_thk() + opt_obj.get_web_h() +
                                                      opt_obj.get_fl_thk()),
                                                  fill=opt_color, stipple=opt_stippe)
            else:
                self._canvas_opt.create_rectangle(ctr_x - m * opt_obj.get_web_thk() / 2, ctr_y
                                                  - m * (
                                                      opt_obj.get_pl_thk() + opt_obj.get_web_h()),
                                                  ctr_x + m * opt_obj.get_fl_w(), ctr_y -
                                                  m * (
                                                      opt_obj.get_pl_thk() + opt_obj.get_web_h() +
                                                      opt_obj.get_fl_thk()),
                                                  fill=opt_color, stipple=opt_stippe)

            self._canvas_opt.create_line(10, 50, 30, 50, fill=opt_color, width=5)
            self._canvas_opt.create_text(270, 50,
                                         text='Optimized - Pl.: ' + str(opt_obj.get_s() * 1000) + 'x' +
                                              str(opt_obj.get_pl_thk() * 1000) + ' Stf.: '
                                              + str(opt_obj.get_web_h() * 1000) +
                                              'x' + str(opt_obj.get_web_thk() * 1000) + '+' +
                                              str(opt_obj.get_fl_w() * 1000) +
                                              'x' + str(opt_obj.get_fl_thk() * 1000),
                                         font='Verdana 8', fill=opt_color)
            self._canvas_opt.create_text(120, 70, text='Weight (per Lg width): '
                                                       + str(int(op.calc_weight([opt_obj.get_s(),
                                                                                 opt_obj.get_pl_thk(),
                                                                                 opt_obj.get_web_h(),
                                                                                 opt_obj.get_web_thk(),
                                                                                 opt_obj.get_fl_w(),
                                                                                 opt_obj.get_fl_thk(),
                                                                                 opt_obj.get_span(),
                                                                                 opt_obj.get_lg()]))),
                                         font='Verdana 8', fill=opt_color)
        else:
            self._canvas_opt.create_text(150, 60, text='No optimized solution found.')

        if line != None:
            if __name__ == '__main__':
                lateral_press = 200  # for testing
            else:
                lateral_press = self.app.get_highest_pressure(line)['normal'] / 1000
            self._canvas_opt.create_text(250, self._prop_canvas_dim[1] - 10,
                                         text='Lateral pressure: ' + str(lateral_press) + ' kPa',
                                         font='Verdana 10 bold', fill='red')

    def draw_select_canvas(self, load_selected=False):
        '''
        Making the lines canvas.
        :return:
        '''
        self._canvas_select.delete('all')

        # stippled lines and text.

        self._canvas_select.create_line(self._canvas_origo[0], 0, self._canvas_origo[0], self._select_canvas_dim[1],
                                        stipple='gray50')
        self._canvas_select.create_line(0, self._canvas_origo[1], self._select_canvas_dim[0], self._canvas_origo[1],
                                        stipple='gray50')
        self._canvas_select.create_text(self._canvas_origo[0] - 30,
                                        self._canvas_origo[1] + 20, text='(0,0)',
                                        font='Text 10')
        self._canvas_select.create_text([800, 50],
                                        text='Mouse left click:  select lines to loads\n'
                                             'Mouse mid click: show properties for one line\n'
                                             'Mouse right click: clear all selection\n'
                                             'Shift key press: add selected line\n'
                                             'Control key press: remove selected line', font='Verdana 8 bold',
                                        fill='red')
        # drawing the line dictionary.
        if len(self._line_dict) != 0:
            for line, value in self._line_dict.items():
                color = 'black'
                coord1 = self.get_point_canvas_coord('point' + str(value[0]))
                coord2 = self.get_point_canvas_coord('point' + str(value[1]))
                vector = [coord2[0] - coord1[0], coord2[1] - coord1[1]]
                # drawing a bold line if it is selected
                if self._line_to_struc[line][0].get_structure_type() not in ('GENERAL_INTERNAL_NONWT','FRAME'):

                    if line in self._active_lines:
                        self._canvas_select.create_line(coord1, coord2, width=6, fill=color,stipple='gray50')
                        self._canvas_select.create_text(coord1[0] + vector[0] / 2 + 5, coord1[1] + vector[1] / 2 + 10,
                                                        text='Line ' + str(get_num(line)), font='Verdand 10 bold',
                                                        fill='red')
                    else:
                        self._canvas_select.create_line(coord1, coord2, width=3, fill=color,stipple='gray25')
                        self._canvas_select.create_text(coord1[0] - 20 + vector[0] / 2 + 5, coord1[1] + vector[1] / 2 +

                                                        10,text='line' + str(get_num(line)),font="Text 8", fill='black')

            if len(self._opt_frames) != 0:
                for key,value in self._opt_frames.items():
                    coord1 = self.get_canvas_coord(value[0])
                    coord2 = self.get_canvas_coord(value[1])
                    vector = [coord2[0] - coord1[0], coord2[1] - coord1[1]]
                    self._canvas_select.create_line(coord1, coord2, width=3, fill='SkyBlue1')
            else:
                pass

        if len(self._active_points)>1:
            color = 'blue'
            coord1 = self.get_point_canvas_coord(self._active_points[0])
            coord2 = self.get_point_canvas_coord(self._active_points[1])
            vector = [coord2[0] - coord1[0], coord2[1] - coord1[1]]
            # drawing a bold line if it is selected
            self._canvas_select.create_line(coord1, coord2, width=6, fill=color)
            if len(self._active_points) > 3:
                coord1 = self.get_point_canvas_coord(self._active_points[2])
                coord2 = self.get_point_canvas_coord(self._active_points[3])
                vector = [coord2[0] - coord1[0], coord2[1] - coord1[1]]
                self._canvas_select.create_line(coord1, coord2, width=6, fill=color)

        # drawing the point dictionary
        for key,value in self._point_dict.items():
            pt_size = 6
            if key in self._active_points:
                self._canvas_select.create_oval(self.get_point_canvas_coord(key)[0] - pt_size + 2,
                                              self.get_point_canvas_coord(key)[1] - pt_size + 2,
                                              self.get_point_canvas_coord(key)[0] + pt_size + 2,
                                              self.get_point_canvas_coord(key)[1] + pt_size + 2, fill='blue')
                if self._active_points.index(key) == 0:
                    self._canvas_select.create_text(self.get_point_canvas_coord(key)[0] - 5,
                                                    self.get_point_canvas_coord(key)[1] - 14, text='START 1',
                                                    font='Verdana 12', fill = 'blue')
                elif self._active_points.index(key) == 1:
                    self._canvas_select.create_text(self.get_point_canvas_coord(key)[0] - 5,
                                                    self.get_point_canvas_coord(key)[1] - 14,
                                                    text='STOP 1',font='Verdana 12', fill='blue')
                elif self._active_points.index(key) == 2:
                    self._canvas_select.create_text(self.get_point_canvas_coord(key)[0] - 5,
                                                    self.get_point_canvas_coord(key)[1] - 14,
                                                    text='START 2',font='Verdana 12', fill='blue')
                elif self._active_points.index(key) == 3:
                    self._canvas_select.create_text(self.get_point_canvas_coord(key)[0] - 5,
                                                    self.get_point_canvas_coord(key)[1] - 14,
                                                    text='STOP 2',font='Verdana 12', fill='blue')
                else:
                    pass
            else:
                self._canvas_select.create_oval(self.get_point_canvas_coord(key)[0] - pt_size,
                                              self.get_point_canvas_coord(key)[1] - pt_size,
                                              self.get_point_canvas_coord(key)[0] + pt_size,
                                              self.get_point_canvas_coord(key)[1] + pt_size, fill='red')

                self._canvas_select.create_text(self.get_point_canvas_coord(key)[0] - 5,
                                                self.get_point_canvas_coord(key)[1] - 14, text='pt.'+str(get_num(key)),
                                                font='Verdana 8', fill='blue')

    def algorithm_info(self):
        ''' When button is clicked, info is displayed.'''

        messagebox.showinfo(title='Algorith information',
                            message='The algorithms currently included is:\n'
                                    'ANYSMART:  \n'
                                    '           Calculates all alternatives using upper and lower bounds.\n'
                                    '           The step used inside the bounds is defined in deltas.\n\n'
                                    'RANDOM:    \n'
                                    '           Uses the same bounds and deltas as in ANYSMART.\n'
                                    '           Number of combinations calculated is defined in "trials",\n'
                                    '           which selects withing the bounds and deltas defined.\n\n'
                                    'RANDOM_NO_BOUNDS:\n'
                                    '           Same as RANDOM, but does not use the defined deltas.\n'
                                    '           The deltas is set to 1 mm for all dimensions/thicknesses.\n\n'
                                    'ANYDETAIL:\n'
                                    '           Same as for ANYSMART, but will take some more time and\n'
                                    '           provide a chart of weight development during execution.\n\n'
                                    'PSO - Particle Swarm Search:\n'
                                    '           The information can be found on \n'
                                    '           http://pythonhosted.org/pyswarm/ \n'
                                    '           For further information google it!\n'
                                    '           Parameters:\n'
                                    '           swarmsize : The number of particles in the swarm (Default: 100)\n'
                                    '           omega : Particle velocity scaling factor (Default: 0.5)\n'
                                    '           phip : Scaling factor to search away from the particle’s \n'
                                    '                           best known position (Default: 0.5)\n'
                                    '           phig : Scaling factor to search away from the swarm’s best \n'
                                    '                           known position (Default: 0.5)\n'
                                    '           maxiter : The maximum number of iterations for the swarm \n'
                                    '                           to search (Default: 100)\n'
                                    '           minstep : The minimum stepsize of swarm’s best position \n'
                                    '                           before the search terminates (Default: 1e-8)\n'
                                    '           minfunc : The minimum change of swarm’s best objective value\n'
                                    '                           before the search terminates (Default: 1e-8)\n\n'

                                    '\n'
                                    'All algorithms calculates local scantling and buckling requirements')

    def slider_used(self, event):
        '''
        Action when slider is activated.
        :return:
        '''
        self._canvas_scale = self.slider.get()
        self.draw_canvas()

    def on_closing(self):
        '''
        Action when closing the window without saving.
        :return:
        '''
        if __name__ == '__main__':
            self._frame.destroy()
            return

        mess = tk.messagebox.showwarning('Closed without saving', 'Closing will not save loads you have created',
                                         type='okcancel')
        if mess == 'ok':
            self._frame.grab_release()
            self._frame.destroy()
            self.app.on_aborted_load_window()

    def get_point_canvas_coord(self, point_no):
        '''
        Returning the canvas coordinates of the point. This value will change with slider.
        :param point_no:
        :return:
        '''
        point_coord_x = self._canvas_origo[0] + self._point_dict[point_no][0] * self._canvas_scale
        point_coord_y = self._canvas_origo[1] - self._point_dict[point_no][1] * self._canvas_scale

        return [point_coord_x, point_coord_y]

    def get_canvas_coord(self, coord):
        '''
        Returning the canvas coordinates of the point. This value will change with slider.
        :param point_no:
        :return:
        '''
        point_coord_x = self._canvas_origo[0] + coord[0] * self._canvas_scale
        point_coord_y = self._canvas_origo[1] - coord[1] * self._canvas_scale

        return [point_coord_x, point_coord_y]

    def controls(self):
        '''
        Specifying the controls to be used.
        :return:
        '''
        self._canvas_select.bind('<Button-1>', self.button_1_click)
        self._canvas_select.bind('<Button-2>', self.button_2_click)
        self._canvas_select.bind('<Button-3>', self.button_3_click)

        self._frame.bind('<Shift_L>', self.shift_pressed)
        self._frame.bind('<Shift_R>', self.shift_pressed)
        self._frame.bind('<Control_L>', self.ctrl_pressed)
        self._frame.bind('<Control_R>', self.ctrl_pressed)

    def shift_pressed(self, event=None):
        '''
        Event is executed when shift key pressed.
        :return:
        '''
        self._add_to_lines = True

    def ctrl_pressed(self, event=None):
        '''
        Event when control is pressed.
        :param event:
        :return:
        '''
        self._add_to_lines = False

    def button_1_click(self, event):
        '''
        When clicking the right button, this method is called.
        method is referenced in
        '''

        click_x = self._canvas_select.winfo_pointerx() - self._canvas_select.winfo_rootx()
        click_y = self._canvas_select.winfo_pointery() - self._canvas_select.winfo_rooty()

        self._point_is_active = False
        margin = 10
        self._active_point = ''
        for point, coords in self._point_dict.items():
            point_coord = self.get_point_canvas_coord(point)
            if point_coord[0]-margin < click_x < point_coord[0]+margin and\
                point_coord[1]-margin < click_y < point_coord[1]+margin:
                self._active_point = point
                self._point_is_active = True
                if len(self._active_points)<4:
                    self._active_points.append(self._active_point)

        if len(self._active_points)==4:
            self.opt_create_frames(self.opt_get_fractions())

        self.draw_select_canvas()

    def button_3_click(self, event):
        '''
        Event when right click.
        :param evnet:
        :return:
        '''
        self._active_lines = []
        self._active_points = []
        self.draw_select_canvas()

    def button_2_click(self, event):
        '''
        Event when right click.
        :param evnet:
        :return:
        '''
        click_x = self._canvas_select.winfo_pointerx() - self._canvas_select.winfo_rootx()
        click_y = self._canvas_select.winfo_pointery() - self._canvas_select.winfo_rooty()

        if len(self._line_dict) > 0:
            for key, value in self._line_dict.items():

                coord1x = self.get_point_canvas_coord('point' + str(value[0]))[0]
                coord2x = self.get_point_canvas_coord('point' + str(value[1]))[0]
                coord1y = self.get_point_canvas_coord('point' + str(value[0]))[1]
                coord2y = self.get_point_canvas_coord('point' + str(value[1]))[1]

                vector = [coord2x - coord1x, coord2y - coord1y]
                click_x_range = [ix for ix in range(click_x - 10, click_x + 10)]
                click_y_range = [iy for iy in range(click_y - 10, click_y + 10)]
                distance = int(dist([coord1x, coord1y], [coord2x, coord2y]))

                # checking along the line if the click is witnin +- 10 around the click
                for dist_mult in range(1, distance - 1):
                    dist_mult = dist_mult / distance
                    x_check = int(coord1x) + int(round(vector[0] * dist_mult, 0))
                    y_check = int(coord1y) + int(round(vector[1] * dist_mult, 0))
                    if x_check in click_x_range and y_check in click_y_range:
                        self._canvas_select.delete('all')
                        self._active_lines = []
                        self._active_lines.append(key)
                        if key in self._opt_resutls.keys() and self._opt_resutls[key] != None:
                            self.draw_properties(init_obj=self._line_to_struc[key][0],
                                                 opt_obj=self._opt_resutls[key][0],
                                                 line=key)
                        else:
                            self.draw_properties(init_obj=self._line_to_struc[key][0], line=key)
                        break
                self.draw_select_canvas()
        self.draw_select_canvas()
        self.update_running_time()

        #############################
        self.opt_create_main_structure(self.opt_create_frames(self.opt_get_fractions()),self._active_points[0],
                                       self._active_points[1],self._active_points[2],self._active_points[3])

    def save_and_close(self):
        '''
        Save and close
        :return:
        '''
        if __name__ == '__main__':
            self._frame.destroy()
            return
        try:
            to_return = {}
            for line in self._active_lines:
                to_return[line] = self._opt_resutls[line]
            self.app.on_close_opt_multiple_window(to_return)
            messagebox.showinfo(title='Return info', message='Returning: ' + str(self._active_lines))
        except IndexError:
            messagebox.showinfo(title='Nothing to return', message='No results to return.')
            return
        self._frame.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    my_app = CreateOptimizeMultipleWindow(master=root)
    root.mainloop()
