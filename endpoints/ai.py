from fastapi import APIRouter, Depends, HTTPException
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sqlalchemy.orm import Session
import numpy as np
from crud import ai
from core import security, deps
from crud.ai import get_bid_data_for_prediction
from schemas.base import SuccessResponse
from typing import Annotated
from models.user import User
import pandas as pd

router = APIRouter(prefix="/ai", tags=["ai"])


@router.get("/{bid_id}", response_model=SuccessResponse[float])
async def get_bid(
    bid_id: int,
    # current_user: Annotated[User, Depends(security.get_current_user)],
    db: Session = Depends(deps.get_db),
):
    # if not current_user.has_role("Bid Manager"):
    #     raise HTTPException(401, "Missing Bid Manager role")

    bids = get_bid_data_for_prediction(db)

    data = []
    for bid in bids:
        # exclude bid we are predicting
        if bid.id == bid_id:
            continue  # Skip this bid and do not include it in the dataset

        row = {
            column.name: getattr(bid, column.name) for column in bid.__table__.columns
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

    # choose columns more than 50% missing values
    threshold = 0.4 * len(df)
    data_cleaned = df.dropna(thresh=threshold, axis=1)

    columns_to_drop = ["id", "name", "created_at", "comments"]
    data_cleaned = data_cleaned.drop(
        columns=[col for col in columns_to_drop if col in data_cleaned.columns]
    )
    data_cleaned = data_cleaned.fillna(0)
    print(data_cleaned)

    X = data_cleaned.drop(columns=["final_cost", "margin"])
    y = data_cleaned["final_cost"]

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train the model
    random_forest_model = RandomForestRegressor(random_state=42)
    random_forest_model.fit(X_train, y_train)

    # Predict and evaluate
    y_pred = random_forest_model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)

    print("Mean Squared Error:", mse)
    print("Root Mean Squared Error:", rmse)
    print("R² Score:", r2)

    return SuccessResponse(data=1.0)
