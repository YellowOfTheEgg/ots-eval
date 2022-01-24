from ots_eval.clustering.cots import COTS
from representatives import Representatives
#from visualizations.plotly.plotter_3d import Plotter
from visualizations.seaborn import Plotter
import pandas as pd
from outlier import Outlier


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
    outlier_df=outlier.get_outliers(clustering,sigma=1)
    plot_result(clustering,outlier_df)
