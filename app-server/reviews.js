class ReviewsUtil{
    constructor(db) {
        this.collection = db.collection('shanghai_parks_reviews');
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
}

module.exports = ReviewsUtil;