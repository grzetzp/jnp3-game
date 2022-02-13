db = db.getSiblingDB('mongodb_sharded');

db.mongodb_sharded.drop();

db.mongodb_sharded.insertMany([
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
