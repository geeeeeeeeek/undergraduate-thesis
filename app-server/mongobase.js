const mongodb = require('mongodb');

class MongoBase {
    constructor() {
        const MongoClient = mongodb.MongoClient;
        const url = 'mongodb://localhost:27017/poi';
        return new Promise((res, rej) => {
            MongoClient.connect(url, (err, db) => {
                if (err) {
                    console.error(err);
                    rej(err);
                } else {
                    res(db);
                }
            });
        });
    }
}

module.exports = MongoBase;