import pandas as pd
class Outlier():  


    def extend_df_by_cluster_path_group(self, df):
        all_cluster_paths = (
            df.groupby(["object_id"])
            .cluster_id.apply(tuple)
            .reset_index(name="cluster_path")
        )
        cluster_path_groups = (
            all_cluster_paths.drop(columns=["object_id"])
            .drop_duplicates("cluster_path")
            .reset_index(drop=True)
            .reset_index()
            .rename(columns={"index": "group_id"})
        )
        

        group_assignments = cluster_path_groups.merge(
            all_cluster_paths, on="cluster_path", how="left"
        ).drop(columns=["cluster_path"])

        df_cluster_path_group_extended = df.merge(
            group_assignments, on="object_id", how="left"
        )
        return df_cluster_path_group_extended

    def filter_by_interval(self, data_df, time_interval):      
        if len(time_interval)>0:
            filtered_df=data_df.loc[(data_df['time']>=time_interval[0]) & (data_df['time']<=time_interval[1])]
        else:
            filtered_df = data_df
        return filtered_df


    def get_filtered_data(self,data_df):
        times = data_df.time.unique()
        object_ids = data_df.object_id.unique()
        pp_data=[]
        for i in range(0,len(times)-1):
            for object_id in object_ids:
                first_qry=f'object_id=={object_id} & time=={times[i]}'
                second_qry=f'object_id=={object_id} & time=={times[i+1]}'            
                first_row=data_df.query(first_qry).head()
                second_row=data_df.query(second_qry).head()         
                row={
                        'object_id':object_id,
                        'cluster_id_first': first_row['cluster_id'].values[0],
                        'cluster_id_next':second_row['cluster_id'].values[0],
                        'time_first': first_row['time'].values[0],
                        'time_next': second_row['time'].values[0]
                }
                pp_data.append(row)
        
        df=pd.DataFrame(pp_data)
        print(df)
        return df
        
    def add_number_of_peers(self,filtered_data):
        peers=filtered_data.groupby(by=['cluster_id_first','cluster_id_next','time_first','time_next'])['object_id'].count().reset_index(name='count')      
        result=filtered_data.merge(peers, on=['cluster_id_first','cluster_id_next','time_first','time_next'], how='left')
        return result

    def get_outliers(self, data_df, sigma=1, time_interval=()):
        filtered_data=self.get_filtered_data(data_df)
        number_of_peers=self.add_number_of_peers(filtered_data)

        

        
        #filtered_data_df=self.filter_by_interval(data_df,time_interval)        
        #grouped_df=self.extend_df_by_cluster_path_group(filtered_data_df)     
        #stats=grouped_df.groupby(['object_id','group_id']).first().reset_index()[['group_id']].groupby('group_id').size().reset_index(name='count')     
        #outlier_group_ids=stats.loc[stats['count']<=sigma]['group_id'].tolist()       
        #result=grouped_df.loc[grouped_df['group_id'].isin(outlier_group_ids)].drop(['group_id'],axis=1)       
        #return result
        
      
        
def get_data():
    test_data = [
        [1, 1, 1, 1 / 3, 1 / 6],
        [2, 1, 1, 2 / 3, 1 / 6],
        [3, 1, 1, 1 / 3, 2 / 6],
        [4, 1, 2, 2 / 3, 4 / 6],
        [5, 1, 2, 3 / 3, 4 / 6],
        [6, 1, 2, 2 / 3, 5 / 6],
        [7, 1, 7, 0.5, 0.5],
        [1, 2, 3, 2 / 3, 1 / 6],
        [2, 2, 3, 3 / 3, 1 / 6],
        [3, 2, 3, 2 / 3, 2 / 6],
        [4, 2, 4, 2 / 3, 5 / 6],
        [5, 2, 4, 3 / 3, 5 / 6],
        [6, 2, 4, 2 / 3, 6 / 6],
        [7, 2, 8, 0.5, 0.5],
        [1, 3, 5, 2 / 3, 1 / 6],
        [2, 3, 5, 2 / 3, 2 / 6],
        [3, 3, 5, 1 / 3, 1 / 6],
        [4, 3, 6, 2 / 3, 5 / 6],
        [5, 3, 6, 3 / 3, 4 / 6],
        [6, 3, 6, 1 / 3, 6 / 6],
        [7, 3, 9, 0.5, 0.5],
    ]

    data = pd.DataFrame(
        test_data, columns=["object_id", "time", "cluster_id", "feature1", "feature2"]
    )
    return data



clustering = get_data()

print(clustering)
outlier=Outlier()
outlier_df=outlier.get_outliers(clustering, sigma=1)