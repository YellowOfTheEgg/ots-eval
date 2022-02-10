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
               'col_wrap': 2,
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


def get_representatives(df):
    rp = Representatives()
    representatives = rp.get_representatives(df)
    return representatives


def plot_result(df, representatives):   
    pl = Plotter(df)
    pl.add_representatives(representatives)
    fig=pl.generate_fig()   
    #fig.show()
    fig.savefig('exampleOut.png')




if __name__ == "__main__":
    data = get_data()
    clustering = get_clustering(data)
    clustering.rename(columns={"cluster": "cluster_id"}, inplace=True)
    rp = get_representatives(clustering)
    outlier=Outlier()
    outlier_df=outlier.detect_outliers(clustering,sigma=1)
    outlier_df=outlier_df.rename(columns={'time':'Time','cluster_id':'cluster'})
    print(outlier_df)
    plotter=DataPlotter(plotter_config)
    plot=plotter.plot_twodim_clusters(outlier_df,outlier=True)
