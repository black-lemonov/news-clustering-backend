from fastapi.responses import Response


class NewsCSVTable(Response):
    table_filename = "news_with_summaries.csv"
    media_type = "text/csv",
    headers = {
        "Content-Disposition": f"attachment; filename={table_filename}",
        "Content-Type": "text/csv; charset=utf-8"
    }
