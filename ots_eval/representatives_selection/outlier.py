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



    def get_outliers(self, data_df, sigma=1, time_interval=()):
        filtered_data_df=self.filter_by_interval(data_df,time_interval)        
        grouped_df=self.extend_df_by_cluster_path_group(filtered_data_df)     
        stats=grouped_df.groupby(['object_id','group_id']).first().reset_index()[['group_id']].groupby('group_id').size().reset_index(name='count')     
        outlier_group_ids=stats.loc[stats['count']<=sigma]['group_id'].tolist()       
        result=grouped_df.loc[grouped_df['group_id'].isin(outlier_group_ids)].drop(['group_id'],axis=1)       
        return result
        
      
        