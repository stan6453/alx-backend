import redis from "redis";

const client = redis.createClient({ url: `redis://127.0.0.1:6379` });

client.on('connect', () => console.log('Redis client connected to the server'));
client.on('error', err => console.log(`Redis client not connected to the server: ${err.message}`));

function setNewSchool(schoolName, value) {
  client.set(schoolName, value, redis.print);
}

function displaySchoolValue(schoolName) {
  client.get(schoolName, function (err, reply) {
    console.log(reply);
  });
}


displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
