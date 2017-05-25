import $ from 'jquery';

export default class POIReviewsUtil{
    constructor() {
        this.urlBase = 'http://172.27.33.117:23333/reviews';
    }

    get(id) {
        const url = `${this.urlBase}/${id}`;

        return new Promise((res, rej) => {
            $.get(url, (data) => {
                let preferenceText = '(数据不足)';
                const si = data.serviceGroupPreferenceIndex,
                vi = data.visitorGroupPreferenceIndex;
                if (si && vi) {
                    if (vi > -0.5) {
                        preferenceText = '以外来游客为主';
                    } else if (vi > -1) {
                        preferenceText = '无明显偏向';
                    } else if (si > 0) {
                        preferenceText = '以周边工作人群为主';
                    } else if (si > -0.5) {
                        preferenceText = '以周边人群为主';
                    } else {
                        preferenceText = '以周边居民为主';
                    }
                }
                data.preferenceText = preferenceText;

                let sentimentsText = '(数据不足)';
                const se = data.sentiments;
                console.log(se);
                if (se) {
                    if (se > 0.93) {
                        sentimentsText = '力荐';
                    } else if (se > 0.86) {
                        sentimentsText = '推荐';
                    } else if (se > 0.80) {
                        sentimentsText = '还行';
                    } else if (se > 0.73) {
                        sentimentsText = '较差';
                    } else{
                        sentimentsText = '极差';
                    }
                }
                data.sentimentsText = sentimentsText;
                res(data);
            }).fail(function() {
                alert( "error" );
            })
        });
    }
}