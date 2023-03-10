import pandas as pd, math
from functools import reduce

def convert(terms, values):
    context = []
    
    for idx, val in enumerate(terms):
        temp = {
            "name": val,
            "values": []
        }
        
        for i, value in enumerate(values[idx]):
            temp["values"].append({"time": i+1, "value": value})    
            
        context.append(temp)
        
    return context

def update_csv(terms, values):
    df_data = {}
    df_data['time'] = [i+1 for i in range(len(values[0]))]
    for idx, term in enumerate(terms):
        df_data[term] = values[idx]

    try:
        # reating dataframe
        df = pd.DataFrame(df_data)

        # saving the dataframe
        df.to_csv('./home/static/csv/graph-data.csv', header=True, index=False)

        return "success"
    except:
        return "failure"

def graph_dict(values, name, base, terms, labels):
    Xval = len(labels)+1
    max_val = max(map(max, values))
    Yval = math.ceil(max_val*10)/10 + 0.2 

    return {
        "rangeX": Xval,
        "rangeY": Yval,
        "name" : name,
        "base_term": base,
        "rel_terms": terms,
        "period_labels": labels,
    }

def common_terms(mat):
    return list(reduce(lambda i, j: i & j, (set(x) for x in mat)))

