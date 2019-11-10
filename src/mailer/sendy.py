from datetime import date
import json

import yagmail


def get_template(**kwargs):
    return """
    <tr>
        <td>
            <img src="{photo}">
        </td>
        <td>
            <p>Price: {price}</p>
            <p>Bedrooms: {bedrooms}</p>
            <p>Bathrooms: {bathrooms}</p>
            <p><a href="{url}" target="_blank">Listing Link</a></p>
        </td>
    </tr>
""".format(**kwargs)


def send_condos():
    contents = make_contents()
    yag = yagmail.SMTP('python.email.879')
    subject = f'Rincon Condos {date.today()}'
    to = ['dmegbert@gmail.com', 'shanoz617@gmail.com']
    yag.send(to, subject, contents)


def make_contents():
    with open('/Users/egbert/projects/condo/data/condos.json', 'r') as f:
        data = json.load(f)

    data = sorted(data, key=_sorter, reverse=True)
    template_start = f'<h2>Check out {len(data)} possible dream homes!</h2><table><tbody>'
    template_end = '</tbody></table>'
    table_rows = [(get_template(**condo)) for condo in data]
    return [template_start, *table_rows, template_end]


def _sorter(element):
    bedrooms = 0
    try:
        bedrooms = int(element.get('bedrooms'))
    except ValueError:
        pass
    return bedrooms


if __name__ == '__main__':
    send_condos()
