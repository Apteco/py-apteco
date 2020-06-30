import pandas as pd

from apteco import DataGrid


def test_datagrid_to_df_bookings_various_columns(holidays, bookings, data_dir):
    expected_df = pd.read_csv(data_dir / "datagrid_001_bookings_various_columns.csv")
    expected_df.loc[:, "Booking URN"] = expected_df.loc[:, "Booking URN"].astype(str)
    expected_df.loc[:, "Booking Date"] = pd.to_datetime(
        expected_df.loc[:, "Booking Date"],
        format="%d/%m/%Y",
    ).dt.date

    bookings_dg = DataGrid(
        [
            bookings[var] for var in
            (
                "boURN",  # Reference (Numeric)
                "boDest",  # Selector
                "boProd",  # Selector
                "boCost",  # Currency (2 dp)
                "boDate",  # Date
            )
        ],
        table=bookings,
        session=holidays,
    )
    bookings_df = bookings_dg.to_df()

    pd.testing.assert_frame_equal(bookings_df, expected_df, check_dtype=False)


def test_datagrid_to_df_policies_2000_rows_various_columns(holidays, policies, data_dir):
    expected_df = pd.read_csv(
        data_dir / "datagrid_002_policies_2000_rows_various_columns.csv",
    )
    expected_df.loc[:, "Policy Number"] = expected_df.loc[:, "Policy Number"].astype(str)
    expected_df.loc[:, "Policy Date"] = pd.to_datetime(
        expected_df.loc[:, "Policy Date"],
        format="%d/%m/%Y",
    ).dt.date

    policies_dg = DataGrid(
        [
            policies[var] for var in
            (
                "PoPolicy",  # Reference (Numeric)
                "PoDaysUn",  # Numeric (0 dp)
                "PoPremiu",  # Currency (2 dp)
                "PoPolic1",  # Date
                "PoCover",  # Selector
             )
         ],
        max_rows=2000,
        table=policies,
        session=holidays,
    )
    pol_df = policies_dg.to_df()

    pd.testing.assert_frame_equal(pol_df, expected_df, check_dtype=False)


def test_datagrid_to_df_web_visits_mobile_social_media_1500_rows_all_columns(
        holidays, web_visits, data_dir
):
    expected_df = pd.read_csv(
        data_dir / "datagrid_003_web_visits_mobile_social_media_1500_rows_all_columns.csv",
    )
    expected_df.loc[:, "Web URN"] = expected_df.loc[:, "Web URN"].astype(str)
    expected_df.loc[:, "Web Visit Time"] = pd.to_datetime(
        expected_df.loc[:, "Web Visit Time"],
        format="%d/%m/%Y %H:%M:%S",
    )

    web_visits_dg = DataGrid(
        [
            web_visits[var] for var in
            (
                "wvURN",  # Reference (Numeric)
                "wvURL",  # Text
                "wvTime",  # DateTime
                "wvDevice",  # Selector
                "wvDuratn",  # Numeric (0 dp, with missing)
                "wvSource",  # Selector
            )
         ],
        selection=((web_visits["wvSource"] == "S") & (web_visits["wvDevice"] == "3")),
        max_rows=1500,
        session=holidays,
    )
    web_visits_df = web_visits_dg.to_df()

    pd.testing.assert_frame_equal(web_visits_df, expected_df, check_dtype=False)

