import { createQueue } from 'kue';
import { expect } from 'chai';

import createPushNotificationsJobs from './8-job';

const queue = createQueue();

describe('createPushNotificationsJobs', function () {
  before(function () {
    queue.testMode.enter();
  });

  beforeEach(function () {
    const list = [
      {
        phoneNumber: '4153518780',
        message: 'This is the code 1234 to verify your account'
      },
      {
        phoneNumber: '888888888',
        message: 'This is the code 6866 to verify your account'
      },
    ];
    createPushNotificationsJobs(list, queue);
  });

  afterEach(function () {
    queue.testMode.clear();
  });

  after(function () {
    queue.testMode.exit()
  });

  it('has 2 jobs in its queue', function () {
    expect(queue.testMode.jobs.length).to.equal(2);
  });

  it('the first jobs is of type push_notification_code_3', function () {
    expect(queue.testMode.jobs[0].type).to.equal('push_notification_code_3');
  });

  it('verify the data in the first job', function () {
    expect(queue.testMode.jobs[0].data).to.eql({
      phoneNumber: '4153518780',
      message: 'This is the code 1234 to verify your account'
    });
  });
});
