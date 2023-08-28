import kue from 'kue'

const queue = kue.createQueue();

const job_type = "push_notification_code"; // queue name
const job_data = {
  phoneNumber: "1111111111",
  message: "This is a text message queue",
};

const job = queue.create(job_type, job_data)
  .save(function (err) {
    if (!err) console.log(`Notification job created: ${job.id}`);
  })


job.on('complete', function (result) {
  console.log('Notification job completed');

}).on('failed attempt', function (errorMessage, doneAttempts) {
  console.log('Notification job failed');

}).on('failed', function (errorMessage) {
  console.log('Notification job failed');

});
