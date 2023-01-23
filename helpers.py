def mb2mw(x):
    return 1.0319 * x + 0.2223


def md2mw(x):
    return 0.7947 * x + 1.3420


def ml2mw(x):
    return 0.8095 * x + 1.3003


def convertif(row):
    if row["type"] == "mb":
        row["magnitude"] = mb2mw(row["magnitude"])
    elif row["type"] == "md":
        row["magnitude"] = md2mw(row["magnitude"])
    elif row["type"] == "ml":
        row["magnitude"] = ml2mw(row["magnitude"])
    return row["magnitude"]
