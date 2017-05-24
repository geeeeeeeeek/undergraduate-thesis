import React, {Component} from 'react';

import POIInfoUtil from '../../utils/POIInfoUtil.jsx';

const mapStyle = {
      height: '1000px'
};
export default class VisualizationView extends Component {
    constructor(state, props) {
        super(state, props);
        this.state = {locations: {}};
        this.poiInfoUtil = new POIInfoUtil();
        this.getLocationsList.bind(this);
    }

    componentDidMount() {
        this.getLocationsList();
    }

    getLocationsList() {
        this.poiInfoUtil
            .getLocationsList()
            .then((locations) => {
                this.setState({locations: locations});
                this.initMap();
            });
    }

    initMap() {
        this.map = new google.maps.Map(this.refs.map, {
                zoom: 9,
                center: {
                    lat: 31.2974197,
                    lng: 121.5014291
                }
            });
        
        const markers = this.state.locations.map(function (location, i) {
            return new google.maps.Marker({
                    position: location,
                    label: location.name
                });
        });

        new MarkerClusterer(this.map, markers, {
            imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'
        });
    }

    render() {
        return (
            <div ref="map" style={mapStyle}></div>
        );
    }
}