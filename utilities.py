from pprint import pprint, pformat
import lasio, las
import pandas as pd

def get_dict_item(my_list, id='id', my_unique_id='id'):
    return next((item for item in my_list if item[id] == my_unique_id), None)

def filtered_df (df, start, end):
    return df[(df['DEPT'] >= start) & (df['DEPT'] <= end)]

class my_las(object):
    def __init__(self, file_name, read_las=True, read_pandas_on_init=False):

        try:

            self._las_file_name = file_name
            self.df = pd.DataFrame()
            self.log = dict()

            if (read_las == True):
                pprint("READING LAS")
                self.log = las.LASReader(self._las_file_name)
                self.l = lasio.read(self._las_file_name)

            if (read_pandas_on_init == True):
                self._fill_pd()

        except Exception as e:
            pprint(["PROBLEM HERE INIT OF LAS MY", str(e)])
            raise

    def read_las(self):

        try:
            pprint("LAS DONE")
            self.log = las.LASReader(self._las_file_name)

        except Exception as e:
            pprint(["In reading the las file", str(e)])
            raise

    def _fill_pd(self):

        try:
            self.df = self.get_df()
        except Exception as e:
            pprint(["In reading the las file", str(e)])
            raise

    def to_excel(self, file_name='temp.xlsx', start_depth=None, end_depth=None):
        df = self.get_df(start_depth, end_depth).to_excel(file_name)

    # This function is invoked to get a slice of the whole data set
    def get_df(self, start=None, end=None):

        try:
            temp_dict = dict()
            depth_col = self.log.data['DEPT']

            # Check if there is a filter applied
            if (start == None) or (start < depth_col[0]):
                start = depth_col[0]
            if (end == None) or (end > depth_col[-1]):
                end = depth_col[-1]
            pprint("before loop")
            # Filter required depths
            # pprint (len(depth_col))
            filter_index = [i for i in range(len(depth_col)) if ((depth_col[i] >= start) and (depth_col[i] <= end))]
            # pprint(filter_index)
            # Done Again
            for key in self.log.curves.items:

                # CHeck if the data needs to be filtered or not
                if (filter_index != None):
                    las_column = [self.log.data[key][i] for i in filter_index]
                else:
                    las_column = self.log.data[key]

                temp_dict[key] = las_column

            # Built the dict. Depth Index now. Now assign to data frame
            df_built = pd.DataFrame(temp_dict, index=temp_dict['DEPT'])
            df_built.index.rename('DEPT', inplace=True)
            return df_built

        except Exception as e:
            pprint(["IN ASSIGNING FILE", str(e)])
            raise

if __name__ == '__main__':
    depth = [x for x in range (2000, 3000)]
    gr = [int(x/100) for x in range (2000, 3000)]
    series_depth = depth
    my_df = pd.DataFrame({'DEPT': depth, 'GR': gr})
    filtered_df = filtered_df (my_df, 2500, 2600)
    pprint (my_df)
    pprint(pformat([filtered_df]))

