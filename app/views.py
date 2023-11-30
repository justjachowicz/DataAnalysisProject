from flask import render_template, Blueprint
from . import db
from functools import reduce
from app.config.configGetter import get_list_of_countries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

views = Blueprint('views', __name__)


@views.route('/<disorder>')
def disorder_page(disorder):
    """
    render template for disorder page
    :param disorder: disorder name
    :return: html page
    """
    number_countries_pos_corr, dic_of_countries_pos_corr = \
        count_countries_positive_corr(disorder)

    number_of_countries_neg_corr, dic_of_countries_neg_corr = \
        count_countries_negative_corr(disorder)

    return render_template('disorder.html',
                           title=f'{disorder.title()}',
                           disorder=disorder,
                           number_countries_pos_corr=number_countries_pos_corr,
                           dic_of_countries_pos_corr=dic_of_countries_pos_corr,
                           number_of_countries_neg_corr=number_of_countries_neg_corr,
                           dic_of_countries_neg_corr=dic_of_countries_neg_corr
                           )


@views.route('/<disorder>/<country>')
def load_data(country, disorder):
    """
    render template for disorder_by_country page
    :param country: country name
    :param disorder: disorder name
    :return: html page
    """

    corr_coefficient = correlation_coefficient(country, disorder)

    linear_plot = create_linear_graph(country, disorder)
    linear_plot_path = 'app/static/linear_plot.png'
    linear_plot.savefig(linear_plot_path, bbox_inches='tight')

    regression_plot = create_regression_plot(country, disorder)
    regression_plot_path = 'app/static/regression_plot.png'
    regression_plot.savefig(regression_plot_path, bbox_inches='tight')

    return render_template(
        'disorder_by_country.html',
        title=f'{disorder.title()} - {country.title()}',
        country=country,
        disorder=disorder,
        corr_coefficient=corr_coefficient
    )


@views.route('/<country>/aggregate')
def aggregate_analysis(country):
    """
    render template for aggregate_analysis page
    :param country: country name
    :return: html page
    """

    heatmap = create_heat_map(country)
    heatmap_path = 'app/static/heatmap.png'
    heatmap.savefig(heatmap_path, bbox_inches='tight')

    return render_template('aggregate_analysis.html',
                           country=country,
                           title='Aggregate analysis')


def modify_disorder_name(disorder):
    """
    create column name for disorder index and table name in database
    :param disorder: disorder name
    :return: column name for disorder index and table name in database
    """
    if 'disorder' in disorder:
        beginning = disorder[:-9]
        table_name = beginning + 'Disorder'
        disorder_index = beginning + '_disorder_index'
    else:
        disorder_index = disorder.lower() + '_index'
        table_name = disorder

    return disorder_index, table_name


@views.route('/fig/<country>/<disorder>')
def create_linear_graph(country, disorder):
    """
    render linear graph showing life quality and disorder prevalence over time for a given country
    :param country: country name
    :param disorder: disorder name
    :return: linear graph
    """

    conn = db.get_db()
    disorder_index, table_name = modify_disorder_name(disorder)

    disorder_df = pd.read_sql(
        f'SELECT country, year, {disorder_index} FROM {table_name} '
        f'WHERE country="{country.title()}" ORDER BY YEAR', conn)
    life_quality_df = pd.read_sql(
        f'SELECT country, year, life_quality FROM life_quality '
        f'WHERE country="{country.title()}" ORDER BY YEAR', conn)

    years = disorder_df['year']
    disorder_prevalence = disorder_df[disorder_index]
    life_quality = life_quality_df['life_quality']

    fig, ax1 = plt.subplots(figsize=(8, 4))

    ax1.plot(years, life_quality, color='black', label='Life quality')
    ax1.grid(False)
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Life quality', color='black')
    ax1.tick_params(axis='y', labelcolor='black')

    ax2 = ax1.twinx()
    ax2.plot(years, disorder_prevalence, color='royalblue', label=f'{disorder.title()} index')
    ax2.grid(False)
    ax2.set_ylabel(f'{disorder.title()}  index', color='royalblue')
    ax2.tick_params(axis='y', labelcolor='royalblue')
    plt.subplots_adjust(bottom=0.15,)
    plt.title(f'Life quality index and {disorder} prevalence rate in {country.title()} (2012-2019)')

    return plt


def count_countries_positive_corr(disorder):
    countries_with_high_corr_coefficient = {}
    countries = get_list_of_countries()
    for country in countries:
        corr_coefficient = correlation_coefficient(country, disorder)
        if corr_coefficient > 0.7:
            countries_with_high_corr_coefficient[country] = corr_coefficient

    return len(countries_with_high_corr_coefficient), countries_with_high_corr_coefficient


