const restify = require('restify');
const fs = require('fs');
const corsMiddleware = require('restify-cors-middleware');

const InfoUtil = require('./info.js');
const ReviewsUtil = require('./reviews.js');
const MongoBase = require('./mongobase.js');

class AppServer {
  constructor() {
    this.server = restify.createServer();
    
    this.server.get('/info/', this.getNearbyInfoList.bind(this));
    this.server.get('/info/locations', this.getLocationsList.bind(this));
    this.server.get('/info/:id', this.getInfoById.bind(this));
    this.server.get('/search/:key', this.getSearchResults.bind(this));
    this.server.get('/reviews/:id', this.getReviewsById.bind(this));

    this.server.pre(restify.CORS());
    this.server.use(restify.fullResponse());

    new MongoBase().then((db) => {
      this.infoUtil = new InfoUtil(db);
      this.reviewsUtil = new ReviewsUtil(db);
    });

    this.server.listen(23333);
  }

  getInfoById(req, res, next) {
    const id = parseInt(req.params.id);
    this.infoUtil.getInfo(id).then((result) => {
      res.send(result[0]);
      next();
    });
  }

  getNearbyInfoList(req, res, next) {
    this.infoUtil.getNearbyList().then((result) => {
      res.send(result);
      next();
    });
  }

  getSearchResults(req, res, next) {

  }

  getReviewsById(req, res, next) {
    if (req.params.id == 'locations') {
      this.getLocationsList(req, res, next);
      return;
    }

    const id = parseInt(req.params.id);
    this.reviewsUtil.getInfo(id).then((result) => {
      let filteredResult = result[0];
      delete filteredResult.reviewList;
      res.send(filteredResult);
      next();
    });
  }

  getLocationsList(req, res, next) {
    this.infoUtil.getLocationsList().then((result) => {
      let filteredResult = [];
      for (let index in result) {
        const newObject = {
          name: result[index].name,
          lat: parseFloat(result[index].lat),
          lng: parseFloat(result[index].lng)
        }
        if (newObject.lat) {
          filteredResult.push(newObject);
        }
      }
      res.send(filteredResult);
      next();
    });
  }
}

new AppServer();
