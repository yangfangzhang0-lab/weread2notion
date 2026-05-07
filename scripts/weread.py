def insert_to_notion(bookName, bookId, cover, sort, author, isbn, rating, categories):
    """插入到notion"""
    if not cover or not cover.startswith("http"):
        cover = "https://www.notion.so/icons/book_gray.svg"
    parent = {"database_id": database_id, "type": "database_id"}
    properties = {
        "书名": get_title(bookName),
        "BookId": get_rich_text(bookId),
        "ISBN": get_rich_text(isbn),
        "链接": get_url(
            f"https://weread.qq.com/web/reader/{calculate_book_str_id(bookId)}"
        ),
        "Sort": get_number(sort),
        "评分": get_number(rating),
        "封面": get_file(cover),
    }
    if categories != None:
        properties["分类"] = get_multi_select(categories)
    read_info = get_read_info(bookId=bookId)
    if read_info != None:
        markedStatus = read_info.get("markedStatus", 0)
        readingTime = read_info.get("readingTime", 0)
        readingProgress = read_info.get("readingProgress", 0)
        format_time = ""
        hour = readingTime // 3600
        if hour > 0:
            format_time += f"{hour}时"
        minutes = readingTime % 3600 // 60
        if minutes > 0:
            format_time += f"{minutes}分"
        properties["阅读状态"] = get_select("已读" if markedStatus == 4 else "在读")
        properties["阅读时长"] = get_number(readingTime)
        properties["阅读进度"] = get_number(readingProgress / 100)
        if "finishedDate" in read_info:
            properties["最后阅读时间"] = get_date(
                datetime.utcfromtimestamp(read_info.get("finishedDate")).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            )

    icon = get_icon(cover)
    response = client.pages.create(parent=parent, icon=icon, cover=icon, properties=properties)
    id = response["id"]
    return id
