import pandas as pd


def add_score2excel(score: float, filename: str):
    try:
        resultDf = pd.read_excel(filename, index_col=0)
    except:
        resultDf = pd.DataFrame(columns=["score"])

    newData = {"score": score}
    resultDf = resultDf.append(newData, ignore_index=True)

    mean = resultDf.score.mean()
    std = resultDf.score.std()
    n = len(resultDf.score)

    print(f"score is {mean} ± {2 * std} (2σ) with n = {n}")
    resultDf.to_csv(filename, sep=",", index=False)
