import pandas as pd
import numpy as np
import jinja2
from os import path

def Report(data, columns, index, report='report'):

    # Sample DataFrame
    df = pd.DataFrame(data, columns=columns, index=index)

    # See: https://pandas.pydata.org/pandas-docs/stable/user_guide/style.html#Building-styles
    def func(val):
        color = 'black'
        return f'color: {color}'
    
    styler = df.style.applymap(func)
    
    # Template handling
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=''))
    template = env.get_template(path.join(path.curdir, 'report', 'template.html'))
    html = template.render(my_table=styler.render())
        
    # Write the HTML file
    with open(path.join(path.curdir, 'output', f'{report}.html'), 'w') as f:
        f.write(html)
    
        print(f'HTML exported: {report}.html')
