import redis from "redis";

const sub = redis.createClient({ url: `redis://127.0.0.1:6379` });

sub.on('connect', () => console.log('Redis client connected to the server'));
sub.on('error', err => console.log(`Redis client not connected to the server: ${err.message}`));


sub.on("message", function (channel, message) {
  if (channel === 'holberton school channel') console.log(message);
  if (message === 'KILL_SERVER') {
    sub.unsubscribe();
    sub.quit();
  }

});

sub.subscribe("holberton school channel");