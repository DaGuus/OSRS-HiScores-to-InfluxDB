from influxdb import InfluxDBClient
from osrs_api import Hiscores
from osrs_api.const import AccountType
from datetime import datetime

username = 'DaGuusIron'
now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

user = Hiscores(username, AccountType.IRONMAN)

json_body = []

# Append total level
json_body.append({
    "measurement": "total_level",
    "tags": {
        "user": username
    },
    "time": now,
    "fields": {
        "value": user.total_level
    }
})

# Append total XP
json_body.append({
    "measurement": "total_xp",
    "tags": {
        "user": username
    },
    "time": now,
    "fields": {
        "value": user.total_xp
    }
})

# Append rank
json_body.append({
    "measurement": "rank",
    "tags": {
        "user": username
    },
    "time": now,
    "fields": {
        "value": user.rank
    }
})

for skill in user.skills.values():
    json_body.append({
        "measurement": skill.name + "_xp",
        "tags": {
            "user": username
        },
        "time": now,
        "fields": {
            "value": skill.xp
        }
    })

    json_body.append({
        "measurement": skill.name + "_level",
        "tags": {
            "user": username
        },
        "time": now,
        "fields": {
            "value": skill.level
        }
    })

    json_body.append({
        "measurement": skill.name + "_rank",
        "tags": {
            "user": username
        },
        "time": now,
        "fields": {
            "value": skill.rank
        }
    })

for boss in user.bosses.values():
    json_body.append({
        "measurement": boss.name + "_kills",
        "tags": {
            "user": username
        },
        "time": now,
        "fields": {
            "value": boss.kills
        }
    })

    json_body.append({
        "measurement": boss.name + "_rank",
        "tags": {
            "user": username
        },
        "time": now,
        "fields": {
            "value": boss.rank
        }
    })

for minigame in user.minigames.values():
    json_body.append({
        "measurement": minigame.name + "_score",
        "tags": {
            "user": username
        },
        "time": now,
        "fields": {
            "value": minigame.score
        }
    })

    json_body.append({
        "measurement": minigame.name + "_rank",
        "tags": {
            "user": username
        },
        "time": now,
        "fields": {
            "value": minigame.rank
        }
    })

client = InfluxDBClient(host='192.168.0.123', port=8086, ssl=False, verify_ssl=False)
client.switch_database('osrs')
client.write_points(json_body)
