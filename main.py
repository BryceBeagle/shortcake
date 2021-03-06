import uvicorn

from shortcake.asgi.app import ShortcakeApp
from shortcake.database.management import ShortcakeDatabase

DATABASE_HOSTNAME = "postgres"
DATABASE_NAME = "shortcake"


def main():
    database = ShortcakeDatabase(
        database_name=DATABASE_NAME,
        hostname=DATABASE_HOSTNAME,
    )

    if not database.exists:
        database.create()

    database.connect()
    database.create_tables()

    app = ShortcakeApp(debug=True)

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")


if __name__ == "__main__":
    main()
