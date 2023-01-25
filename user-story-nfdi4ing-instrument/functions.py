import datetime
import json
import os
import regex
from IPython.core.display import display, HTML
import vega
import altair as alt
import altair_saver
import vl_convert as vlc
import requests
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

alt.renderers.enable('default')


_transport = RequestsHTTPTransport(
    url='https://api.datacite.org/graphql',
    use_json=True,
)

client = Client(
    transport=_transport,
    fetch_schema_from_transport=True,
)



def get_events_by_doi_and_relation_type(doi, relation_type):
    params = {'doi':  doi , 'relation_type_id': relation_type, 'page[size]': 100}
    try:
        events = requests.get('https://api.datacite.org/events', params=params)
        events.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
        return None
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
        return None
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
        return None
    except requests.exceptions.RequestException as err:
        print ("OOps: Something Else",err)
        return None
    
    return events.json()


def get_metadata_display(doi):
    query_params = {
        "instrumentId" : doi
    }

    query = gql("""query getInstrument($instrumentId: ID!)
      {
        work(id: $instrumentId) {
          id
          citationCount
          formattedCitation
          repository {
            uid
            name
          }
          citations{
            nodes{
                id
                formattedCitation
            }
          }
        }
      }
    """)

    try:
        data = client.execute(query, variable_values=json.dumps(query_params))
    except Exception as e:
        print("Unable to get metadata for %s: %s" % (doi, e))
        return None

    return data


def format_citations(events, resourceType, include_authors=False):

    ids = extract_ids(events)
    if len(ids) == 0: return None

    query_params = {
        "instrumentIds" : ids
    }

    author_query ="""authors {
        title
        id
    }""" if include_authors else ''

    query = gql("""query getInstruments($instrumentIds: [String!])
        {
            """ + resourceType + """(ids: $instrumentIds) {
                """ + author_query + """
                nodes {
                    id
                    formattedCitation
                }
            }
        }
    """)

    try:
        formatted_citations = client.execute(query, variable_values=json.dumps(query_params))
    except Exception as e:
        print("Unable to get metadata for %s: %s" % ("events", e))
        return None

    return formatted_citations



def extract_ids(events):
    """Return the property sub_id of array of events."""
    ids = []

    for event in events['data']:
        ids.append(get_doi_name_from_doi_url(event['attributes']['subj-id']))
        ids.append(get_doi_name_from_doi_url(event['attributes']['obj-id']))

    return [x for x in ids if x is not None]


def get_doi_name_from_doi_url(doi_url):
    m = regex.search(r'(?<=https://doi.org/)\b\S+', doi_url)
    if m:
        # Return the DOI suffix if it is found
        return m.group()
    else:
        # Return None if the DOI suffix is not found
        return None



def generate_histogram_spec(data):
    """Return a vega-lite specification for a bar chart with the citation counts."""
    ## data['meta']['occurred']
    
    chartWidth = 500
    thisYear = datetime.datetime.now().year + 1
    lowerBoundYear = int(((thisYear - 10) / 5) * 5)

    spec = {
    "$schema": 'https://vega.github.io/schema/vega-lite/v4.json',
    "data": {
        "values": data
    },
    "padding": { "left": 5, "top": 5, "right": 5, "bottom": 5 },
    "transform": [
        {
        "calculate": 'toNumber(datum.title)',
        "as": 'period'
        },
        {
        "calculate": 'toNumber(datum.title)+1',
        "as": 'bin_end'
        },
        {
        "filter": f"toNumber(datum.title) >= {lowerBoundYear}"
        }
    ],
    "width": chartWidth,
    "mark": {
        "type": 'bar',
        "cursor": 'pointer',
        "tooltip": True
    },
    "selection": {
        "highlight": {
        "type": 'single',
        "empty": 'none',
        "on": 'mouseover'
        }
    },
    "encoding": {
        "x": {
        "field": 'period',
        "bin": {
            "binned": True,
            "step": 1,
            "maxbins": thisYear - lowerBoundYear
        },
        "type": 'quantitative',
        "axis": {
            "format": '1',
            "labelExpr": 'datum.label % 2 === 0 ? datum.label : ""'
        },
        "scale": {
            "domain": [lowerBoundYear, thisYear]
        }
        },
        "x2": {
        "field": 'bin_end'
        },
        "y": {
        "field": 'count',
        "type": 'quantitative',
        "axis": {
            "format": ',f',
            "tickMinStep": 1
        }
        },
        "color": {
        "field": 'count',
        "scale": { "range": ["#1abc9c"] },
        "type": 'nominal',
        "legend": None,
        "condition": [{ "selection": 'highlight', "value": '#34495e' }]
        }
    },
    "config": {
        "view": {
        "stroke": None
        },
        'axis': {
        "grid": False,
        "title": None,
        "labelFlush": False
        }
    }
    }
    return spec


