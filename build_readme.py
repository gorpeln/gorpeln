import feedparser
import pathlib
import re
from datetime import datetime

root = pathlib.Path(__file__).parent.resolve()


def replace_chunk(content, marker, chunk, inline=False):
    pattern = re.compile(
        r"<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->".format(marker, marker),
        re.DOTALL,
    )
    if not inline:
        chunk = "\n{}\n".format(chunk)
    chunk = f"<!-- {marker} starts -->{chunk}<!-- {marker} ends -->"
    return pattern.sub(chunk, content)


def fetch_blog_entries():
    feed = feedparser.parse("https://gorpeln.top/feed.xml")
    entries = feed.get("entries", [])
    result = []
    for entry in entries:
        try:
            pub_dt = datetime.strptime(entry["published"], "%a, %d %b %Y %H:%M:%S %z")
            pub_str = pub_dt.strftime("%Y-%m-%d")
            result.append({
                "title": entry["title"],
                "url": entry["link"].split("#")[0],
                "published": pub_str,
            })
        except Exception as e:
            print(f"解析单篇文章失败：{e}")
    return result


if __name__ == "__main__":
    readme_path = root / "README.md"
    readme_contents = readme_path.open("r", encoding="utf-8").read()

    entries = fetch_blog_entries()[:6]
    entries_md = "\n".join(
        [f'* <span style="background:#eee;padding:2px 6px;border-radius:6px;color:#444;">{entry["published"]}</span> · [{entry["title"]}]({entry["url"]})'
         for entry in entries]
    )
    rewritten = replace_chunk(readme_contents, "blog", entries_md)

    readme_path.open("w", encoding="utf-8").write(rewritten)
