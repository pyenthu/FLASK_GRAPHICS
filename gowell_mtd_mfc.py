from pprint import pprint
import pandas as pd
from custom_plot import log_curve, log_plot, curve_group, log_heatmap
from utilities import my_las, filtered_df
import openpyxl


def build_mtd_curves(df_mtd):
    try:

        mtd_groups = dict()
        mtd_groups['casing_1'] = curve_group("CASING_1")
        plot_curve = log_curve('9_5_8in_CSG_Thickness',
                               df_mtd['9_5_8in_CSG_Thickness'], df_mtd['DEPT'], [0, 1],
                               showticklabels=True,
                               xaxis_title='9-5/8" Thickness')

        mtd_groups['casing_1'].add_curve(plot_curve)
        mtd_groups['casing_2'] = curve_group('CASING_2')
        plot_curve = log_curve('13_3_8in_CSG_Thickness',
                               df_mtd['13_3_8in_CSG_Thickness'], df_mtd['DEPT'], [0, 1],
                               showticklabels=True,
                               xaxis_title='13-3/8" Thickness')

        mtd_groups['casing_2'].add_curve(plot_curve)
        return mtd_groups

    except Exception as e:
        pprint(["Build MTD Plot Error", str(e)])
        raise


def build_mfc_heat_map(df, num_fingers=40):
    y_depth = df['DEPT']
    x_tuple = []
    curve_prefix = 'D'
    for finger_num in range(1, num_fingers + 1):
        las_curve_name = ''.join([curve_prefix, str('{:02d}'.format(finger_num))])
        plot_curve_name = ''.join(['Finger ', str(finger_num)])
        x_tuple.append(las_curve_name)
    df_heat_map = df[x_tuple].apply(tuple, axis=1)
    pprint(df_heat_map.head())
    # pprint(x_tuple)

    return dict(x=x_tuple, y=y_depth, z=df_heat_map)


def build_mfc_plot_curves(df, corrected=False,
                          plot_scale=[0, 10], num_fingers=40):
    try:

        # Build Multi Finger Caliper Curves
        mfc_curves = curve_group("MFC")
        y_depth = df['DEPT']

        plot_scale = plot_scale

        step_scale = (max(plot_scale) - min(plot_scale)) / (num_fingers + 1)

        if (corrected == False):
            curve_prefix = 'D'
        else:
            curve_prefix = 'D'

        for finger_num in range(1, num_fingers + 1):
            las_curve_name = ''.join([curve_prefix, str('{:02d}'.format(finger_num))])
            plot_curve_name = ''.join(['Finger ', str(finger_num)])

            if (finger_num in [1]):
                showticklabels = True
                xaxis_title = plot_curve_name
            else:
                showticklabels = False
                xaxis_title = ''

            x_curve = df[las_curve_name]
            plot_curve = log_curve(plot_curve_name, x_curve,
                                   y_depth, plot_scale,
                                   showticklabels=showticklabels,
                                   xaxis_title=xaxis_title)

            mfc_curves.add_curve(plot_curve)

            plot_scale = [plot_scale[0] - step_scale, plot_scale[1] - step_scale]

        return mfc_curves

    except Exception as e:
        pprint(["Build MIT Plot", str(e)])
        raise


class gowell_plot():

    def __init__(self):

        # Status Flaga
        self._read_update_required = True
        self._plot_update_required = True

        # Curve Groups
        self.mfc_group = None
        self.mtd_group = None

        # Plot
        self.my_plot = log_plot()

        # Curves Themselves
        self.heat_map = None
        self.mfc_heatmap = None

        if self.read_data_xl():
            self._read_update_required = False
        else:
            self._read_update_required = True

    def write_to_excel(self):

        # Multi Fingered Caliper Data
        ''' mfc_file = './INPUT/GOWELL/MFC_Processed Las.las'
        log_mfc = my_las(mfc_file)/df_mfc = log_mfc.get_df(depth_range[0], depth_range[1])
        df_mfc.to_excel('static/temp/INPUT/GOWELL/mfc_small.xlsx')
        '''
        df_filtered_mfc = filtered_df(self.df_mfc, 1000, 1020)
        df_filtered_mtd = filtered_df(self.df_mtd, 1000, 1020)

        df_filtered_mfc.to_excel('static/temp/INPUT/GOWELL/mfc_small.xlsx')
        df_filtered_mtd.to_excel('static/temp/INPUT/GOWELL/mtd_small.xlsx')

    def read_data_xl(self,
                     mfc_file='static/temp/INPUT/GOWELL/mfc_small.xlsx',
                     mtd_file='static/temp/INPUT/GOWELL/mtd_small.xlsx',
                     ):
        try:
            self.df_mfc = pd.read_excel(mfc_file)
            self.df_mtd = pd.read_excel(mtd_file)
            return True

        except Exception as e:
            pprint(["PROBLEM HERE MAIN", str(e)])
            return False

    def read_data(self,
                  mfc_file='static/temp/INPUT/GOWELL/mfc_small.xlsx',
                  mtd_file='static/temp/INPUT/GOWELL/MTD_Processed Las.las',
                  ):
        try:
            self.df_mfc = pd.read_excel(mfc_file)
            self.df_mtd = my_las(mtd_file).get_df(1000, 1050)
            return True

        except Exception as e:
            pprint(["PROBLEM HERE MAIN", str(e)])
            return False

            # Multi Fingered Caliper Data
            ''' mfc_file = './INPUT/GOWELL/MFC_Processed Las.las'
            log_mfc = my_las(mfc_file)/df_mfc = log_mfc.get_df(depth_range[0], depth_range[1])
            df_mfc.to_excel('static/temp/INPUT/GOWELL/mfc_small.xlsx')
            '''

    def get_plot_json(self):
        if self._plot_update_required == True:
            self.build_gowell_plot()

        return self.my_plot.get_json()

    def build_gowell_plot(self, start=0, end=0):

        try:

            pprint("JUST BEFORE PLOT")

            # Just two panes
            self.my_plot.add_pane(dict(domain=[0.0, 0.15]))
            self.my_plot.add_pane(dict(domain=[0.15, 0.3]))
            self.my_plot.add_pane(dict(domain=[0.3, 0.65]))
            self.my_plot.add_pane(dict(domain=[0.65, 1]))

            # Build Curves
            self.mfc_group = build_mfc_plot_curves(self.df_mfc, corrected=False, plot_scale=[8.5, 18.5], num_fingers=56)
            self.mtd_group = build_mtd_curves(self.df_mtd)

            # CREATE HEATMAP
            self.heat_map = build_mfc_heat_map(self.df_mfc, num_fingers=56)

            self.mfc_heatmap = curve_group("MFC_HMAP")
            self.mfc_heatmap.add_curve(log_heatmap("MFC_HMAP",
                                                   x=self.heat_map['x'],
                                                   y=self.heat_map['y'],
                                                   z=self.heat_map['z']))

            self.my_plot.assign_curve_group(self.mtd_group['casing_1'], 0)
            self.my_plot.assign_curve_group(self.mtd_group['casing_2'], 1)
            self.my_plot.assign_curve_group(self.mfc_heatmap, 2)
            self.my_plot.assign_curve_group(self.mfc_group, 3)

            self._plot_update_required = False
            return self.my_plot

        except Exception as e:
            pprint(["PROBLEM HERE MAIN", str(e)])
            raise


if __name__ == '__main__':
    new_gowell_plot = gowell_plot()
    # new_gowell_plot.write_to_excel()
