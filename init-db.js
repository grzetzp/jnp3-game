db = db.getSiblingDB('test_mongodb');

db.test_tb.drop();

db.test_tb.insertMany([
    {
        "id": 1,
        "name": "asd"
    },
    {
        "id": 2,
        "name": "def"
    },
    {
        "id": 3,
        "name": "qwe"
    },
]);