def count_countries_negative_corr(disorder):
    countries_with_high_corr_coefficient = {}
    countries = get_list_of_countries()
    for country in countries:
        corr_coefficient = correlation_coefficient(country, disorder)
        if corr_coefficient < -0.7:
            countries_with_high_corr_coefficient[country] = corr_coefficient

    return len(countries_with_high_corr_coefficient), countries_with_high_corr_coefficient


@views.route('/correlation_coefficient/<country>/<disorder>')
def correlation_coefficient(country, disorder):
    """
    calculate correlation coefficient for specific country and disorder
    :param country: country name
    :param disorder: disorder name
    :return: correlation coefficient
    """
    conn = db.get_db()
    disorder_index, table_name = modify_disorder_name(disorder)

    disorder_df = pd.read_sql(
        f'SELECT country, year, {disorder_index} FROM {table_name} '
        f'WHERE country="{country.title()}" ORDER BY YEAR', conn)
    life_quality_df = pd.read_sql(
        f'SELECT country, year, life_quality FROM life_quality '
        f'WHERE country="{country.title()}" ORDER BY YEAR', conn)
    merged_df = disorder_df.merge(life_quality_df, on=['country', 'year'])

    corr_coefficient = merged_df['life_quality'].corr(merged_df[disorder_index])
    corr_coefficient = round(corr_coefficient, 2)

    return corr_coefficient


@views.route('/create_regression_plot/<country>/<disorder>/')
def create_regression_plot(country, disorder):
    """
    create regression plot for given country and disorder
    :param country: country name
    :param disorder: disorder name
    :return: regression plot
    """
    conn = db.get_db()

    disorder_index, table_name = modify_disorder_name(disorder)

    disorder_df = pd.read_sql(
        f'SELECT country, year, {disorder_index} FROM {table_name} '
        f'WHERE country="{country.title()}" ORDER BY YEAR', conn)
    life_quality_df = pd.read_sql(
        f'SELECT country, year, life_quality FROM life_quality '
        f'WHERE country="{country.title()}" ORDER BY YEAR', conn)

    merged_df = disorder_df.merge(life_quality_df, on=['country', 'year'])

    # todo: check if everything is necessary
    sb.set()
    sb.set_style('whitegrid')
    sb.lmplot(x='life_quality', y=f'{disorder_index}', data=merged_df)
    plt.xlabel('Life quality')
    plt.ylabel(f'{disorder.title()} index')
    plt.legend()
    plt.title('Linear regression plot')
    plt.subplots_adjust(bottom=0.15)
    return plt


@views.route('/fig/<country>/aggregate')
def create_heat_map(country):
    """
    create heat map showing correlation of all variables for a given country
    :param country: country name
    :return: heat map
    """
    conn = db.get_db()

    bipolar_disorder = pd.read_sql(
        f'SELECT country, year, bipolar_disorder_index FROM bipolarDisorder '
        f'WHERE country="{country.title()}" ORDER BY YEAR', conn)
    depression = pd.read_sql(
        f'SELECT country, year, depression_index FROM depression '
        f'WHERE country="{country.title()}" ORDER BY YEAR', conn)
    eating_disorder = pd.read_sql(
        f'SELECT country, year, eating_disorder_index FROM eatingDisorder '
        f'WHERE country="{country.title()}" ORDER BY YEAR', conn)
    life_quality = pd.read_sql(
        f'SELECT country, year, life_quality FROM life_quality '
        f'WHERE country="{country.title()}" ORDER BY YEAR', conn)
    schizophrenia = pd.read_sql(
        f'SELECT country, year, schizophrenia_index FROM schizophrenia '
        f'WHERE country="{country.title()}" ORDER BY YEAR', conn)

    dfs = [bipolar_disorder, depression, eating_disorder, life_quality, schizophrenia]

    # merge all DataFrames into one
    final_df = reduce(lambda left, right: pd.merge(left, right, on=['country', 'year'],
                                                   how='outer'), dfs)

    final_df = final_df[['bipolar_disorder_index',
                         'depression_index',
                         'eating_disorder_index',
                         'life_quality',
                         'schizophrenia_index']].\
        rename(columns={
            'bipolar_disorder_index': 'bipolar disorder',
            'depression_index': 'depression',
            'eating_disorder_index': 'eating disorder',
            'life_quality': 'life quality',
            'schizophrenia_index': 'schizophrenia'
        })

    fig, ax1 = plt.subplots(figsize=(10, 6))
    sb.heatmap(final_df.corr(), cmap="YlGnBu", annot=True)
    ax1.grid(False)
    plt.title('Correlation heatmap')

    return plt
