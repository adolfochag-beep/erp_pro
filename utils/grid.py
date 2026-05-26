from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder


def tabela(df):

    gb = GridOptionsBuilder.from_dataframe(df)

    gb.configure_pagination(
        enabled=True,
        paginationAutoPageSize=False,
        paginationPageSize=10
    )

    gb.configure_default_column(
        sortable=True,
        filter=True,
        resizable=True
    )

    gb.configure_side_bar()

    gridOptions = gb.build()

    AgGrid(
        df,
        gridOptions=gridOptions,
        fit_columns_on_grid_load=True,
        height=400
    )