from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def multi_year_bar(
    df: pd.DataFrame,
    bar_function,
    years=None,
    years_per_row: int = 3,
    figsize=(16, 6),
    sharex=True,
    sharey=True,
    **kwargs,
):
    """
    Create a collection of bar charts over years.

    Parameters
    ----------
    df : pd.DataFrame
        Expected to have "years" as the first level of index
        Additionally should have been passed through *turnout_year_key*
    bar_function : Callable
        Function accepting (df, year, ax=ax) and populating a bar graph
    years : arraylike, optional
        The years to make plots for. Default *None* will make for all years
        in the dataframe.
    years_per_row : int
        How many year plots to put on one year
    figsize, sharex, sharey:
        Passed on *plt.subplots*
    **kwargs :
        Passed to *bar_function*.

    Returns
    -------
    fig, axs
    """
    if years is None:
        years = sorted(df.index.unique(level=0))[::-1]
    nrows = np.ceil(len(years) / years_per_row).astype(int)
    fig, axs = plt.subplots(
        nrows, years_per_row, figsize=figsize, sharex=sharex, sharey=sharey
    )

    flat_ax = axs.reshape(-1)
    for i, year in enumerate(years):
        ax = flat_ax[i]
        ax.set_title(f"{year}")
        bar_function(df, year, ax=ax, **kwargs)

    # now hide any unused axes
    for i in range(len(years), nrows * years_per_row):
        flat_ax[i].axis("off")
    return fig, axs


def turnout_bar_graph(
    df: pd.DataFrame,
    year: float,
    registered_color="gray",
    voted_color="tab:green",
    ax=None,
    **style_kwargs,
):
    """Generate a bar graph of turnout by year.

    Can be used on it's own or as part of *multi_year_bar*

    Parameters
    ----------
    df : pd.DataFrame
        Output from the *turnout_by_year_key* function.
    year : Number
        The year to select from the index for plotting.
    registered_color : str
        The bar color for people who registered but did not vote.
    voted_color : str
        The bar color for people who voted.
    ax : matplotlib axis
        The axis on which to plot.
    **style_kwargs :
        Passed to *ax.bar*
    """
    if ax is None:
        ax = plt.gca()
    bar_width = style_kwargs.pop("bar_width", 3.75)
    ax.bar(
        df.loc[year]["mid_points"],
        df.loc[year]["registered"],
        width=bar_width,
        color=registered_color,
        label="Registered - did not vote",
        **style_kwargs,
    )
    ax.bar(
        df.loc[year]["mid_points"],
        df.loc[year]["voted"],
        width=bar_width,
        color=voted_color,
        label="Voted",
        **style_kwargs,
    )


def university_housing_bar_chart(
    df,
    year,
    idx,
    ax,
    bar_width=0.75,
):
    """Create a bar chart of voters living in the given University housing."""
    registered = df[idx].loc[year]["univ_housing_name"].value_counts().sort_index()
    voted = (
        df[idx]
        .loc[year]
        .groupby("univ_housing_name")
        .sum(numeric_only=True)
        .sort_index()
    )
    sort_idx = voted["voted"].argsort()[::-1]
    voted = voted.iloc[sort_idx]
    registered = registered.iloc[sort_idx]
    ax.bar(
        registered.index,
        registered,
        width=bar_width,
        color="gray",
        label="Registered - did not vote",
    )
    ax.bar(
        voted.index, voted["voted"], width=bar_width, color="tab:green", label="Voted"
    )
    ax.set_title(f"{year}")
    # adjust the names to drop the suffixes that are in there.

    ax.tick_params(axis="x", labelrotation=90)
