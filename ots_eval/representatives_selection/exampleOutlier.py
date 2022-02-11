from ots_eval.clustering.cots import COTS
from representatives import Representatives
#from visualizations.plotly.plotter_3d import Plotter
#from visualizations.seaborn import Plotter
from visualizations.gk.data_plotter import DataPlotter
import pandas as pd
from outlier import Outlier


plotter_config={
    'features':['feature1','feature2'],
    'feature_renames':['feature1','feature2'],
    'identifier':'object_id',
    'time_column_name': 'Time',
    'plot': {
               'time_axis_name': 'time stamp',
               'col_wrap': 4,
               'no_timepoints':12,
               'title': 'Covid Data',
               '1DPlot': True,
           },}

def get_data():
    folder_path = "../../data/"
    csv_name = "pub1_generated_datasetA.csv"
    df = pd.read_csv(folder_path + csv_name)
    return df


def get_clustering(df):
    cots = COTS(df)
    clusters = cots.get_clusters_df(min_cf=0.2, sw=3)
    return clusters




if __name__ == "__main__":
    data = get_data()
    clustering = get_clustering(data)
    clustering.rename(columns={"cluster": "cluster_id"}, inplace=True) 
    outlier=Outlier()
    outlier_df=outlier.detect_outliers(clustering,sigma=1)
    
    outlier_df=outlier_df.rename(columns={'time':'Time','cluster_id':'cluster','object_id':'ObjectID'})

    outlier_df['outlier']=outlier_df['outlier'].apply(lambda x: -1 if x is True  else 0)

    paths_weights=outlier_df.groupby(['count']).size()
    outliers=outlier_df.query('outlier == -1')
    print('OUTLIER DF:')
    print(outlier_df)
    print()
    print('OUTLIERS:')
    print(outliers)
    print()   
    print('paths weights:')
    print(paths_weights)
    
    #df_qry_result=outlier_df.query()

    plotter=DataPlotter(plotter_config)
    plot=plotter.plot_twodim_clusters(outlier_df,outlier=True)
    plot.savefig('test.png')