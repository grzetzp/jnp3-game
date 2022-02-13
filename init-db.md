```
sudo docker-compose up -d
```

```
sudo docker-compose exec configsvr01 sh -c "mongo < /scripts/init-configserver.js"

sudo docker-compose exec shard01-a sh -c "mongo < /scripts/init-shard01.js"
sudo docker-compose exec shard02-a sh -c "mongo < /scripts/init-shard02.js"
sudo docker-compose exec shard03-a sh -c "mongo < /scripts/init-shard03.js"
```

```
sudo docker-compose exec router01 sh -c "mongo < /scripts/init-router.js"
```

```
sudo docker-compose exec router01 mongo --port 27017

// Enable sharding for database `MyDatabase`
sh.enableSharding("MyDatabase")

// Setup shardingKey for collection `MyCollection`**
db.adminCommand( { shardCollection: "MyDatabase.MyCollection", key: { player_id: "hashed" } } )
```


```
sudo docker-compose exec router01 mongo --port 27017
sh.status()
```


```
sudo docker exec -it game_shard-01-node-a bash -c "echo 'rs.status()' | mongo --port 27017" 
sudo docker exec -it game_shard-02-node-a bash -c "echo 'rs.status()' | mongo --port 27017" 
sudo docker exec -it game_shard-03-node-a bash -c "echo 'rs.status()' | mongo --port 27017" 
```


```
sudo docker-compose exec router01 mongo --port 27017
use MyDatabase
db.stats()
db.MyCollection.getShardDistribution()
```
