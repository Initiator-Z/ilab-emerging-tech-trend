import arxiv
import pandas as pd

def get_academic_data(query, num):
    search = arxiv.Search(
        query=query,
        max_results=num,
        sort_by=arxiv.SortCriterion.Relevance
    )

    data_list = []

    for result in search.results():
        data = {
            'title': result.title,
            'entry_id': result.entry_id,
            'publish_date': result.published,
            #'authors': result.authors,
            'authors': str(result.authors),
            'description': result.summary,
            'primary_category': result.primary_category,
            'categories': result.categories,
            'link': str(result.links),
            'pdf_url': result.pdf_url
        }

        data_list.append(data)

    df = pd.DataFrame.from_dict(data_list)
    return df
