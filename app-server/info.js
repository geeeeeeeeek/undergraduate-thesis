class InfoUtil{
    constructor(db) {
        this.collection = db.collection('shanghai_parks_info');
    }

    getInfo(id) {
        return new Promise((res, rej) => {
            this.collection.find({id: id}).limit(1).toArray((err, docs) => {
                if (err) {
                    rej(err);
                } else {
                    res(docs);
                }
            });
        })
        
    }

    getNearbyList() {
        return new Promise((res, rej) => {
            this.collection.find({}).limit(10).toArray((err, docs) => {
                if (err) {
                    rej(err);
                } else {
                    res(docs);
                }
            });
        })
    }

    getLocationsList() {
        return new Promise((res, rej) => {
            this.collection.find({}).toArray((err, docs) => {
                if (err) {
                    rej(err);
                } else {
                    res(docs);
                }
            });
        })
    }
}

module.exports = InfoUtil;