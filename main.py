from regressionTree import *
import pandas as pd


def prepare_df(file_path: str, to_estimate: str, features: list, size: int) -> pd.core.frame.DataFrame:
    df = pd.read_csv(file_path)
    ocean_proximity_dict = {'NEAR BAY': 1, '<1H OCEAN': 2, 'INLAND': 3, 'NEAR OCEAN': 4, 'ISLAND': 5}

    # cast ocean_proximity to numeric number
    if 'ocean_proximity' in features:
        df['ocean_proximity'] = pd.Series(ocean_proximity_dict[i] for i in df['ocean_proximity'])

    # drop na values for both estimating value and features
    df.dropna(subset=np.concatenate((to_estimate, features), axis=None), inplace=True)

    # cast to numeric
    for ft in features:
        df[ft] = pd.to_numeric(df[ft])

    # always pick random sample with
    df = df.head(size) # TODO decide if we use head() or sample()

    return df


def prepare_data(df: pd.core.frame.DataFrame) -> tuple:
    # set of features
    X = df[features]

    # continous variable
    Y = df[to_estimate].values.tolist()

    return X, Y


if __name__ == '__main__':
    quantity_from_csv = 1000
    max_depth = 3
    min_elements = 3

    file_path = "housing.csv"
    to_estimate = "median_house_value"
    features = ['housing_median_age', 'total_rooms', 'total_bedrooms', 'population',
                'households', 'median_income', 'ocean_proximity']

    dataFrame = prepare_df(file_path=file_path, to_estimate=to_estimate, features=features, size=quantity_from_csv)

    X, Y = prepare_data(dataFrame)

    tree = Node(X=X, Y=Y, max_depth=max_depth, min_elements=min_elements)
    tree.grow_tree()
    tree.print_tree()

    dataFrame = dataFrame.head(50)

    new_column_name = 'estimated'

    tree.predict(df=dataFrame, new_column_name=new_column_name)

    for index, row in dataFrame.iterrows():
        print("real value: " + str(row[to_estimate]))
        print("estimated value: " + str(row[new_column_name]))
        print("-------------------")