def save_histogram(spec, name):
    chart = alt.Chart.from_dict(spec)

    png_data = vlc.vegalite_to_png(chart.to_dict())
    with open(f'charts/{name}.png', 'wb') as f:
        f.write(png_data)


def generate_html(metadata, chart_name, datasets_table_html, publications_table_html, related_works_table_html, authors_table_html):
    HTML_TEMPLATE_FILE = './nfdi-template.html'
    STYLES_FILE = './nfdi-styles.css'
    html = ''
    styles = ''

    with open(HTML_TEMPLATE_FILE, 'r') as html_template, open(STYLES_FILE) as styles_file:
        html = html_template.read()
        styles = styles_file.read()
    
    formatted_citation = ''
    citation_count = ''
    repo_link = ''
    repo_name = ''

    if metadata is not None and metadata['work'] is not None:
        formatted_citation = metadata['work']['formattedCitation']
        citation_count = metadata['work']['citationCount']

        if metadata['work']['repository'] is not None:
            repo_link = metadata['work']['repository']['uid']
            repo_name = metadata['work']['repository']['name']

    
    html = html.format(
        style=styles,
        formatted_citation=formatted_citation,
        citation_count=citation_count,
        repository_link=repo_link,
        repository_name=repo_name,
        chart=chart_name,
        datasets=datasets_table_html,
        publications=publications_table_html,
        related_works=related_works_table_html,
        authors=authors_table_html
    )
    return html


def generate_html_table(title, data):
    rows = ''
    for item in data:
        rows += '<tr><td>' + item + '</td></tr>'
    
    html = f"""<table class="list">
        <tr><th><h3>{title}</h3></tr></th>
        {rows}
    </table>"""

    return html

def deduplicate_ids(datasets_formatted_citations, citations_formatted_citations, related_works_formatted_citations):

    datasets_ids = map(lambda item: item['id'], datasets_formatted_citations['datasets']['nodes']) if datasets_formatted_citations is not None else []
    citations_ids = map(lambda item: item['id'], citations_formatted_citations['work']['citations']['nodes']) if citations_formatted_citations is not None else []
    ids = list(datasets_ids) + list(citations_ids) + [citations_formatted_citations['work']['id']]

    related_works_formatted_citations = list(filter(lambda item: item['id'] not in ids, related_works_formatted_citations['works']['nodes'])) if related_works_formatted_citations is not None else []

    return related_works_formatted_citations


def main(doi):
    # Instrument metadata display
    metadata = get_metadata_display(doi)

    if metadata is None:
        return f'Unable to get metadata for {doi}'
    
    doiSet = set([metadata['work']['formattedCitation']])

    # Data that used an instrument
    datasets_events = get_events_by_doi_and_relation_type(doi, 'is-compiled-by')
    datasets_formatted_citations = format_citations(datasets_events, 'datasets')
    datasets_data = map(lambda item: item['formattedCitation'], datasets_formatted_citations['datasets']['nodes']) if datasets_formatted_citations is not None else []
    datasets_html = generate_html_table('Datasets', set(datasets_data) - doiSet)

    # Citations (10.1002/cssc.201900799)
    citations_data = map(lambda item: item['formattedCitation'], metadata['work']['citations']['nodes']) if metadata['work']['citations']['nodes'] is not None else []
    citations_html = generate_html_table('Citations', set(citations_data) - doiSet)

    # Related works
    related_works_events = get_events_by_doi_and_relation_type(doi, '')
    formatted_citations = format_citations(related_works_events, 'works', include_authors=True)

    related_works_formatted_citations = deduplicate_ids(datasets_formatted_citations, metadata, formatted_citations)
    related_works_data = map(lambda item: item['formattedCitation'], related_works_formatted_citations) if related_works_formatted_citations is not None else []
    related_works_html = generate_html_table('Other Related Works', set(related_works_data))

    # Co-authors List
    authors_data = map(lambda item: f"{item['title']}<br><a href='{item['id']}'>{item['id']}</a>", formatted_citations['works']['authors']) if formatted_citations is not None else []
    authors_html = generate_html_table('Authors', set(authors_data))


    # Save histogram as SVG
    spec = generate_histogram_spec(related_works_events['meta']['occurred'])
    chart_name = doi.replace('/', '_')
    save_histogram(spec, chart_name)

    # Generate and save full HTML
    html = generate_html(metadata, chart_name, datasets_html, citations_html, related_works_html, authors_html)
    display(HTML(html))

    # with open('./nfdi.html', 'w') as file: file.write(html)