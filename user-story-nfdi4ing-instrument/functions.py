import requests
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import json
import datetime
import altair as alt
# import vega
from IPython.core.display import display, HTML
alt.renderers.enable('default')
import regex


_transport = RequestsHTTPTransport(
    url='https://api.datacite.org/graphql',
    use_json=True,
)

client = Client(
    transport=_transport,
    fetch_schema_from_transport=True,
)



def get_events_by_doi_and_relation_type(doi, relation_type):
    params = {'doi':  doi , 'relation_type_id': relation_type, 'rows': 1000}
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
        }
      }
    """)

    try:
        data = client.execute(query, variable_values=json.dumps(query_params))
    except Exception as e:
        print("Unable to get metadata for %s: %s" % (doi, e))
        return None

    return data


def format_citations(events, include_authors=False):

    ids = extract_ids(events)

    query_params = {
        "instrumentIds" : ids
    }

    author_query ="""authors {
        title
        id
    }""" if include_authors else ''

    query = gql("""query getInstruments($instrumentIds: [String!])
        {
            works(ids: $instrumentIds) {
                """ + author_query + """
                nodes {
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


def render_histogram(spec):
    return(alt.Chart.from_dict(spec))



def generate_html(metadata, datasets_table_html, publications_table_html, related_works_table_html, authors_table_html):
    HTML_TEMPLATE_FILE = './nfdi-template.html'
    STYLES_FILE = './nfdi-styles.css'
    html = ''
    styles = ''

    with open(HTML_TEMPLATE_FILE, 'r') as html_template, open(STYLES_FILE) as styles_file:
        html = html_template.read()
        styles = styles_file.read()
    
    html = html.format(
        style=styles,
        formatted_citation=metadata['work']['formattedCitation'],
        citation_count=metadata['work']['citationCount'],
        repository_link=metadata["work"]["repository"]["uid"],
        repository_name=metadata["work"]["repository"]["name"],
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
    
    html = f"""<table>
        <tr><th><h3>{title}</h3></tr></th>
        {rows}
    </table>"""

    return html



def main(doi):

    # Instrument metadata display
    metadata = get_metadata_display(doi)

    if metadata is None:
        return("Unable to get metadata for %s" % (doi))   

    # Instrument connections list and histogram
    related_works_events = get_events_by_doi_and_relation_type(doi, '')
    spec = generate_histogram_spec(related_works_events['meta']['occurred'])

    # Data that used an instrument
    datasets_events = get_events_by_doi_and_relation_type(doi, 'is-compiled-by')
    formatted_citations = format_citations(datasets_events)
    datasets_data = map(lambda item: item['formattedCitation'], formatted_citations['works']['nodes'])
    datasets_html = generate_html_table('Datasets', datasets_data)

    # Publications that used an instrument
    publications_events = get_events_by_doi_and_relation_type(doi, 'is-referenced-by')
    formatted_citations = format_citations(publications_events)
    publications_data = map(lambda item: item['formattedCitation'], formatted_citations['works']['nodes'])
    publications_html = generate_html_table('Publications', publications_data)

    # Related works
    related_works_events = get_events_by_doi_and_relation_type(doi, '')
    formatted_citations = format_citations(related_works_events, include_authors=True)
    related_works_data = map(lambda item: item['formattedCitation'], formatted_citations['works']['nodes'])
    related_works_html = generate_html_table('Related Works', related_works_data)

    # Co-authors List
    authors_data = map(lambda item: item['title'], formatted_citations['works']['authors'])
    authors_html = generate_html_table('Authors', authors_data)


    # Generate and save full HTML
    html = generate_html(metadata, datasets_html, publications_html, related_works_html, authors_html)
    display(HTML(html))

    # with open('./nfdi.html', 'w') as file:
    #     file.write(html)


    # Histogram
    spec = generate_histogram_spec(related_works_events['meta']['occurred'])
    return render_histogram(spec)