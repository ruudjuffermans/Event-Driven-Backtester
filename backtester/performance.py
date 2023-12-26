import numpy as np
import pandas as pd


def create_sharpe_ratio(returns, periods=252):
    return np.sqrt(periods) * (np.mean(returns)) / np.std(returns)


def create_drawdowns(equity_curve):
    high_water_mark = [0]

    idx = equity_curve.index
    drawdown = pd.Series(index=idx)
    duration = pd.Series(index=idx)

    for i in range(1, len(idx)):
        high_water_mark.append(max(high_water_mark[i - 1], equity_curve[i]))
        drawdown[i] = high_water_mark[i] - equity_curve[i]
        duration[i] = 0 if drawdown[i] == 0 else duration[i - 1] + 1
    return drawdown, drawdown.max(), duration.max()
