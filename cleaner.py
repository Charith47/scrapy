from pymongo import MongoClient

CONNECTION_STRING = (
    "mongodb+srv://loki:cwdcwd123@cluster0.x7kb8.mongodb.net/scrapy-storage"
)


def delete_all_items():
    # get db
    db_client = MongoClient(CONNECTION_STRING)
    db = db_client["scrapy-storage"]
    db_collection = db["scrapy-news"]

    # delete all items
    db_collection.delete_many({})

    print("DELETED ALL ITEMS SUCCESSFULLY")


def user_confirm():
    usr_choice = input("DELETE ALL ITEMS FROM DATABASE? [y/n]")
    if usr_choice == "y":
        usr_collection_name = input("ENTER COLLECTION NAME: ")
        if usr_collection_name == "scrapy-news":
            delete_all_items()
        else:
            print("OPERATION FAILED")
            return
    elif usr_choice == "n":
        return


if __name__ == "__main__":
    user_confirm()
