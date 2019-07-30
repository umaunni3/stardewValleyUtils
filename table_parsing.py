import requests
import lxml.html as lh
import pandas as pd

def get_table(url, id="roundedborder"):
    """ Given a URL and the ID of the element to retrieve,
    makes a GET request to retrieve the body of the HTML DOM
    element with the ID specified (if it exists). Returns a list
    of the <tr> elements of the table (if the table exists);
    else, returns None.
    """

    page = requests.get(url)
    doc = lh.fromstring(page.content)
    row_elements = doc.xpath('//tr')
    return row_elements


def parse_row(row, categories):
    """ Given a row of the table, parses it to produce a dictionary
    containing the row's data for each of the 7 columns (specified
    by the categories parameter):
        {'Villager', 'Birthday', 'Loves', 'Likes', 'Neutral',
          'Dislikes', 'Hates'}
    If the row is malformed or complications arise during parsing,
    returns None. Otherwise, returns the dictionary.
    """

    i = 0
    data = {}
    for elem in row:
        value = elem.text_content()
        # print("====VALUE: ", value)
        values_list = value.strip().split('\n') # trim off last elem bc it's empty
        values_list = [v.strip() for v in values_list]
        if not values_list[0]:
            values_list = values_list[1:]
        if len(values_list) == 1:
            values_list = values_list[0]
        data[categories[i]] = values_list
        i += 1
    print("DATA!!!", data)
    return data

def retrieve_categories(row):
    """ Given the first row of a table, parse it to return a list
    of its values; this will serve as the set of categories used
    by other functions in this program. """

    categories = []
    for elem in row:
        print("++++ ELEM: ", elem.text_content())
        categories.append(elem.text_content().replace('\n', '').strip().split('\xa0')[0].strip())
    print("CATEGORIES!!!", categories)
    return categories

def generate_dataframe(url, id="roundedborder"):
    """ Given a URL and the ID of the table element to fetch,
    generates a Pandas Dataframe containing the data. """

    rows = get_table(url, id)
    categories = retrieve_categories(rows[0])
    all_data = merge_dict(rows[1:], categories)
    df = pd.DataFrame(all_data)
    df.set_index('Villager', inplace=True)
    return df


def merge_dict(lst, categories):
    """ Takes in a list of dictionaries with the same keys, and
    merges them into a format which will let us convert into a
    DataFrame. Returns a dictionary. """
    all_data = {category: [] for category in categories}

    # first row (containing categories/headers) should have been trimmed off already
    for row in lst:  # don't use first row, as it just contains the categories/headers
        parsed_row = parse_row(row, categories)
        print(parsed_row)
        for category, lst in all_data.items():
            lst.append(parsed_row[category])

    return all_data


def is_contained(df, categories, value):
    """ Searches the given DataFrame for rows which contain the
    specified value in the specified columns (categories). Returns
    a DataFrame containing only those rows where the value was
    found in the specified columns, sorted by which column it was
    found in. """


    new_data = {category:[] for category in categories}
    # yay i love being inefficient
    for row in df.iterrows():
        villager, data = row
        for category in categories:
            this_category = data[category]
            if (type(this_category) is list and any([value.lower() == v.lower() for v in this_category])) or (type(this_category) is str and value.lower() == this_category.lower()):
                this_elem_dict = dict(data)
                this_elem_dict['Villager'] = villager
                new_data[category].append(this_elem_dict)
    return new_data


def item_search(item_name, df=None, return_table=False):
    """ Given an item and DataFrame, create a table of all the
    villagers who either Love, Like, or are Neutral towards that
    item. Provide the output as a dictionary with keys 'Love',
    'Like', and 'Neutral', with each key corresponding to a list
    of villagers who have that sentiment towards the item. """

    df = df or data_table
    query_result = is_contained(df, ['Loves', 'Likes', 'Neutral'], item_name)
    if return_table:
        return query_result
    else:
        not_all_empty = False
        output = {'Loves':[], 'Likes':[], 'Neutral':[]}
        for key in ['Loves', 'Likes', 'Neutral']:
            dct = query_result[key]
            if len(dct) > 0:
                not_all_empty = True
            output[key] = [entry['Villager'] for entry in dct]
        return None if (not not_all_empty) else output

def villager_search(villager_name, df=None, return_table=False):

    df = df or data_table
    if villager_name in df.index:
        data = df.loc[villager_name]
        output = {}
        # print("!!!!!*@(&#Q*@&# " + data['Likes'])
        for keyword in ['Loves', 'Likes', 'Neutral']:
            if type(data[keyword]) is str:
                output[keyword] = [data[keyword]]
            else:
                output[keyword] = data[keyword]
        # output['Loves'] = list(data['Loves'])
        # output['Likes'] = list(data['Likes'])
        # output['Neutral'] = list(data['Neutral'])
        return output
    else:
        return None


all_flowers = ['Sweet Pea', 'Crocus', 'Sunflower', 'Tulip', 'Summer Spangle', 'Fairy Rose',
            'Blue Jazz', 'Poppy']
all_artisan_goods = ['Honey', 'Wine', 'Pale Ale', 'Beer', 'Mead', 'Cheese', 'Goat Cheese', 'Coffee',
                     'Cloth', 'Mayonnaise', 'Duck Mayonnaise', 'Void Mayonnaise', 'Truffle Oil',
                     'Oil', 'Pickles', 'Jelly']
data_table = generate_dataframe('https://stardewvalleywiki.com/List_of_All_Gifts')