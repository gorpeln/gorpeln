import feedparser
import pathlib
import re
 
root = pathlib.Path(__file__).parent.resolve()


def replace_chunk(content, marker, chunk, inline=False):
    r = re.compile(
        r"<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->".format(marker, marker),
        re.DOTALL,
    )
    if not inline:
        chunk = "\n{}\n".format(chunk)
    chunk = "<!-- {} starts -->{}<!-- {} ends -->".format(marker, chunk, marker)
    return r.sub(chunk, content)




def fetch_blog_entries():
    entries = feedparser.parse("https://gorpeln.top/feed.xml")["entries"]
    return [
        {
            "title": entry["title"],
            "url": entry["link"].split("#")[0],
            "published": entry["published"].split("T")[0],
        }
        for entry in entries
    ]



if __name__ == "__main__":
    readme = root / "README.md"
    readme_contents = readme.open().read()


    entries = fetch_blog_entries()[:6]
    entries_md = "\n".join(
        ["* {published} - <a href='{url}' target='_blank'>{title}</a>".format(**entry) for entry in entries]
    )
    rewritten = replace_chunk(readme_contents, "blog", entries_md)

    readme.open("w").write(rewritten)

