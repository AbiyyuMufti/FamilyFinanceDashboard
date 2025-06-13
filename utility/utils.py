import polars as pl

def currency_to_number(column_to_convert:str) -> pl.Expr:
    return (
        pl.col(column_to_convert)
        .str.replace_all(r'[Rp.\s]', '')
        .str.replace(',','.').cast(pl.Float64)
    )