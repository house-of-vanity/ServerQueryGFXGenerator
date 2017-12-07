# ServerQueryGFXGenerator
Script provides server info and stats gfx generator via HTTP

warning! Script was tested only with v43 cs1.6 server with (and without) dproto. using python 2

Requre flask python module for web based version. 

* cs.py   - web based version. Provide http://localhost/status with current cs1.6 server statistic including player list. Also you can get simple gfx lable related with servers from servers.yaml config file using https://localhost/gfx/<servername>.
* cli.py  - cli based version. You can use it with any other scripts, bash and etc. Doesn't requre any libraries but native python 2.

gfx example:
![Image of Yaktocat](https://hg.hexor.ru/cs-gfx/gfx/cs.hexor.ru)

Response format is json:
```
$ curl https://localhost/status
{
  "data": [
    {
      "{#FOLDER}": "cstrike", 
      "{#GAME}": "Counter-Strike", 
      "{#MAP}": "fy_pool_day", 
      "{#MAX_PLAYERS}": 16, 
      "{#NAME}": "-- Pool Day ONLY -- cs.hexor.ru", 
      "{#PLATFORM}": "linux", 
      "{#PLAYERS}": 1, 
      "{#PLAYER_LIST}": [
        "Rohan"
      ], 
      "{#SERVER_TYPE}": "dedicated"
    }
  ]
}
```
