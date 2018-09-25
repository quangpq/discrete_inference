from bs4 import BeautifulSoup


def openHTMLfile(name):
    path = "/Users/quangphan/Documents/Projects/discrete_thesis/data/" + name + ".html"
    with open(path, "r") as f:
        soup = BeautifulSoup(f, features="html.parser")
        tags = soup.findAll('div')

    return converHTML2SQL(tags)


def converHTML2SQL(divTag):
    results = []
    for tag in divTag:
        if 'id' in tag.attrs:
            k = tag.attrs['id']
            content = str(tag)
            statement = f'UPDATE `knowledges` SET `content`=\'{content}\' WHERE `keyphrase` = \'{k}\';\n'
            results.append(statement)

    return results


if __name__ == "__main__":
    filenames = ["Set", "Logic", "Boolean", "Relation"]

    statements = []
    for filename in filenames:
        statements.extend(openHTMLfile(filename))

    with open("/Users/quangphan/Documents/Projects/discrete_thesis/sql/html_content.txt", "w") as the_file:
        the_file.writelines(statements)
