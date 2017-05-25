import $ from 'jquery';

const parkPlaceholderImage = 'http://images.clipartpanda.com/city-clipart-City-Park.png';
export default class POIInfoutil{
    constructor() {
        this.urlBase = 'http://172.27.33.117:23333/info';
    }

    get(id) {
        const url = `${this.urlBase}/${id}`;

        return new Promise((res, rej) => {
            $.get(url, (data) => {
                for (let item of data) {
                    if (item.originalUrlKey.indexOf('http') == -1) {
                        item.originalUrlKey = parkPlaceholderImage;
                    }
                }
                res(data);
            }).fail(function() {
                alert( "error" );
            })
        });
    }

    listNearest() {
        const url = `${this.urlBase}`;

        return new Promise((res, rej) => {
            $.get(url, (data) => {
                for (let item of data) {
                    if (item.originalUrlKey.indexOf('http') == -1) {
                        item.originalUrlKey = parkPlaceholderImage;
                    }
                }
                res(data);
            }).fail(function() {
                alert( "error" );
            })
        });
    }

    getLocationsList() {
        const url = `${this.urlBase}/locations`;

        return new Promise((res, rej) => {
            $.get(url, (data) => {
                res(data);
            }).fail(function() {
                alert( "error" );
            })
        });
    }
}