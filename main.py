import redis

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
redis = redis.Redis(connection_pool=pool)

redis.set('name', 'Acassio Mendonca Vilas Boas')
value = redis.get('name')
print(value)