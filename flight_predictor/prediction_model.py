import pandas as pd
import sys
import os

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data_processing import FlightDataProcessor
from sklearn.ensemble import RandomForestRegressor, HistGradientBoostingRegressor
from sklearn.metrics import r2_score, root_mean_squared_error, mean_squared_error
from sklearn.model_selection import train_test_split, KFold
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from category_encoders import TargetEncoder
from sklearn.feature_selection import (
    RFE,
    SelectKBest,
    f_classif,
    mutual_info_classif,
    f_regression,
    mutual_info_regression,
)
from scipy.stats import pearsonr
import numpy as np


class FlightPredictionModel:
    def __init__(self):
        # Read the data
        processor = FlightDataProcessor()
        self.flight_data = processor.get_processed_main_data()
        self.flight_data = self.flight_data.dropna()
        self.flight_data = self.flight_data.drop(
            [
                "flight_direction",
                "search_date",
                "departure_date",
                "departure_city",
                "departure_time",
                "arrival_city",
                "arrival_airport",
                "arrival_time",
                "arrival_date",
                "travel_duration",
                "Duration_Hour",
                "Duration_Min",
                "Departure_Hour",
                "Arrival_Hour",
                "Search_Day",
                "Departure_Day",
                "Departure_Time",
                "Arrival_Day",
                "Arrival_Time",
            ],
            axis=1,
        )
        self.quant_features = []
        self.cat_features = []
        self.cat_features = self.getCatFeatures()
        # print(cat_features)
        self.quant_features = self.getQuantFeatures()
        self.flight_data.replace("NaN", np.nan, inplace=True)
        self.flight_data.dropna(inplace=True)

        # print(quant_features)
        hist_flight_price = self.flight_data["flight_price"]
        # self.flight_data = self.flight_data.drop(["flight_price"], axis=1)
        # exit()
        """Handle Missing Data"""
        for quant in self.quant_features:
            self.flight_data.fillna(
                {f"{quant}": self.flight_data[f"{quant}"].median()}, inplace=True
            )
            self.flight_data[f"{quant}"] = np.where(
                self.flight_data[f"{quant}"]
                > self.flight_data[f"{quant}"].quantile(0.99),
                self.flight_data[f"{quant}"].quantile(0.99),
                self.flight_data[f"{quant}"],
            )
        for cat in self.cat_features:
            self.flight_data.fillna({cat: "Unknown"}, inplace=True)

        """Encode Data"""
        self.flight_data_encoded = self.encodeCatVariables()
        print(self.flight_data_encoded["flight_price"].head())
        # print(flight_data_encoded.isna().sum())
        """Retrieve Selected Features"""
        selected_features = self.getSelectedFeatures(
            self.flight_data_encoded, hist_flight_price
        )
        print(selected_features)
        self.model = self.train_model()

        # exit()
        # self.flight_data = self.flight_data.drop(["flight_price"], axis=1)
        # self.auto_feature_selection(hist_flight_price, self.flight_data)

    def preprocess_new_data(self, df):
        quant_features = []
        cat_features = []
        cat_features = self.getCatFeatures()
        quant_features = self.getQuantFeatures()

        """Handle Missing Data"""
        for quant in quant_features:
            df.fillna({f"{quant}": df[f"{quant}"].median()}, inplace=True)
            self.flight_data[f"{quant}"] = np.where(
                df[f"{quant}"] > df[f"{quant}"].quantile(0.99),
                df[f"{quant}"].quantile(0.99),
                df[f"{quant}"],
            )
        for cat in cat_features:
            df.fillna({cat: "Unknown"}, inplace=True)

        """Encode Data"""
        df_encoded = self.encodePre_CatVariables(df, quant_features, cat_features)
        print(df_encoded["flight_price"].head())
        # print(flight_data_encoded.isna().sum())
        return df

    def encodePre_CatVariables(self, df, quant_features, cat_features):
        numeric_df = df[quant_features].copy()
        oh_list = []

        for col in df.columns:
            df.fillna({col: "Unknown"}, inplace=True)
            print(df[f"{col}"].unique())
            exit()

        oh_encoder = OneHotEncoder(
            sparse_output=False, handle_unknown="ignore", drop="first"
        )  # Avoid dummy variable trap
        tar_encoder = TargetEncoder()

        # One-hot encode selected columns
        oh_encoded = pd.DataFrame(
            oh_encoder.fit_transform(df[oh_list]),
            columns=oh_encoder.get_feature_names_out(),
            index=self.flight_data.index,
        )

        # Target encode selected columns
        tar_cols = ["departure_airplane_type", "arrival_airplane_type", "airline_name"]
        tar_encoded = pd.DataFrame(index=self.flight_data.index)
        kf = KFold(n_splits=5, shuffle=True, random_state=420)

        for col in tar_cols:
            # Initialize a series to store encoded values
            encode_col = pd.Series(index=self.flight_data.index, dtype=float)

            # Use K-fold to encode
            for train_idx, test_idx in kf.split(self.flight_data):
                # Fit on training fold
                temp_encoder = TargetEncoder()
                temp_encoder.fit(
                    self.flight_data.iloc[train_idx][col],
                    self.flight_data.iloc[train_idx]["flight_price"],
                )

                # Transform test fold
                encode_col.iloc[test_idx] = temp_encoder.transform(
                    self.flight_data.iloc[test_idx][[col]]
                ).iloc[:, 0]

                # Add to df
                tar_encoded[f"{col}_encoded"] = encode_col

        # Combine all encoded data with numeric features and target
        flight_data_encoded = pd.concat(
            [
                numeric_df,
                oh_encoded,
                tar_encoded,
                self.flight_data[["flight_price"]],
            ],
            axis=1,
        )

        return flight_data_encoded

    def train_model(self):
        X = self.flight_data_encoded.drop("flight_price", axis=1)
        y = self.flight_data_encoded["flight_price"]

        # Split our data for a 70/30 train/test set
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=420
        )

        # create our model
        model = HistGradientBoostingRegressor()
        model.fit(X_train, y_train)

        # Evaluate model
        train_preds = model.predict(X_train)
        test_preds = model.predict(X_test)

        print(f"Train R²: {r2_score(y_train, train_preds):.4f}")
        print(f"Test R²: {r2_score(y_test, test_preds):.4f}")
        print(f"Train RMSE: {root_mean_squared_error(y_train, train_preds):.2f}")
        print(f"Test RMSE: {root_mean_squared_error(y_test, test_preds):.2f}")
        exit()
        self.model = model
        self.X_test = X_test
        self.y_test = y_test

    def getCatFeatures(self, df):
        cat = []
        for col in df.columns:
            if self.flight_data[f"{col}"].dtype == "object":
                # print(f"{col}:{df[f"{col}"].dtype}")
                cat.append(col)

        return cat

    def getQuantFeatures(self, df):
        quant = []
        for col in df.drop("flight_price", axis=1).columns:
            if self.flight_data[f"{col}"].dtype != "object":
                # print(f"{col}:{df[f"{col}"].dtype}")
                quant.append(col)

        return quant

    def auto_feature_selection(self, flight_price, flight_data):
        model = RandomForestRegressor()
        rfe = RFE(model, n_features_to_select=10)  # Keep top 2 features
        rfe.fit(flight_data, flight_price)

        # Print selected features
        selected_features = flight_data.columns[rfe.support_]
        print("Selected Features:", selected_features)

    def getSelectedFeatures(self, X_encoded, y):
        mi = mutual_info_regression(X_encoded, y)
        mi_scores = pd.Series(mi, index=X_encoded.columns).sort_values(ascending=False)

        return mi_scores.head(10).index.tolist()

    def encodeCatVariables(self):
        numeric_df = self.flight_data[self.quant_features].copy()

        for col in self.flight_data.columns:
            self.flight_data.fillna({col: "Unknown"}, inplace=True)
        oh_encoder = OneHotEncoder(
            sparse_output=False, handle_unknown="ignore", drop="first"
        )  # Avoid dummy variable trap
        tar_encoder = TargetEncoder()

        # One-hot encode selected columns
        oh_encoded = pd.DataFrame(
            oh_encoder.fit_transform(
                self.flight_data[
                    [
                        "departure_airport",
                        "seating_class",
                        "Duration_Label",
                        "Layover_Label",
                        "Departure_AMPM",
                        "Departure_Time_Label",
                        "Arrival_AMPM",
                        "Arrival_Time_Label",
                        "Departure_Region",
                        "Arrival_Region",
                        "Departure_Season",
                        "Arrival_Season",
                    ]
                ]
            ),
            columns=oh_encoder.get_feature_names_out(),
            index=self.flight_data.index,
        )

        # Target encode selected columns
        tar_cols = ["departure_airplane_type", "arrival_airplane_type", "airline_name"]
        tar_encoded = pd.DataFrame(index=self.flight_data.index)
        kf = KFold(n_splits=5, shuffle=True, random_state=420)

        for col in tar_cols:
            # Initialize a series to store encoded values
            encode_col = pd.Series(index=self.flight_data.index, dtype=float)

            # Use K-fold to encode
            for train_idx, test_idx in kf.split(self.flight_data):
                # Fit on training fold
                temp_encoder = TargetEncoder()
                temp_encoder.fit(
                    self.flight_data.iloc[train_idx][col],
                    self.flight_data.iloc[train_idx]["flight_price"],
                )

                # Transform test fold
                encode_col.iloc[test_idx] = temp_encoder.transform(
                    self.flight_data.iloc[test_idx][[col]]
                ).iloc[:, 0]

                # Add to df
                tar_encoded[f"{col}_encoded"] = encode_col

        # Combine all encoded data with numeric features and target
        flight_data_encoded = pd.concat(
            [
                numeric_df,
                oh_encoded,
                tar_encoded,
                self.flight_data[["flight_price"]],
            ],
            axis=1,
        )

        return flight_data_encoded

    def predict(self, new_data=None):
        # Placeholder for prediction logic
        print("Prediction logic not implemented yet.")

        if new_data is None:
            # Use test data if no new data is provided
            predictions = self.model.predict(self.X_test)
            print(f"Test R²: {r2_score(self.y_test, predictions):.4f}")
            print(f"Test RMSE: {root_mean_squared_error(self.y_test, predictions):.2f}")
            return predictions
        else:

            proccessed_data = self.preprocess_new_data(new_data)
            return self.model.predict(proccessed_data)


if __name__ == "__main__":
    model = FlightPredictionModel()
    model.predict(pd.DataFrame({}))
