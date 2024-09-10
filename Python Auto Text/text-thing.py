def AutoFormat(content : list, title : str):
    biggest = max(content)
    padding = round(len(biggest))
    lenth = len(biggest) + padding

    half_title = lenth/2
    title_surround = '-'*(round(half_title) - round(len(title)/2)+1)

    print(f"{title_surround}{title}{title_surround}")
    for word in content:
        content_end = ' '*(lenth - len(word)-1)
        print(f"| {word}{content_end}|")


content = ["I just authed in gtag", "made by clown", "it is FUDDDDD", "its called an 0day", "kid..."]
AutoFormat(content, "Wsg mommies")