import pandas as pd
import numpy as np


class Outlier:
    def restructure_df(self, data_df):
        times = data_df.time.unique()
        object_ids = data_df.object_id.unique()
        pp_data = []
        for i in range(0, len(times) - 1):
            for object_id in object_ids:
                first_qry = f"object_id=={object_id} & time=={times[i]}"
                second_qry = f"object_id=={object_id} & time=={times[i+1]}"
                first_row = data_df.query(first_qry).head()
                second_row = data_df.query(second_qry).head()
                row = {
                    "object_id": object_id,
                    "cluster_id_first": first_row["cluster_id"].values[0],
                    "cluster_id_next": second_row["cluster_id"].values[0],
                    "time_first": first_row["time"].values[0],
                    "time_next": second_row["time"].values[0],
                }
                pp_data.append(row)

        df = pd.DataFrame(pp_data)

        return df

    def add_number_of_peers(self, filtered_data):
        peers = (
            filtered_data.groupby(
                by=["cluster_id_first", "cluster_id_next", "time_first", "time_next"]
            )["object_id"]
            .count()
            .reset_index(name="count")
        )
        result = filtered_data.merge(
            peers,
            on=["cluster_id_first", "cluster_id_next", "time_first", "time_next"],
            how="left",
        )
        return result

    def merge_dfs(self, data_df, outlier):
        result = data_df.merge(
            outlier,
            left_on=["object_id", "cluster_id", "time"],
            right_on=["object_id", "cluster_id_next", "time_next"],
            how="left",
        ).drop(
            columns=["cluster_id_first", "cluster_id_next", "time_first", "time_next"]
        )
        return result

    def mark_outliers(self, merged_df, sigma):
        def mark_row(row, sigma):
            if row["count"] <= sigma:
                return True
            else:
                return False

        merged_df["outlier"] = merged_df.apply(lambda row: mark_row(row, sigma), axis=1)
        return merged_df

    def detect_outliers(self, data_df, sigma=1):
        restructured_df = self.restructure_df(data_df)
        number_of_peers = self.add_number_of_peers(restructured_df)
        merged_df = self.merge_dfs(data_df, number_of_peers)
        marked_outliers = self.mark_outliers(merged_df, sigma)
        return marked_outliers
