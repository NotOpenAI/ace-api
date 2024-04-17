from fastapi import APIRouter, Depends, HTTPException
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, make_scorer
from sklearn.model_selection import train_test_split, cross_val_score
from sqlalchemy.orm import Session
import numpy as np
from crud import ai, bid
from core import security, deps
from schemas.base import SuccessResponse
from typing import Annotated
from models.user import User
import pandas as pd

router = APIRouter(prefix="/ai", tags=["ai"])


@router.get("/{bid_id}", response_model=SuccessResponse[float])
async def get_bid(
    bid_id: int,
    current_user: Annotated[User, Depends(security.get_current_user)],
    db: Session = Depends(deps.get_db),
):
    bid_obj = bid.get_by_id(bid_id, db)
    if not bid_obj:
        raise HTTPException(404, "Bid not found")

    bids = ai.get_bid_datar_prediction(db)
    data, original_contract = data_to_df(bid_id, bids)

    data_cleaned = clean_data(bid_id, data)

    current_bid_data = data_cleaned[data_cleaned["id"] == bid_id]
    if current_bid_data.empty:
        raise HTTPException(
            status_code=404, detail="Current bid data not found for prediction"
        )

    data_cleaned = data_cleaned[data_cleaned["id"] != bid_id]
    X_test, random_forest_model, y_test = train_model(data_cleaned)

    predicted_margin = predict_margin(
        current_bid_data.drop(columns=["id", "final_cost"]),
        random_forest_model,
        original_contract,
    )

    return SuccessResponse(data=predicted_margin)


def data_to_df(bid_id, bids):
    data = []
    original_contract = 0
    for bid in bids:
        if bid.id == bid_id:
            original_contract = (
                bid.original_contract
                if hasattr(bid, "original_contract")
                else original_contract
            )
        row = {
            column.name: getattr(bid, column.name)
            for column in bid.__table__.columns
            if hasattr(bid, column.name)
        }
        for attribute in bid.attributes:
            attribute_name = attribute.type.name
            row[attribute_name] = (
                attribute.num_val
                if attribute.num_val is not None
                else attribute.option_id
            )

        data.append(row)

    df = pd.DataFrame(data)
    return df, original_contract


def clean_data(bid_id, data):
    # choose columns with at least 40% of data
    threshold = 0.5 * len(data)
    data_cleaned = data.dropna(thresh=threshold, axis=1)

    columns_to_drop = ["name", "created_at", "comments", "desired_margin"]
    data_cleaned = data_cleaned.drop(
        columns=[col for col in columns_to_drop if col in data_cleaned.columns]
    )

    mask = data_cleaned["id"] != bid_id
    data_cleaned.loc[mask] = data_cleaned.loc[mask].fillna(0)

    return data_cleaned


def train_model(data_cleaned):
    X = data_cleaned.drop(columns=["id", "final_cost"])
    y = data_cleaned["final_cost"]
    random_forest_model = RandomForestRegressor(random_state=42)

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.1, random_state=42
    )

    # Train the model
    random_forest_model.fit(X_train, y_train)

    return X_test, random_forest_model, y_test


def predict_margin(current_bid_data, model, original_contract):
    if current_bid_data.isnull().values.any():
        raise HTTPException(400, "Not enough bid information to predict.")
    if original_contract == 0:
        predicted_margin = 0
        return predicted_margin
    predicted_cost = model.predict(current_bid_data)
    predicted_margin = 1 - (float(predicted_cost) / float(original_contract))
    return predicted_margin


# def evaluate_model_performance(X_test, random_forest_model, y_test):
#     # Predict and evaluate
#     y_pred = random_forest_model.predict(X_test)
#     mse = mean_squared_error(y_test, y_pred)
#     rmse = np.sqrt(mse)
#     r2 = r2_score(y_test, y_pred)
#     print("Mean Squared Error:", mse)
#     print("Root Mean Squared Error:", rmse)
#     print("R² Score:", r2)
