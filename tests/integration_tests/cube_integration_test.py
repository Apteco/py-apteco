import pandas as pd

from apteco import Cube


def test_cube_to_df_people_various_dimensions(
    holidays, people, cube_001_people_various_dimensions
):

    cube = Cube(
        [people[var] for var in ("Income", "Occupation", "Source")],
        table=people,
        session=holidays,
    )
    df = cube.to_df()
    df_reduced = df.reindex_like(cube_001_people_various_dimensions)

    missing_indices = df.index.difference(cube_001_people_various_dimensions.index)
    assert all("TOTAL" in idx[:-1] for idx in missing_indices)

    pd.testing.assert_frame_equal(
        df_reduced, cube_001_people_various_dimensions, check_dtype=False, check_like=True
    )
